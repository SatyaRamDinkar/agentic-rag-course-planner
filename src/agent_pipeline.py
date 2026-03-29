from crewai import Task, Crew
from src.agents import get_agents
from src.retriever import get_retriever

def run_agent_pipeline(query):


intake, retriever_agent, planner, verifier = get_agents()
retriever = get_retriever()

# Step 1: Retrieve documents
docs = retriever.get_relevant_documents(query)
context = "\n\n".join([doc.page_content for doc in docs])

# Task 1: Intake
intake_task = Task(
    description=f"Check if query needs more student info: {query}",
    agent=intake
)

# Task 2: Planning
planning_task = Task(
    description=f"""


Answer the question using ONLY this context:

{context}

Follow format:
Answer:
Why:
Citations:
Clarifying Questions:
Assumptions:
""",
agent=planner
)


# Task 3: Verification
verify_task = Task(
    description="Check if answer has citations and no hallucination",
    agent=verifier
)

crew = Crew(
    agents=[intake, planner, verifier],
    tasks=[intake_task, planning_task, verify_task]
)

result = crew.kickoff()
return result


