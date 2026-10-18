# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Require native source-binding proof for the shipped browser boundaries."""

import argparse
import hashlib
import json
from collections.abc import Sequence
from pathlib import Path

from archkeel.check.report import run_report
from archkeel.cli.config import load_config
from archkeel.cli.observe import observer_for
from archkeel.ir.codec import decode_canonical_model, parse_contract, parse_observation


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--output", type=Path, default=Path("test-artifacts/browser-architecture/architecture.json")
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    configuration = Path("docs/architecture/browser.toml")
    config = load_config(root, str(configuration))
    contract = parse_contract(json.loads((root / config.contract).read_bytes()))
    assets = root / "src/archkeel/render/assets"
    # Runtime derivation and vendor publication have separate generation/source witnesses.
    derived_or_vendor = {assets / "flow.runtime.js", assets / "elkjs-0.12.0.bundled.js"}
    selected = {root / path for path in config.roots}
    if selected | derived_or_vendor != set(assets.glob("*.js")):
        raise ValueError("Browser roots must cover every shipped JavaScript source")
    inputs = {
        *selected,
        *derived_or_vendor,
        *assets.glob("*.ts"),
        *assets.glob("*.md"),
        root / configuration,
        root / config.contract,
        root / (config.tsconfig or "tsconfig.json"),
    }
    before = {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in inputs
    }
    result, artifact = run_report(
        root,
        config=config,
        analyzer=observer_for(config.language, tsconfig=config.tsconfig or "tsconfig.json"),
    )
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if artifact is None:
        print(result)
        return 1
    output.write_bytes(artifact)
    model = parse_observation(decode_canonical_model(json.loads(artifact)))
    after = {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in inputs
    }
    observed = {row.data.get("file") for row in model.records("modules") or ()}
    rows = result.rule_assessments or ()
    expected = {rule.id for rule in contract.rules}
    passed = (
        before == after
        and observed == set(config.roots)
        and model.coverage.files_discovered
        == model.coverage.files_read
        == model.coverage.files_parsed
        == len(selected)
        > 0
        and {row.id for row in rows} == expected
        and bool(rows)
        and all(
            row.status == "PASS" and row.evaluation_proven and row.count == row.undecided == 0
            for row in rows
        )
    )
    receipt = {
        "passed": passed,
        "git_head": model.source.git_head,
        "source_digest": model.source.source_digest,
        "contract_digest": model.contract.digest,
        "artifact_sha256": hashlib.sha256(artifact).hexdigest(),
        "files_discovered": model.coverage.files_discovered,
        "files_read": model.coverage.files_read,
        "files_parsed": model.coverage.files_parsed,
        "observation_complete": result.observation_complete,
        "declared_rules": result.declared_rules,
        "coverage_gaps": len(model.coverage.failures),
        "input_hashes": before,
        "source_drift": before != after,
        "rules": [
            {
                "id": row.id,
                "status": row.status,
                "evaluation_proven": row.evaluation_proven,
                "violations": row.count,
                "undecided": row.undecided,
            }
            for row in rows
        ],
    }
    output.with_suffix(".receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(receipt, sort_keys=True))
    return int(not passed)


if __name__ == "__main__":
    raise SystemExit(main())
