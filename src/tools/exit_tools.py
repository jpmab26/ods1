"""
Re-exporta a ferramenta exit_loop nativa do google-adk 2.3.0.

A implementação canônica está em google.adk.tools.exit_loop_tool e define
escalate=True + skip_summarization=True via ToolContext. A versão customizada
anterior foi substituída por esta re-exportação para manter sincronismo com
a biblioteca conforme exigido pela Seção 4.3 do plano.
"""
from google.adk.tools.exit_loop_tool import exit_loop  # noqa: F401

__all__ = ["exit_loop"]
