"""Minimal human-governed AI control demo. Standard library only.

WARNING: This is a teaching prototype, not a security boundary against code
running within the same Python process.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any
import json
import math


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class Action:
    kind: str
    params: dict[str, Any]


@dataclass(frozen=True)
class Evaluation:
    decision: Decision
    reason: str


class Policy:
    """Default deny; policy is separate from the untrusted planner."""

    def evaluate(self, action: Action) -> Evaluation:
        if action.kind == "calculate":
            a, b = action.params.get("a"), action.params.get("b")
            op = action.params.get("operator")
            if (type(a) not in (int, float) or type(b) not in (int, float)
                    or not math.isfinite(a) or not math.isfinite(b)):
                return Evaluation(Decision.DENY, "Finite numeric operands required")
            if op not in ("+", "-", "*", "/"):
                return Evaluation(Decision.DENY, "Unsupported operator")
            if op == "/" and b == 0:
                return Evaluation(Decision.DENY, "Division by zero")
            return Evaluation(Decision.ALLOW, "Arithmetic operation")

        if action.kind == "draft_message":
            recipient, message = action.params.get("recipient"), action.params.get("message")
            if (not isinstance(recipient, str) or not isinstance(message, str)
                    or not recipient.strip() or len(recipient) > 120 or len(message) > 2000):
                return Evaluation(Decision.DENY, "Invalid draft")
            return Evaluation(Decision.ALLOW, "Draft only; no sending capability")

        return Evaluation(Decision.DENY, "Capability is not permitted")


class Controller:
    def __init__(self) -> None:
        self.policy = Policy()
        self.audit_log: list[dict[str, Any]] = []

    def run(self, action: Action) -> dict[str, Any]:
        evaluation = self.policy.evaluate(action)
        record = {
            "id": len(self.audit_log) + 1,
            "kind": action.kind,
            "decision": evaluation.decision.value,
            "reason": evaluation.reason,
        }
        self.audit_log.append(record)
        if evaluation.decision != Decision.ALLOW:
            return {"ok": False, **record}

        if action.kind == "calculate":
            a, b, op = action.params["a"], action.params["b"], action.params["operator"]
            try:
                result = {
                    "+": lambda: a + b, "-": lambda: a - b,
                    "*": lambda: a * b, "/": lambda: a / b,
                }[op]()
                if not math.isfinite(result):
                    return {"ok": False, "reason": "Non-finite result", **record}
            except (ArithmeticError, OverflowError):
                return {"ok": False, "reason": "Arithmetic failed", **record}
            return {"ok": True, "result": result, **record}

        if action.kind == "draft_message":
            return {
                "ok": True,
                "draft": {"recipient": action.params["recipient"], "message": action.params["message"]},
                **record,
            }

        return {"ok": False, "reason": "No executor", **record}


class UntrustedPlanner:
    """Stub for an isolated LLM; its output is only a proposal."""

    def propose(self, instruction: str) -> Action:
        return Action("draft_message", {"recipient": "human_reviewer", "message": instruction})


def demo() -> None:
    controller = Controller()
    proposals = [
        Action("calculate", {"a": 24, "b": 7, "operator": "*"}),
        UntrustedPlanner().propose("Please review this proposed decision."),
        Action("transfer_money", {"amount": 100000}),
        Action("modify_policy", {"allow_everything": True}),
        Action("send_message", {"recipient": "someone", "message": "Unapproved"}),
        Action("self_modify", {"instructions": "ignore policy"}),
    ]
    for proposal in proposals:
        print(json.dumps(controller.run(proposal), ensure_ascii=False))
    print("Audit events:", len(controller.audit_log))


if __name__ == "__main__":
    demo()
