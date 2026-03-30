

from langchain_openai import ChatOpenAI
from src.retriever import get_retriever
import os


def ask_question(query):
    """Ask a question about course eligibility using RAG pipeline.
    
    Args:
        query: The user's question about course eligibility.
        
    Returns:
        A structured response with eligibility decision, explanation, and citations.
    """
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
- Use ONLY the provided context
- MUST include citations exactly as given
- If missing information, say "I don't know"

Context:
{context}

Available Citations:
{citation_text}

Question:
{query}

Output format:

Decision: (Eligible / Not Eligible / Need More Info)

Answer:

Why:
- Explain prerequisite logic step-by-step

Citations:
- Must include chunk IDs

Next Step:
- What student should do next

Clarifying Questions:

Assumptions:
"""

    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    response = llm.predict(prompt)
    return response
