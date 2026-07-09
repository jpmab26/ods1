"""
Conjunto de avaliação de retrieval (Fase 2, item 3 de `prompt_consolidacao.md`).

Pares (query -> chunk-fonte esperado) construídos manualmente, direto do código de
`backend/usuarios/` e `backend/monitorias/` (NÃO a partir de `data/oracle/` — o oráculo é
resultado de outra fase e não deve virar atalho aqui). 3-5 pares por US, cobrindo US01, US08
(experimento) e US04, US07 (oráculo ampliado, Fase 3).

Uso:
    python -m eval.retrieval_eval                 # roda com RETRIEVAL_K e limiares atuais
    python -m eval.retrieval_eval --sweep          # testa combinações de k/limiares e reporta
                                                       a que maximiza recall@k sem explodir ruído

Métrica: recall@k — o chunk-fonte esperado (por prefixo de `fonte`, ex.
"backend/usuarios/service.py#deactivate_user") aparece entre os top-k resultados de
`recuperar_contexto`? Reporta também a confiança com que apareceu.
"""
from __future__ import annotations

import argparse
import json

# Pares (US, query, fonte_esperada_prefixo, descrição)
#
# As queries combinam linguagem natural com termos literais do código (nomes de função,
# constantes de status) — decisão deliberada: o sistema é híbrido semântico+léxico
# (ver src/tools/retriever.py), e uma query 100% parafraseada em PT-BR (sem nenhum termo
# literal) não dá ao canal BM25 nada para casar, subutilizando metade do retriever. Os agentes
# reais (prompts/a1_gerador.md etc.) também são instruídos a buscar termos exatos, então isso é
# representativo do uso real, não um ajuste artificial para inflar recall.
_PARES: list[tuple[str, str, str, str]] = [
    # US01 — Admin cadastra usuários
    ("US01", "create_user cadastro de aluno ou professor com senha temporária gerada",
     "backend/usuarios/service.py#create_user", "Cenário 1: cadastro bem-sucedido"),
    ("US01", "get_user_by_email rejeitar cadastro com email já existente duplicado",
     "backend/usuarios/repository.py#get_user_by_email", "Cenário 2: unicidade de email"),
    ("US01", "create_user status PENDENTE senha temporária gerada após cadastro pelo admin",
     "backend/usuarios/repository.py#create_user", "status inicial do usuário"),
    ("US01", "create_user validação de papel ALUNO PROFESSOR ADMIN no cadastro",
     "backend/usuarios/service.py#create_user", "Cenário 1: papel inválido"),

    # US08 — Admin aprova ou rejeita indicação de monitor
    ("US08", "approve_monitoria aprovar indicação de monitor pendente muda status para ativo",
     "backend/monitorias/service.py#approve_monitoria", "Cenário 1: aprovação"),
    ("US08", "reject_monitoria rejeitar indicação com motivo muda status para rejeitado",
     "backend/monitorias/service.py#reject_monitoria", "Cenário 3: rejeição com motivo"),
    ("US08", "list_pending_monitorias listar indicações pendentes de aprovação para o admin",
     "backend/monitorias/service.py#list_pending_monitorias", "Cenário 4: fila de pendentes"),
    ("US08", "approve_monitoria ALUNO_JA_MONITOR bloquear aprovação aluno já monitor ativo",
     "backend/monitorias/repository.py#approve_monitoria", "Cenário 2: regra ALUNO_JA_MONITOR"),

    # US04 — Admin desativa um usuário
    ("US04", "deactivate_user desativar usuário ativo muda status para inativo",
     "backend/usuarios/service.py#deactivate_user", "Cenário 1: desativação"),
    ("US04", "rota deactivate admin não pode desativar o próprio usuário autoproteção",
     "backend/usuarios/routes.py#deactivate", "regra de borda: autodesativação bloqueada"),
    ("US04", "reactivate_user reativar usuário previamente desativado",
     "backend/usuarios/service.py#reactivate_user", "função de reativação"),

    # US07 — Professor indica aluno como monitor
    ("US07", "create_indicacao professor indica aluno como monitor de uma disciplina",
     "backend/monitorias/service.py#create_indicacao", "Cenário 1: indicação"),
    ("US07", "rota indicar validar que professor só pode indicar monitor das próprias disciplinas",
     "backend/monitorias/routes.py#indicar", "Cenário 2: validação de posse da disciplina"),
    ("US07", "list_by_professor listar indicações de monitor feitas por um professor",
     "backend/monitorias/service.py#list_by_professor", "listagem de indicações do professor"),
]


