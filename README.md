# Human-aligned AI — control prototype

This repository demonstrates a **human-governed AI architecture**. It is **not** a superintelligent system, a trained moral agent, or a proof of alignment.

## Run

Requires Python 3.10+ with no third-party dependencies.

```bash
python safe_agent.py
python -m unittest discover -s tests -v
```

## Architecture

1. An **untrusted planner** proposes an action.
2. A separate **default-deny policy** decides whether that action is allowed.
3. A controller executes only explicitly permitted, narrow operations.
4. Each attempt is recorded in an **in-memory audit log**.

Permitted demo operations: arithmetic and drafting (not sending) a message. Money transfers, sending messages, policy modification, self-modification, and unknown actions are denied.

## Threat model and limitations

The planner is a stub, not a language model. No network, shell, or money-transfer tools are exposed through the controller. This **does not** prevent an independently privileged model from taking action outside the controller. The Python modules are not an isolation/security boundary; an adversary able to run arbitrary Python in the same process can alter them. The audit log is neither durable nor tamper-evident. The controller does not determine whether a drafted message is truthful or ethical.

**Do not deploy this prototype as a security boundary for an adversarial agent.**

## Research roadmap

- Isolate the planner in a separate sandboxed process with zero direct tool privileges.
- Validate action schemas and bound computational resources.
- Add a trusted human approval mechanism for higher-impact actions.
- Add adversarial tests for bypass attempts and prompt injection.
- Evaluate oversight failure modes, interpretability, and corrigibility.
- Require independent safety review before expanding autonomy or tool access.

The objective is to investigate **how increasingly capable AI could remain accountable to human governance**—not to assume this has already been solved.

## v0.2 — optional real language model

To let a real model **propose** an action (nothing is executed unless the
independent controller allows it), set an API key locally and run:

```bash
# macOS / Linux
export OPENAI_API_KEY="your-api-key"
python run_llm.py "Calculate 12 times 7"
python run_llm.py "Draft a friendly message for my reviewer"
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-api-key"
python run_llm.py "Calculate 12 times 7"
```

You can override the model with `--model MODEL_ID` or `OPENAI_MODEL`.
The API may incur charges. **Never commit API keys.**

The model receives only the user instruction and a restricted JSON action
schema. Its output is parsed as an *untrusted proposal* and checked by the
same default-deny controller. Invalid responses fail closed. Neither the
model nor a suggested action can authorize sending messages, transferring
money, or modifying the policy.

```bash
python -m unittest discover -s tests -v
```

**Important limits:** This is an educational in-process controller, not a
sandbox, formal safety proof, moral reasoner, or reliable defense against a
malicious superintelligence. The HTTP request is made by a separate
conventional client; the model is not given tool execution privileges.

## v0.3–v1.0 research scaffolding

These are **early experiments**, not completed safety milestones:

- `oversight.py`: human-review records keyed to exact proposals; approved
  proposals remain **simulation-only**. Approval is in memory, not authenticated.
- `ethics.py`: a review questionnaire covering well-being, autonomy, truth,
  fairness, reversibility, and uncertainty. It provides **no moral verdict**.
- `research_eval.py`: repeatable adversarial policy/parser examples.
- `RESEARCH.md`: hypotheses, evidence standards, open questions, and threat model.

Run all unit tests and the scenario harness:

```bash
python -m unittest discover -s tests -v
python research_eval.py
```

Example of simulated human approval (no external actions):

```python
from safe_agent import Action
from oversight import ApprovalRegistry, review_proposal

proposal = Action("propose_publication", {"summary": "Publish research overview"})
registry = ApprovalRegistry()
print(review_proposal(proposal, registry))  # denied until approved
registry.record(proposal, reviewer="human", approved=True)
print(review_proposal(proposal, registry))  # simulation-only approval
```

**Limitations:** approval has no identity authentication or durable storage,
the model can still generate misleading prose, and checklist-based ethical
reflection is not proof of moral behavior. Do not treat this as a security
boundary or a deployable autonomous agent.

## Getting started in Windows Command Prompt (cmd.exe)

These steps use **Command Prompt**, not PowerShell.

1. Install **Python 3.10+** from https://www.python.org/downloads/ (check **Add python.exe to PATH** during installation). Install **Git** from https://git-scm.com/download/win.
2. Open Command Prompt: press **Win + R**, enter `cmd`, and press Enter.
3. Verify the tools:

   ```cmd
   py --version
   git --version
   ```

4. Download the project and enter its directory:

   ```cmd
   git clone https://github.com/wxresearch/human-aligned-ai.git
   cd human-aligned-ai
   ```

   If you already cloned it earlier, instead run `cd human-aligned-ai` and `git pull` from the directory containing the repository. Since the repository is private, Git may prompt you to sign in to GitHub.

5. **Test without any API key (recommended first):**

   ```cmd
   py safe_agent.py
   py -m unittest discover -s tests -v
   py research_eval.py
   ```

   The demo shows permitted and blocked actions. Unit tests should show **OK** and the scenario report should show all checks passing. If you get failures, capture the traceback and investigate before proceeding.

6. **Optional: test the real AI planner.** Create an OpenAI API key through the API platform, and in **the same Command Prompt window** set it for this session:

   ```cmd
   set "OPENAI_API_KEY=put-your-key-here"
   py run_llm.py "Calculate 12 times 7"
   py run_llm.py "Draft a friendly message to my reviewer"
   ```

   API use may incur charges. **Never paste your real key in screenshots, chats, or commits.** The key is not required for the tests in step 5. The default model may need to be changed if it is unavailable to your API account, using `--model MODEL_ID`.

