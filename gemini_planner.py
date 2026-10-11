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
    except HTTPError as exc:
        # Only print recognized Google error codes/reasons, never response text
        # (which could contain sensitive account details).
        reason = ""
        try:
            body = json.loads(exc.read(8192).decode("utf-8"))
            details = body.get("error", {}).get("details", [])
            candidates = [d.get("reason", "") for d in details if isinstance(d, dict)]
            known = {
                "API_KEY_INVALID", "API_KEY_EXPIRED", "API_KEY_SERVICE_BLOCKED",
                "API_KEY_HTTP_REFERRER_BLOCKED", "API_KEY_IP_ADDRESS_BLOCKED",
                "API_KEY_API_TARGET_BLOCKED", "SERVICE_DISABLED",
            }
            reason = next((r for r in candidates if r in known), "")
            status = body.get("error", {}).get("status", "")
            if not reason and status in {"FAILED_PRECONDITION", "INVALID_ARGUMENT", "PERMISSION_DENIED", "RESOURCE_EXHAUSTED"}:
                reason = status
        except (ValueError, AttributeError, UnicodeDecodeError, OSError):
            pass
        guidance = {
            400: "Invalid request or API key; check the Gemini API key and request format.",
            401: "Authentication failed; check the API key.",
            403: "Permission denied; check API key restrictions, API access or billing.",
            404: "Model not found or not available to this API key; try a supported model.",
            429: "Quota or rate limit reached; check Google AI Studio usage and billing.",
            500: "Google server error; retry later.",
            503: "Gemini temporarily unavailable; retry later.",
        }.get(exc.code, "See Google AI Studio API access and model settings.")
        detail = f" ({reason})" if reason else ""
        if reason in {"API_KEY_INVALID", "API_KEY_EXPIRED"}:
            guidance = "The Gemini key is invalid or expired. Create a new key in Google AI Studio."
        elif reason == "FAILED_PRECONDITION":
            guidance = "Project prerequisites may be unmet (e.g. billing/region); check Google AI Studio."
        raise ModelProposalError(f"Gemini HTTP {exc.code}{detail}: {guidance} No action executed.") from None
    except URLError:
        raise ModelProposalError("Network error contacting Gemini; check internet, proxy or firewall. No action executed.") from None
    except (KeyError, IndexError, TypeError, ValueError):
        raise ModelProposalError("Unexpected Gemini response; no action executed.") from None
    return parse_proposal(raw)
