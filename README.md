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
