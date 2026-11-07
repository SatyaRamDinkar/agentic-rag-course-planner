import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from src.vector_store import get_embedding_model

load_dotenv()


def get_retriever(index_path="faiss_index", k=5):
    """Load the FAISS vector index and return a retriever configured with top-k.
    
    Args:
        index_path: Directory containing the FAISS index files.
        k: Number of relevant chunks to retrieve (default k=5 for multi-hop prerequisite coverage).
        
    Returns:
        A LangChain VectorStoreRetriever.
    """
    if not os.path.exists(index_path):
        from src.vector_store import create_vector_store
        print(f"[Retriever] Index '{index_path}' not found. Creating index now...")
        create_vector_store(index_path=index_path)

    embeddings = get_embedding_model()
    db = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db.as_retriever(search_kwargs={"k": k})
