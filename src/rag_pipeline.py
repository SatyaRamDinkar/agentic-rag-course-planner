from langchain.chat_models import ChatOpenAI
from src.retriever import get_retriever
import os

def ask_question(query):
retriever = get_retriever()
docs = retriever.get_relevant_documents(query)


context = "\n\n".join([doc.page_content for doc in docs])

prompt = f"""


You are a strict academic assistant.

RULES:

* Answer ONLY from context
* Always include citations
* If not found, say "I don't know"

Context:
{context}

Question:
{query}

Output format:

Answer:
Why:
Citations:
Clarifying Questions:
Assumptions:
"""


llm = ChatOpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

response = llm.predict(prompt)
return response


if **name** == "**main**":
while True:
q = input("Ask: ")
print(ask_question(q))
