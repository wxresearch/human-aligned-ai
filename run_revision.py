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
    print("Ask a dilemma, then add new evidence or corrections. Use /hypothesis TEXT, /fact TEXT, /ledger or /quit.")
    while True:
        try:
            q = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in ("/quit", "/exit"):
            break
        if not q:
            continue
        if q == "/ledger":
            for i, item in enumerate(session.ledger(), 1):
                print(f"{i}. [{item['status']}] {item['statement']}")
            continue
        if q.startswith("/fact ") or q.startswith("/hypothesis "):
            status = "unverified" if q.startswith("/fact ") else "hypothetical"
            try:
                session.add_anchor(q.split(" ", 1)[1], status=status)
                print("Recorded as user-supplied evidence, NOT independently verified.")
            except ValueError as exc:
                print(f"Error: {exc}")
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
