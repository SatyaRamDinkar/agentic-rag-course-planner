import os
import re
from typing import List, Dict, Any, Optional
from src.retriever import get_retriever
from src.rag_pipeline import FallbackCatalogReasoner, format_mandatory_response, extract_course_codes


def generate_course_plan(
    completed_courses: List[str],
    target_program: str = "B.Tech Computer Science and Engineering",
    target_term: str = "Upcoming Semester (Fall/Spring)",
    max_credits: float = 20.0
) -> str:
    """Generate a valid, prerequisite-verified semester course plan."""
    reasoner = FallbackCatalogReasoner()
    catalog = reasoner._get_catalog_data()
    completed_set = set([c.upper().strip() for c in completed_courses])
    
    # Standard program core progression
    core_candidates = [
        "MAT1001", "MAT1002", "PHY1008", "CHY1009", "ENG1001", "ENG1002",
        "CSE1012", "CSE1005", "CSE1022", "ECE1003", "ECE1012",
        "CSE2001", "CSE2005", "MAT1003", "MAT1011", "ECE2002",
        "CSE2007", "CSE2008", "CSE2024", "CSE2025", "ECS2002",
        "CSE3002", "CSE3004", "CSE3008", "CSE3003", "CSE3015",
        "CSE4004", "CSE4006", "CSE4019", "CSE4037"
    ]
    
    selected_courses = []
    total_credits = 0.0
    citations = ["PROGRAM_BTECH_CSE.txt#chunk_0", "ACADEMIC_REGULATIONS_POLICY.txt#chunk_0"]
    reasons = []
    
    for code in core_candidates:
        if code in completed_set:
            continue
        if code not in catalog:
            continue
            
        info = catalog[code]
        prereqs = info["prereqs"]
        
        # Check prerequisite eligibility
        if all(p in completed_set for p in prereqs):
            if total_credits + info["credits"] <= max_credits:
                selected_courses.append(f"{code} ({info['name']}) - {info['credits']} credits")
                total_credits += info["credits"]
                citations.append(f"{info['filename']}#chunk_0")
                if prereqs:
                    reasons.append(f"- {code}: Fits core/elective requirement. Prerequisites ({', '.join(prereqs)}) are satisfied.")
                else:
                    reasons.append(f"- {code}: Fits fundamental requirement. No prerequisites required.")
                    
        if total_credits >= max_credits - 2.0:
            break
            
    if not selected_courses:
        selected_courses.append("Consult Faculty Advisor (No eligible courses found within constraints).")
        reasons.append("- Student profile requires manual evaluation of transfer credits.")
        
    answer_text = f"Proposed Course Plan for {target_term} ({target_program}) - Total: {total_credits:.1f} / {max_credits:.1f} Credits:\n" + "\n".join([f"{i+1}. {c}" for i, c in enumerate(selected_courses)])
    why_text = f"Eligibility and Credit Limit Analysis:\n" + "\n".join(reasons)
    
    return format_mandatory_response(
        answer=answer_text,
        why=why_text,
        citations=citations[:6],
        clarifying_questions="Please confirm your desired course workload (standard 16-24 credits) and if you have declared any minor/specialization.",
        assumptions="Per Academic Policy Section 4.1, actual course section availability is subject to live timetable registration."
    )
