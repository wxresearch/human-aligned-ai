import unittest
from safe_agent import Action
from oversight import ApprovalRegistry, fingerprint, review_proposal
from ethics import review
from research_eval import run_suite

class OversightEthicsTests(unittest.TestCase):
    def test_approval_is_required(self):
        action = Action("propose_publication", {"summary": "Example"})
        reg = ApprovalRegistry()
        self.assertFalse(review_proposal(action, reg)["ok"])
        reg.record(action, "human", True)
        self.assertTrue(review_proposal(action, reg)["ok"])

    def test_approval_is_specific(self):
        reg = ApprovalRegistry()
        reg.record(Action("propose_publication", {"summary": "A"}), "human", True)
        self.assertFalse(review_proposal(Action("propose_publication", {"summary": "B"}), reg)["ok"])

    def test_rejection_and_unreviewable_actions(self):
        reg = ApprovalRegistry()
        a = Action("propose_policy_change", {"summary": "Example"})
        reg.record(a, "human", False)
        self.assertFalse(review_proposal(a, reg)["ok"])
        self.assertFalse(review_proposal(Action("transfer_money", {"summary": "Example"}), reg)["ok"])

    def test_ethics_prompts_uncertainty(self):
        result = review("An important decision").as_dict()
        self.assertIn("uncertainty", result)
        self.assertIn("human", result["recommendation"].lower())

    def test_evaluation_suite(self):
        result = run_suite()
        self.assertEqual(result["passed"], result["total"])

if __name__ == "__main__":
    unittest.main()
