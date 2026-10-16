# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Independent authored intent checks the actual deviation value owner."""

import copy
import json
from pathlib import Path

from test_architecture_demo import _prepare_repo
from test_uml_evaluation import _model

from archkeel.check.ports import ScanConfig
from archkeel.ir.decisions import rule_assessments
from archkeel.ir.report_graph import architecture_report
from archkeel.ir.trace import trace_valid_violations

ROOT = Path(__file__).parents[1]
OWNER = "archkeel.render.atlas_deviations"
GUARD = "RENDER-DEVIATION-TYPED-CONTROL"
SPEC = "docs/superpowers/specs/2026-10-16-atlas-deviation-boundary.md"


def _contract():
    render = json.loads((ROOT / "docs/architecture/contracts/render.json").read_text())
    component = copy.deepcopy(next(row for row in render["components"] if row["label"] == "atlas-payload"))
    component["exact_modules"] = [OWNER]
    component["public"] = [port for port in component["public"] if port.startswith(OWNER + ":")]
    component["provenance"] = [SPEC]
    return {
        "schema_version": render["schema_version"], "components": [component],
        "declarations": {"uml": {"schema_version": "1.2.0", "entities": [
            row for row in render["declarations"]["uml"]["entities"]
            if row["id"].startswith("RENDER-DEVIATION-")
        ], "relationships": [], "scopes": []}},
        "rules": [row for row in render["rules"] if row["id"] == GUARD],
    }


def _repository(tmp_path):
    files = {
        "archkeel/__init__.py": "", "archkeel/render/__init__.py": "",
        "contract.json": json.dumps(_contract()), SPEC: (ROOT / SPEC).read_text(),
    }
    owner = ROOT / "src/archkeel/render/atlas_deviations.py"
    if owner.is_file():
        files["archkeel/render/atlas_deviations.py"] = owner.read_text()
    else:
        files["archkeel/render/atlas.py"] = (ROOT / "src/archkeel/render/atlas.py").read_text()
    root = _prepare_repo(tmp_path, files)
    return root, ScanConfig(("archkeel",), "archkeel", "contract.json", "0" * 64)


def test_actual_deviation_owner_fulfills_fixed_types_and_whole_owner_guard(tmp_path):
    root, config = _repository(tmp_path)
    model = _model(root, config)
    comparison = architecture_report(model).comparison
    assert comparison is not None and comparison.status == "PASS", comparison
    guard = next(row for row in rule_assessments(model, undecided_by_rule={}) if row.id == GUARD)
    assert guard.status == "PASS" and guard.evaluation_proven, guard
    assert not trace_valid_violations(model)
