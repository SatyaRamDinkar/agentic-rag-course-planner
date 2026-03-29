from crewai import Agent
from langchain.chat_models import ChatOpenAI
import os

llm = ChatOpenAI(
temperature=0,
openai_api_key=os.getenv("OPENAI_API_KEY")
)

def get_agents():


intake_agent = Agent(
    role="Student Intake Agent",
    goal="Collect missing student info before answering",
    backstory="Expert academic advisor",
    llm=llm
)

retriever_agent = Agent(
    role="Catalog Retriever",
    goal="Fetch relevant course and program requirements",
    backstory="Search expert",
    llm=llm
)

planner_agent = Agent(
    role="Course Planner",
    goal="Generate course plan with strict citations",
    backstory="Academic planning expert",
    llm=llm
)

verifier_agent = Agent(
    role="Verifier",
    goal="Check if all answers have citations and no hallucination",
    backstory="Strict auditor",
    llm=llm
)

return intake_agent, retriever_agent, planner_agent, verifier_agent


