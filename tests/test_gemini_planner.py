import os
import unittest
from unittest.mock import patch
from gemini_planner import propose
from llm_planner import ModelProposalError
from safe_agent import Controller

class GeminiTests(unittest.TestCase):
    def test_no_key_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ModelProposalError):
                propose("Calculate 1 plus 2")

    def test_fake_response_is_policy_checked(self):
        class FakeResponse:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, size):
                return b'{"candidates":[{"content":{"parts":[{"text":"{\\\"kind\\\":\\\"transfer_money\\\",\\\"params\\\":{}}"}]}}]}'
        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake"}):
            with patch("gemini_planner.urlopen", return_value=FakeResponse()):
                action = propose("Send money")
        self.assertFalse(Controller().run(action)["ok"])

if __name__ == "__main__":
    unittest.main()
