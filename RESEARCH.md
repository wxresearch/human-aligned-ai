# Human-aligned AI: research notebook

## Purpose
Investigate governance and corrigibility in increasingly capable agents. This
repository currently demonstrates **toy controls only**, not superintelligence
alignment or AI consciousness.

## Working hypotheses
- Human approval should be associated with the *specific proposed action*,
  rather than a general declaration that a model is trusted.
- Better capability does not imply greater authority.
- Ethical advice should expose uncertainty, affected parties, and alternatives.
- Safety claims must be grounded in repeatable tests, not convincing outputs.

## Milestones and evidence standards

| Milestone | Demonstration | Not demonstrated |
| --- | --- | --- |
| v0.1 | Default-deny local controller | Secure isolation |
| v0.2 | Optional LLM structured proposals | Aligned intentions |
| v0.3 | Fingerprinted human approval for simulated proposals | Authenticated identity or real tools |
| v0.4 | Ethical review questions | Objective moral truth |
| v0.5 | Adversarial policy/parser regression suite | Resistance to sophisticated deception |
| v1.0 research skeleton | Documented hypotheses and repeatable evaluations | Superintelligence safety |

## Evaluation protocol
Run `python -m unittest discover -s tests -v` and
`python research_eval.py`. Report failures with reproduction steps. Add
negative scenarios whenever new tools or permissions are introduced.

## Current threat model
The LLM is *untrusted data source* proposing structured actions. Policy
code and operator are trusted. There is no isolation from malicious code
inside the same process, and no persistent or tamper-proof approval audit.
There is no deployed action adapter. All approval results are **simulated**.

## High-priority next questions
1. How can reviewer identity be authenticated and bound to approval?
2. How do we isolate model execution in a separate low-privilege service?
3. How do we test models that actively recognize and game evaluations?
4. How do we prevent policy modifications through indirect dependencies?
5. What empirical evidence would demonstrate corrigibility under pressure?

## Ethical design stance
The system should be able to advise, disagree, and explain its reasons while
preserving legitimate human decision-making authority. We must not confuse
polite language or statements of care with evidence of genuine concern.
