# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""A nested owner move keeps publication and dependency policy deliberate."""

import json
from pathlib import Path

from test_architecture_demo import _prepare_repo
from test_dart_uml_acceptance import FIXTURE

from archkeel.check.report import run_report, run_saved_report
from archkeel.check.validation import run_validate
from archkeel.cli.config import load_config
from archkeel.cli.observe import observe

OLD = "commerce.ordering.domain.pricing.discount_policy"
NEW = "commerce.ordering.domain.orders.discount_policy"
OLD_PATH = "lib/ordering/domain/pricing/discount_policy.dart"
NEW_PATH = "lib/ordering/domain/orders/discount_policy.dart"


def _move_discount(root: Path) -> None:
    (root / OLD_PATH).rename(root / NEW_PATH)
    path = root / "contracts/domain.json"
    domain = json.loads(path.read_text().replace(OLD, NEW).replace(OLD_PATH, NEW_PATH))
    orders = next(item for item in domain["components"] if item["id"] == "orders")
    orders["public"].append(NEW)
    orders["responsibilities"].append("Own the discount policy applied to orders.")
    domain["components"] = [orders]
    module = next(
        item for item in domain["declarations"]["uml"]["entities"] if item["id"] == "pricing-module"
    )
    module["parent_id"] = "orders"
    path.write_text(json.dumps(domain, indent=2) + "\n")
    parent = root / "contracts/ordering.json"
    parent.write_text(parent.read_text().replace(OLD, NEW))


def test_nested_owner_move_preserves_native_target_and_forbidden_import(tmp_path: Path) -> None:
    root = _prepare_repo(tmp_path, {}, fixture=FIXTURE)
    root_contract = (root / "architecture-contract.json").read_bytes()
    before, _ = run_report(root, config=load_config(root), analyzer=observe)
    assert before.exit_code == 0 and before.declared_rules == "PASS", before.diagnostics
    assert before.architecture_projection is not None
    previous = next(
        owner
        for owner in before.architecture_projection.components
        if owner.label == "pricing" and any(module.name == OLD for module in owner.modules)
    )
    _move_discount(root)
    after, encoded = run_report(root, config=load_config(root), analyzer=observe)
    assert after.exit_code == 0 and after.declared_rules == "PASS", after.diagnostics
    assert after.architecture_projection is not None
    current = next(
        owner
        for owner in after.architecture_projection.components
        if owner.label == "orders" and any(module.name == NEW for module in owner.modules)
    )
    assert NEW in current.public and current.scope != previous.scope
    assert (root / "architecture-contract.json").read_bytes() == root_contract
    packet = tmp_path / "architecture.json"
    packet.write_bytes(encoded)
    focused = run_saved_report(
        packet, only_architecture=True, component="ordering:domain:orders", full_architecture=True
    )
    assert focused.exit_code == 0 and focused.declared_rules == "PASS", focused.diagnostics
    assert focused.architecture_projection is not None
    assert focused.architecture_projection.components == (current,)
    validation, _ = run_validate(root, load_config(root), observe, against="HEAD")
    assert validation.exit_code == 1 and validation.widenings

    source = root / NEW_PATH
    source.write_text(
        "import 'package:commerce/adapters/diagnostics/receipt_formatter.dart';\n"
        + source.read_text()
    )
    failed, _ = run_report(root, config=load_config(root), analyzer=observe)
    assert failed.exit_code == 0 and failed.declared_rules == "FAIL", failed.diagnostics
    assert any(
        row.id == "REQUIRES-COMPLETE" and row.status == "FAIL" for row in failed.rule_assessments
    )
