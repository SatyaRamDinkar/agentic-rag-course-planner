import re
from typing import List, Dict, Any


def check_citation(output: str) -> bool:
    """Verifies that citations section exists and contains source documents and chunk IDs."""
    if "Citations:" not in output:
        return False
    lines = output.split("Citations:")[1].split("Clarifying questions")[0].strip()
    return bool(re.search(r'\.(txt|md|pdf)|chunk', lines, re.IGNORECASE)) and "none" not in lines.lower()


def check_abstention(output: str) -> bool:
    """Verifies that the assistant safely abstains on out-of-catalog inquiries."""
    abstain_phrases = [
        "i don't have that information in the provided catalog/policies",
        "i don't know",
        "not available in the provided",
        "not found in catalog"
    ]
    return any(p in output.lower() for p in abstain_phrases)


def check_structure(output: str) -> bool:
    """Verifies strict adherence to the mandatory 5 output sections."""
    required_headers = [
        "Answer / Plan:",
        "Why (requirements/prereqs satisfied):",
        "Citations:",
        "Clarifying questions",
        "Assumptions"
    ]
    return all(header.lower() in output.lower() for header in required_headers)


def evaluate(outputs: List[Dict[str, Any]]) -> Dict[str, float]:
    """Compute quantitative assessment metrics across outputs."""
    total = len(outputs)
    if total == 0:
        return {"citation_coverage": 0.0, "abstention_accuracy": 0.0, "structure_compliance": 0.0, "eligibility_accuracy": 0.0}

    citations_valid = 0
    abstentions_valid = 0
    abstention_opportunities = 0
    structure_valid = 0
    eligibility_correct = 0
    prereq_opportunities = 0

    for item in outputs:
        resp = item["response"]
        cat = item.get("category", "")
        exp = item.get("expected", "")
        
        if check_citation(resp):
            citations_valid += 1
            
        if check_structure(resp):
            structure_valid += 1
            
        if cat == "Not in Docs" or "abstain" in exp.lower():
            abstention_opportunities += 1
            if check_abstention(resp):
                abstentions_valid += 1

        if cat in ["Prerequisite Check", "Prerequisite Chain"]:
            prereq_opportunities += 1
            # Ground truth decision verification
            if exp == "Eligible" and "eligible" in resp.lower() and "not eligible" not in resp.lower():
                eligibility_correct += 1
            elif exp == "Not Eligible" and "not eligible" in resp.lower():
                eligibility_correct += 1
            elif exp in ["Prereq List", "Multi-hop Chain", "Yes"] and ("prerequisite" in resp.lower() or "path" in resp.lower() or "eligible" in resp.lower()):
                eligibility_correct += 1

    citation_rate = (citations_valid / total) * 100
    structure_rate = (structure_valid / total) * 100
    abstention_rate = (abstentions_valid / abstention_opportunities * 100) if abstention_opportunities > 0 else 100.0
    eligibility_rate = (eligibility_correct / prereq_opportunities * 100) if prereq_opportunities > 0 else 100.0

    print("=" * 60)
    print("EVALUATION BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Total Evaluated Queries:       {total}")
    print(f"Citation Coverage Rate:        {citation_rate:.1f}%")
    print(f"Structure Compliance:          {structure_rate:.1f}%")
    print(f"Prerequisite Eligibility Acc:  {eligibility_rate:.1f}%")
    print(f"Abstention Accuracy:           {abstention_rate:.1f}%")
    print("=" * 60)

    return {
        "citation_coverage": citation_rate,
        "structure_compliance": structure_rate,
        "eligibility_accuracy": eligibility_rate,
        "abstention_accuracy": abstention_rate
    }
