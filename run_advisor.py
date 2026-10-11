"""Ask an ethical question using the Groq API, without tools or execution."""
import argparse
from ethical_advisor import AdvisorError, advise

def main():
    parser = argparse.ArgumentParser(description="Read-only Ethical Advisor")
    parser.add_argument("question", nargs="?", help="Question or dilemma")
    parser.add_argument("--model", help="Groq model ID")
    args = parser.parse_args()
    question = args.question or input("Your ethical question: ")
    try:
        print("\nAI advice (not an authoritative moral ruling):\n")
        print(advise(question, model=args.model))
    except (AdvisorError, ValueError) as exc:
        print(f"Could not get advice: {exc}")
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
