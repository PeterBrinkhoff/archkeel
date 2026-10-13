# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Named TypeScript parameter properties are direct declarations, not inferred storage."""

import json
from pathlib import Path

import pytest
from test_typescript_inner import _collected
from test_typescript_partial_uml import _project, _TypeScriptCollector

from archkeel.analyzer.typescript.parse import parse
from archkeel.check.observe import Observer
from archkeel.check.report import run_report, run_saved_report
from archkeel.ir.codec import decode_canonical_model, parse_observation
from archkeel.ir.report_graph import architecture_report


@pytest.mark.parametrize(
    "modifier,visibility",
    [
        ("public", "public"),
        ("private", "private"),
        ("protected", "protected"),
        ("readonly", None),
        ("private readonly", "private"),
    ],
)
def test_named_parameter_properties_preserve_parameter_and_member(modifier, visibility):
    source = f"export class Store {{ constructor({modifier} repo: string, ordinary: number) {{}} }}"
    syntax = parse("src/main.ts", source.encode())
    owner = next(d for d in syntax.definitions if d.kind == "class")
    constructor = next(d for d in syntax.definitions if d.name == "constructor")
    assert [(m.name, m.annotation, m.visibility, m.static) for m in owner.members] == [
        ("repo", "string", visibility, False)
    ]
    assert owner.members_complete
    assert [(p.name, p.annotation) for p in constructor.parameters] == [
        ("repo", "string"),
        ("ordinary", "number"),
    ]
    assert constructor.signature_complete
    assert owner.members[0].span.column == source.index("repo") + 1


def test_default_literal_belongs_to_parameter_not_constant_property():
    syntax = parse("main.ts", b"class Store { constructor(readonly count: number = 7) {} }")
    owner = next(d for d in syntax.definitions if d.kind == "class")
    constructor = next(d for d in syntax.definitions if d.name == "constructor")
    assert [m.name for m in owner.members] == ["count"]
    assert owner.members[0].literal is None
    assert constructor.parameters[0].default == "7"
    assert constructor.signature_complete is False


@pytest.mark.parametrize(
    "body",
    [
        "constructor(private {repo}: object) {}",
        "constructor(private ...repo: string[]) {}",
        "constructor(private repo: string, private repo: string) {}",
        "repo: string; constructor(private repo: string) {}",
        "constructor(private repo: string); constructor(repo: string) {}",
        "constructor(repo: string); constructor(private repo: string) {}",
        "constructor(private repo: ) {}",
    ],
)
def test_ambiguous_or_malformed_parameter_properties_keep_inventory_partial(body):
    syntax = parse("main.ts", f"class Store {{ {body} }}".encode())
    owners = [d for d in syntax.definitions if d.kind == "class"]
    if syntax.first_error is not None:
        assert all(owner.members_complete is False for owner in owners)
        return
    owner = owners[0]
    assert owner.members_complete is False
    assert len({m.name for m in owner.members}) == len(owner.members)


@pytest.mark.parametrize("extra", ["[key](): void {}", "@Get() read(): void {}"])
def test_other_unsupported_members_do_not_become_complete(extra):
    syntax = parse(
        "main.ts", f"class Store {{ constructor(private repo: string) {{}} {extra} }}".encode()
    )
    owner = next(d for d in syntax.definitions if d.kind == "class")
    assert [m.name for m in owner.members] == ["repo"]
    assert owner.members_complete is False


def test_parameter_properties_use_existing_bound_source_attribute_facts(tmp_path: Path):
    source = (
        "export class Store { constructor(\n"
        "  protected readonly repo: string, ordinary: number\n) {} }\n"
    )
    facts = _collected(tmp_path, source)
    records = next(s.records for s in facts.sections if s.name == "symbols")
    owner = next(r for r in records if r.kind == "class")
    declarations = owner.data.get("attribute_declarations")
    assert len(declarations) == 1
    field = declarations[0]
    assert field.get("name") == "repo" and field.get("annotation") == "string"
    assert field.get("visibility").get("kind") == "protected"
    assert field.get("static") is False
    evidence = next(e for e in facts.evidence if e.id in field.get("evidence_ids"))
    assert (evidence.file, evidence.line, evidence.column) == ("src/main.ts", 2, 22)
    inventories = owner.data.get("member_inventories")
    assert all(i.get("status") == "complete" for i in inventories)
    assert next(i for i in inventories if i.get("kind") == "attribute").get("definition_ids") == (
        field.get("definition_id"),
    )


def _target(root: Path, expected: str):
    root, config = _project(root, matching=True)
    (root / "src/main.ts").write_text(
        "export class Store { constructor(readonly repo: string, ordinary: number) {} }\n"
    )
    contract_path = root / "architecture-contract.json"
    contract = json.loads(contract_path.read_bytes())
    declaration = {
        "presence": "planned",
        "language": "typescript",
        "provenance": ["docs/target.md"],
        "responsibilities": ["Declare the independent Store API."],
    }
    entities = [
        {
            **declaration,
            "id": "main",
            "kind": "module",
            "qualified_name": "demo.src.main_x2e_ts",
            "parent_id": "app",
            "file_path": "src/main.ts",
        },
        {
            **declaration,
            "id": "store",
            "kind": "class",
            "qualified_name": "demo.src.main_x2e_ts.Store",
            "parent_id": "main",
        },
    ]
    if expected:
        entities.append(
            {
                **declaration,
                "id": "field",
                "kind": "attribute",
                "qualified_name": f"demo.src.main_x2e_ts.Store.{expected}",
                "parent_id": "store",
                "annotation": "string",
            }
        )
    uml = contract["declarations"]["uml"]
    uml["schema_version"] = "1.1.0"
    uml["entities"] = entities
    uml["scopes"] = [
        {
            "scope_id": "store",
            "entity_kinds": ["attribute"],
            "mode": "closed",
            "rationale": "Only declared direct fields.",
            "provenance": ["docs/target.md"],
        }
    ]
    contract_path.write_text(json.dumps(contract))
    return root, config


@pytest.mark.parametrize("expected,status", [("repo", "PASS"), ("missing", "FAIL"), ("", "FAIL")])
def test_readonly_only_property_matches_native_and_saved_reports(tmp_path, expected, status):
    root, config = _target(tmp_path / "project", expected)
    result, encoded = run_report(root, config=config, analyzer=Observer(_TypeScriptCollector()))
    assert encoded is not None
    model = parse_observation(decode_canonical_model(json.loads(encoded)))
    comparison = architecture_report(model).comparison
    assert comparison.status == status
    assert result.declared_rules == status
    if expected == "missing":
        assert any(a.subject_id == "field" and a.status == "FAIL" for a in comparison.assessments)
    if not expected:
        assert any(
            a.aspect == "completeness" and a.status == "FAIL" for a in comparison.assessments
        )
    saved = root / "saved.json"
    saved.write_bytes(encoded)
    replay = run_saved_report(saved)
    assert replay.declared_rules == result.declared_rules
    assert replay.rule_assessments == result.rule_assessments