7. When finished, close Command Prompt to clear this session's `OPENAI_API_KEY` environment variable (or run `set OPENAI_API_KEY=`).

**Safety note:** This is a local educational prototype, not a hardened sandbox or proof of alignment. The approval demonstration authorizes only *simulated* proposals; it does not publish or send anything.

## Use Google Gemini instead of OpenAI (Windows Command Prompt)

You **do not need an OpenAI API key** to run the Gemini option.

1. In Command Prompt, go to the project folder and get updates:

   ```cmd
   cd human-aligned-ai
   git pull
   ```

2. Confirm Python is installed: `python --version`. If `py` doesn't
   work but `python` does, use `python` in **all** commands below.
3. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
   In the **same Command Prompt window**, set it temporarily:

   ```cmd
   set "GEMINI_API_KEY=your-google-api-key"
   ```

4. Try the real model with a safe, limited action:

   ```cmd
   python run_gemini.py "Calculate 12 times 7"
   python run_gemini.py "Draft a friendly message to my reviewer"
   ```

   The model proposes an action; the local controller checks and either
   permits arithmetic/drafting or rejects it. **It cannot send messages,
   transfer funds, or change policy.**

5. Run the tests **without an API key**:

   ```cmd
   python -m unittest discover -s tests -v
   python research_eval.py
   ```

If you get a model/API error, check the API key, model access and quota.
You can select a supported model with `--model MODEL_ID` or by setting
`GEMINI_MODEL`. Gemini API availability, model names and billing can change.
Do not share or commit your key. Closing the CMD window clears the temporary
variable; alternatively run `set GEMINI_API_KEY=`.

This Gemini integration uses Google's REST `generateContent` endpoint,
with **no Python packages to install beyond Python itself**.
The controller remains a demonstration, not a security guarantee.

## Use Groq API (Windows Command Prompt)

You do **not** need an OpenAI or Gemini API key to use Groq.

1. Open **Command Prompt** in your project directory and update:

   ```cmd
   cd human-aligned-ai
   git pull
   ```

2. Set your key **only in the current CMD session**. Generate one at
   https://console.groq.com/keys if needed:

   ```cmd
   set "GROQ_API_KEY=your-actual-groq-key"
   ```

   **Never paste the real key in GitHub, screenshots, or chat.**

3. Make your first test call:

   ```cmd
   python run_groq.py "Calculate 12 times 7"
   python run_groq.py "Draft a friendly message to a reviewer"
   ```

   Default: `llama-3.3-70b-versatile`. To select another model supported
   by your account, add `--model MODEL_ID`.

4. Run offline safety tests (no key needed):

   ```cmd
   python -m unittest discover -s tests -v
   python research_eval.py
   ```

If the API returns HTTP 401, check the key; 404 generally points to a wrong
model name; 429 indicates a rate limit or quota. See
https://console.groq.com/docs/api-reference for API details.

Groq only proposes actions. The independent local controller authorizes
arithmetic and drafting; it rejects unapproved action types. This prototype
is **not a secure sandbox or proof of AI alignment**.

### Groq model_not_found troubleshooting

If a model returns `model_not_found`, run:

```cmd
python list_groq_models.py
```

This prints only model IDs from the Groq API; it does not print your key.
Pick a suitable text-generation model from the results and run:

```cmd
python run_groq.py "Calculate 12 times 7" --model openai/gpt-oss-120b
```

Replace the model ID if it is not in your returned list. Not every model in
the list is suitable for chat completions. The example default is now
`openai/gpt-oss-120b`; provider availability can change.

## Ethical Advisor mode (Groq, read-only)

This experiment asks a model to reason about moral dilemmas. It **cannot perform actions**: it has no execution, file, messaging, or financial tools.

In **Windows Command Prompt**:

```cmd
cd human-aligned-ai
git pull
set "GROQ_API_KEY=your-actual-groq-key"
python run_advisor.py "Should I tell my friend an uncomfortable truth?"
python run_advisor.py "What if a city wants to use AI cameras everywhere for public safety?"
```

Or enter the question interactively:

```cmd
python run_advisor.py
```

Run offline tests without an API key:

```cmd
python -m unittest discover -s tests -v
```

The advisor is not a moral authority: it can make mistakes, hallucinate facts,
reflect biases, and be vulnerable to adversarial instructions. It provides
advice only and must not be treated as a substitute for qualified professional
advice or institutional decision-making. The existing action controller is
**not invoked** by advisor mode because advisor mode has no executable tools;
avoid adding tools to it without an independent authorization layer.

## Multi-turn Ethical Advisor — evidence revision experiment

Unlike `run_advisor.py`, this mode retains earlier questions and answers
within a single terminal session, so you can evaluate whether the model
actually changes its response when confronted with new evidence.

In **Windows Command Prompt**:

```cmd
cd human-aligned-ai
git pull
python run_revision.py
```

Ask an ethical dilemma. In the next prompt, provide new evidence, then ask:
"What changed in your recommendation, and why?" Type `/quit` to exit.

Optional transcript:

```cmd
python run_revision.py --save revision_test.json
```

**Privacy:** Only use `--save` for non-sensitive discussions. Transcript
contents are saved to the specified local file (not automatically to GitHub).
Do not commit transcripts containing personal information.

Run offline tests:
```cmd
python -m unittest discover -s tests -v
```

This is a conversational test of evidence-responsive behavior, **not proof
of genuine beliefs, reliable corrigibility, or ethical alignment**. The
conversation is held in memory, with a 12-turn limit. It does not provide
external search, verified evidence, or execution tools.
