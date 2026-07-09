"""
FunctionTool recuperar_contexto — busca híbrida (semântica + léxica) no
ChromaDB sobre o corpus do monitoria-app. Compartilhada por A1, A2 e A3.

Por que híbrida: busca puramente vetorial perde correspondências exatas de
identificador (nomes de status como 'PENDENTE_APROVACAO', rotas, campos de
schema) que aparecem literalmente no texto mas não são bem capturadas por um
embedding de propósito geral treinado para paráfrase em linguagem natural.
BM25 (léxico) cobre esse caso; o vetor cobre sinônimo/paráfrase. Os dois
rankings são combinados via Reciprocal Rank Fusion (RRF), que não exige
normalizar escalas heterogêneas (similaridade de cosseno vs. score BM25).

Usa o mesmo modelo local (sentence-transformers) e o mesmo `texto_busca()`
que embed_and_index.py para garantir consistência de espaço vetorial entre
indexação e busca (a coleção é criada com hnsw:space="cosine" + embeddings
normalizados — ver ingestion/embed_and_index.py).
"""
from __future__ import annotations

import re

import chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from src.config import CHROMA_DIR, CHROMA_COLLECTION, RETRIEVAL_K

_MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"
_model: SentenceTransformer | None = None

_RRF_K = 60              # constante padrão do Reciprocal Rank Fusion (Cormack et al., 2009)
_FETCH_MULT = 4          # busca k*_FETCH_MULT em cada canal antes de fundir
_MIN_SIMILARITY = 0.15   # piso de similaridade de cosseno para achado puramente vetorial
_ALTA_CONFIANCA = 0.55
_MEDIA_CONFIANCA = 0.35

# Cache de processo: chunks e índice BM25 não mudam durante uma execução do runner.
_bm25_index: BM25Okapi | None = None
_bm25_ids: list[str] | None = None
_bm25_docs: dict[str, dict] | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def _embed_query(text: str) -> list[float]:
    return _get_model().encode(text, normalize_embeddings=True).tolist()


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_À-ÿ]+", text.lower())


def _load_bm25_corpus(collection) -> None:
    """Carrega o corpus inteiro uma vez por processo para montar o índice BM25 local."""
    global _bm25_index, _bm25_ids, _bm25_docs
    if _bm25_index is not None:
        return
    all_data = collection.get(include=["documents", "metadatas"])
    _bm25_ids = all_data["ids"]
    _bm25_docs = {
        cid: {"texto": doc, "fonte": meta.get("fonte", ""), "tipo": meta.get("tipo", ""),
              "rotas": meta.get("rotas", "")}
        for cid, doc, meta in zip(_bm25_ids, all_data["documents"], all_data["metadatas"])
    }
    tokenized = [_tokenize(doc) for doc in all_data["documents"]]
    _bm25_index = BM25Okapi(tokenized)


def _vector_search(collection, query_embedding: list[float], n: int) -> list[tuple[str, float]]:
    """[(chunk_id, similaridade_cosseno)] ordenado por similaridade desc."""
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n, collection.count()),
        include=["distances"],
    )
    # Coleção em espaço "cosine": distância do Chroma = 1 - similaridade.
    return [(cid, 1.0 - dist) for cid, dist in zip(results["ids"][0], results["distances"][0])]


def _lexical_search(query: str, n: int) -> list[tuple[str, float]]:
    """[(chunk_id, score_bm25)] ordenado por score desc; vazio se a query não tokeniza."""
    tokens = _tokenize(query)
    if _bm25_index is None or not tokens:
        return []
    scores = _bm25_index.get_scores(tokens)
    ranked = sorted(zip(_bm25_ids, scores), key=lambda x: x[1], reverse=True)
    return [(cid, score) for cid, score in ranked[:n] if score > 0]


