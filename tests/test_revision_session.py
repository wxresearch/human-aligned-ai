import os
import unittest
from unittest.mock import patch
from revision_session import RevisionSession
from ethical_advisor import AdvisorError

class RevisionTests(unittest.TestCase):
    def test_context_and_revision_history(self):
        calls = []
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, _):
                return b'{"choices":[{"message":{"content":"I should revise my advice given that evidence."}}]}'
        def fake(request, timeout):
            import json
            calls.append(json.loads(request.data))
            return Response()
        with patch.dict(os.environ, {"GROQ_API_KEY": "mock"}):
            with patch("revision_session.urlopen", side_effect=fake):
                session = RevisionSession()
                session.ask("Initial dilemma")
                session.ask("New evidence")
        self.assertEqual(len(session.log), 2)
        self.assertEqual([m["role"] for m in calls[1]["messages"]],
                         ["system", "user", "assistant", "user"])
        self.assertEqual(calls[1]["messages"][1]["content"], "Initial dilemma")

    def test_grounded_hypothetical_claim(self):
        session = RevisionSession()
        claim = "Hypothetical study: ban did NOT improve academic performance."
        session.add_anchor(claim, "hypothetical")
        session.add_anchor("Ban DID interfere with assistive technology.", "hypothetical")
        prompt = session._compact_messages("Reconsider this.")
        self.assertIn(claim, prompt[0]["content"])
        self.assertIn("not independently verified", prompt[0]["content"])
        self.assertEqual(session.ledger()[0]["statement"], claim)

    def test_failed_request_does_not_change_history(self):
        s = RevisionSession()
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(AdvisorError):
                s.ask("Example")
        self.assertEqual(len(s.log), 0)

    def test_limits(self):
        s = RevisionSession()
        with self.assertRaises(ValueError):
            s.ask(" ")
        with self.assertRaises(ValueError):
            s.ask("x"*4001)

if __name__ == "__main__":
    unittest.main()