def _bate(fonte_encontrada: str, fonte_esperada: str) -> bool:
    return fonte_encontrada == fonte_esperada


def avaliar(k: int, alta: float, media: float, min_sim: float) -> dict:
    import src.tools.retriever as retriever
    retriever._ALTA_CONFIANCA = alta
    retriever._MEDIA_CONFIANCA = media
    retriever._MIN_SIMILARITY = min_sim

    acertos = 0
    detalhes = []
    for us_id, query, fonte_esperada, desc in _PARES:
        resultados = retriever.recuperar_contexto(query, k=k)
        posicao = next(
            (i for i, r in enumerate(resultados) if _bate(r["fonte"], fonte_esperada)), None
        )
        acertou = posicao is not None
        acertos += int(acertou)
        detalhes.append({
            "us": us_id, "query": query, "fonte_esperada": fonte_esperada, "desc": desc,
            "acertou": acertou,
            "posicao": posicao,
            "confianca": resultados[posicao]["confianca"] if acertou else None,
            "n_resultados": len(resultados),
        })
    recall = round(acertos / len(_PARES), 4)
    return {"k": k, "alta": alta, "media": media, "min_sim": min_sim,
            "recall_at_k": recall, "acertos": acertos, "total": len(_PARES), "detalhes": detalhes}


def main() -> None:
    parser = argparse.ArgumentParser(description="Avaliação de retrieval (recall@k)")
    parser.add_argument("--sweep", action="store_true",
                         help="testa combinações de k e limiares, reporta a melhor por recall@k")
    args = parser.parse_args()

    from src.config import RETRIEVAL_K
    import src.tools.retriever as retriever

    if not args.sweep:
        resultado = avaliar(RETRIEVAL_K, retriever._ALTA_CONFIANCA, retriever._MEDIA_CONFIANCA,
                             retriever._MIN_SIMILARITY)
        print(f"recall@{resultado['k']} = {resultado['recall_at_k']} "
              f"({resultado['acertos']}/{resultado['total']})")
        for d in resultado["detalhes"]:
            status = f"pos={d['posicao']} conf={d['confianca']}" if d["acertou"] else "NÃO ENCONTRADO"
            print(f"  [{'OK' if d['acertou'] else 'FALHA'}] {d['us']} — {d['desc']}: {status}")
        return

    ks = [3, 5, 7, 10]
    limiares = [(0.55, 0.35), (0.45, 0.30), (0.40, 0.25), (0.50, 0.30)]
    min_sims = [0.15, 0.10]

    resultados = []
    for k in ks:
        for alta, media in limiares:
            for min_sim in min_sims:
                r = avaliar(k, alta, media, min_sim)
                resultados.append(r)
                print(f"k={k} alta={alta} media={media} min_sim={min_sim} "
                      f"-> recall@k={r['recall_at_k']} ({r['acertos']}/{r['total']})")

    melhor = max(resultados, key=lambda r: (r["recall_at_k"], -r["k"]))
    print(f"\nMelhor combinação: k={melhor['k']} alta={melhor['alta']} media={melhor['media']} "
          f"min_sim={melhor['min_sim']} -> recall@k={melhor['recall_at_k']}")

    from src.config import ROOT
    out_path = ROOT / "outputs" / "retrieval_eval_sweep.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps([{k: v for k, v in r.items() if k != "detalhes"} for r in resultados],
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Resultados completos salvos: {out_path}")


if __name__ == "__main__":
    main()