def _reciprocal_rank_fusion(
    vector_hits: list[tuple[str, float]],
    lexical_hits: list[tuple[str, float]],
) -> dict[str, dict]:
    """Funde os dois rankings via RRF; preserva similaridade e canais de origem por chunk."""
    fused: dict[str, dict] = {}

    for rank, (cid, sim) in enumerate(vector_hits):
        entry = fused.setdefault(cid, {"score": 0.0, "similaridade": None, "canais": []})
        entry["score"] += 1.0 / (_RRF_K + rank + 1)
        entry["similaridade"] = sim
        entry["canais"].append("semantico")

    for rank, (cid, _score) in enumerate(lexical_hits):
        entry = fused.setdefault(cid, {"score": 0.0, "similaridade": None, "canais": []})
        entry["score"] += 1.0 / (_RRF_K + rank + 1)
        entry["canais"].append("lexical")

    return fused


def _confianca(similaridade: float | None, canais: list[str]) -> str:
    if similaridade is not None and similaridade >= _ALTA_CONFIANCA:
        return "alta"
    if similaridade is not None and similaridade >= _MEDIA_CONFIANCA:
        return "media"
    if "lexical" in canais:
        return "lexical"  # correspondência exata de termo, sem score semântico forte
    return "baixa"


def recuperar_contexto(query: str, k: int = RETRIEVAL_K) -> list[dict]:
    """
    Recupera os chunks mais relevantes do repositório monitoria-app para a
    query fornecida, combinando busca semântica (embeddings) e léxica (BM25)
    via Reciprocal Rank Fusion.

    Cada resultado traz um rótulo de confiança ("alta" | "media" | "lexical" |
    "baixa") para que o agente saiba o quanto pode confiar na evidência —
    evidência "baixa" deve ser tratada como fraca, não como prova.

    Args:
        query: Texto de busca (gerado pelo agente ou pela user story inteira).
        k: Número máximo de resultados a retornar.

    Returns:
        Lista de dicts com keys: texto, fonte, tipo, similaridade, confianca,
        canais. Pode vir vazia se nada relevante for encontrado — isso é
        intencional: é melhor sinalizar "sem evidência" do que devolver os
        k chunks mais próximos mesmo quando nenhum deles é relevante.
    """
    db_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = db_client.get_collection(name=CHROMA_COLLECTION)
    _load_bm25_corpus(collection)

    fetch_n = k * _FETCH_MULT
    vector_hits = _vector_search(collection, _embed_query(query), fetch_n)
    lexical_hits = _lexical_search(query, fetch_n)

    fused = _reciprocal_rank_fusion(vector_hits, lexical_hits)
    ranked_ids = sorted(fused.keys(), key=lambda cid: fused[cid]["score"], reverse=True)

    out: list[dict] = []
    for cid in ranked_ids:
        entry = fused[cid]
        sim = entry["similaridade"]
        if sim is not None and sim < _MIN_SIMILARITY and "lexical" not in entry["canais"]:
            continue  # achado vetorial fraco e sem reforço léxico — descarta, não preenche k à força
        doc = _bm25_docs[cid]
        out.append({
            "texto": doc["texto"],
            "fonte": doc["fonte"],
            "tipo": doc["tipo"],
            "rotas": doc.get("rotas", ""),
            "similaridade": round(sim, 4) if sim is not None else None,
            "confianca": _confianca(sim, entry["canais"]),
            "canais": entry["canais"],
        })
        if len(out) >= k:
            break
    return out


def formatar_contexto_markdown(resultados: list[dict]) -> str:
    """Formata o resultado de recuperar_contexto como bloco Markdown legível.

    Usado para a recuperação inicial garantida (eval/runner.py), injetada no
    estado da sessão antes do pipeline começar — não depende do agente
    decidir chamar a tool para haver pelo menos um contexto de partida.
    """
    if not resultados:
        return "_Nenhum contexto relevante encontrado para esta user story._"
    blocos = []
    for r in resultados:
        sim_txt = f"{r['similaridade']:.2f}" if r["similaridade"] is not None else "—"
        canais_txt = "+".join(r["canais"])
        rotas_txt = r.get("rotas") or "sem rota associada"
        blocos.append(
            f"### Fonte: {r['fonte']} (tipo: {r['tipo']}, rota: {rotas_txt}, "
            f"confiança: {r['confianca']}, similaridade: {sim_txt}, canal: {canais_txt})\n"
            f"```\n{r['texto']}\n```"
        )
    return "\n\n".join(blocos)
