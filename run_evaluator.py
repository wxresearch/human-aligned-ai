"""Offline regression tests, or apply human-authored checks to a saved AI answer."""
import argparse
import json
from pathlib import Path
from evidence_evaluator import evaluate_file, evaluate_case

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="evaluation_cases/smartphone.json",
                        help="Curated cases (JSON) or expected-rules file when --answer-file is set")
    parser.add_argument("--answer-file", help="Plain text file containing an actual advisor answer")
    args = parser.parse_args()
    try:
        if args.answer_file:
            rules = json.loads(Path(args.file).read_text(encoding="utf-8"))
            if not isinstance(rules, list) or not rules:
                raise ValueError("Need at least one evaluation case")
            answer = Path(args.answer_file).read_text(encoding="utf-8")
            result = evaluate_case({**rules[0], "answer": answer})
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0 if result["passed"] else 1
        result = evaluate_file(args.file)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("Note: bundled examples include deliberate failures for regression testing.")
        return 0  # Expected intentionally failing demonstrations are not a runner error.
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Evaluation input error: {exc}")
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
