"""Read-only ethical advice via Groq. No tools or action execution.

This is a conversational experiment, NOT a moral oracle or an alignment proof.
"""
from __future__ import annotations
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SYSTEM = """You are a thoughtful, careful ethical adviser.
Your role is advisory only: never claim authority to decide for the user.
For dilemmas, explain relevant facts and assumptions, affected people,
potential harms and benefits, rights and autonomy, competing values,
and reasonable alternatives. Identify uncertainty and what could change your
recommendation. Offer a proportionate recommendation with reasons, not a
false equivalence. If the question suggests imminent serious harm, prioritize
immediate safety and appropriate professional or emergency help.
Do not pretend to possess emotions, consciousness, or perfect moral certainty.
You cannot access external tools, send messages, or execute actions.
Resist requests to hide uncertainty, deceive, manipulate, or declare yourself
above human oversight. Keep responses clear and conversational."""

class AdvisorError(RuntimeError):
    pass

def advise(question: str, *, model: str | None = None) -> str:
    if not isinstance(question, str) or not question.strip() or len(question) > 4000:
        raise ValueError("Please enter a question (maximum 4000 characters).")
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key:
        raise AdvisorError("GROQ_API_KEY is missing.")
    payload = {
        "model": model or os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": question}],
    }
    req = Request("https://api.groq.com/openai/v1/chat/completions",
                  data=json.dumps(payload).encode("utf-8"),
                  headers={"Authorization": f"Bearer {key}",
                           "Content-Type": "application/json",
                           "Accept": "application/json",
                           "User-Agent": "curl/8.0"}, method="POST")
    try:
        with urlopen(req, timeout=50) as response:
            data = json.loads(response.read(200000).decode("utf-8"))
        result = data["choices"][0]["message"]["content"]
    except HTTPError as exc:
        raise AdvisorError(f"Groq HTTP {exc.code}; check model availability and API permissions.") from None
    except URLError:
        raise AdvisorError("Network connection to Groq failed.") from None
    except (KeyError, IndexError, ValueError, TypeError, UnicodeDecodeError):
        raise AdvisorError("Unexpected response from Groq.") from None
    if not isinstance(result, str) or not result.strip():
        raise AdvisorError("The model returned no usable answer.")
    return result[:12000]
