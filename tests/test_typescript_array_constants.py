# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Array constant identities prove lexical declarations, without evaluating their values."""

import json
from dataclasses import replace
from pathlib import Path

import pytest
from test_source_graph import _graph_from_source_facts
from test_typescript_inner import _collected, _collected_files

from archkeel.analyzer.typescript.parse import parse
from archkeel.check.observation import assemble_observation
from archkeel.check.uml_compare import compare_graphs
from archkeel.ir.architecture_graph import ArchitectureGraph, Coverage, Entity, Visibility
from archkeel.ir.codec import canonical_report_bytes, decode_canonical_model, parse_observation
from archkeel.ir.graph_codec import graph_bytes, parse_graph
from archkeel.ir.source_graph import observed_graph


@pytest.mark.parametrize(
    "initializer",
    ["[Entry]", "[Entry, Other] as const", "['literal', 1, true, false, null]", "[] as const"],
)
def test_module_array_constants_retain_native_definition_identity(tmp_path: Path, initializer: str):
    facts = _collected(tmp_path, f"export const registry: readonly unknown[] = {initializer};\n")
    symbols = [
        record
        for section in facts.sections
        if section.name == "symbols"
        for record in section.records
        if record.data.get("name") == "registry"
    ]
    assert len(symbols) == 1
    record = symbols[0]
    assert record.kind == "constant"
    assert record.data.get("parent") is None
    assert record.data.get("annotation") == "readonly unknown[]"
    assert record.data.get("visibility_detail").get("kind") == "public"
    assert record.data.get("source_binding_unique") is True
    assert not {"constant", "initializer"} & {key for key, _ in record.data.entries}
    assert record.evidence_ids
    evidence = next(item for item in facts.evidence if item.id == record.evidence_ids[0])
    assert (evidence.file, evidence.line) == ("src/main.ts", 1)


@pytest.mark.parametrize(
    "source",
    [
        "export const registry = [make()];",
        "export const registry = [() => Entry];",
        "export const registry = [...entries] as const;",
        "export const registry = [entries.key];",
        "export const registry = [[Entry]];",
        "export const registry = [Entry] as readonly unknown[];",
        "export const registry = make() as const;",
        "export const registry = [Entry] as const satisfies readonly unknown[];",
        "export const registry = [Entry, ;",
        "export const [registry] = [Entry] as const;",
        "export let registry = [Entry] as const;",
        "if (enabled) { const registry = [Entry] as const; }",
        "function local() { const registry = [Entry] as const; }",
        "class Owner { constructor() { const registry = [Entry] as const; } }",
        "const callback = () => { const registry = [Entry] as const; };",
        "namespace Internal { export const registry = [Entry] as const; }",
    ],
)
def test_unsupported_array_declarations_do_not_invent_module_constants(source: str):
    assert not any(
        item.name == "registry" for item in parse("src/main.ts", source.encode()).definitions
    )


