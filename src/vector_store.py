
'''
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from src.ingest import load_documents
from src.chunking import split_docs
import os

def create_vector_store():
docs = load_documents("data")
split_documents = split_docs(docs)


embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

vectorstore = FAISS.from_documents(split_documents, embeddings)
vectorstore.save_local("faiss_index")

print("Vector store created!")


if **name** == "**main**":
create_vector_store()
'''

from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from src.ingest import load_documents
from src.chunking import split_docs
import os

def create_vector_store():
raw_docs = load_documents("data")
split_documents = split_docs(raw_docs)


# Add metadata
for i, doc in enumerate(split_documents):
    doc.metadata = {
        "source": f"doc_{i//5}",
        "chunk_id": i
    }

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

vectorstore = FAISS.from_documents(split_documents, embeddings)
vectorstore.save_local("faiss_index")

print("Vector store created with metadata!")


if **name** == "**main**":
create_vector_store()
