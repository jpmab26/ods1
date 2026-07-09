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
OUTPUTS_TABELAS = OUTPUTS_DIR / "tabelas"
OUTPUTS_ROTULAGENS = OUTPUTS_DIR / "rotulagens"   # rótulos manuais VP/FP — NÃO apagados por make clean

# Prompts
PROMPTS_DIR = ROOT / "prompts"

# Pipeline
MAX_ITERATIONS = 3
CHROMA_COLLECTION = "monitoria_kb"
# Ajustado de 5 para 10 na Fase 2 de `prompt_consolidacao.md`, com base em
# eval/retrieval_eval.py: recall@k sobre 14 pares query->chunk (US01/US04/US07/US08,
# construídos direto do código) subiu de 0,43 (k=5) para 0,71 (k=10) e não melhorou mais até
# k=15; k=20 chega a 0,93 mas dobra o contexto injetado por execução. Ver
# outputs/retrieval_eval_sweep.json para o sweep completo.
RETRIEVAL_K = 10

# Repositório-alvo
MONITORIA_REPO_URL = "https://github.com/WillianPessoa/monitoria-app"
