"""Google Gemini planner: proposes untrusted actions, never executes tools."""
from __future__ import annotations
import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from llm_planner import ModelProposalError, parse_proposal, SYSTEM
from safe_agent import Action

def propose(instruction: str, *, model: str | None = None) -> Action:
    if not isinstance(instruction, str) or not instruction.strip() or len(instruction) > 4000:
        raise ValueError("Instruction must contain 1 to 4000 characters")
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ModelProposalError("Set GEMINI_API_KEY in Command Prompt first")
    model_name = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    if not isinstance(model_name, str) or not model_name.replace("-", "").replace(".", "").isalnum():
        raise ModelProposalError("Invalid model name")
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM}]},
        "contents": [{"role": "user", "parts": [{"text": instruction}]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    request = Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent",
        data=json.dumps(payload).encode("utf-8"),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=45) as response:
            obj = json.loads(response.read(100_000).decode("utf-8"))
        parts = obj["candidates"][0]["content"]["parts"]
        raw = "".join(part.get("text", "") for part in parts)
    except (HTTPError, URLError, KeyError, IndexError, TypeError, ValueError) as exc:
        raise ModelProposalError("Gemini request failed; no action was executed. Check API key, model access and quota.") from exc
    return parse_proposal(raw)
