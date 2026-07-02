"""
Orquestrador de experimentos — executa T0/T1/T2/T3 × N US × n repetições.

Design experimental (CP4):
  T0-*  : zero-shot com 5 backends (gemini, gemini_flash, nvidia, nvidia_super, openai_oss)
  T1    : pipeline multiagente + Gemini 2.5 Flash
  T2    : pipeline multiagente + NVIDIA Nemotron Super (120B)
  T3    : ABANDONADO — gpt-oss-120b:free sofreu rate limiting upstream persistente
          no OpenRouter durante toda a janela de execução do experimento

Comparação cruzada (item 3 do plano):
  - Gemini Flash / Nemotron Ultra (modelos grandes) via zero-shot (T0)
  - Gemini Flash-Lite / gpt-oss / Nemotron Super (modelos menores) via pipeline (T1/T2/T3)
  → responde: a arquitetura multi-agente compensa capacidade bruta do modelo?

Rotação de chaves (item 4):
  GOOGLE_API_KEY_1..4 e OPENROUTER_API_KEY_1..4 — quota diária × número de membros do grupo.
  Fallback automático para GOOGLE_API_KEY / OPENROUTER_API_KEY se as chaves numeradas não existirem.

Uso via Makefile (recomendado):
  make smoke-gemini          # 1 US, T0-Gemini — verifica integração antes do run completo
  make smoke-nvidia          # 1 US, T0-NVIDIA Nemotron Ultra (OpenRouter, free)
  make smoke-nvidia-super    # 1 US, T0-NVIDIA Nemotron Super (OpenRouter, free)
  make smoke-openai-oss      # 1 US, T0-OpenAI gpt-oss-120b (OpenRouter, free)
  make run-t0                # T0 zero-shot, 5 backends, 2 US × 2 reps
  make run-t1                # Pipeline multiagente + Gemini Flash-Lite
  make run-t2                # Pipeline multiagente + NVIDIA Nemotron Super
  make run-t3                # Pipeline multiagente + OpenAI gpt-oss-120b
  make run-all               # Todos os tratamentos

Uso direto (linha de comando):
  python -m eval.runner --pipeline zero_shot  --backend gemini       --us US01 --repeticoes 1
  python -m eval.runner --pipeline multiagent --backend nvidia_super --us all  --repeticoes 2

Saída por execução:
  outputs/raw/{tratamento}_{us_id}_{rep:02d}.json  — metadados (latência, tokens, custo)
  outputs/raw/{tratamento}_{us_id}_{rep:02d}.md    — Markdown gerado (legível por humanos)

Os arquivos .md são parseados por src/parsers.py durante eval/metrics.py e eval/labeling.py.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import google.genai.types as genai_types
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from src.config import OUTPUTS_RAW, OUTPUTS_INTER, USER_STORIES_DIR
from eval.instrumentation import build_execution_record

load_dotenv()

# 2 US escolhidas para o experimento: cobrem EP01 (auth), EP02 (monitores).
ORACLE_US_IDS = ["US01", "US08"]

# ---------------------------------------------------------------------------
# Rotação de chaves de API (até 6 por provedor)
# ---------------------------------------------------------------------------

def _collect_keys(prefix: str) -> list[str]:
    """Carrega {prefix}_1..6; ignora índices não definidos; fallback para {prefix} (chave única)."""
    keys = [os.getenv(f"{prefix}_{i}", "") for i in range(1, 7)]
    keys = [k for k in keys if k]
    if not keys:
        single = os.getenv(prefix, "")
        if single:
            keys = [single]
    return keys


_GOOGLE_KEYS: list[str] = _collect_keys("GOOGLE_API_KEY")
_OPENROUTER_KEYS: list[str] = _collect_keys("OPENROUTER_API_KEY")
_key_counter: int = 0


def _rotate_api_keys() -> None:
    """Round-robin: exporta a próxima chave disponível no ambiente antes de cada execução."""
    global _key_counter
    if _GOOGLE_KEYS:
        os.environ["GOOGLE_API_KEY"] = _GOOGLE_KEYS[_key_counter % len(_GOOGLE_KEYS)]
    if _OPENROUTER_KEYS:
        os.environ["OPENROUTER_API_KEY"] = _OPENROUTER_KEYS[_key_counter % len(_OPENROUTER_KEYS)]
    _key_counter += 1


_APP_NAME = "cogerador_testes"
_RETRY_WAIT_S = 65   # espera ao bater em rate limit 429
_MAX_RETRIES = 5


def _load_user_story(us_id: str) -> str:
    path = USER_STORIES_DIR / "individual" / f"{us_id.lower()}.md"
    if not path.exists():
        raise FileNotFoundError(f"User story não encontrada: {path}")
    return path.read_text(encoding="utf-8")


async def _run_pipeline_async(
    pipeline_agent,
    us_id: str,
    us_text: str,
    output_key: str,
    usa_rag: bool,
) -> tuple[str, dict, int, int]:
    """Executa o pipeline via ADK Runner e retorna
    (markdown_casos, intermediarios_md, tokens_entrada, tokens_saida).

    Quando usa_rag=True, faz uma recuperação inicial garantida (síncrona, em
    Python — não é uma tool call do LLM) com a própria user story como query
    e popula o estado `contexto_recuperado` antes de iniciar a sessão. Isso
    garante um contexto de partida mesmo que o agente nunca chame a tool
    `recuperar_contexto`; o agente ainda pode chamá-la livremente para buscas
    adicionais mais específicas durante os laços de crítica/verificação.

    Tokens: o Runner emite um Event por chamada de LLM (A1, A2, A1b, A3, A1c,
    A4 num pipeline multiagente são eventos distintos) — somamos
    prompt_token_count/candidates_token_count de todos os eventos do stream,
    não só do último, para refletir o custo real da execução inteira.
    """
    initial_state = {"user_story": us_text}
    if usa_rag:
        from src.tools.retriever import recuperar_contexto, formatar_contexto_markdown
        contexto_inicial = recuperar_contexto(us_text)
        initial_state["contexto_recuperado"] = formatar_contexto_markdown(contexto_inicial)

    session_service = InMemorySessionService()
    runner = Runner(
        agent=pipeline_agent,
        app_name=_APP_NAME,
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name=_APP_NAME,
        user_id="exp",
        state=initial_state,
    )

    user_msg = genai_types.Content(
        parts=[genai_types.Part(text=f"Gere casos de teste para: {us_id}")],
        role="user",
    )

    tokens_entrada = 0
    tokens_saida = 0
    async for event in runner.run_async(
        user_id="exp",
        session_id=session.id,
        new_message=user_msg,
    ):
        usage = getattr(event, "usage_metadata", None)
        if usage is not None:
            tokens_entrada += getattr(usage, "prompt_token_count", 0) or 0
            tokens_saida += getattr(usage, "candidates_token_count", 0) or 0

    session = await session_service.get_session(
        app_name=_APP_NAME,
        user_id="exp",
        session_id=session.id,
    )

    # Saída principal: Markdown de casos (string pura)
    markdown_casos = session.state.get(output_key, "")
    if not isinstance(markdown_casos, str):
        markdown_casos = str(markdown_casos)

    # Intermediários de A2 e A3 (também Markdown)
    intermediarios = {
        k: session.state[k]
        for k in ("casos_atuais", "critica_cobertura", "relatorio_factual")
        if k in session.state
    }
    return markdown_casos.strip(), intermediarios, tokens_entrada, tokens_saida


def _tratamento_name(pipeline: str, backend: str) -> str:
    if backend == "dryrun":
        return f"smoke_{pipeline}"
    if pipeline == "zero_shot":
        return f"t0_{backend}"
    # multiagent: T1=gemini_flash, T2=nvidia_super, T3=openai_oss
    # gemini (Flash-Lite) também mapeia para t1 como fallback de compatibilidade
    _multiagent_map = {
        "gemini_flash": "t1",
        "gemini":       "t1",
        "nvidia_super": "t2",
        "openai_oss":   "t3",
    }
    return _multiagent_map.get(backend, f"t_{backend}")


def _run_single(pipeline: str, backend: str, us_id: str, rep: int) -> tuple[str, dict]:
    """Executa uma rodada e retorna (markdown_casos, metadata_dict)."""
    os.environ["MODEL_BACKEND"] = backend
    us_text = _load_user_story(us_id)

    t_start = time.time()

    if pipeline == "zero_shot":
        from src.zero_shot import build_zero_shot
        agent = build_zero_shot()
        markdown_casos, intermediarios, tokens_in, tokens_out = asyncio.run(
            _run_pipeline_async(agent, us_id, us_text, output_key="casos_atuais", usa_rag=False)
        )
    else:
        from src.pipeline import build_pipeline
        agent = build_pipeline()
        # dryrun nunca chama tools (DryRunModel ignora o prompt) — pular o RAG
        # mantém make smoke-adk funcionando sem exigir ChromaDB populado.
        usa_rag = backend != "dryrun"
        markdown_casos, intermediarios, tokens_in, tokens_out = asyncio.run(
            _run_pipeline_async(agent, us_id, us_text, output_key="casos_finais", usa_rag=usa_rag)
        )

    elapsed = round(time.time() - t_start, 3)
    tratamento = _tratamento_name(pipeline, backend)
    record = build_execution_record(tokens_in, tokens_out, elapsed, backend, pipeline)

    metadata = {
        "tratamento": tratamento,
        "user_story_id": us_id,
        "repeticao": rep,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "latencia_s": elapsed,
        "tokens_entrada": record.tokens_entrada,
        "tokens_saida": record.tokens_saida,
        "custo_usd": record.custo_usd,
        "model_backend": backend,
        "pipeline": pipeline,
        "modo": "dry_run" if backend == "dryrun" else "real",
        "intermediarios": {k: str(v)[:2000] for k, v in intermediarios.items()},
    }
    return markdown_casos, metadata


def run(pipeline: str, backend: str, us_ids: list[str], repeticoes: int) -> None:
    if pipeline == "multiagent" and backend == "nvidia":
        raise ValueError(
            "backend 'nvidia' (Nemotron Ultra 550B) só roda no pipeline zero_shot — "
            "é grande demais para justificar o custo das chamadas extras do pipeline "
            "multiagente (A1+A2+A1b+A3+A1c+A4 por execução). Use --pipeline zero_shot."
        )
    OUTPUTS_RAW.mkdir(parents=True, exist_ok=True)
    OUTPUTS_INTER.mkdir(parents=True, exist_ok=True)

    concluidos = 0
    pulados = 0
    falhas = 0

    for us_id in us_ids:
        for rep in range(1, repeticoes + 1):
            tratamento = _tratamento_name(pipeline, backend)
            base = OUTPUTS_RAW / f"{tratamento}_{us_id}_{rep:02d}"
            json_path = base.with_suffix(".json")
            md_path = base.with_suffix(".md")

            if json_path.exists() and md_path.exists():
                print(f"  [skip] {json_path.name} já existe")
                pulados += 1
                continue

            print(f"Executando {json_path.name} ...")
            sucesso = False
            for attempt in range(1, _MAX_RETRIES + 1):
                # Roda a chave a cada tentativa (não só uma vez por execução):
                # se a chave atual estiver com a cota diária esgotada, repetir
                # com a MESMA chave nunca teria sucesso — alternar para outra
                # chave do pool dá uma chance real de recuperação automática.
                _rotate_api_keys()
                try:
                    markdown_casos, metadata = _run_single(pipeline, backend, us_id, rep)

                    # .json — metadados (latência, tokens, etc.)
                    json_path.write_text(
                        json.dumps(metadata, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    # .md — output legível por humanos e parseável por src/parsers.py
                    md_path.write_text(markdown_casos, encoding="utf-8")

                    concluidos += 1
                    sucesso = True
                    break
                except Exception as exc:
                    exc_str = str(exc)
                    if any(k in exc_str for k in ("429", "RESOURCE_EXHAUSTED", "ResourceExhausted", "503", "UNAVAILABLE", "Timeout", "timeout", "Provider returned error", "Worker local total request limit",
                                                   # 403 PERMISSION_DENIED "project has been denied access" — indica uma
                                                   # chave banida, mas como a rotação já avançou para outra chave em
                                                   # cada tentativa, vale retentar: se houver outra chave válida no
                                                   # pool a próxima tentativa vai usá-la automaticamente.
                                                   "PERMISSION_DENIED", "project has been denied access")):
                        print(
                            f"  [retry] {exc_str[:80]!r} — aguardando {_RETRY_WAIT_S}s "
                            f"(tentativa {attempt}/{_MAX_RETRIES})..."
                        )
                        time.sleep(_RETRY_WAIT_S)
                    else:
                        raise

            if not sucesso:
                falhas += 1
                print(
                    f"  [falha] {json_path.name} — esgotadas {_MAX_RETRIES} tentativas, "
                    "pulando para a próxima execução. Rode novamente mais tarde para retentar "
                    "(execuções já concluídas são puladas automaticamente)."
                )

    print(
        f"Concluídos: {concluidos} | Pulados: {pulados} | Falhas: {falhas} | "
        f"Total esperado: {len(us_ids) * repeticoes}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Executor de tratamentos experimentais")
    parser.add_argument(
        "--pipeline", choices=["zero_shot", "multiagent"], required=True,
        help="zero_shot=T0, multiagent=T1(gemini)/T2(nvidia_super)/T3(openai_oss)"
    )
    parser.add_argument(
        "--backend",
        choices=["gemini", "gemini_flash", "nvidia", "nvidia_super", "openai_oss", "dryrun"],
        required=True,
        help=(
            "gemini=Gemini 2.5 Flash-Lite (T0 zero-shot) | "
            "gemini_flash=Gemini 2.5 Flash (pipeline T1) | "
            "nvidia=Nemotron Ultra 550B (T0 only) | "
            "nvidia_super=Nemotron Super 120B (pipeline T2) | "
            "openai_oss=gpt-oss-120b (T3 abandonado) | dryrun=fixture"
        ),
    )
    parser.add_argument(
        "--us", default="all",
        help="ID da US (ex.: US01) ou 'all' para rodar o conjunto do oráculo"
    )
    parser.add_argument("--repeticoes", type=int, default=2)
    args = parser.parse_args()

    us_ids = ORACLE_US_IDS if args.us == "all" else [args.us]
    run(args.pipeline, args.backend, us_ids, args.repeticoes)


if __name__ == "__main__":
    main()
