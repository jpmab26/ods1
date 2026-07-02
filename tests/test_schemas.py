"""Testes de validação do esquema Pydantic (CasoDeTeste, etc.)."""
import pytest
from pydantic import ValidationError
from src.schemas import CasoDeTeste, Verificacao, Lacuna, RelatorioCobertura, RelatorioFactual, VerificacaoItem


def caso_valido() -> dict:
    return {
        "id": "US01-CT01",
        "nome": "Login com credenciais válidas",
        "pre_condicao": "Usuário cadastrado e ativo",
        "objetivo": "Validar autenticação bem-sucedida",
        "resultado_esperado": "Sistema autentica e redireciona",
        "tipo": "principal",
        "criterios_cobertos": ["AC1"],
    }


def test_caso_de_teste_valido():
    caso = CasoDeTeste(**caso_valido())
    assert caso.id == "US01-CT01"
    assert caso.tipo == "principal"
    assert caso.verificacao is None
    assert caso.aprovado_humano is None


def test_caso_de_teste_com_verificacao():
    data = caso_valido()
    data["verificacao"] = {
        "status": "SUPORTADO",
        "evidencia": "backend/db/schema.sql",
        "fonte": "backend/db/schema.sql#usuarios",
    }
    caso = CasoDeTeste(**data)
    assert caso.verificacao.status == "SUPORTADO"


def test_caso_de_teste_tipo_invalido():
    data = caso_valido()
    data["tipo"] = "invalido"
    with pytest.raises(ValidationError):
        CasoDeTeste(**data)


def test_caso_de_teste_campo_obrigatorio_ausente():
    data = caso_valido()
    del data["nome"]
    with pytest.raises(ValidationError):
        CasoDeTeste(**data)


def test_verificacao_status_invalido():
    with pytest.raises(ValidationError):
        Verificacao(status="INVALIDO", evidencia="x", fonte="y")


def test_lacuna_valida():
    lac = Lacuna(descricao="Falta cenário de borda", tipo="borda", justificativa="Valor vazio não coberto")
    assert lac.tipo == "borda"


def test_relatorio_cobertura_vazio():
    rel = RelatorioCobertura(lacunas=[])
    assert rel.lacunas == []


def test_relatorio_factual():
    item = VerificacaoItem(id_caso="US01-CT01", status="NAO_VERIFICAVEL", evidencia="", fonte="")
    rel = RelatorioFactual(verificacoes=[item], relatorio_factual="Sem evidência")
    assert rel.verificacoes[0].status == "NAO_VERIFICAVEL"
