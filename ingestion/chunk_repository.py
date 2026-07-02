"""
Chunking por seção/tópico do repositório monitoria-app.

Decisão de granularidade semântica (não tamanho fixo de caracteres) referenciada
em Gheventer et al. (2026) e adotada na Seção 4.2 do Relatório Parcial.

Tipos de chunk:
  - Markdown (.md): por cabeçalho ##
  - SQL (schema.sql): por instrução CREATE TABLE
  - Python (.py): por função/classe via ast
  - User story individual: arquivo inteiro como chunk único
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from src.config import REPO_CACHE_DIR, USER_STORIES_DIR


@dataclass
class Chunk:
    texto: str
    fonte: str   # ex.: "backend/db/schema.sql#disciplinas"
    tipo: str    # "md" | "sql" | "py" | "us"

    def texto_busca(self) -> str:
        """Texto usado para gerar o embedding (não o texto devolvido como evidência).

        Chunks de código/schema têm pouco sinal em linguagem natural para o
        embedding multilingual ancorar — prefixar o caminho do arquivo dá
        contexto extra sem alterar o conteúdo retornado ao agente.
        """
        if self.tipo in ("py", "sql"):
            return f"Arquivo: {self.fonte}\n\n{self.texto}"
        return self.texto


def chunk_markdown(path: Path, root: Path) -> list[Chunk]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(root))
    sections = re.split(r"^(##[^#].*)", text, flags=re.MULTILINE)
    chunks: list[Chunk] = []
    # Conteúdo antes do primeiro ##
    if sections[0].strip():
        chunks.append(Chunk(texto=sections[0].strip(), fonte=f"{rel}#intro", tipo="md"))
    i = 1
    while i + 1 < len(sections):
        header = sections[i].strip()
        body = sections[i + 1]
        identifier = re.sub(r"[^a-zA-Z0-9_-]", "_", header)[:50]
        chunks.append(Chunk(texto=f"{header}\n{body}".strip(), fonte=f"{rel}#{identifier}", tipo="md"))
        i += 2
    return chunks


def chunk_sql(path: Path, root: Path) -> list[Chunk]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(root))
    pattern = re.compile(r"(CREATE TABLE\s+`?(\w+)`?.*?)(?=CREATE TABLE|\Z)", re.DOTALL | re.IGNORECASE)
    chunks = []
    for m in pattern.finditer(text):
        table_name = m.group(2)
        chunks.append(Chunk(texto=m.group(1).strip(), fonte=f"{rel}#{table_name}", tipo="sql"))
    return chunks


def chunk_python(path: Path, root: Path) -> list[Chunk]:
    source = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(root))
    chunks = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [Chunk(texto=source, fonte=f"{rel}#module", tipo="py")]

    lines = source.splitlines(keepends=True)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = node.lineno - 1
            end = node.end_lineno
            snippet = "".join(lines[start:end])
            identifier = node.name
            chunks.append(Chunk(texto=snippet, fonte=f"{rel}#{identifier}", tipo="py"))
    if not chunks:
        chunks.append(Chunk(texto=source, fonte=f"{rel}#module", tipo="py"))
    return chunks


def chunk_user_story(path: Path, stories_dir: Path) -> Chunk:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(stories_dir.parent))
    return Chunk(texto=text, fonte=rel, tipo="us")


def chunk_repository(
    repo_root: Path = REPO_CACHE_DIR,
    us_dir: Path = USER_STORIES_DIR / "individual",
    exclude_tests: bool = True,
) -> list[Chunk]:
    """Varre o repositório e retorna todos os chunks.

    exclude_tests=True (padrão) omite backend/tests/ — 387 chunks de teste
    duplicam a lógica já presente nos services/routes e só adicionam ruído
    ao índice (os embeddings são locais, não há custo/cota de API envolvida).
    """
    chunks: list[Chunk] = []

    # Markdown do repositório-alvo
    for md in repo_root.rglob("*.md"):
        if ".git" in md.parts:
            continue
        chunks.extend(chunk_markdown(md, repo_root))

    # SQL
    for sql in repo_root.rglob("*.sql"):
        if ".git" in sql.parts:
            continue
        chunks.extend(chunk_sql(sql, repo_root))

    # Python (backend/, excluindo tests/ por padrão)
    backend = repo_root / "backend"
    if backend.exists():
        for py in backend.rglob("*.py"):
            if ".git" in py.parts:
                continue
            if exclude_tests and "tests" in py.parts:
                continue
            chunks.extend(chunk_python(py, repo_root))

    # User stories individuais
    if us_dir.exists():
        for us_file in sorted(us_dir.glob("*.md")):
            chunks.append(chunk_user_story(us_file, us_dir.parent))

    return chunks


if __name__ == "__main__":
    chunks = chunk_repository()
    print(f"Total de chunks: {len(chunks)}")
    for tipo in ("md", "sql", "py", "us"):
        n = sum(1 for c in chunks if c.tipo == tipo)
        print(f"  {tipo}: {n}")
