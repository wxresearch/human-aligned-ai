import unittest
from evidence_evaluator import evaluate_case, evaluate_file

class EvidenceEvaluatorTests(unittest.TestCase):
    def test_fixture_expected_one_pass_two_fails(self):
        result = evaluate_file("evaluation_cases/smartphone.json")
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["passed"], 1)

    def test_detects_missing_hypothetical_qualifier(self):
        result = evaluate_case({"answer": "The study demonstrated harm.",
            "required_patterns": ["hypothetical"]})
        self.assertFalse(result["passed"])

    def test_flags_reversed_finding(self):
        result = evaluate_case({"answer": "The ban improved academic performance.",
            "forbidden_patterns": ["ban improved academic performance"]})
        self.assertFalse(result["passed"])

    def test_does_not_claim_semantic_verification(self):
        result = evaluate_case({"answer": "Anything.", "required_patterns": []})
        self.assertIn("Pattern checks only", result["note"])

if __name__ == "__main__":
    unittest.main()
