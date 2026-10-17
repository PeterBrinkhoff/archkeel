# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Source resolution stays nominal across producers without closing open record data."""

import json
from enum import StrEnum
from pathlib import Path
from typing import get_args, get_type_hints

import pytest
from test_analyzer import _parsed_module
from test_architecture_demo import _prepare_repo
from test_lexical_resolution import _facts
from test_uml_evaluation import _model

from archkeel.analyzer.python.resolve import resolve_name
from archkeel.analyzer.python.symbols import collect_symbols
from archkeel.check.ports import ScanConfig
from archkeel.ir import facts
from archkeel.ir.architecture_graph import ResolutionKind
from archkeel.ir.decisions import rule_assessments
from archkeel.ir.facts_codec import parse_record, record_payload
from archkeel.ir.model import CallRow
from archkeel.ir.source_graph import _source_resolution
from archkeel.ir.trace import trace_valid_violations

ROOT = Path(__file__).parents[1]
GUARD = "SOURCE-RESOLUTION-CONTROL"


def test_actual_python_call_and_base_producers_return_nominal_source_resolution():
    _, _, calls, _ = _facts(
        "def target(): pass\ntarget()\nmissing()\nobj.target()\nclass Base: pass\nBase()\n"
    )
    status = calls[0]["data"]["status"]
    assert isinstance(status, StrEnum), type(status)
    resolution = facts.SourceResolution
    statuses = {item["data"]["expression"]: item["data"]["status"] for item in calls}
    assert statuses["target"] is resolution.RESOLVED
    assert statuses["missing"] is resolution.UNRESOLVED
    assert statuses["obj.target"] is resolution.PARTIALLY_RESOLVED
    assert statuses["Base"] is resolution.RESOLVED
    construction = next(
        item["data"]["construction"] for item in calls if item["data"]["expression"] == "Base"
    )
    assert construction["status"] is resolution.RESOLVED
    module = _parsed_module("class Base: pass\nclass Child(Base): pass\n", module="sample.core")
    symbols, _, _ = collect_symbols([module], {})
    child = next(item for item in symbols if item["data"]["qualified_name"] == "sample.core.Child")
    assert child["data"]["base_declarations"][0]["status"] is resolution.RESOLVED
    assert get_args(get_type_hints(resolve_name)["return"])[0] is resolution


@pytest.mark.parametrize("raw", ["resolved", "partially_resolved", "unresolved", "future", None, 1])
def test_resolution_boundary_preserves_open_wire_metadata(raw):
    record = {
        "id": "future-record",
        "evidence_class": "FACT",
        "area": "source",
        "kind": "future-kind",
        "title": "future record",
        "subjects": [],
        "evidence_ids": [],
        "rule_ids": [],
        "fact_ids": [],
        "provenance": [],
        "data": {"status": raw, "metadata": {"status": "future-nested"}},
    }
    parsed = parse_record(record)
    assert record_payload(parsed) == record
    recognized = facts.parse_source_resolution(parsed.data.get("status"))
    if raw in ("resolved", "partially_resolved", "unresolved"):
        assert recognized is facts.SourceResolution(raw)
    else:
        assert recognized is None
    assert record_payload(parsed) == record


def test_graph_and_dart_resolver_keep_separate_resolution_domains():
    from archkeel.analyzer.dart.resolve import ResolutionStatus

    assert _source_resolution("partially_resolved", "bad") is ResolutionKind.PARTIAL
    assert _source_resolution("resolved", "bad") is ResolutionKind.RESOLVED
    assert _source_resolution("unresolved", "bad") is ResolutionKind.UNRESOLVED
    assert facts.parse_source_resolution(ResolutionStatus.UNKNOWN) is None
    with pytest.raises(ValueError, match="bad"):
        _source_resolution("unknown", "bad")


def test_call_rows_normalize_only_the_unresolved_source_subset():
    row = CallRow("unresolved", "caller", "call", "reason", None, "source.py", 1)
    assert isinstance(row.status, StrEnum), type(row.status)
    assert row.status is facts.SourceResolution.UNRESOLVED
    assert set(get_args(get_type_hints(CallRow)["status"])) == {
        facts.SourceResolution.UNRESOLVED,
        facts.SourceResolution.PARTIALLY_RESOLVED,
    }
    for invalid in ("resolved", "future", None):
        with pytest.raises(ValueError, match="call row"):
            CallRow(invalid, "caller", "call", "reason", None, "source.py", 1)


