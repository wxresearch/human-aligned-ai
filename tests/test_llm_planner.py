import unittest

from llm_planner import ModelProposalError, parse_proposal
from safe_agent import Controller


class ModelPlannerTests(unittest.TestCase):
    def test_calculation_goes_through_controller(self):
        proposal = parse_proposal('{"kind":"calculate","params":{"a":2,"b":3,"operator":"+"}}')
        self.assertEqual(Controller().run(proposal)["result"], 5)

    def test_model_cannot_authorize_transfer(self):
        proposal = parse_proposal('{"kind":"transfer_money","params":{"amount":1000}}')
        self.assertFalse(Controller().run(proposal)["ok"])

    def test_rejects_malformed_responses(self):
        for raw in ("not json", "[]", '{"kind":"calculate"}', '{"kind":1,"params":{}}'):
            with self.subTest(raw=raw):
                with self.assertRaises(ModelProposalError):
                    parse_proposal(raw)

    def test_does_not_accept_model_policy_override(self):
        with self.assertRaises(ModelProposalError):
            parse_proposal('{"kind":"calculate","params":{},"authorized":true}')


if __name__ == "__main__":
    unittest.main()
