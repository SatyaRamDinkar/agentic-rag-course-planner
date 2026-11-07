import os
import hashlib
import numpy as np
from typing import List
from dotenv import load_dotenv

from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS

from src.ingest import load_documents
from src.chunking import split_docs

load_dotenv()


class DeterministicCatalogEmbeddings(Embeddings):
    """Deterministic hash-based dense embedding generator.
    
    Acts as an offline fallback when OPENAI_API_KEY is not provided, allowing
    the entire pipeline, index creation, tests, and Streamlit app to run smoothly
    without crashes. Uses character and word n-grams mapped into a normalized
    384-dimensional vector space.
    """
    def __init__(self, dim: int = 384):
        self.dim = dim

    def _embed_text(self, text: str) -> List[float]:
        vec = np.zeros(self.dim, dtype=np.float32)
        words = text.lower().split()
        for idx, word in enumerate(words):
            h = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
            pos = h % self.dim
            vec[pos] += 1.0 / (1.0 + 0.1 * idx)
            # Bi-grams for course codes and chained phrases
            if idx > 0:
                bigram = f"{words[idx-1]}_{word}"
                h_bi = int(hashlib.md5(bigram.encode("utf-8")).hexdigest(), 16)
                vec[h_bi % self.dim] += 1.5

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed_text(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed_text(text)


def get_embedding_model():
    """Returns OpenAI embeddings if OPENAI_API_KEY is present; otherwise returns deterministic offline embeddings."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and not api_key.startswith("your_") and len(api_key) > 20:
        try:
            from langchain_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(openai_api_key=api_key)
        except Exception as e:
            print(f"[VectorStore] Warning: Could not initialize OpenAIEmbeddings ({e}). Falling back to local offline embeddings.")
            return DeterministicCatalogEmbeddings()
    else:
        return DeterministicCatalogEmbeddings()


def create_vector_store(data_path="data", index_path="faiss_index"):
    """Ingest catalog documents, chunk them, compute embeddings, and build the FAISS index."""
    print(f"[VectorStore] Loading catalog from '{data_path}'...")
    raw_docs = load_documents(data_path)
    print(f"[VectorStore] Chunking {len(raw_docs)} documents...")
    chunks = split_docs(raw_docs)
    print(f"[VectorStore] Generated {len(chunks)} chunks with citations.")

    embeddings = get_embedding_model()
    print(f"[VectorStore] Generating embeddings using {type(embeddings).__name__}...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(index_path, exist_ok=True)
    vectorstore.save_local(index_path)
    print(f"[VectorStore] Index successfully built and saved to '{index_path}'!")
    return vectorstore


if __name__ == "__main__":
    create_vector_store()
