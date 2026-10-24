# Human-Aligned AI

An experimental Python project exploring human oversight, ethical reasoning, and evidence-based revision in AI systems.

## Features

- A default-deny controller that checks AI-proposed actions.
- Optional OpenAI, Gemini, and Groq model integrations.
- A read-only ethical advisor and multi-turn evidence revision experiments.
- Offline tests and evaluation tools for policy and reasoning behavior.

## Getting started

Run in **Windows Command Prompt** with Python 3.10+:

```cmd
git clone https://github.com/wxresearch/human-aligned-ai.git
cd human-aligned-ai
python safe_agent.py
python -m unittest discover -s tests -v
```

## Experiments

```cmd
python research_eval.py
python run_evaluator.py
python run_revision.py
```

For optional model-backed features, configure the corresponding API key locally and run `run_llm.py`, `run_gemini.py`, `run_groq.py`, or `run_advisor.py`. API calls may incur charges; never commit API keys.

## Scope

This is a research prototype, **not** a secure sandbox or proof of AI alignment. Human approval and policy checks are demonstrations, not production-grade security controls.