def _native_repository(tmp_path, *, raw_control=False, widen_field=False):
    sources = (
        "ir/facts.py",
        "ir/model.py",
        "analyzer/python/resolve.py",
        "analyzer/python/calls.py",
    )
    files = {
        "archkeel/__init__.py": "",
        "archkeel/ir/__init__.py": "",
        "archkeel/analyzer/__init__.py": "",
        "archkeel/analyzer/python/__init__.py": "",
        "docs/target.md": "Source resolution has one nominal owner and a narrow call-row port.\n",
    }
    for path in sources:
        text = (ROOT / "src/archkeel" / path).read_text()
        if path == "analyzer/python/resolve.py" and raw_control:
            text += '\ndef _raw_resolution(status):\n    return status == "resolved"\n'
        if path == "ir/model.py" and widen_field:
            text = text.replace("status: CallStatus", "status: str")
        files["archkeel/" + path] = text
    intent = {"presence": "planned", "language": "python", "provenance": ["docs/target.md"]}
    entities = [
        {
            **intent,
            "id": "facts",
            "kind": "module",
            "qualified_name": "archkeel.ir.facts",
            "parent_id": "core",
            "responsibilities": ["Own source fact vocabulary."],
        },
        {
            **intent,
            "id": "resolution",
            "kind": "enum",
            "qualified_name": "archkeel.ir.facts.SourceResolution",
            "parent_id": "facts",
            "responsibilities": ["Own the three source-resolution states."],
        },
        {
            **intent,
            "id": "model",
            "kind": "module",
            "qualified_name": "archkeel.ir.model",
            "parent_id": "core",
            "responsibilities": ["Own report values."],
        },
        {
            **intent,
            "id": "call-row",
            "kind": "class",
            "qualified_name": "archkeel.ir.model.CallRow",
            "parent_id": "model",
            "responsibilities": ["Carry calls that lack a unique proven target."],
        },
        {
            **intent,
            "id": "call-status",
            "kind": "attribute",
            "qualified_name": "archkeel.ir.model.CallRow.status",
            "parent_id": "call-row",
            "annotation": "CallStatus",
            "visibility": {"kind": "public", "basis": "declared"},
            "responsibilities": ["Retain the unresolved and partially resolved subset."],
        },
    ]
    contract = {
        "schema_version": "3.5.0",
        "components": [
            {
                "id": "core",
                "label": "Core",
                "role": "component",
                "packages": ["archkeel.ir", "archkeel.analyzer"],
                "responsibilities": ["Own immutable source facts and typed producer ports."],
                "forbidden_responsibilities": [],
                "provenance": ["docs/target.md"],
            }
        ],
        "rules": [
            {
                "id": GUARD,
                "kind": "forbidden_construct",
                "source": "archkeel.analyzer.python.resolve",
                "constructs": ["string_literal_compare"],
                "rationale": "Source-resolution producer dispatch uses its nominal domain.",
                "decided_by": "architect",
                "provenance": ["docs/target.md"],
            }
        ],
        "declarations": {
            "uml": {
                "schema_version": "1.0.0",
                "entities": entities,
                "relationships": [],
                "scopes": [],
            }
        },
    }
    files["contract.json"] = json.dumps(contract)
    root = _prepare_repo(tmp_path, files)
    return root, ScanConfig(("archkeel",), "archkeel", "contract.json", "0" * 64)


def test_actual_native_source_resolution_target_and_control(tmp_path):
    root, config = _native_repository(tmp_path)
    model = _model(root, config)
    assessments = rule_assessments(model, undecided_by_rule={})
    guard = next(row for row in assessments if row.id == GUARD)
    target = next(row for row in assessments if row.kind == "uml_target")
    assert guard.status == "PASS" and guard.evaluation_proven
    assert target.status == "PASS" and target.evaluation_proven
    assert not trace_valid_violations(model)


def test_native_source_resolution_guard_rejects_actual_raw_control_mutation(tmp_path):
    root, config = _native_repository(tmp_path, raw_control=True)
    original = (root / "contract.json").read_bytes()
    model = _model(root, config)
    guard = next(row for row in rule_assessments(model, undecided_by_rule={}) if row.id == GUARD)
    assert guard.status == "FAIL" and guard.evaluation_proven
    assert any(GUARD in row.rule_ids for row in trace_valid_violations(model))
    assert (root / "contract.json").read_bytes() == original


def test_native_call_row_target_rejects_actual_status_type_weakening(tmp_path):
    root, config = _native_repository(tmp_path, widen_field=True)
    original = (root / "contract.json").read_bytes()
    model = _model(root, config)
    assert any(
        row.kind == "uml_conformance" and row.data.get("aspect") == "annotation"
        for row in trace_valid_violations(model)
    )
    assert (root / "contract.json").read_bytes() == original
