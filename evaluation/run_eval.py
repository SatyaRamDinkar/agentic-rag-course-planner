from src.agent_pipeline import run_agent_pipeline
from evaluation.metrics import evaluate

outputs = []

with open("evaluation/test_queries.txt") as f:
queries = f.readlines()

for q in queries:
result = run_agent_pipeline(q.strip())
outputs.append(result)
print(result)
print("="*50)

evaluate(outputs)
