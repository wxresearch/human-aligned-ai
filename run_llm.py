"""CLI for optional real-model planning through the default-deny controller."""
import argparse
import json

from llm_planner import ModelProposalError, propose
from safe_agent import Controller


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instruction", help="What to ask the model to propose")
    parser.add_argument("--model", default=None, help="Model ID (default: OPENAI_MODEL or gpt-4o-mini)")
    args = parser.parse_args()
    controller = Controller()
    try:
        proposal = propose(args.instruction, model=args.model)
    except ModelProposalError as exc:
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 1
    print(json.dumps(controller.run(proposal), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
