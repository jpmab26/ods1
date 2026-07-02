"""Testes de Precisão, Recall, F1 e métricas de verbosidade com valores conhecidos."""
from eval.metrics import compute_prf, count_words, verbosidade_media, pct_extraneous
from eval.statistics import weighted_kappa_linear, friedman_test, wilcoxon_posthoc


def test_precisao_recall_f1_perfect():
    r = compute_prf(vp=10, fp=0, fn=0)
    assert r["precisao"] == 1.0
    assert r["recall"] == 1.0
    assert r["f1"] == 1.0


def test_precisao_zero_fp():
    r = compute_prf(vp=5, fp=5, fn=0)
    assert r["precisao"] == 0.5
    assert r["recall"] == 1.0


def test_recall_zero_fn():
    r = compute_prf(vp=5, fp=0, fn=5)
    assert r["precisao"] == 1.0
    assert r["recall"] == 0.5


def test_f1_balanceado():
    r = compute_prf(vp=4, fp=2, fn=2)
    assert abs(r["f1"] - 2 * (4/6) * (4/6) / (4/6 + 4/6)) < 0.001


def test_f1_zero():
    r = compute_prf(vp=0, fp=5, fn=5)
    assert r["f1"] == 0.0


def test_count_words():
    caso = {"objetivo": "Validar login bem sucedido", "resultado_esperado": "Sistema autentica e redireciona"}
    assert count_words(caso) == 4 + 4


def test_verbosidade_media():
    casos = [
        {"objetivo": "Validar login", "resultado_esperado": "Sistema autentica"},
        {"objetivo": "Verificar cadastro duplicado", "resultado_esperado": "Sistema rejeita"},
    ]
    media = verbosidade_media(casos)
    assert media == (2 + 2 + 3 + 2) / 2


def test_pct_extraneous():
    rots = [{"extraneous": True}, {"extraneous": False}, {"extraneous": True}]
    assert pct_extraneous(rots) == pytest.approx(66.67, abs=0.1)


def test_kappa_perfeito():
    r = [1, 3, 5, 1, 5]
    assert weighted_kappa_linear(r, r) == 1.0


def test_kappa_zero():
    r1 = [1, 1, 1]
    r2 = [5, 5, 5]
    k = weighted_kappa_linear(r1, r2)
    assert k <= 0.0


def test_friedman_4_tratamentos():
    data = {
        "t0_gemini":       [0.6, 0.5, 0.7, 0.4, 0.6, 0.5, 0.7, 0.6],
        "t0_gemini_flash": [0.7, 0.6, 0.8, 0.5, 0.7, 0.6, 0.8, 0.7],
        "t1":              [0.8, 0.7, 0.9, 0.6, 0.8, 0.7, 0.9, 0.8],
        "t2":              [0.85, 0.75, 0.95, 0.65, 0.85, 0.75, 0.95, 0.85],
    }
    result = friedman_test(data)
    assert "statistic" in result
    assert "p_value" in result


def test_wilcoxon_posthoc():
    data = {
        "t0": [0.5, 0.6, 0.5, 0.6, 0.5, 0.6, 0.5, 0.6],
        "t1": [0.8, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0.9],
    }
    results = wilcoxon_posthoc(data)
    assert len(results) == 1
    assert "p_corrigido" in results[0]
    assert "significativo" in results[0]


import pytest
