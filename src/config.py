from pathlib import Path

ROOT = Path(__file__).parent.parent

# Dados
DATA_DIR = ROOT / "data"
REPO_CACHE_DIR = DATA_DIR / "repo_cache"
CHROMA_DIR = DATA_DIR / "chroma"
USER_STORIES_DIR = DATA_DIR / "user_stories"
ORACLE_DIR = DATA_DIR / "oracle"

# Saída
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_RAW = OUTPUTS_DIR / "raw"
OUTPUTS_INTER = OUTPUTS_DIR / "intermediarios"
OUTPUTS_TABELAS = OUTPUTS_DIR / "tabelas"
OUTPUTS_EXEMPLOS = OUTPUTS_DIR / "exemplos"
OUTPUTS_ROTULAGENS = OUTPUTS_DIR / "rotulagens"   # rótulos manuais VP/FP — NÃO apagados por make clean

# Prompts
PROMPTS_DIR = ROOT / "prompts"

# Pipeline
MAX_ITERATIONS = 3
CHROMA_COLLECTION = "monitoria_kb"
RETRIEVAL_K = 5

# Repositório-alvo
MONITORIA_REPO_URL = "https://github.com/WillianPessoa/monitoria-app"
