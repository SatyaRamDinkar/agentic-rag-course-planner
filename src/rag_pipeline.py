'''
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
{
    Can I take CSE4019 if I completed CSE3002, CSE3004, CSE3008, and CSE3015?
    What is the prerequisite chain for CSE4019?
    Can I take CSE9999?
}

Question:
{Enter your query:}

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
'''

from langchain.chat_models import ChatOpenAI
from src.retriever import get_retriever
import os

def ask_question(query):
retriever = get_retriever()
docs = retriever.get_relevant_documents(query)


context = ""
citations = []

for doc in docs:
    context += doc.page_content + "\n\n"
    citations.append(
        f"{doc.metadata.get('source')} - chunk {doc.metadata.get('chunk_id')}"
    )

citation_text = "\n".join(citations)

prompt = f"""


You are a strict academic assistant.

RULES:

* Use ONLY the context
* MUST include citations exactly as given
* If missing info, say "I don't know"

Context:
{context}

Citations Available:
{citation_text}

Question:
{query}

Output format:

You must respond like this:

Decision: (Eligible / Not Eligible / Need More Info)

Answer:

Why:

* Explain prerequisite logic step-by-step

Citations:

* Must include chunk IDs

Next Step:

* What student should do next

Clarifying Questions:

Assumptions:


"""

llm = ChatOpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

return llm.predict(prompt)

