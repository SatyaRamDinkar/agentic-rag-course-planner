import os
import sys
import csv
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_pipeline import ask_question
from evaluation.metrics import evaluate


def run_evaluation(benchmark_csv="evaluation/evaluation_benchmark.csv", output_csv="evaluation/evaluation_results.csv"):
    """Run full evaluation suite across the 25 benchmark queries."""
    if not os.path.exists(benchmark_csv):
        print(f"Error: {benchmark_csv} not found.")
        return

    queries_data = []
    with open(benchmark_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            queries_data.append(row)

    print(f"Running evaluation benchmark on {len(queries_data)} queries...\n")
    results = []

    for idx, item in enumerate(queries_data):
        q = item["Query"]
        cat = item["Category"]
        exp = item["Expected_Decision"]
        
        start_time = time.time()
        response = ask_question(q)
        duration = round(time.time() - start_time, 2)
        
        results.append({
            "query": q,
            "category": cat,
            "expected": exp,
            "response": response,
            "latency_seconds": duration
        })
        print(f"[{idx+1}/{len(queries_data)}] ({cat}) {q[:50]}... [{duration}s]")

    # Run metrics
    metrics = evaluate(results)

    # Save to output CSV
    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["Query", "Category", "Expected_Decision", "Agent_Response", "Latency_Seconds"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "Query": r["query"],
                "Category": r["category"],
                "Expected_Decision": r["expected"],
                "Agent_Response": r["response"],
                "Latency_Seconds": r["latency_seconds"]
            })

    print(f"\nEvaluation results exported to '{output_csv}'.")
    return metrics


if __name__ == "__main__":
    run_evaluation()
