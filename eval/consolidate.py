"""
Gera artefatos de saída do contrato (tabelas de métricas e custo).

Lê pares {tratamento}_{us}_{rep}.json + {tratamento}_{us}_{rep}.md de outputs/raw/.
Execuções com modo=dry_run são excluídas da agregação estatística.
"""
from __future__ import annotations

import json
from pathlib import Path

from src.config import OUTPUTS_RAW, OUTPUTS_TABELAS, OUTPUTS_DIR


def load_all_executions() -> list[dict]:
    """Carrega metadados de todas as execuções reais."""
    execucoes = []
    for f in sorted(OUTPUTS_RAW.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        if data.get("modo") != "dry_run":
            execucoes.append(data)
    return execucoes


def generate_tables(execucoes: list[dict]) -> None:
    OUTPUTS_TABELAS.mkdir(parents=True, exist_ok=True)

    if not execucoes:
        print("Nenhuma execução real encontrada. Execute os tratamentos com credenciais reais.")
        return

    # Tabela de métricas quantitativas (preenchida após eval/labeling + eval/metrics)
    linhas = [
        "| Tratamento | US | Repetição | Precisão | Recall | F1 |",
        "|------------|----|-----------|---------:|------:|---:|",
    ]
    for e in execucoes:
        linhas.append(
            f"| {e.get('tratamento', '')} | {e.get('user_story_id', '')} "
            f"| {e.get('repeticao', '')} "
            f"| {e.get('precisao', 'N/A')} | {e.get('recall', 'N/A')} | {e.get('f1', 'N/A')} |"
        )
    (OUTPUTS_TABELAS / "metricas_quantitativas.md").write_text(
        "\n".join(linhas), encoding="utf-8"
    )

    # Tabela de custo/latência
    linhas_c = [
        "| Tratamento | US | Rep | Tokens In | Tokens Out | Latência (s) | Custo (US$) |",
        "|------------|----|-----|----------:|-----------:|-------------:|------------:|",
    ]
    for e in execucoes:
        linhas_c.append(
            f"| {e.get('tratamento', '')} | {e.get('user_story_id', '')} "
            f"| {e.get('repeticao', '')} "
            f"| {e.get('tokens_entrada', 0)} | {e.get('tokens_saida', 0)} "
            f"| {e.get('latencia_s', 0)} | {e.get('custo_usd', 0)} |"
        )
    (OUTPUTS_TABELAS / "custo_latencia.md").write_text(
        "\n".join(linhas_c), encoding="utf-8"
    )

    # Consolidado JSON (para análise programática)
    consolidated_path = OUTPUTS_DIR / "resultados_consolidados.json"
    consolidated_path.write_text(
        json.dumps(execucoes, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Artefatos gerados em {OUTPUTS_TABELAS}")
    print(f"Consolidado: {consolidated_path}")


def main() -> None:
    execucoes = load_all_executions()
    generate_tables(execucoes)


if __name__ == "__main__":
    main()
