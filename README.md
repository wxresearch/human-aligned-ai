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
