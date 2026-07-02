"""
Testes estatísticos: Kappa ponderado linear, Friedman e Wilcoxon pareado.

Replica o protocolo estatístico de Silva et al. (2026): Friedman sobre os
tratamentos com as N=3 US como blocos; pós-teste de Wilcoxon pareado com
correção Holm para as comparações múltiplas, aplicado apenas quando Friedman
for significativo (α=0,05).

Uso:
    python -m eval.statistics   # lê outputs/metricas_por_tratamento.json,
                                  # roda Friedman + Wilcoxon pós-hoc,
                                  # salva outputs/relatorio_estatistico.md
"""
from __future__ import annotations

import itertools
import math

import numpy as np
from scipy import stats


# Escala 1/3/5 (Gheventer et al., 2026 / plano Seção 3.5)
_KAPPA_WEIGHTS = {(1, 1): 1, (1, 3): 0.5, (1, 5): 0,
                  (3, 1): 0.5, (3, 3): 1, (3, 5): 0.5,
                  (5, 1): 0, (5, 3): 0.5, (5, 5): 1}

LANDIS_KOCH = [
    (float("-inf"), 0.00, "Pobre"),
    (0.00, 0.20, "Leve"),
    (0.20, 0.40, "Razoável"),
    (0.40, 0.60, "Moderada"),
    (0.60, 0.80, "Substancial"),
    (0.80, float("inf"), "Quase perfeita"),
]


def interpret_kappa(kappa: float) -> str:
    for lo, hi, label in LANDIS_KOCH:
        if lo <= kappa < hi:
            return label
    return "Quase perfeita"


def weighted_kappa_linear(ratings1: list[int], ratings2: list[int]) -> float:
    """Kappa ponderado linear sobre escala 1/3/5."""
    n = len(ratings1)
    if n == 0:
        return 0.0
    po = sum(_KAPPA_WEIGHTS.get((r1, r2), 0) for r1, r2 in zip(ratings1, ratings2)) / n
    categories = [1, 3, 5]
    freq1 = {c: ratings1.count(c) / n for c in categories}
    freq2 = {c: ratings2.count(c) / n for c in categories}
    pe = sum(
        _KAPPA_WEIGHTS.get((c1, c2), 0) * freq1[c1] * freq2[c2]
        for c1 in categories
        for c2 in categories
    )
    return round((po - pe) / (1 - pe), 4) if pe < 1 else 1.0


def friedman_test(data: dict[str, list[float]]) -> dict:
    """
    Teste de Friedman sobre tratamentos.

    Args:
        data: {tratamento: [f1_us01, f1_us02, ...]} — listas alinhadas por US.
    """
    groups = list(data.values())
    stat, p = stats.friedmanchisquare(*groups)
    return {"statistic": round(float(stat), 4), "p_value": round(float(p), 6)}


def wilcoxon_posthoc(data: dict[str, list[float]], alpha: float = 0.05) -> list[dict]:
    """
    Pós-teste de Wilcoxon pareado com correção Holm para comparações múltiplas.
    Aplicado apenas sobre pares após Friedman significativo.
    """
    pairs = list(itertools.combinations(data.keys(), 2))
    raw_results = []
    for t1, t2 in pairs:
        x, y = data[t1], data[t2]
        try:
            stat, p = stats.wilcoxon(x, y)
            n = len(x)
            r = stat / math.sqrt(n * (n + 1) * (2 * n + 1) / 6) if n > 0 else 0.0
        except ValueError:
            stat, p, r = 0.0, 1.0, 0.0
        raw_results.append({"par": (t1, t2), "statistic": round(float(stat), 4),
                             "p_raw": round(float(p), 6), "r": round(float(r), 4)})

    # Correção Holm
    raw_results.sort(key=lambda x: x["p_raw"])
    m = len(raw_results)
    for i, res in enumerate(raw_results):
        res["p_corrigido"] = round(min(res["p_raw"] * (m - i), 1.0), 6)
        res["significativo"] = res["p_corrigido"] < alpha

    return raw_results


def main() -> None:
    """Carrega métricas agregadas e executa Friedman + Wilcoxon pós-hoc."""
    import json
    from src.config import OUTPUTS_DIR

    agg_path = OUTPUTS_DIR / "metricas_por_tratamento.json"
    if not agg_path.exists():
        print(f"Arquivo não encontrado: {agg_path}\nExecute eval/metrics.py primeiro.")
        return

    data: dict[str, list[float]] = json.loads(agg_path.read_text(encoding="utf-8"))

    if len(data) < 3:
        print(f"Apenas {len(data)} tratamento(s) disponível — Friedman requer ≥ 3 grupos. "
              "Aguarde mais execuções rotuladas.")
        return

    # Garante listas alinhadas (trunca para o mínimo comum)
    min_len = min(len(v) for v in data.values())
    if min_len == 0:
        print("Listas de F1 vazias — verifique eval/metrics.py.")
        return
    data = {k: v[:min_len] for k, v in data.items()}

    friedman = friedman_test(data)
    significativo = friedman["p_value"] < 0.05
    print(f"\nFriedman: stat={friedman['statistic']}, p={friedman['p_value']} "
          f"({'significativo' if significativo else 'não significativo'} α=0,05)")

    posthoc: list[dict] = []
    if significativo:
        posthoc = wilcoxon_posthoc(data)
        print("\nWilcoxon pós-hoc (correção Holm):")
        for r in posthoc:
            sig = " *" if r["significativo"] else ""
            print(f"  {r['par'][0]} vs {r['par'][1]}: p={r['p_corrigido']}, r={r['r']}{sig}")
    else:
        print("Resultado não significativo — sem pós-teste de pares.")

    # Relatório Markdown
    linhas = [
        "# Relatório Estatístico\n\n",
        "## Teste de Friedman\n\n",
        "| Estatística | p-valor | Significativo |\n",
        "|-------------|---------|---------------|\n",
        f"| {friedman['statistic']} | {friedman['p_value']} | {'Sim' if significativo else 'Não'} |\n\n",
    ]
    if posthoc:
        linhas += [
            "## Pós-teste de Wilcoxon (correção Holm)\n\n",
            "| Par | p (corrigido) | r | Significativo |\n",
            "|-----|:-------------:|---|:--------------:|\n",
        ]
        for r in posthoc:
            sig_str = "Sim *" if r["significativo"] else "Não"
            linhas.append(
                f"| {r['par'][0]} vs {r['par'][1]} | {r['p_corrigido']} | {r['r']} | {sig_str} |\n"
            )

    report_path = OUTPUTS_DIR / "relatorio_estatistico.md"
    report_path.write_text("".join(linhas), encoding="utf-8")
    print(f"\nRelatório salvo: {report_path}")


if __name__ == "__main__":
    main()
