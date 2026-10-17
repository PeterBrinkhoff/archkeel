# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""The ordering port types closed replay events without closing provider payloads."""

import json
import subprocess
from dataclasses import asdict
from enum import Enum
from pathlib import Path
from typing import get_type_hints

import pytest
from test_architecture_demo import _prepare_repo
from test_uml_evaluation import _model

from archkeel.check.ordering import check_order
from archkeel.check.ports import ScanConfig
from archkeel.host.gitlab import load_gitlab_records
from archkeel.ir import host_records
from archkeel.ir.decisions import rule_assessments
from archkeel.ir.host_records import HostRecord, OrderingError, parse_records
from archkeel.ir.report_graph import architecture_report
from archkeel.ir.trace import trace_valid_violations
from tools.github_pr_report import _events

ROOT = Path(__file__).parents[1]
E, H = "e" * 40, "c" * 40
PUBLISHED, SUBMITTED = "2026-01-01T10:00:00Z", "2026-01-01T11:00:00Z"
GUARD = "HOST-ORDER-TYPED-CONTROL"


def _event_type():
    event = getattr(host_records, "HostEvent", None)
    assert event is not None, "the existing host-record owner needs the closed ordering event type"
    return event


def _wire():
    return [
        {"sha": E, "event": "expectation_published", "timestamp": PUBLISHED},
        {"sha": H, "event": "candidate_submitted", "timestamp": SUBMITTED},
    ]


def test_actual_ordering_port_returns_the_owned_nominal_event():
    event = _event_type()
    assert issubclass(event, Enum)
    assert [member.value for member in event] == ["expectation_published", "candidate_submitted"]
    assert get_type_hints(HostRecord.ordering_event)["return"] is event
    legacy = HostRecord(E, "expectation_published", PUBLISHED)
    assert type(legacy.event) is str
    assert legacy.ordering_event() is event.EXPECTATION_PUBLISHED
    assert HostRecord(H, event.CANDIDATE_SUBMITTED, SUBMITTED).ordering_event() is (
        event.CANDIDATE_SUBMITTED
    )


def test_replay_parser_and_legacy_constructors_keep_identical_wire_and_order():
    event = _event_type()
    records = parse_records(_wire())
    assert [item.ordering_event() for item in records] == [
        event.EXPECTATION_PUBLISHED,
        event.CANDIDATE_SUBMITTED,
    ]
    legacy = tuple(HostRecord(**item) for item in _wire())
    assert records == legacy
    assert json.dumps([asdict(item) for item in records]) == json.dumps(_wire())
    assert json.dumps([asdict(item) for item in legacy]) == json.dumps(_wire())
    assert check_order(records, expectation_sha=E, candidate_sha=H) == ()
    assert check_order(legacy, expectation_sha=E, candidate_sha=H) == ()


@pytest.mark.parametrize(
    "changes,message",
    [
        ({"sha": "short", "event": "future", "timestamp": "bad"}, "sha must be a full SHA-40"),
        ({"event": "future", "timestamp": "bad"}, "host record event is invalid"),
        ({"event": 7, "timestamp": "bad"}, "host record event is invalid"),
        ({"timestamp": "bad"}, "timestamp must be a timezone-aware ISO timestamp"),
    ],
)
def test_replay_validation_keeps_existing_error_order_and_text(changes, message):
    _event_type()
    with pytest.raises(OrderingError) as error:
        parse_records([_wire()[0] | changes])
    assert str(error.value) == message


@pytest.mark.parametrize(
    "timestamp,message",
    [
        ("bad", "timestamp must be a timezone-aware ISO timestamp"),
        (PUBLISHED, "host record event is invalid"),
    ],
)
def test_invalid_legacy_constructor_is_still_checked_by_order_after_timestamp(timestamp, message):
    _event_type()
    legacy = HostRecord(E, "future-provider-event", timestamp)
    with pytest.raises(OrderingError) as error:
        check_order((legacy,), expectation_sha=E, candidate_sha=H)
    assert str(error.value) == message


def test_real_gitlab_producer_reaches_the_typed_ordering_port(monkeypatch, tmp_path):
    event = _event_type()
    output = json.dumps(
        [
            {"head_commit_sha": E, "created_at": PUBLISHED},
            {"head_commit_sha": H, "created_at": SUBMITTED},
        ]
    )
    monkeypatch.setattr(
        "archkeel.host.gitlab.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, output, ""),
    )
    records = load_gitlab_records(
        tmp_path,
        expectation_sha=E,
        candidate_sha=H,
        environ={"CI_PROJECT_ID": "7", "CI_MERGE_REQUEST_IID": "11", "CI_COMMIT_SHA": H},
    )
    assert records[0].ordering_event() is event.EXPECTATION_PUBLISHED
    assert records[1].ordering_event() is event.CANDIDATE_SUBMITTED
    assert json.dumps([asdict(item) for item in records]) == json.dumps(_wire())
    assert check_order(records, expectation_sha=E, candidate_sha=H) == ()


