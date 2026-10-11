"""Run a Groq-backed model with independent default-deny checking."""
import argparse
import json
from groq_planner import propose
from llm_planner import ModelProposalError
from safe_agent import Controller


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instruction")
    parser.add_argument("--model", default=None)
    args = parser.parse_args()
    try:
        action = propose(args.instruction, model=args.model)
    except (ModelProposalError, ValueError) as exc:
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 1
    print(json.dumps(Controller().run(action), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
