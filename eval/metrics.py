"""
Precisão, Recall, F1, palavras/caso, % Extraneous.

Os casos de teste são fornecidos como dicts parseados de Markdown por src/parsers.py.
Verbosidade medida sobre os campos `objetivo` e `resultado_esperado` (os dois campos
que A4 é instruído a limitar a ≤25 palavras).

Uso:
    python -m eval.metrics    # lê outputs/rotulagens/*.labels.json, computa métricas,
                               # atualiza os *.json em outputs/raw/ com precisao/recall/f1
                               # e salva outputs/metricas_por_tratamento.json para stats.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


def compute_prf(vp: int, fp: int, fn: int) -> dict:
    """Calcula Precisão, Recall e F1 a partir das contagens."""
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    recall = vp / (vp + fn) if (vp + fn) > 0 else 0.0
    f1 = (
        2 * precisao * recall / (precisao + recall)
        if (precisao + recall) > 0
        else 0.0
    )
    return {"precisao": round(precisao, 4), "recall": round(recall, 4), "f1": round(f1, 4)}


def count_words(caso: dict) -> int:
    """Conta palavras em objetivo + resultado_esperado."""
    objetivo = caso.get("objetivo", "")
    resultado = caso.get("resultado_esperado", "")
    return len(objetivo.split()) + len(resultado.split())


def verbosidade_media(casos: list[dict]) -> float:
    if not casos:
        return 0.0
    return round(sum(count_words(c) for c in casos) / len(casos), 2)


def pct_extraneous(rotulagens: list[dict]) -> float:
    """Percentual de casos com rótulo Extraneous Information."""
    if not rotulagens:
        return 0.0
    n_ext = sum(1 for r in rotulagens if r.get("extraneous", False))
    return round(n_ext / len(rotulagens) * 100, 2)


def load_casos_from_execution(json_path) -> list[dict]:
    """Lê o .md correspondente ao .json e parseia com src/parsers.py."""
    from src.parsers import parse_markdown_casos
    md_path = Path(str(json_path)).with_suffix(".md")
    if not md_path.exists():
        return []
    return parse_markdown_casos(md_path.read_text(encoding="utf-8"))


def main() -> None:
    """Computa métricas de todas as execuções rotuladas e salva agregado para estatística."""
    from src.config import OUTPUTS_RAW, OUTPUTS_ROTULAGENS, OUTPUTS_DIR, ORACLE_DIR
    from src.parsers import load_oracle_md

    oraculo = load_oracle_md(ORACLE_DIR / "oraculo_consolidado.md")

    label_files = sorted(OUTPUTS_ROTULAGENS.glob("*.labels.json"))
    if not label_files:
        print("Nenhum arquivo de rótulos encontrado em outputs/rotulagens/. Execute eval/labeling.py primeiro.")
        return

    # agg[tratamento][us_id] = [f1_rep1, f1_rep2, ...]
    agg: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for label_path in label_files:
        stem = label_path.name.replace(".labels.json", "")
        json_path = OUTPUTS_RAW / f"{stem}.json"
        if not json_path.exists():
            print(f"  [aviso] JSON não encontrado para {label_path.name} — ignorando")
            continue

        metadata = json.loads(json_path.read_text(encoding="utf-8"))
        us_id = metadata.get("user_story_id", "")
        tratamento = metadata.get("tratamento", "")
        rotulagens = json.loads(label_path.read_text(encoding="utf-8"))
        casos_gerados = load_casos_from_execution(json_path)

        vp = sum(1 for r in rotulagens if r.get("correto", False))
        fp = sum(1 for r in rotulagens if not r.get("correto", False))
        # FN = casos do oráculo para esta US que não foram gerados corretamente
        oraculo_us = [c for c in oraculo if c["id"].upper().startswith(us_id.upper())]
        fn = max(0, len(oraculo_us) - vp)

        prf = compute_prf(vp, fp, fn)
        verb = verbosidade_media(casos_gerados)
        pct_ext = pct_extraneous(rotulagens)

        # Atualiza o .json de metadados com as métricas
        metadata.update({
            "precisao": prf["precisao"],
            "recall": prf["recall"],
            "f1": prf["f1"],
            "verbosidade_media": verb,
            "pct_extraneous": pct_ext,
            "vp": vp, "fp": fp, "fn": fn,
        })
        json_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{stem}: P={prf['precisao']} R={prf['recall']} F1={prf['f1']} (vp={vp} fp={fp} fn={fn})")

        agg[tratamento][us_id].append(prf["f1"])

    # Média de reps por (tratamento, US) → alinha para Friedman
    metricas_finais: dict[str, list[float]] = {}
    for trat, us_dict in sorted(agg.items()):
        us_sorted = sorted(us_dict.keys())
        metricas_finais[trat] = [
            round(sum(us_dict[us]) / len(us_dict[us]), 4) for us in us_sorted
        ]

    agg_path = OUTPUTS_DIR / "metricas_por_tratamento.json"
    agg_path.write_text(json.dumps(metricas_finais, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nMétricas salvas em {agg_path}")


if __name__ == "__main__":
    main()
