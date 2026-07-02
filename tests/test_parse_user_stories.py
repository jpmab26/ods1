"""Testes do parser de user stories."""
import pytest
from pathlib import Path
from ingestion.parse_user_stories import parse_user_stories, UserStory


def test_parse_total_stories():
    """Deve retornar 21 entradas de US + sub-histórias de US06 e US18."""
    stories = parse_user_stories()
    us_ids_base = {s.id for s in stories}
    # Deve conter US01 a US21
    for n in range(1, 22):
        assert f"US{n:02d}" in us_ids_base, f"US{n:02d} não encontrada"


def test_sub_historias_us06():
    """US06 deve gerar sub-histórias us06a, us06b, us06c."""
    stories = parse_user_stories()
    sub_ids = [s.sub_id for s in stories if s.id == "US06" and s.sub_id]
    assert len(sub_ids) >= 2, f"US06 deve ter ≥2 sub-histórias, encontrou: {sub_ids}"
    assert "US06a" in sub_ids
    assert "US06b" in sub_ids


def test_sub_historias_us18():
    """US18 deve gerar sub-histórias (admin, professor, monitor, aluno)."""
    stories = parse_user_stories()
    sub_ids = [s.sub_id for s in stories if s.id == "US18" and s.sub_id]
    assert len(sub_ids) >= 2, f"US18 deve ter ≥2 sub-histórias, encontrou: {sub_ids}"


def test_us_simples_sem_sub():
    """US01 (sem sub-histórias) deve gerar exatamente 1 entrada sem sub_id."""
    stories = parse_user_stories()
    us01 = [s for s in stories if s.id == "US01"]
    assert len(us01) == 1
    assert us01[0].sub_id is None


def test_epico_extraido():
    """Todos os registros devem ter épico não vazio."""
    stories = parse_user_stories()
    for s in stories:
        assert s.epico, f"{s.sub_id or s.id} sem épico"


def test_texto_nao_vazio():
    """Nenhum registro deve ter texto vazio."""
    stories = parse_user_stories()
    for s in stories:
        assert s.texto_completo.strip(), f"{s.sub_id or s.id} com texto vazio"
