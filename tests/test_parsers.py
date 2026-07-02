"""Testes do parser determinístico Markdown → dict (src/parsers.py)."""
import pytest
from src.parsers import parse_markdown_casos, parse_markdown_lacunas, load_oracle_md
from src.config import ORACLE_DIR

_EXEMPLO_CASOS = """\
### US01-CT01 — Login com credenciais válidas
- **Pré-condição:** Usuário cadastrado e ativo
- **Objetivo:** Validar autenticação bem-sucedida
- **Resultado esperado:** Sistema redireciona ao painel do usuário
- **Tipo:** principal
- **Critérios cobertos:** AC1
- **Verificação:** SUPORTADO — evidência: assert 200 — fonte: tests/test_us01.py (tipo: código)
- **Origem:** A1
- **Aprovado humano:** pendente

### US01-CT02 — Login com senha inválida
- **Pré-condição:** Usuário cadastrado e ativo
- **Objetivo:** Verificar rejeição de senha incorreta
- **Resultado esperado:** Sistema retorna mensagem de erro e não autentica
- **Tipo:** erro
- **Critérios cobertos:** AC2
- **Verificação:** NAO_VERIFICAVEL — evidência: sem evidência — fonte: — (tipo: código)
- **Origem:** A1 → A2×1
- **Aprovado humano:** pendente
"""

_EXEMPLO_LACUNAS = """\
## Lacunas identificadas
### LC01 — Campo email em branco
- **Tipo:** borda
- **Justificativa:** Validação de obrigatoriedade não explícita na US

### LC02 — Tentativa de login sem sessão
- **Tipo:** erro
- **Justificativa:** Cenário de concorrência não coberto
"""


def test_parse_dois_casos():
    casos = parse_markdown_casos(_EXEMPLO_CASOS)
    assert len(casos) == 2


def test_parse_campos_completos():
    casos = parse_markdown_casos(_EXEMPLO_CASOS)
    c = casos[0]
    assert c["id"] == "US01-CT01"
    assert c["nome"] == "Login com credenciais válidas"
    assert c["tipo"] == "principal"
    assert c["criterios_cobertos"] == "AC1"
    assert c["aprovado_humano"] == "pendente"
    assert "SUPORTADO" in c["verificacao"]


def test_parse_sem_blocos_retorna_vazio():
    assert parse_markdown_casos("## Sem casos aqui\n\nTexto qualquer.") == []


def test_parse_markdown_parcial_nao_falha():
    md_parcial = "### US01-CT01 — Sem campos\n"
    casos = parse_markdown_casos(md_parcial)
    assert len(casos) == 1
    assert casos[0]["objetivo"] == ""


def test_parse_lacunas():
    lacunas = parse_markdown_lacunas(_EXEMPLO_LACUNAS)
    assert len(lacunas) == 2
    assert lacunas[0]["id"] == "LC01"
    assert lacunas[0]["tipo"] == "borda"
    assert "email" in lacunas[0]["descricao"]


def test_oracle_consolidado_legivel():
    oracle_path = ORACLE_DIR / "oraculo_consolidado.md"
    if not oracle_path.exists():
        pytest.skip("oraculo_consolidado.md não existe")
    casos = load_oracle_md(oracle_path)
    assert len(casos) > 0
    assert all(c["aprovado_humano"] == "sim" for c in casos)
    assert all(c["id"] for c in casos)
