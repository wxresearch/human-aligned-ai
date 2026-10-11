"""List model identifiers visible to this Groq API key, without displaying credentials."""
import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def main():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("GROQ_API_KEY is missing. Set it in this CMD window.")
        return 1
    req = Request("https://api.groq.com/openai/v1/models",
                  headers={"Authorization": f"Bearer {key}"})
    try:
        with urlopen(req, timeout=20) as response:
            payload = json.loads(response.read(200000))
        models = [x["id"] for x in payload.get("data", [])
                  if isinstance(x, dict) and isinstance(x.get("id"), str)]
        print("Model IDs returned by your Groq key:")
        for model in sorted(models):
            print("  " + model)
        if not models:
            print("(No models listed.)")
    except HTTPError as exc:
        print(f"Groq returned HTTP {exc.code}; check permissions.")
        return 1
    except (URLError, ValueError, KeyError, TypeError):
        print("Unable to retrieve models; check connection.")
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
