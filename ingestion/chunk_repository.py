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
    rotas: str = ""  # endpoints Flask que alcançam este chunk (só tipo "py"), ex.: "POST /usuarios/<id>/desativar"

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


_ROUTE_METHOD_ATTRS = {"get": ["GET"], "post": ["POST"], "put": ["PUT"],
                       "delete": ["DELETE"], "patch": ["PATCH"]}


def _extract_route_decorator(decorator: ast.expr) -> tuple[str, list[str]] | None:
    """Retorna (path, methods) se o decorator for `@bp.route(...)`/`@bp.get(...)`/etc."""
    if not isinstance(decorator, ast.Call) or not isinstance(decorator.func, ast.Attribute):
        return None
    attr = decorator.func.attr
    if attr != "route" and attr not in _ROUTE_METHOD_ATTRS:
        return None
    if not decorator.args or not isinstance(decorator.args[0], ast.Constant) \
            or not isinstance(decorator.args[0].value, str):
        return None
    path = decorator.args[0].value

    methods = _ROUTE_METHOD_ATTRS.get(attr)
    if methods is None:
        methods = ["GET"]
        for kw in decorator.keywords:
            if kw.arg == "methods" and isinstance(kw.value, (ast.List, ast.Tuple)):
                found = [elt.value for elt in kw.value.elts
                         if isinstance(elt, ast.Constant) and isinstance(elt.value, str)]
                if found:
                    methods = found
    return path, methods


_RouteKey = tuple[str, str]  # (subpacote, nome_da_função)


def _subpacote(path: Path, backend_root: Path) -> str:
    """Primeiro componente de diretório sob backend/ (ex.: 'monitorias', 'usuarios'); '' na raiz."""
    rel = path.relative_to(backend_root)
    return rel.parts[0] if len(rel.parts) > 1 else ""


def build_route_call_maps(repo_root: Path, exclude_tests: bool = True) -> tuple[dict[_RouteKey, str], dict[_RouteKey, set[str]]]:
    """
    Análise estática (AST) de `backend/**/*.py` para dar rastreabilidade requisito↔rota↔código
    aos chunks Python (Fase 2 de `prompt_consolidacao.md` — o chunking por função original não
    tinha metadado de call-graph, permitindo que A3 aceitasse evidência de uma função de outro
    fluxo de negócio como se sustentasse a US sob verificação).

    Retorna:
      - route_map: (subpacote, nome_de_função) -> "MET1/MET2 /caminho" para toda função decorada
        com uma rota Flask (`@blueprint.route(...)`, `@blueprint.get(...)`, etc.).
      - reverse_call_graph: (subpacote, nome_de_função_chamada) -> {nomes das funções que a
        chamam diretamente}.

    Heurística baseada em nome de função, escopada ao subpacote de `backend/` (ex.:
    `monitorias/`, `usuarios/`) — não resolve import real nem overload, mas evita a maior fonte
    de ruído de uma resolução puramente por nome global: dois subpacotes distintos frequentemente
    reusam nomes de método convencionais (`list_x`, `get_x`, `create_x`), e sem esse escopo uma
    função de `monitorias/service.py` herdava rotas de `disciplinas/` só por coincidência de
    nome. Escopar ao subpacote reflete o padrão real de import do projeto
    (`from monitorias import service`, sempre relativo ao próprio subpacote). Suficiente para
    propagar rota a 1 nível de chamada, que é o que a Fase 2 pediu — não tenta reconstruir o
    call-graph completo nem cruzar chamadas entre subpacotes.
    """
    backend = repo_root / "backend"
    route_map: dict[_RouteKey, str] = {}
    reverse_call_graph: dict[_RouteKey, set[str]] = {}
    if not backend.exists():
        return route_map, reverse_call_graph

    for py in backend.rglob("*.py"):
        if ".git" in py.parts or (exclude_tests and "tests" in py.parts):
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        subpkg = _subpacote(py, backend)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            key = (subpkg, node.name)
            for dec in node.decorator_list:
                rota = _extract_route_decorator(dec)
                if rota is None:
                    continue
                path, methods = rota
                entry = f"{'/'.join(methods)} {path}"
                route_map[key] = f"{route_map[key]}; {entry}" if key in route_map else entry
            for sub in ast.walk(node):
                if not isinstance(sub, ast.Call):
                    continue
                if isinstance(sub.func, ast.Name):
                    callee = sub.func.id
                elif isinstance(sub.func, ast.Attribute):
                    callee = sub.func.attr
                else:
                    continue
                reverse_call_graph.setdefault((subpkg, callee), set()).add(node.name)

    return route_map, reverse_call_graph


def _resolver_rotas(
    subpkg: str, func_name: str,
    route_map: dict[_RouteKey, str], reverse_call_graph: dict[_RouteKey, set[str]],
) -> str:
    """Rota(s) Flask associada(s) a uma função: direta (decorador) ou por 1 nível de chamada,
    sempre restrita ao mesmo subpacote de `backend/`."""
    key = (subpkg, func_name)
    if key in route_map:
        return route_map[key]
    rotas = {
        route_map[(subpkg, caller)]
        for caller in reverse_call_graph.get(key, ())
        if (subpkg, caller) in route_map
    }
    return "; ".join(sorted(rotas))


def chunk_python(
    path: Path,
    root: Path,
    route_map: dict[_RouteKey, str] | None = None,
    reverse_call_graph: dict[_RouteKey, set[str]] | None = None,
) -> list[Chunk]:
    source = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(root))
    chunks = []
    route_map = route_map or {}
    reverse_call_graph = reverse_call_graph or {}
    subpkg = _subpacote(path, root / "backend")
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
            rotas = (
                _resolver_rotas(subpkg, identifier, route_map, reverse_call_graph)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                else ""
            )
            chunks.append(Chunk(texto=snippet, fonte=f"{rel}#{identifier}", tipo="py", rotas=rotas))
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
        route_map, reverse_call_graph = build_route_call_maps(repo_root, exclude_tests=exclude_tests)
        for py in backend.rglob("*.py"):
            if ".git" in py.parts:
                continue
            if exclude_tests and "tests" in py.parts:
                continue
            chunks.extend(chunk_python(py, repo_root, route_map, reverse_call_graph))

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