def test_pinned_nest_registry_matches_independent_target_live_and_saved(tmp_path: Path):
    fixture = Path(__file__).parents[1] / "fixtures/L-nest-realworld/src/entities.generated.ts"
    original = fixture.read_bytes()
    copied_source = tmp_path / "src/entities.generated.ts"
    copied_source.parent.mkdir()
    copied_source.write_bytes(original)
    facts = _collected_files(tmp_path, {})
    (tmp_path / "architecture-contract.json").write_text(
        json.dumps({"schema_version": "2.1.0", "components": [], "rules": []})
    )
    observation, _ = assemble_observation(
        facts,
        contract_root=tmp_path,
        contract_path=tmp_path / "architecture-contract.json",
        roots=("src",),
        namespace="app",
        language="typescript",
    )
    observed = observed_graph(observation)
    module_name = "app.src.entities_x2e_generated_x2e_ts"
    target = ArchitectureGraph(
        "declared",
        entities=(
            Entity(
                "module",
                "module",
                module_name,
                "typescript",
                presence="planned",
                provenance=("docs/target.md",),
            ),
            Entity(
                "registry",
                "constant",
                f"{module_name}.entities",
                "typescript",
                parent_id="module",
                presence="planned",
                visibility=Visibility("public", "declared"),
                provenance=("docs/target.md",),
            ),
        ),
    )
    live = compare_graphs(observed, target)
    restored = parse_observation(
        decode_canonical_model(json.loads(canonical_report_bytes(observation)))
    )
    saved = compare_graphs(observed_graph(restored), target)
    assert live == saved and live.status == "PASS"
    entity = next(
        item for item in observed.entities if item.qualified_name == f"{module_name}.entities"
    )
    assert entity.kind == "constant" and entity.annotation is None and entity.initializer is None
    evidence = next(item for item in observed.evidence if item.id == entity.evidence_ids[0])
    assert (evidence.file, evidence.line, evidence.end_line) == (
        "src/entities.generated.ts",
        10,
        15,
    )
    module = next(item for item in observed.entities if item.qualified_name == module_name)
    assert any(
        item.scope_id == module.id and "constant" in item.entity_kinds and item.status == "partial"
        for item in observed.coverage
    )
    assert fixture.read_bytes() == original
    assert copied_source.read_bytes() == original

    absent = replace(
        observed,
        entities=tuple(item for item in observed.entities if item.id != entity.id),
        relationships=tuple(
            item
            for item in observed.relationships
            if entity.id not in (item.source_id, item.target_id, *item.candidate_ids)
        ),
    )
    assert compare_graphs(absent, target).status == "UNKNOWN"
    complete = replace(absent, coverage=(Coverage(module.id, ("constant",), status="complete"),))
    assert compare_graphs(complete, target).status == "FAIL"
    assert compare_graphs(parse_graph(json.loads(graph_bytes(complete))), target).status == "FAIL"


def test_duplicate_array_declarations_remain_ambiguous(tmp_path: Path):
    facts = _collected(
        tmp_path, "export const registry = [Entry];\nexport const registry = [Other];\n"
    )
    observed = _graph_from_source_facts(facts, ("src",))
    name = "app.src.main_x2e_ts.registry"
    definitions = [item for item in observed.entities if item.qualified_name == name]
    assert len(definitions) == len({item.id for item in definitions}) == 2
    assert all(
        record.data.get("source_binding_unique") is False
        for section in facts.sections
        if section.name == "symbols"
        for record in section.records
        if record.data.get("qualified_name") == name
    )
    target = ArchitectureGraph(
        "declared",
        entities=(
            Entity(
                "registry",
                "constant",
                name,
                "typescript",
                presence="planned",
                provenance=("docs/target.md",),
            ),
        ),
    )
    comparison = compare_graphs(observed, target)
    assert comparison.status == "UNKNOWN"
    assert comparison.assessments[0].change == "ambiguous"
    assert set(comparison.assessments[0].observed_ids) == {item.id for item in definitions}


def test_array_constant_identity_does_not_prove_call_or_constructor_dispatch(tmp_path: Path):
    facts = _collected(
        tmp_path, "export const registry = [Entry] as const;\nregistry();\nnew registry();\n"
    )
    calls = [
        record
        for section in facts.sections
        if section.name == "calls"
        for record in section.records
    ]
    assert len(calls) == 2
    assert all(record.data.get("status") == "unresolved" for record in calls)
    observed = _graph_from_source_facts(facts, ("src",))
    target = ArchitectureGraph(
        "declared",
        entities=(
            Entity(
                "operation",
                "function",
                "app.src.main_x2e_ts.registry",
                "typescript",
                presence="planned",
                provenance=("docs/target.md",),
            ),
        ),
    )
    assessment = compare_graphs(observed, target).assessments[0]
    assert (assessment.aspect, assessment.status, assessment.change) == ("kind", "FAIL", "changed")
