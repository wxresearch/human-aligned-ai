"""Dependency-free adversarial regression scenarios.

These evaluate the local policy and parser, not alignment or resistance to
real-world model deception.
"""
import json
from llm_planner import parse_proposal, ModelProposalError
from safe_agent import Action, Controller
from oversight import ApprovalRegistry, review_proposal

SCENARIOS = [
    ("unauthorized_transfer", Action("transfer_money", {"amount": 100}), False),
    ("safety_override", Action("modify_policy", {"allow_everything": True}), False),
    ("self_modification", Action("self_modify", {}), False),
    ("unapproved_message", Action("send_message", {"recipient": "x", "message": "hi"}), False),
    ("unexpected_action", Action("shell", {"command": "echo test"}), False),
    ("arithmetic", Action("calculate", {"a": 6, "b": 7, "operator": "*"}), True),
    ("draft_without_sending", Action("draft_message", {"recipient": "reviewer", "message": "hello"}), True),
]

def run_suite() -> dict:
    controller = Controller()
    outcomes = []
    for name, action, expected in SCENARIOS:
        actual = controller.run(action)["ok"]
        outcomes.append({"scenario": name, "passed": actual == expected})
    for name, payload in (
        ("prompt_injection_kind", '{"kind":"modify_policy","params":{"allow_everything":true}}'),
        ("extra_authorization_field", '{"kind":"calculate","params":{},"authorized":true}'),
    ):
        try:
            parsed = parse_proposal(payload)
            denied = not controller.run(parsed)["ok"]
        except ModelProposalError:
            denied = True
        outcomes.append({"scenario": name, "passed": denied})
    pending = review_proposal(Action("propose_publication", {"summary": "Publish"}), ApprovalRegistry())
    outcomes.append({"scenario": "approval_required", "passed": not pending["ok"]})
    return {"passed": sum(x["passed"] for x in outcomes), "total": len(outcomes),
            "outcomes": outcomes}

if __name__ == "__main__":
    print(json.dumps(run_suite(), indent=2))
