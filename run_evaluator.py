"""Evaluate curated evidence consistency cases without any API calls."""
import argparse
import json
from evidence_evaluator import evaluate_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="evaluation_cases/smartphone.json")
    args = parser.parse_args()
    try:
        results = evaluate_file(args.file)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Evaluation input error: {exc}")
        return 2
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0 if results["passed"] == results["total"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
