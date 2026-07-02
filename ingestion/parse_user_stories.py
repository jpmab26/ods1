"""
Parser de user stories do arquivo data/user_stories/user-stories.md.

Divide em documentos individuais por US (e sub-histórias com sufixo a/b/c para
US06 e US18), conforme especificado na Seção 3.2 do plano.

Casos especiais tratados:
  - Sub-histórias dentro de uma mesma US (US06, US18): separadas por `---`
    sob o mesmo cabeçalho # [USxx]. Geram sub-registros US06a, US06b, US06c.
  - Identificador sempre lido dos colchetes ([US05]), nunca por contagem posicional.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from src.config import USER_STORIES_DIR


@dataclass
class UserStory:
    id: str
    titulo: str
    epico: str
    texto_completo: str
    sub_id: str | None = None  # ex.: "US06a"


def parse_user_stories(
    source: Path = USER_STORIES_DIR / "user-stories.md",
) -> list[UserStory]:
    """Lê o arquivo de user stories e retorna lista de UserStory."""
    text = source.read_text(encoding="utf-8")

    # Divide nos cabeçalhos # [USxx]
    pattern = re.compile(r"^# \[(?P<id>US\d+)\] (?P<titulo>.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))

    stories: list[UserStory] = []
    for i, m in enumerate(matches):
        us_id = m.group("id")
        titulo = m.group("titulo").strip()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]

        # Extrai épico
        epico_match = re.search(r"\*\*Épico:\*\*\s*(.+)", body)
        epico = epico_match.group(1).strip() if epico_match else ""

        # Verifica sub-histórias (blocos separados por linha `---`)
        # Mantemos os separadores para dividir o corpo corretamente
        sub_blocks = re.split(r"^---\s*$", body, flags=re.MULTILINE)

        if len(sub_blocks) <= 1:
            stories.append(UserStory(id=us_id, titulo=titulo, epico=epico, texto_completo=body))
        else:
            # Cada bloco após o primeiro `---` é uma sub-história
            suffixes = "abcdefghijklmnopqrstuvwxyz"
            for j, block in enumerate(sub_blocks):
                sub_id = f"{us_id}{suffixes[j]}"
                stories.append(
                    UserStory(
                        id=us_id,
                        titulo=titulo,
                        epico=epico,
                        texto_completo=block.strip(),
                        sub_id=sub_id,
                    )
                )

    return stories


def export_individual(
    stories: list[UserStory],
    dest_dir: Path = USER_STORIES_DIR / "individual",
) -> None:
    """Salva cada UserStory como arquivo .md individual."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    for us in stories:
        filename = f"{(us.sub_id or us.id).lower()}.md"
        (dest_dir / filename).write_text(us.texto_completo, encoding="utf-8")
    print(f"{len(stories)} arquivos gerados em {dest_dir}")


if __name__ == "__main__":
    stories = parse_user_stories()
    export_individual(stories)
    print(f"Total de histórias (incluindo sub): {len(stories)}")
