"""
Smoke test do retriever RAG: ≥5 consultas cobrindo os 4 tipos de chunk.

Valida que os top-k resultados contêm as palavras-chave esperadas.
Executar somente após `make index` (requer ChromaDB populado).
"""
import pytest
from src.config import CHROMA_DIR, CHROMA_COLLECTION


pytestmark = pytest.mark.skipif(
    not (CHROMA_DIR / CHROMA_COLLECTION).exists() and not any(CHROMA_DIR.iterdir() if CHROMA_DIR.exists() else []),
    reason="ChromaDB não populado — execute 'make index' antes.",
)

QUERIES = [
    ("papéis de usuário", ["papel", "ALUNO", "MONITOR", "PROFESSOR", "ADMIN"]),
    ("regra de cancelamento com 6 horas de antecedência", ["cancelamento", "6", "horas"]),
    ("tabela de votações", ["votacoes", "votacao", "votos"]),
    ("endpoint de reset de senha", ["senha", "reset", "password"]),
    ("disciplinas cadastro código", ["disciplinas", "codigo", "código"]),
]


def test_retriever_queries():
    try:
        from src.tools.retriever import recuperar_contexto
    except Exception as e:
        pytest.skip(f"Retriever não disponível: {e}")

    for query, keywords in QUERIES:
        results = recuperar_contexto(query, k=5)
        assert len(results) > 0, f"Nenhum resultado para: {query}"
        all_text = " ".join(r["texto"].lower() for r in results)
        found = any(kw.lower() in all_text for kw in keywords)
        assert found, (
            f"Consulta '{query}': nenhuma palavra-chave {keywords} "
            f"encontrada nos top-5 resultados."
        )


def test_retriever_resultado_traz_confianca_e_canais():
    from src.tools.retriever import recuperar_contexto

    results = recuperar_contexto("aprovação de indicação de monitor", k=5)
    assert len(results) > 0
    for r in results:
        assert r["confianca"] in ("alta", "media", "lexical", "baixa")
        assert r["canais"], "todo resultado deve vir de pelo menos um canal (semantico/lexical)"
        assert set(r["canais"]) <= {"semantico", "lexical"}


def test_retriever_query_relevante_tem_alta_confianca():
    from src.tools.retriever import recuperar_contexto

    # A própria US08 deve bater quase exatamente contra seu próprio texto indexado.
    results = recuperar_contexto(
        "Admin aprova ou rejeita indicação de monitor — vínculo muda para Ativo", k=3
    )
    assert any(r["confianca"] == "alta" for r in results)


def test_retriever_query_sem_relacao_nao_retorna_alta_confianca():
    from src.tools.retriever import recuperar_contexto

    results = recuperar_contexto("lorem ipsum dolor sit amet consectetur adipiscing", k=5)
    assert all(r["confianca"] != "alta" for r in results)


def test_formatar_contexto_markdown_vazio():
    from src.tools.retriever import formatar_contexto_markdown

    assert "Nenhum contexto" in formatar_contexto_markdown([])


def test_formatar_contexto_markdown_com_resultados():
    from src.tools.retriever import recuperar_contexto, formatar_contexto_markdown

    results = recuperar_contexto("cancelamento de monitoria", k=3)
    md = formatar_contexto_markdown(results)
    assert "confiança:" in md
    for r in results:
        assert r["fonte"] in md
