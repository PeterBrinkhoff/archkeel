# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Exercise the compact target without weakening missing-evidence controls."""

import json
from pathlib import Path

import jsonschema
import pytest
from test_architecture_demo import _prepare_repo

from archkeel.check.ports import ScanConfig
from archkeel.check.report import run_report
from archkeel.cli.observe import observe
from archkeel.ir.codec import contract_bytes, parse_contract
from archkeel.ir.model import requires_covers

ROOT = Path(__file__).parents[1]
CONTRACTS = [
    ROOT / "architecture-contract.json",
    *sorted((ROOT / "docs/architecture/contracts").glob("*.json")),
]


@pytest.mark.parametrize("path", CONTRACTS, ids=lambda path: path.stem)
def test_target_contract_schema_roundtrip_and_closed_owners(path):
    raw = json.loads(path.read_bytes())
    jsonschema.validate(raw, json.loads((ROOT / "schema" / Path(raw["$schema"]).name).read_bytes()))
    encoded = contract_bytes(parse_contract(raw))
    assert encoded == contract_bytes(parse_contract(json.loads(encoded)))
    assert {
        "complete_assignment",
        "complete_requires",
        "interface_boundary",
        "no_component_cycles",
    } <= {rule["kind"] for rule in raw["rules"]}


@pytest.mark.parametrize(
    "module,symbol,allowed",
    [
        ("archkeel.ir.codec", "decode_json", True),
        ("archkeel.ir.codec", "result_bytes", False),
        ("archkeel.ir.codec", None, False),
        ("archkeel.ir.command_view", "decode_json", False),
    ],
)
def test_report_reader_permission_is_symbol_specific(module, symbol, allowed):
    contract = parse_contract(json.loads(CONTRACTS[0].read_bytes()))
    api = next(component for component in contract.components if component.label == "api")
    assert requires_covers(api, "ir", module, symbol) is allowed


@pytest.mark.parametrize(
    "case,expected",
    [
        ("allowed", "PASS"),
        ("forbidden", "FAIL"),
        ("missing_target", "UNKNOWN"),
        ("missing_source", "UNKNOWN"),
    ],
)
def test_onboarding_dependency_uses_exact_modules_and_real_source_evidence(
    tmp_path, case, expected
):
    raw = json.loads((ROOT / "docs/architecture/contracts/check.json").read_bytes())
    rule = next(
        rule for rule in raw["rules"] if rule["id"] == "CHECK-ONBOARDING-NO-REPORT-IMPLEMENTATION"
    )
    files = {
        "archkeel/__init__.py": "",
        "archkeel/check/__init__.py": "",
        "archkeel/check/onboarding.py": (
            "from archkeel.check.report import observe_repository\n"
            if case == "forbidden"
            else "from archkeel.check.ports import ScanConfig\n"
        ),
        "archkeel/check/ports.py": "class ScanConfig: pass\n",
        "archkeel/check/report.py": "def observe_repository(): pass\n",
        # Another command must not be captured by expansion to the whole owner pair.
        "archkeel/check/run.py": "from archkeel.check.report import observe_repository\n",
        "docs/architecture/target/design.md": "Independent command responsibilities.\n",
        "intent.json": json.dumps(
            {
                "schema_version": raw["schema_version"],
                "components": raw["components"],
                "rules": [rule],
            }
        ),
    }
    if case == "missing_target":
        del files["archkeel/check/report.py"]
    if case == "missing_source":
        del files["archkeel/check/onboarding.py"]
    root = _prepare_repo(tmp_path, files)
    result, artifact = run_report(
        root,
        config=ScanConfig(("archkeel",), "archkeel", "intent.json", "0" * 64),
        analyzer=observe,
    )
    assert artifact is not None, result.diagnostics
    row = next(row for row in result.rule_assessments if row.id == rule["id"])
    assert row.status == expected


PORTS = (
    "archkeel.api.load_violations",
    "archkeel.ir.renames.renamed_contract",
    "archkeel.check.report.run_report",
    "archkeel.check.report.run_saved_report",
    "archkeel.check.report.observe_repository",
    "archkeel.check.run.run_check",
    "archkeel.check.validation.run_validate",
    "archkeel.check.validation.invalid_result",
    "archkeel.check.onboarding.run_init",
    "archkeel.check.ports.Analyzer.__call__",
    "archkeel.check.ports.Host.__call__",
    "archkeel.check.observe.Observer.__call__",
    "archkeel.check.uml.observe_repository",
    "archkeel.render.html.render_architecture_html",
    "archkeel.render.html.render_architecture_details",
    "archkeel.render.html.render_check_html",
    "archkeel.render.atlas.atlas_payload",
    "archkeel.render.atlas.boundary_permissions_payload",
    "archkeel.render.summary.report_summary",
    "archkeel.render.summary.check_summary",
    "archkeel.render.summary.init_summary",
    "archkeel.render.terminal.print_result",
)


