"""
Workflow assistido de rotulagem humana (VP/FP, taxonomia de Travassos et al., 1999).

Os casos a rotular são lidos dos arquivos .md em outputs/raw/ (formato Markdown) e
parseados por src/parsers.py. O oráculo é lido de data/oracle/oraculo_consolidado.md.

Rotulagem é um julgamento semântico humano — a correspondência automática por
similaridade (abaixo) é apenas um auxílio de produtividade, nunca um substituto.

Uso:
    python -m eval.labeling       # sessão interativa CLI para rotular execuções pendentes
    make eval                      # rotulagem → métricas → estatística

Saída: outputs/rotulagens/{tratamento}_{us}_{rep}.labels.json por execução.
Os labels NÃO são apagados por make clean (são trabalho humano irreversível).
"""
from __future__ import annotations

import json
from pathlib import Path
from src.config import OUTPUTS_RAW, OUTPUTS_ROTULAGENS, ORACLE_DIR
from src.parsers import parse_markdown_casos, load_oracle_md

TAXONOMIA = ["Incorrect Fact", "Ambiguity", "Inconsistency", "Extraneous Information"]

_ORACLE_PATH = ORACLE_DIR / "oraculo_consolidado.md"


def load_oracle() -> list[dict]:
    """Carrega o oráculo consolidado em Markdown."""
    if not _ORACLE_PATH.exists():
        raise FileNotFoundError(
            f"Oráculo não encontrado: {_ORACLE_PATH}\n"
            "O oráculo é construído manualmente — consulte data/oracle/selecao_us_oraculo.md."
        )
    return load_oracle_md(_ORACLE_PATH)


def load_execution_casos(json_path: Path) -> list[dict]:
    """Lê os casos gerados de uma execução (arquivo .md pareado com o .json)."""
    md_path = json_path.with_suffix(".md")
    if not md_path.exists():
        return []
    return parse_markdown_casos(md_path.read_text(encoding="utf-8"))


def interactive_label_session(execucao_json: Path, oraculo: list[dict]) -> list[dict]:
    """
    Sessão CLI interativa de rotulagem de uma execução contra o oráculo.
    Retorna lista de rótulos por caso gerado.
    """
    metadata = json.loads(execucao_json.read_text(encoding="utf-8"))
    casos = load_execution_casos(execucao_json)
    us_id = metadata.get("user_story_id", "?")
    tratamento = metadata.get("tratamento", "?")
    rep = metadata.get("repeticao", "?")

    # Filtra oráculo pela mesma US
    oraculo_us = [c for c in oraculo if c["id"].upper().startswith(us_id.upper())]

    print(f"\n=== Rotulagem: {tratamento} | {us_id} | rep {rep} ===")
    print(f"Oráculo ({us_id}): {len(oraculo_us)} casos | Gerados: {len(casos)} casos\n")

    rotulagens = []
    for caso in casos:
        print(f"--- Caso gerado: {caso.get('id', '?')} ---")
        print(f"  Nome: {caso.get('nome', '')}")
        print(f"  Objetivo: {caso.get('objetivo', '')}")
        print(f"  Resultado esperado: {caso.get('resultado_esperado', '')}")
        rotulo = input("  Rótulo [C=Correto / D=Defeituoso]: ").strip().upper()
        label: dict = {"id_caso": caso.get("id"), "correto": rotulo == "C"}

        if rotulo == "D":
            print(f"  Taxonomia: {', '.join(f'{i+1}={t}' for i, t in enumerate(TAXONOMIA))}")
            cat = input("  Categoria (número): ").strip()
            try:
                label["categoria_defeito"] = TAXONOMIA[int(cat) - 1]
            except (ValueError, IndexError):
                label["categoria_defeito"] = "Não classificado"

        if label["correto"]:
            ext = input("  Extraneous Information? [s/n]: ").strip().lower()
            label["extraneous"] = ext == "s"

        rotulagens.append(label)

    return rotulagens


def main() -> None:
    """Sessão interativa de rotulagem para todas as execuções ainda não rotuladas."""
    oraculo = load_oracle()
    OUTPUTS_ROTULAGENS.mkdir(parents=True, exist_ok=True)

    pendentes = []
    for json_path in sorted(OUTPUTS_RAW.glob("*.json")):
        try:
            meta = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if meta.get("modo") == "dry_run":
            continue
        label_path = OUTPUTS_ROTULAGENS / f"{json_path.stem}.labels.json"
        if label_path.exists():
            print(f"  [skip] {json_path.stem} — já rotulado")
            continue
        pendentes.append(json_path)

    if not pendentes:
        print("Nenhuma execução pendente de rotulagem.")
        return

    print(f"\n{len(pendentes)} execuções para rotular. Ctrl+C para interromper e retomar depois.\n")
    try:
        for json_path in pendentes:
            rotulagens = interactive_label_session(json_path, oraculo)
            label_path = OUTPUTS_ROTULAGENS / f"{json_path.stem}.labels.json"
            label_path.write_text(json.dumps(rotulagens, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  Rótulos salvos: {label_path.name}\n")
    except KeyboardInterrupt:
        print("\nInterrompido — execute novamente para continuar de onde parou.")
        return

    print("Rotulagem concluída.")


if __name__ == "__main__":
    main()
