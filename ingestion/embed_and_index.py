"""
Geração de embeddings locais + indexação ChromaDB.

Usa sentence-transformers (paraphrase-multilingual-mpnet-base-v2) em CPU,
sem chamadas de API e sem quota. Modelo baixado uma vez (~420 MB) para
~/.cache/huggingface/.

Dimensão dos vetores: 768 (vs 3072 do Gemini embedding-001).
Qualidade suficiente para retrieval semântico em PT-BR (modelo multilingual).

Espaço de distância: a coleção é criada explicitamente com hnsw:space="cosine"
(o padrão do Chroma é L2, que só corresponde a similaridade de cosseno se os
vetores forem normalizados — por isso normalize_embeddings=True abaixo). Sem
isso, o campo "distância" devolvido pelo retriever não tem escala interpretável
e não dá para calibrar um limiar de confiança sobre ele.
"""
from __future__ import annotations

import chromadb
from sentence_transformers import SentenceTransformer

from ingestion.chunk_repository import chunk_repository, Chunk
from src.config import CHROMA_DIR, CHROMA_COLLECTION

_MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"


def embed_chunks(chunks: list[Chunk], batch_size: int = 64) -> list[list[float]]:
    """Gera embeddings locais via sentence-transformers (vetores normalizados)."""
    print(f"  Carregando modelo local '{_MODEL_NAME}' (download único ~420 MB)...")
    model = SentenceTransformer(_MODEL_NAME)
    texts = [c.texto_busca() for c in chunks]
    print(f"  Codificando {len(texts)} chunks em batches de {batch_size}...")
    vectors = model.encode(
        texts, batch_size=batch_size, show_progress_bar=True, normalize_embeddings=True
    )
    return [v.tolist() for v in vectors]


def index_chunks(chunks: list[Chunk], embeddings: list[list[float]]) -> None:
    """Persiste chunks e embeddings no ChromaDB (espaço de cosseno)."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        client.delete_collection(name=CHROMA_COLLECTION)
    except Exception:
        pass
    collection = client.create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    documents = [c.texto for c in chunks]
    metadatas = [{"fonte": c.fonte, "tipo": c.tipo, "rotas": c.rotas} for c in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print(f"ChromaDB populado: {collection.count()} chunks em '{CHROMA_COLLECTION}' (espaço: cosseno)")


def main() -> None:
    print("Carregando chunks (excluindo tests/)...")
    chunks = chunk_repository()
    print(f"Total de chunks: {len(chunks)}")

    print("Gerando embeddings (local, sem API)...")
    embeddings = embed_chunks(chunks)

    print("Indexando no ChromaDB...")
    index_chunks(chunks, embeddings)


if __name__ == "__main__":
    main()