def test_declared_module_responsibilities_name_existing_implementations():
    for path in CONTRACTS:
        for module in json.loads(path.read_bytes()).get("declarations", {}).get("modules", []):
            assert (ROOT / module["path"]).is_file(), (path, module)


def _port_repository(tmp_path):
    # Keep authored signatures; isolate them from unrelated ownership and rule fixtures.
    entities = {
        entity["qualified_name"]: entity
        for path in CONTRACTS
        for entity in json.loads(path.read_bytes())
        .get("declarations", {})
        .get("uml", {})
        .get("entities", [])
    }
    selected = {entities[name]["id"]: entities[name] for name in PORTS}
    assert all(entity.get("signature") for entity in selected.values())
    by_id = {entity["id"]: entity for entity in entities.values()}
    for entity in list(selected.values()):
        parent = by_id.get(entity.get("parent_id"))
        while parent is not None:
            selected[parent["id"]] = parent
            parent = by_id.get(parent.get("parent_id"))
    selected.update(
        (entity["id"], entity)
        for entity in entities.values()
        if entity.get("parent_id") == "COMPACT-OBSERVER" and entity["kind"] == "attribute"
    )
    target = []
    files = {
        "archkeel/__init__.py": "",
        "docs/architecture/target/design.md": "Exact compact architecture ports.\n",
    }
    for entity in selected.values():
        row = dict(entity)
        if row["kind"] == "module":
            row.pop("parent_id", None)
            relative = Path(*row["qualified_name"].split("."))
            source = ROOT / "src" / relative.with_suffix(".py")
            if not source.is_file():
                relative /= "__init__.py"
                source = ROOT / "src" / relative
            else:
                relative = relative.with_suffix(".py")
            files[relative.as_posix()] = source.read_text()
            for parent in relative.parents:
                if str(parent) != ".":
                    files.setdefault((parent / "__init__.py").as_posix(), "")
        target.append(row)
    files["contract.json"] = json.dumps(
        {
            "schema_version": "2.3.0",
            "components": [],
            "rules": [],
            "declarations": {
                "uml": {
                    "schema_version": "1.1.0",
                    "entities": target,
                    "relationships": [],
                    "scopes": [],
                }
            },
        }
    )
    root = _prepare_repo(tmp_path, files)
    return root, ScanConfig(("archkeel",), "archkeel", "contract.json", "0" * 64)


def _port_comparison(root, config):
    from test_uml_evaluation import _model

    from archkeel.ir.report_graph import architecture_report

    comparison = architecture_report(_model(root, config)).comparison
    assert comparison is not None
    return comparison


def test_real_core_and_render_ports_fulfil_independent_authored_signatures(tmp_path):
    root, config = _port_repository(tmp_path)
    comparison = _port_comparison(root, config)
    assert comparison.status == "PASS", [
        row for row in comparison.assessments if row.status != "PASS"
    ]
    assert sum(row.aspect == "signature" for row in comparison.assessments) == len(PORTS)


@pytest.mark.parametrize(
    "path,before,after",
    [
        ("api.py", "-> tuple[ViolationRow, ...]:", "-> str:"),
        ("check/ports.py", "roots: tuple[str, ...],", "roots: list[str],"),
        ("check/observe.py", 'tsconfig: str = "tsconfig.json"', "tsconfig: int = 1"),
        (
            "render/summary.py",
            "def report_summary(result: RunResult)",
            "def report_summary(result: str)",
        ),
    ],
)
def test_real_port_drift_fails_without_changing_authored_intent(tmp_path, path, before, after):
    root, config = _port_repository(tmp_path)
    intent = (root / "contract.json").read_bytes()
    source = root / "archkeel" / path
    assert before in source.read_text()
    source.write_text(source.read_text().replace(before, after, 1))
    comparison = _port_comparison(root, config)
    assert comparison.status == "FAIL"
    assert any(row.status == "FAIL" for row in comparison.assessments)
    assert (root / "contract.json").read_bytes() == intent


@pytest.mark.parametrize("path", ["api.py", "check/ports.py", "check/observe.py", "render/html.py"])
def test_missing_port_source_cannot_prove_conformance(tmp_path, path):
    root, config = _port_repository(tmp_path)
    intent = (root / "contract.json").read_bytes()
    (root / "archkeel" / path).unlink()
    comparison = _port_comparison(root, config)
    assert comparison.status == "UNKNOWN"
    assert any(row.status == "UNKNOWN" for row in comparison.assessments)
    assert (root / "contract.json").read_bytes() == intent
