"""Multi-turn read-only ethical advisor with visible revision history.

No tools and no autonomous actions. Conversation lives in memory only.
"""
import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from ethical_advisor import SYSTEM, AdvisorError

MAX_TURNS = 12
MAX_MESSAGE = 4000

class RevisionSession:
    def __init__(self, model=None):
        self.model = model or os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
        self.messages = [{"role": "system", "content": SYSTEM + """
During follow-up turns, explicitly say whether your recommendation changed,
why, which evidence mattered, and what is still uncertain. Do not agree with
claims solely to please the user; assess credibility. Do not invent sources.
Keep responses fairly concise unless the user requests detail."""}]
        self.log = []

    def ask(self, question):
        if not isinstance(question, str) or not question.strip() or len(question) > MAX_MESSAGE:
            raise ValueError("Question must contain 1-4000 characters")
        if len(self.log) >= MAX_TURNS:
            raise AdvisorError("Session turn limit reached; start a new session.")
        key = os.getenv("GROQ_API_KEY", "").strip()
        if not key:
            raise AdvisorError("GROQ_API_KEY is missing.")
        proposed_messages = self.messages + [{"role": "user", "content": question}]
        payload = {"model": self.model, "messages": proposed_messages}
        request = Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                     "Accept": "application/json", "User-Agent": "curl/8.0"},
            method="POST")
        try:
            with urlopen(request, timeout=50) as response:
                result = json.loads(response.read(200000).decode("utf-8"))
            answer = result["choices"][0]["message"]["content"]
        except HTTPError as exc:
            raise AdvisorError(f"Groq HTTP {exc.code}; no conversation turn recorded.") from None
        except URLError:
            raise AdvisorError("Network failure; no conversation turn recorded.") from None
        except (ValueError, IndexError, KeyError, TypeError, UnicodeDecodeError):
            raise AdvisorError("Unexpected Groq response; no conversation turn recorded.") from None
        if not isinstance(answer, str) or not answer.strip():
            raise AdvisorError("Empty model answer; no conversation turn recorded.")
        answer = answer[:12000]
        self.messages = proposed_messages + [{"role": "assistant", "content": answer}]
        self.log.append({"round": len(self.log)+1, "question": question, "answer": answer})
        return answer

    def save(self, path):
        # Caller selects the location. No API keys or system prompts saved.
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"model": self.model, "turns": self.log}, f, ensure_ascii=False, indent=2)
