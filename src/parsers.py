"""
Parser determinístico de Markdown estruturado → lista de dicts.

Os agentes comunicam-se e entregam saída em Markdown estruturado (não JSON).
Este módulo converte mecanicamente esse Markdown em registros estruturados
para cálculo de métricas, exportação e comparação com o oráculo.

Nunca chama um LLM — toda a lógica é Python puro.
"""
from __future__ import annotations

import re
from typing import Any


# Separador de blocos de caso: linha que começa com "### "
_BLOCO_RE = re.compile(r"(?=^### )", re.MULTILINE)
# Campo no formato "- **Nome:** valor"
_CAMPO_RE = re.compile(r"^- \*\*([^:]+):\*\*\s*(.*)$")


def parse_markdown_casos(texto_md: str) -> list[dict[str, Any]]:
    """
    Extrai casos de teste de um bloco Markdown estruturado.

    Formato esperado por bloco:
        ### US01-CT01 — Nome do caso
        - **Pré-condição:** ...
        - **Objetivo:** ...
        - **Resultado esperado:** ...
        - **Tipo:** principal | alternativo | borda | erro
        - **Critérios cobertos:** ...
        - **Verificação:** SUPORTADO | NAO_SUPORTADO | NAO_VERIFICAVEL — evidência: ... — fonte: ...
        - **Origem:** ...
        - **Aprovado humano:** pendente | sim | não
        - **Justificativa:** ...   (somente no oráculo)

    Campos ausentes retornam string vazia; não lança exceção para Markdown
    parcialmente malformado (robustez intencional para modelos lite).
    """
    blocos = _BLOCO_RE.split(texto_md)
    casos: list[dict[str, Any]] = []

    for bloco in blocos:
        bloco = bloco.strip()
        if not bloco.startswith("### "):
            continue

        linhas = bloco.splitlines()
        cabecalho = linhas[0][4:].strip()  # remove "### "

        # Separa ID e nome: "US01-CT01 — Nome" ou "US01-CT01 - Nome"
        if " — " in cabecalho:
            id_, nome = cabecalho.split(" — ", 1)
        elif " - " in cabecalho:
            id_, nome = cabecalho.split(" - ", 1)
        else:
            id_, nome = cabecalho, cabecalho

        campos: dict[str, str] = {}
        for linha in linhas[1:]:
            m = _CAMPO_RE.match(linha.strip())
            if m:
                campos[m.group(1).strip()] = m.group(2).strip()

        caso: dict[str, Any] = {
            "id": id_.strip(),
            "nome": nome.strip(),
            "pre_condicao": campos.get("Pré-condição", ""),
            "objetivo": campos.get("Objetivo", ""),
            "resultado_esperado": campos.get("Resultado esperado", ""),
            "tipo": campos.get("Tipo", ""),
            "criterios_cobertos": campos.get("Critérios cobertos", ""),
            "verificacao": campos.get("Verificação", ""),
            "origem": campos.get("Origem", ""),
            "aprovado_humano": campos.get("Aprovado humano", "pendente"),
            "justificativa": campos.get("Justificativa", ""),
        }
        casos.append(caso)

    return casos


def parse_markdown_lacunas(texto_md: str) -> list[dict[str, str]]:
    """
    Extrai lacunas do relatório de A2 (Crítico de Cobertura).

    Formato esperado:
        ## Lacunas identificadas
        ### LC01 — Descrição curta
        - **Tipo:** alternativo | borda | erro
        - **Justificativa:** ...
    """
    lacunas: list[dict[str, str]] = []
    blocos = re.split(r"(?=^### LC)", texto_md, flags=re.MULTILINE)

    for bloco in blocos:
        bloco = bloco.strip()
        if not bloco.startswith("### LC"):
            continue
        linhas = bloco.splitlines()
        cabecalho = linhas[0][4:].strip()
        if " — " in cabecalho:
            id_, descricao = cabecalho.split(" — ", 1)
        else:
            id_, descricao = cabecalho, cabecalho

        campos: dict[str, str] = {}
        for linha in linhas[1:]:
            m = _CAMPO_RE.match(linha.strip())
            if m:
                campos[m.group(1).strip()] = m.group(2).strip()

        lacunas.append({
            "id": id_.strip(),
            "descricao": descricao.strip(),
            "tipo": campos.get("Tipo", ""),
            "justificativa": campos.get("Justificativa", ""),
        })

    return lacunas


def load_oracle_md(path) -> list[dict[str, Any]]:
    """Carrega e parseia o oráculo consolidado em Markdown."""
    from pathlib import Path
    texto = Path(path).read_text(encoding="utf-8")
    return parse_markdown_casos(texto)
