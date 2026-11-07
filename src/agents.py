import os
from typing import List, Dict, Any
from dotenv import load_dotenv

from crewai import Agent
from langchain_core.tools import tool

from src.retriever import get_retriever
from src.rag_pipeline import FallbackCatalogReasoner

load_dotenv()


@tool("search_academic_catalog")
def search_academic_catalog(query: str) -> str:
    """Searches the official university academic catalog and policy documents for prerequisites, course codes, and degree rules."""
    retriever = get_retriever()
    docs = retriever.invoke(query) if hasattr(retriever, "invoke") else retriever.get_relevant_documents(query)
    if not docs:
        return "No relevant catalog documents found."
    
    formatted = []
    for d in docs:
        source = d.metadata.get("source", "catalog_doc")
        chunk_id = d.metadata.get("chunk_id", "chunk")
        formatted.append(f"[{source} (Citation: {source}#{chunk_id})]\n{d.page_content}")
    return "\n\n---\n\n".join(formatted)


def get_llm():
    """Returns ChatOpenAI if API key is valid, otherwise None for fallback pipeline."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and not api_key.startswith("your_") and len(api_key) > 20:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(temperature=0.0, openai_api_key=api_key)
        except Exception:
            return None
    return None


def get_agents():
    """Create and return the 4 required specialized academic planning agents."""
    llm = get_llm()

    intake_agent = Agent(
        role="Student Intake Specialist",
        goal="Extract completed courses, major, target term, credit constraints, and identify missing context requiring clarifying questions.",
        backstory="An attentive academic advisor who ensures all necessary student context is collected before attempting course planning.",
        tools=[search_academic_catalog],
        verbose=False,
        llm=llm
    )

    retriever_agent = Agent(
        role="Academic Catalog Researcher",
        goal="Search the university catalog and academic policy files for verbatim prerequisite rules and degree requirements with verifiable citations.",
        backstory="A detail-oriented university registrar researcher who never guesses and only cites verifiable catalog text.",
        tools=[search_academic_catalog],
        verbose=False,
        llm=llm
    )

    planner_agent = Agent(
        role="Course Planning Advisor",
        goal="Formulate an eligible term course plan or answer prerequisite eligibility strictly grounded in retrieved evidence.",
        backstory="An experienced curriculum planner skilled in sequencing prerequisite chains, handling co-requisites, and observing credit caps.",
        tools=[search_academic_catalog],
        verbose=False,
        llm=llm
    )

    verifier_agent = Agent(
        role="Compliance Auditor",
        goal="Audit draft responses for citation completeness, eliminate hallucinations, enforce safe abstention, and format the output strictly.",
        backstory="A strict academic compliance officer who rejects any claim lacking a citation and enforces the mandatory 5-section layout.",
        verbose=False,
        llm=llm
    )

    return intake_agent, retriever_agent, planner_agent, verifier_agent
