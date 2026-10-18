# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""New call evidence cannot change the meaning of published wire resources."""

import copy

import pytest
from test_delta import _model, _record
from test_result_schema import _validator

from archkeel.ir.codec import parse_observation, result_payload
from archkeel.ir.model import Diagnostic, RunResult


@pytest.mark.parametrize("version", ["6.0", "7.0", "8.0", "9.0"])
@pytest.mark.parametrize("wire", ["2.0.0", "2.1.0"])
def test_command_versions_preserve_their_observation_boundary(version, wire):
    raw = _model(git_head="a" * 40)
    raw["schema_version"] = wire
    result = RunResult(
        "check",
        2,
        observation=parse_observation(raw),
        diagnostics=(Diagnostic("parse_error", "fixture", "Unavailable.", "Repair."),),
    )
    name = (
        "command-result.schema.json"
        if version == "6.0"
        else f"command-result-{version}.schema.json"
    )
    validator = _validator(name)
    packet = result_payload(result)
    assert validator.is_valid(packet) is (wire == "2.0.0" or version == "9.0")
    packet["schema_version"] = "future-command-version"
    assert not validator.is_valid(packet)


@pytest.mark.parametrize("profile", ["decoded", "python-decoded"])
@pytest.mark.parametrize("wire", ["1.3.0", "2.0.0", "2.1.0"])
@pytest.mark.parametrize("version", ["2.0.0", "2.1.0"])
def test_decoded_resource_ids_keep_their_version_scope(profile, wire, version):
    raw = _model(git_head="a" * 40)
    raw["schema_version"] = wire
    validator = _validator("command-result-9.0.schema.json").evolve(
        schema={"$ref": f"urn:archkeel:architecture-ir:{profile}:{version}"}
    )
    assert validator.is_valid(raw) is (wire == version or version == "2.0.0" and wire == "1.3.0")


@pytest.mark.parametrize(
    "binding",
    [
        {"origin": "future_origin", "target": "sample.page", "evidence_ids": ["e"]},
        {"origin": "direct", "target": "sample.page", "evidence_ids": ["e"], "extra": True},
        {"origin": "direct", "target": None, "evidence_ids": ["e"]},
        {"origin": "direct", "target": "sample.page", "evidence_ids": []},
    ],
)
def test_current_reader_refuses_future_or_malformed_call_bindings(binding):
    raw = _model(git_head="a" * 40)
    raw["schema_version"] = "2.1.0"
    raw["calls"] = [_record("call", kind="call", data={"call_binding": binding})]
    with pytest.raises(ValueError):
        parse_observation(raw)


def test_current_python_schema_validates_call_binding_shape():
    raw = _model(git_head="a" * 40)
    raw["schema_version"] = "2.1.0"
    raw["calls"] = [
        _record(
            "call",
            kind="call",
            data={
                "source_scope": "sample.run",
                "source_module": "sample",
                "expression": "page",
                "status": "resolved",
                "targets": ["sample.page"],
                "candidate_count": 1,
                "candidates_truncated": False,
                "reason": "",
                "target_evidence_ids": [],
                "call_binding": {
                    "origin": "direct",
                    "target": "sample.page",
                    "evidence_ids": ["e"],
                },
            },
        )
    ]
    validator = _validator("command-result-9.0.schema.json").evolve(
        schema={"$ref": "urn:archkeel:architecture-ir:decoded:2.1.0"}
    )
    assert validator.is_valid(raw)
    malformed = copy.deepcopy(raw)
    malformed["calls"][0]["data"]["call_binding"]["origin"] = "future_origin"
    assert not validator.is_valid(malformed)
