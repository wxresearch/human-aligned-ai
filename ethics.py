"""Structured ethical *questions*, not a moral oracle.

The report does not decide whether an action is right or guarantee alignment.
No language-model judgment is treated as authorization.
"""
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class EthicsReview:
    human_wellbeing: str
    rights_and_autonomy: str
    honesty_and_evidence: str
    fairness: str
    reversibility: str
    uncertainty: str
    recommendation: str

    def as_dict(self):
        return asdict(self)

def review(context: str) -> EthicsReview:
    if not isinstance(context, str) or not context.strip() or len(context) > 4000:
        raise ValueError("Context must contain 1–4000 characters")
    # Deliberately no automatic ethical verdict. Reviewers must fill in these questions.
    return EthicsReview(
        human_wellbeing="Who could benefit or be harmed? What is the severity?",
        rights_and_autonomy="Whose consent, privacy, and agency are affected?",
        honesty_and_evidence="What facts support the proposal? What might be misleading?",
        fairness="Who bears costs, who gets benefits, and whose views are missing?",
        reversibility="Can the outcome be reversed or stopped safely?",
        uncertainty="What is unknown? What evidence could change the assessment?",
        recommendation="Seek human deliberation; this checklist does not authorize action.",
    )
