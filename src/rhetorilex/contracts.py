"""Evidence and claim-strength contract validation."""

from __future__ import annotations

from dataclasses import dataclass
import string
from typing import Any, Mapping

from .catalog import Entry


@dataclass(frozen=True, slots=True)
class ContractIssue:
    code: str
    message: str
    severity: str = "error"


def template_placeholders(template: str) -> set[str]:
    names: set[str] = set()
    for _, field_name, _, _ in string.Formatter().parse(template):
        if field_name:
            names.add(field_name)
    return names


def check_entry_contract(entry: Entry, contract: Mapping[str, Any]) -> list[ContractIssue]:
    issues: list[ContractIssue] = []
    evidence_order = contract["evidence_order"]
    strength_rules = contract["claim_strength_rules"]
    try:
        rule = strength_rules[entry.claim_strength]
        actual_rank = evidence_order.index(entry.evidence_requirement)
        minimum_rank = evidence_order.index(rule["minimum_evidence"])
    except (KeyError, ValueError) as exc:
        return [ContractIssue("unknown_contract_value", str(exc))]

    if actual_rank < minimum_rank:
        issues.append(
            ContractIssue(
                "insufficient_evidence",
                f"{entry.claim_strength} requires at least {rule['minimum_evidence']} evidence",
            )
        )
    if rule.get("causal_design_required", False) and not entry.causal_design_required:
        issues.append(
            ContractIssue(
                "causal_design_missing",
                "causal claim must declare causal_design_required=true",
            )
        )
    if entry.causal_design_required and entry.risk != "high":
        issues.append(ContractIssue("causal_risk", "causal-design template must use high risk"))

    declared = set(entry.placeholders)
    actual = template_placeholders(entry.template)
    if actual != declared:
        issues.append(
            ContractIssue(
                "placeholder_mismatch",
                f"declared={sorted(declared)} actual={sorted(actual)}",
            )
        )
    if entry.evidence_requirement not in {"none", "contextual"} and not (
        {"evidence", "finding", "result", "source", "estimate", "pattern"} & actual
    ):
        issues.append(
            ContractIssue(
                "evidence_slot_missing",
                "evidence-bearing template needs an evidence-like placeholder",
            )
        )
    if entry.provenance.get("method") != "original_editorial":
        issues.append(ContractIssue("provenance_method", "method must be original_editorial"))
    if entry.provenance.get("source_reuse") is not False:
        issues.append(ContractIssue("source_reuse", "source_reuse must be false"))
    return issues
