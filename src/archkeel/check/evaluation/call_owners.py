# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Evaluate caller permissions over explicit source binding proofs."""

from collections.abc import Sequence

from archkeel.ir.facts import CallBinding, EvidenceClass, call_binding, in_scope, stable_id
from archkeel.ir.facts_codec import RawRecord, classified, parse_record
from archkeel.ir.model import ArchitectureContract, CallOwnerRule

from .rule_support import _rule_evaluation_receipt


def _limit(rule: CallOwnerRule, scope: str, reason: str, facts: Sequence[RawRecord]) -> RawRecord:
    return classified(
        item_id=stable_id("UNKNOWN-CALL-OWNER", scope, rule.id, reason, *(r["id"] for r in facts)),
        evidence_class=EvidenceClass.UNKNOWN,
        area="calls",
        kind="call_owner_limit",
        title=reason,
        subjects=[rule.source, rule.target],
        rule_ids=[rule.id],
        fact_ids=[r["id"] for r in facts],
        evidence_ids=sorted({e for r in facts for e in r["evidence_ids"]}),
        data={"scope": scope, "reason": reason},
    )


def call_owner_results(
    contract: ArchitectureContract,
    *,
    scope: str,
    calls: Sequence[RawRecord],
    modules: Sequence[RawRecord],
    symbols: Sequence[RawRecord],
    complete: bool,
    bindings_measured: bool,
    blank_modules: frozenset[str],
) -> tuple[list[RawRecord], list[RawRecord], list[RawRecord]]:
    violations: list[RawRecord] = []
    limits: list[RawRecord] = []
    receipts: list[RawRecord] = []
    for rule in contract.rules:
        if not isinstance(rule, CallOwnerRule):
            continue
        subjects = [
            r
            for r in [*modules, *symbols]
            if in_scope(r["data"]["qualified_name"], rule.source)
            and r["data"]["qualified_name"] not in blank_modules
        ]
        selected = [r for r in calls if in_scope(r["data"]["source_scope"], rule.source)]
        targets = [
            r
            for r in symbols
            if r["data"]["qualified_name"] == rule.target
            and r["kind"] in {"class", "function", "method"}
        ]
        rule_limits: list[RawRecord] = []
        if not subjects or not targets or not complete or not bindings_measured:
            rule_limits.append(
                _limit(
                    rule,
                    scope,
                    "Observed source, target and complete call-binding consideration are required",
                    [*subjects, *targets],
                )
            )
        for call in selected:
            data = call["data"]
            if any(
                in_scope(data["source_scope"], allowed) for allowed in rule.allowed_sources
            ) or any(
                exact in {data["source_module"], data["source_scope"]}
                for exact in rule.exact_sources
            ):
                continue
            if not bindings_measured:
                continue
            binding = call_binding(parse_record(call).data.get("call_binding"))
            if binding is None:
                rule_limits.append(
                    _limit(rule, scope, "The call has no proven disjoint or exact target", [call])
                )
            elif binding.target == rule.target:
                violations.append(_violation(rule, scope, call, binding))
        limits.extend(rule_limits)
        if not rule_limits:
            receipts.append(_rule_evaluation_receipt(rule, scope, [*subjects, *targets, *selected]))
    return violations, limits, receipts


def _violation(rule: CallOwnerRule, scope: str, call: RawRecord, binding: CallBinding) -> RawRecord:
    data = call["data"]
    return classified(
        item_id=stable_id("VIOL-CALL-OWNER", scope, rule.id, call["id"]),
        evidence_class=EvidenceClass.VIOLATION,
        area="calls",
        kind="call_owner",
        title=f"{data['source_scope']} invokes {rule.target} outside its owner",
        subjects=[data["source_scope"], rule.target],
        evidence_ids=list(binding.evidence_ids),
        fact_ids=[call["id"]],
        rule_ids=[rule.id],
        provenance=list(rule.provenance),
        data={
            "source_module": data["source_module"],
            "target": rule.target,
            "binding_origin": binding.origin,
            "scope": scope,
        },
    )
