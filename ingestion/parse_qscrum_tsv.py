"""
Stub documentado do parser de TSV do quadro QScrum.

Não bloqueante: nenhum arquivo .tsv foi disponibilizado até a data do plano.
Implementa a assinatura esperada e um teste com TSV sintético de 2 linhas.
Não é utilizado em nenhum checkpoint subsequente (Seção 3.2 do plano).
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from io import StringIO
from pathlib import Path


@dataclass
class UserStoryTSV:
    titulo: str
    descricao: str
    criterios_aceitacao: str
    labels: str
    status: str


def parse_qscrum_tsv(path: str | Path) -> list[UserStoryTSV]:
    """
    Lê um arquivo TSV exportado do quadro QScrum e retorna lista de UserStoryTSV.

    Colunas esperadas: titulo, descricao, criterios_aceitacao, labels, status.
    """
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return [
            UserStoryTSV(
                titulo=row.get("titulo", ""),
                descricao=row.get("descricao", ""),
                criterios_aceitacao=row.get("criterios_aceitacao", ""),
                labels=row.get("labels", ""),
                status=row.get("status", ""),
            )
            for row in reader
        ]
