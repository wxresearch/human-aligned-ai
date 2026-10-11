"""Groq API planner. All model output is treated as an untrusted proposal."""
from __future__ import annotations
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from llm_planner import ModelProposalError, parse_proposal, SYSTEM
from safe_agent import Action


def propose(instruction: str, *, model: str | None = None) -> Action:
    if not isinstance(instruction, str) or not instruction.strip() or len(instruction) > 4000:
        raise ValueError("Instruction must contain 1 to 4000 characters")
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise ModelProposalError("GROQ_API_KEY is not set; no action executed")
    model_name = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    payload = {
        "model": model_name,
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": instruction}],
        "response_format": {"type": "json_object"},
        "temperature": 0,
    }
    request = Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=40) as response:
            result = json.loads(response.read(100_000).decode("utf-8"))
        raw = result["choices"][0]["message"]["content"]
    except HTTPError as exc:
        descriptions = {
            400: "Invalid request or unsupported model settings",
            401: "Invalid or expired Groq API key",
            403: "Permission denied",
            404: "Model unavailable or model ID incorrect",
            429: "Rate limit or quota reached",
            500: "Groq server error",
            503: "Groq service unavailable",
        }
        message = descriptions.get(exc.code, "Check your Groq API account")
        raise ModelProposalError(f"Groq HTTP {exc.code}: {message}; no action executed") from None
    except URLError:
        raise ModelProposalError("Network connection to Groq failed; no action executed") from None
    except (ValueError, KeyError, IndexError, TypeError):
        raise ModelProposalError("Unexpected Groq API response; no action executed") from None
    if not isinstance(raw, str):
        raise ModelProposalError("Groq response had no text; no action executed")
    return parse_proposal(raw)
