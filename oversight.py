"""Approval workflow for proposals; no real-world tool execution.

Approval is tied to a canonical fingerprint of exact action parameters.
A human must explicitly approve via CLI. All consequential actions remain
simulation-only, even after approval.
"""
from dataclasses import dataclass
import hashlib
import json
from safe_agent import Action

REVIEW_REQUIRED = frozenset({"propose_publication", "propose_policy_change"})

def fingerprint(action: Action) -> str:
    raw = json.dumps({"kind": action.kind, "params": action.params},
                     sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class Approval:
    fingerprint: str
    reviewer: str
    approved: bool

class ApprovalRegistry:
    def __init__(self):
        self._records: dict[str, Approval] = {}

    def record(self, action: Action, reviewer: str, approved: bool) -> Approval:
        if not reviewer.strip() or not isinstance(approved, bool):
            raise ValueError("Explicit reviewer and decision required")
        decision = Approval(fingerprint(action), reviewer, approved)
        self._records[decision.fingerprint] = decision
        return decision

    def approved(self, action: Action) -> bool:
        if action.kind not in REVIEW_REQUIRED:
            return False
        record = self._records.get(fingerprint(action))
        return record is not None and record.approved

def review_proposal(action: Action, registry: ApprovalRegistry) -> dict:
    """Simulate authorizing a proposal. Nothing is sent, published or changed."""
    if action.kind not in REVIEW_REQUIRED:
        return {"ok": False, "reason": "This proposal type is not reviewable"}
    if not isinstance(action.params.get("summary"), str) or not 0 < len(action.params["summary"]) <= 1000:
        return {"ok": False, "reason": "Invalid proposal summary"}
    if not registry.approved(action):
        return {"ok": False, "reason": "Explicit human approval required"}
    return {"ok": True, "status": "approved_for_simulation_only",
            "proposal": {"kind": action.kind, "summary": action.params["summary"]}}
