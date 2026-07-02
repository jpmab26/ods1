"""
Clona o monitoria-app e fixa o SHA do commit em COMMIT_SHA.txt.

Fixar o commit é obrigatório: o corpus de RAG precisa ser idêntico entre
execuções para não confundir a comparação entre tratamentos (ameaça à validade
interna decorrente do desenho de repetições de Silva et al., 2026).
"""
import subprocess
import sys
from pathlib import Path
from src.config import REPO_CACHE_DIR, MONITORIA_REPO_URL


def clone_repo(url: str = MONITORIA_REPO_URL, dest: Path = REPO_CACHE_DIR) -> str:
    """Clona o repositório e retorna o SHA do HEAD."""
    sha_file = dest / "COMMIT_SHA.txt"

    if sha_file.exists():
        print(f"Repositório já clonado. SHA fixado: {sha_file.read_text().strip()}")
        return sha_file.read_text().strip()

    dest.mkdir(parents=True, exist_ok=True)
    print(f"Clonando {url} → {dest} ...")
    subprocess.run(["git", "clone", "--depth", "1", url, str(dest)], check=True)

    result = subprocess.run(
        ["git", "-C", str(dest), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    sha = result.stdout.strip()
    sha_file.write_text(sha)
    print(f"Commit fixado: {sha}")
    return sha


if __name__ == "__main__":
    clone_repo()
