from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os

def get_retriever():
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
db = FAISS.load_local("faiss_index", embeddings)

return db.as_retriever(search_kwargs={"k": 3})


