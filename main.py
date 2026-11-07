import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from src.rag_pipeline import ask_question
from src.course_planner import generate_course_plan

load_dotenv()


def main():
    print("=" * 70)
    print("  GRADUATE & UNDERGRADUATE COURSE PLANNING ASSISTANT (CLI)")
    print("  Catalog-Grounded RAG System with CrewAI & LangChain")
    print("=" * 70)
    print("Commands:")
    print("  1. Type your question directly (e.g., 'Can I take CSE4019 if I finished CSE3002, CSE3004, CSE3008, CSE3015?')")
    print("  2. Type 'plan' to generate a personalized semester course plan")
    print("  3. Type 'eval' to run the 25-query benchmark evaluation suite")
    print("  4. Type 'exit' or 'quit' to close\n")

    while True:
        try:
            user_input = input("Student Query >> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting Assistant. Best of luck with your academics!")
                break
            elif user_input.lower() == "eval":
                print("\nExecuting evaluation suite...")
                from evaluation.run_eval import run_evaluation
                run_evaluation()
                print("\n")
            elif user_input.lower() == "plan":
                completed = input("Enter completed courses (comma-separated, e.g. CSE1012, MAT1001, CSE2005): ")
                comp_list = [c.strip() for c in completed.split(",") if c.strip()]
                credits_str = input("Max credits for next term [default 20.0]: ").strip()
                max_credits = float(credits_str) if credits_str else 20.0
                print("\nGenerating grounded course plan...\n")
                result = generate_course_plan(completed_courses=comp_list, max_credits=max_credits)
                print(result)
                print("\n" + "-" * 70 + "\n")
            else:
                print("\nProcessing request against catalog documents...\n")
                result = ask_question(user_input)
                print(result)
                print("\n" + "-" * 70 + "\n")
        except KeyboardInterrupt:
            print("\nExiting Assistant.")
            break
        except Exception as e:
            print(f"\n[Error]: {e}\n")


if __name__ == "__main__":
    main()