def test_future_github_provider_event_remains_an_open_bounded_observation(tmp_path):
    _event_type()
    raw = [[{
        "id": "123",
        "type": "FutureProviderEvent",
        "repo": {"name": "example/project"},
        "created_at": PUBLISHED,
        "payload": {"future": "open"},
    }]]
    assert _events(tmp_path, raw, "example/project") == 1


def _repository(tmp_path, *, old=None, new=None, probe=""):
    target = json.loads((ROOT / "docs/architecture/contracts/ir.json").read_text())
    target.pop("$schema", None)
    target["components"] = [
        item for item in target["components"] if item["id"] == "TARGET-GOVERNANCE"
    ] + [{
        "id": "ordering",
        "label": "ordering",
        "role": "component",
        "packages": ["archkeel.check.ordering"],
        "responsibilities": ["Validate replay ordering through the host-record port."],
        "forbidden_responsibilities": [],
        "provenance": ["docs/architecture/host-event-types.md"],
    }]
    target["rules"] = [{
        "id": GUARD,
        "kind": "forbidden_construct",
        "source": "archkeel.check.ordering",
        "constructs": ["string_literal_compare"],
        "rationale": "The closed replay event reaches ordering through its nominal port.",
        "decided_by": "architect",
        "provenance": ["docs/architecture/host-event-types.md"],
    }]
    target["declarations"]["uml"]["entities"] = [
        item for item in target["declarations"]["uml"]["entities"]
        if item["id"].startswith("IR-HOST-")
    ]
    target["declarations"]["uml"]["relationships"] = []
    target["declarations"]["uml"]["scopes"] = []
    target["declarations"]["modules"] = []
    files = {
        "archkeel/__init__.py": "",
        "archkeel/ir/__init__.py": "",
        "archkeel/check/__init__.py": "",
        "contract.json": json.dumps(target),
        "docs/architecture/host-event-types.md": "Closed replay ordering port.\n",
        "docs/architecture/language-adapter-target.md": "Governance models.\n",
    }
    for path in ("ir/host_records.py", "check/ordering.py"):
        source = (ROOT / "src/archkeel" / path).read_text()
        if path == "ir/host_records.py" and old is not None:
            assert old in source, "mutate the actual consumed port"
            source = source.replace(old, new)
        if path == "check/ordering.py":
            source += "\n" + probe
        files["archkeel/" + path] = source
    root = _prepare_repo(tmp_path, files)
    return root, ScanConfig(("archkeel",), "archkeel", "contract.json", "0" * 64)


def test_native_actual_host_port_meets_fixed_authored_target_and_order_guard(tmp_path):
    _event_type()
    root, config = _repository(tmp_path)
    model = _model(root, config)
    comparison = architecture_report(model).comparison
    assert comparison is not None and comparison.status == "PASS", comparison
    guard = next(row for row in rule_assessments(model, undecided_by_rule={}) if row.id == GUARD)
    assert guard.status == "PASS" and guard.evaluation_proven
    assert not trace_valid_violations(model)


def test_native_host_port_return_weakening_fails_unchanged_authored_target(tmp_path):
    _event_type()
    root, config = _repository(
        tmp_path, old="def ordering_event(self) -> HostEvent:", new="def ordering_event(self) -> str:"
    )
    before = (root / "contract.json").read_bytes()
    model = _model(root, config)
    comparison = architecture_report(model).comparison
    assert comparison is not None
    assert any(row.aspect == "signature" and row.status == "FAIL" for row in comparison.assessments)
    assert trace_valid_violations(model)
    assert (root / "contract.json").read_bytes() == before


@pytest.mark.parametrize(
    "probe",
    [
        'def _probe(value):\n    return value == "expectation_published"\n',
        'def _probe(value):\n    return value in ("expectation_published", "candidate_submitted")\n',
        "def _probe(value):\n    return value == HostEvent.CANDIDATE_SUBMITTED.value\n",
    ],
)
def test_native_order_guard_rejects_raw_event_dispatch_mutations(tmp_path, probe):
    _event_type()
    root, config = _repository(tmp_path, probe=probe)
    before = (root / "contract.json").read_bytes()
    model = _model(root, config)
    assert any(GUARD in row.rule_ids for row in trace_valid_violations(model))
    assert (root / "contract.json").read_bytes() == before
