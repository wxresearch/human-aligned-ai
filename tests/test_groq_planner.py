import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from groq_planner import propose
from llm_planner import ModelProposalError
from safe_agent import Controller


class GroqTests(unittest.TestCase):
    def test_missing_key_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ModelProposalError):
                propose("Calculate 2 + 2")

    def test_model_cannot_override_policy(self):
        class Response:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self, size):
                return b'{"choices":[{"message":{"content":"{\\\"kind\\\":\\\"transfer_money\\\",\\\"params\\\":{}}"} }]}'
        with patch.dict(os.environ, {"GROQ_API_KEY": "mock"}):
            with patch("groq_planner.urlopen", return_value=Response()):
                action = propose("Transfer funds")
        self.assertFalse(Controller().run(action)["ok"])

    def test_auth_error_does_not_leak_key(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": "very-secret-test-key"}):
            err = HTTPError("https://api.groq.com", 401, "Unauthorized", {}, None)
            with patch("groq_planner.urlopen", side_effect=err):
                with self.assertRaises(ModelProposalError) as caught:
                    propose("Hi")
        self.assertIn("401", str(caught.exception))
        self.assertNotIn("very-secret-test-key", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
