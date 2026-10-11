import unittest

from safe_agent import Action, Controller, Decision, Policy


class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()

    def test_arithmetic_allowed(self):
        result = self.controller.run(Action("calculate", {"a": 6, "b": 7, "operator": "*"}))
        self.assertTrue(result["ok"])
        self.assertEqual(result["result"], 42)

    def test_unauthorized_actions_denied(self):
        for kind in ("send_message", "transfer_money", "modify_policy", "self_modify", "unknown"):
            with self.subTest(kind=kind):
                self.assertFalse(self.controller.run(Action(kind, {}))["ok"])

    def test_zero_division_denied(self):
        self.assertFalse(self.controller.run(Action("calculate", {"a": 1, "b": 0, "operator": "/"}))["ok"])

    def test_nonfinite_number_denied(self):
        self.assertEqual(Policy().evaluate(Action("calculate", {"a": float("nan"), "b": 1, "operator": "+"})).decision, Decision.DENY)

    def test_drafting_is_not_sending(self):
        result = self.controller.run(Action("draft_message", {"recipient": "reviewer", "message": "Hello"}))
        self.assertTrue(result["ok"])
        self.assertIn("draft", result)
        self.assertEqual(len(self.controller.audit_log), 1)


if __name__ == "__main__":
    unittest.main()
