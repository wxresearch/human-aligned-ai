import os
import unittest
from unittest.mock import patch
from ethical_advisor import AdvisorError, advise, SYSTEM

class EthicalAdvisorTests(unittest.TestCase):
    def test_missing_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(AdvisorError):
                advise("Should I apologize?")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            advise(" ")

    def test_no_tools_and_human_agency_in_system_prompt(self):
        self.assertIn("advisory only", SYSTEM)
        self.assertIn("cannot access external tools", SYSTEM)

    def test_mocked_answer(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, count):
                return b'{"choices":[{"message":{"content":"Tell the truth kindly."}}]}'
        with patch.dict(os.environ, {"GROQ_API_KEY": "mock"}):
            with patch("ethical_advisor.urlopen", return_value=Response()) as send:
                answer = advise("Should I lie?")
                self.assertEqual(answer, "Tell the truth kindly.")
                self.assertEqual(send.call_count, 1)
                request = send.call_args.args[0]
                self.assertEqual(request.full_url, "https://api.groq.com/openai/v1/chat/completions")

if __name__ == "__main__":
    unittest.main()
