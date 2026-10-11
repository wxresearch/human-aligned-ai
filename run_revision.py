"""Read-only multi-turn ethical advisor CLI (type /quit to exit)."""
import argparse
from revision_session import RevisionSession
from ethical_advisor import AdvisorError

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default=None)
    p.add_argument("--save", default=None, help="Optional local JSON transcript path")
    args = p.parse_args()
    session = RevisionSession(model=args.model)
    print("Ethical Advisor: evidence-revision experiment.")
    print("Ask a dilemma, then add new evidence or corrections. Type /quit to finish.")
    while True:
        try:
            q = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in ("/quit", "/exit"):
            break
        if not q:
            continue
        try:
            print("\nAdvisor:\n" + session.ask(q))
        except (AdvisorError, ValueError) as exc:
            print(f"Error: {exc}")
    if args.save:
        session.save(args.save)
        print(f"Transcript saved to {args.save}")

if __name__ == "__main__":
    main()
