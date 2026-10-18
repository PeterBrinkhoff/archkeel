# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""The actual shipped sources must satisfy independent browser intent."""

import json
import shutil
from pathlib import Path

import jsonschema
import pytest
from test_architecture_demo import _prepare_repo

from archkeel.ir.codec import contract_bytes, parse_contract
from tools.browser_architecture import main

ROOT = Path(__file__).parents[1]
ASSETS = Path("src/archkeel/render/assets")
INTENT = Path("docs/architecture/target/browser-contract.json")


def _repository(tmp_path):
    fixture = tmp_path / "fixture"
    shutil.copytree(ROOT / ASSETS, fixture / ASSETS)
    for relative in (
        INTENT,
        Path("docs/architecture/browser.toml"),
        Path("docs/architecture/browser.tsconfig.json"),
        Path("docs/architecture/target/design.md"),
    ):
        destination = fixture / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    return _prepare_repo(tmp_path, {}, fixture)


def test_browser_contract_schema_and_canonical_roundtrip():
    raw = json.loads((ROOT / INTENT).read_bytes())
    jsonschema.validate(
        raw, json.loads((ROOT / "schema/architecture-contract.schema.json").read_bytes())
    )
    encoded = contract_bytes(parse_contract(raw))
    assert contract_bytes(parse_contract(json.loads(encoded))) == encoded


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [("none", "PASS"), ("forbidden", "FAIL"), ("missing-publication", "UNKNOWN")],
)
def test_actual_browser_sources_require_proven_bindings_with_fixed_intent(
    tmp_path, mutation, expected
):
    root = _repository(tmp_path)
    intent = (root / INTENT).read_bytes()
    if mutation == "forbidden":
        layout = root / ASSETS / "report-layout.js"
        layout.write_text(layout.read_text() + "\nArchkeelReportScene.search([], 'probe');\n")
    elif mutation == "missing-publication":
        scene = root / ASSETS / "report-scene.js"
        original = (
            "global.ArchkeelReportScene = "
            "{ create, search, sceneToMermaid, decider, perspectives };"
        )
        text = scene.read_text()
        assert text.count(original) == 1
        scene.write_text(
            text.replace(
                original, "void { create, search, sceneToMermaid, decider, perspectives };"
            )
        )
    output = tmp_path / "architecture.json"
    code = main(["--root", str(root), "--output", str(output)])
    receipt = json.loads(output.with_suffix(".receipt.json").read_bytes())
    assert code == (0 if expected == "PASS" else 1), receipt
    assert receipt["files_discovered"] == receipt["files_read"] == receipt["files_parsed"] == 9
    assert receipt["source_drift"] is False
    [rule] = receipt["rules"]
    assert rule["status"] == expected, receipt
    if expected == "PASS":
        assert rule["evaluation_proven"] is True
        assert rule["undecided"] == rule["violations"] == 0
    assert (root / INTENT).read_bytes() == intent


@pytest.mark.parametrize("mutation", ["missing-file", "unowned-file"])
def test_browser_gate_rejects_incomplete_or_unowned_physical_scope(tmp_path, mutation):
    root = _repository(tmp_path)
    if mutation == "missing-file":
        (root / ASSETS / "report-scene.js").unlink()
    else:
        (root / ASSETS / "new-owner.js").write_text("window.NewOwner = {};\n")
    output = tmp_path / "architecture.json"
    message = (
        "scan root is not a directory or file"
        if mutation == "missing-file"
        else "every shipped JavaScript source"
    )
    with pytest.raises(ValueError, match=message):
        main(["--root", str(root), "--output", str(output)])
    assert not output.exists()
