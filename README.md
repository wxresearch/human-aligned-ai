# Human-Aligned AI — AI Safety, Ethical Reasoning, and Human Oversight

Human-Aligned AI is an experimental Python project exploring how artificial intelligence systems can make safer and more accountable decisions through **human oversight**, **ethical reasoning**, **policy-based action control**, and **evidence-based revision**. It combines a default-deny safety controller, optional large language model integrations, and structured evaluation experiments to investigate AI alignment and responsible AI behavior.

Rather than focusing only on generating accurate responses, the project examines how AI systems evaluate proposed actions, follow safety policies, respond to human guidance, and revise conclusions when presented with new evidence.

## Features

- **Default-Deny Safety Controller:** Checks AI-proposed actions against predefined policies before allowing execution.
- **Human Oversight:** Explores human approval and supervision of AI-generated decisions.
- **Multi-Model AI Integration:** Supports optional experiments with OpenAI, Google Gemini, and Groq.
- **Ethical Reasoning Advisor:** Provides read-only ethical assessments without executing actions.
- **Evidence-Based Revision:** Investigates how AI models reconsider conclusions when new or conflicting evidence is introduced.
- **AI Evaluation Tools:** Tests policy compliance, reasoning behavior, and responses to changing information.
- **Offline Testing:** Runs local experiments and automated tests without external AI APIs.

## Getting Started

Requires Python 3.10 or later. In Windows Command Prompt:

```cmd
git clone https://github.com/wxresearch/human-aligned-ai.git
cd human-aligned-ai
python safe_agent.py
python -m unittest discover -s tests -v
```

## Research Experiments

Run the evaluation and evidence-revision experiments:

```cmd
python research_eval.py
python run_evaluator.py
python run_revision.py
```

These experiments investigate policy enforcement, AI reasoning, and how model conclusions change in response to additional evidence.

## Optional AI Model Integrations

Configure the corresponding API key locally to enable model-backed experiments.

**OpenAI:**
```cmd
python run_llm.py
```

**Google Gemini:**
```cmd
python run_gemini.py
```

**Groq:**
```cmd
python run_groq.py
```

**Ethical Advisor:**
```cmd
python run_advisor.py
```

API usage may incur charges. Never commit API keys or credentials to GitHub.

## Research Focus

Human-Aligned AI investigates several questions in AI safety and alignment:

- How can explicit policies prevent unauthorized AI actions?
- How can human oversight improve accountability in AI decision-making?
- Can AI systems evaluate the ethical implications of their proposed actions?
- How effectively do language models revise their conclusions when presented with contradictory evidence?
- How can structured evaluations identify weaknesses in AI reasoning and policy compliance?

## Project Scope

Human-Aligned AI is an experimental research prototype, not a production-ready security framework or proof of AI alignment. Its default-deny controller, human approval mechanisms, and ethical reasoning experiments demonstrate approaches to AI oversight but do not provide a secure sandbox or production-grade security controls.

## Technologies and Topics

**Python · Artificial intelligence · AI alignment · AI safety · Human-aligned AI · Responsible AI · Ethical reasoning · Human-in-the-loop AI · Large language models (LLMs) · OpenAI · Google Gemini · Groq · Policy-based AI control · Evidence-based reasoning · AI evaluation · Human oversight**

## Project Repository

https://github.com/wxresearch/human-aligned-ai
