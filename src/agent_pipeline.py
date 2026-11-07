import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from crewai import Task, Crew, Process

from src.agents import get_agents, get_llm
from src.retriever import get_retriever
from src.rag_pipeline import FallbackCatalogReasoner, format_mandatory_response

load_dotenv()


def run_agent_pipeline(query: str) -> str:
    """Run the 4-agent sequential workflow for student advising and course planning.
    
    If OpenAI API credentials are available, kicks off the full CrewAI agent team.
    Otherwise, uses the deterministic catalog reasoner with zero compromise on
    citations, formatting, and correctness.
    """
    llm = get_llm()
    retriever = get_retriever()
    
    if llm is not None:
        try:
            intake, retriever_agent, planner, verifier = get_agents()
            
            task_intake = Task(
                description=f"Analyze student query: '{query}'. Identify completed courses, grades, major, target term, and credit limits. Note any missing info.",
                expected_output="Normalized student profile with missing parameters highlighted.",
                agent=intake
            )

            task_retrieve = Task(
                description="Search the catalog for all course prerequisites, degree core/electives, and policies needed for the student profile.",
                expected_output="Curated catalog evidence with exact file and chunk citations.",
                agent=retriever_agent
            )

            task_plan = Task(
                description="Draft the eligibility decision or proposed course plan based solely on catalog evidence from the previous step. Explain step-by-step why requirements are satisfied.",
                expected_output="Drafted academic recommendation with logical reasoning.",
                agent=planner
            )

            task_verify = Task(
                description="""Audit the draft response. Ensure every single claim is cited with source and chunk IDs. Strip any uncited statements. If policy is missing, output 'I don't have that information in the provided catalog/policies.'
                Format the final output EXACTLY as:
                
Answer / Plan:
<Decision / Course List>

Why (requirements/prereqs satisfied):
<Prerequisite logic and evidence>

Citations:
<Exact source and chunk IDs>

Clarifying questions (if needed):
<1-3 questions or None>

Assumptions / Not in catalog:
<What to check next or assumptions made>
""",
                expected_output="Strictly formatted compliance-verified response.",
                agent=verifier
            )

            crew = Crew(
                agents=[intake, retriever_agent, planner, verifier],
                tasks=[task_intake, task_retrieve, task_plan, task_verify],
                process=Process.sequential,
                verbose=False
            )

            return str(crew.kickoff())
        except Exception as e:
            print(f"[Agent Pipeline] CrewAI execution error ({e}). Using catalog reasoner.")
            reasoner = FallbackCatalogReasoner(retriever=retriever)
            return reasoner.answer_query(query)
    else:
        reasoner = FallbackCatalogReasoner(retriever=retriever)
        return reasoner.answer_query(query)
