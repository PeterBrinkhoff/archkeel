# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""A direct alias permission binds source origin and every syntactic payload leaf."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from test_analyzer import _observe
from test_boundary_type_opaque_map_values import _app
from test_boundary_types_contained_mapping import _commit_report_fixture

from archkeel.analyzer.python.type_shapes import collect_type_shapes
from archkeel.check.evaluation.boundary_types import _boundary_type_verdict, boundary_type_indexes
from archkeel.ir.codec import (
    decode_canonical_model,
    observation_payload,
    parse_contract,
    parse_observation,
)
from archkeel.ir.model import Observation, Record, RecordData
from archkeel.ir.trace import trace_valid_violations

_BODY = (
    "tuple[tuple[str, list[object]] | tuple[str, list[object], Metadata], list[dict[str, object]]]"
)
_SHAPE = _BODY.replace("Metadata", "sample.app.types.Metadata")
_BINDING = {"origin": "sample.app.impl:Packet", "shape": _SHAPE}
_SELECTIONS = [(), (0,), (1,), (2,), (3,), (0, 1, 2, 3)]


def _selectors(facade: bool) -> list[dict[str, object]]:
    owner = f"sample.app{'' if facade else '.impl'}.Session"
    return [
        {
            "qualified_name": f"{owner}.{method}",
            "position": position,
            "annotation": "Packet",
            "alias_body": _BINDING,
            **({"container_depth": 3} if depth else {}),
        }
        for method, position in [("prepare", "return"), ("dispatch", "packet")]
        for depth in [None, 3]
    ]


def _fixture(
    root: Path,
    *,
    facade: bool = False,
    selected: tuple[int, ...] = (0, 1, 2, 3),
    body: str = _BODY,
    prefix: str = "",
    metadata: str = "class Metadata:\n    label: str\n",
    annotation: str = "Packet",
    change: dict[str, object] | None = None,
    bound: bool = True,
    alias_module: bool = False,
    metadata_module: str = "types",
    alias_suffix: str = "",
) -> None:
    owner = f"sample.app{'' if facade else '.impl'}"
    source = (
        f"from .{metadata_module} import Metadata\n"
        + prefix
        + ("from .moved import Packet\n" if alias_module else f"Packet = {body}\n")
        + alias_suffix
        + "class Session:\n"
        + f"    def prepare(self) -> {annotation}: pass\n"
        + f"    def dispatch(self, packet: {annotation}) -> None: pass\n"
        + "    def unrelated(self, counts: dict[str, int]) -> None: pass\n"
        + "    def undecided(self, value: Missing) -> None: pass\n"
    )
    selectors = _selectors(facade)
    if not bound:
        selectors = [
            {key: value for key, value in item.items() if key != "alias_body"} for item in selectors
        ]
    _app(
        root,
        source=source,
        declared=(
            f"{owner}:Session",
            f"sample.app.{metadata_module}:Metadata",
            f"sample.app.{metadata_module}:Other",
        ),
        allowances=tuple({**selectors[index], **(change or {})} for index in selected),
    )
    (root / f"sample/app/{metadata_module}.py").write_text(
        metadata + "class Other:\n    label: str\n"
    )
    (root / "sample/app/moved.py").write_text(
        "from .types import Metadata\n" + f"Packet = {body}\n"
    )
    if facade:
        (root / "sample/app/__init__.py").write_text(
            "from .impl import Session\n__all__ = ['Session']\n"
        )
    contract_path = root / "contract.json"
    contract = json.loads(contract_path.read_text())
    contract["schema_version"] = "3.0.0"
    contract_path.write_text(json.dumps(contract))
    (root / "pyproject.toml").write_text(
        '[project]\nname = "sample"\nversion = "0.0.0"\nrequires-python = ">=3.11"\n'
    )
    (root / "archkeel.toml").write_text(
        '[scan]\nroots = ["."]\nnamespace = "sample"\ncontract = "contract.json"\n'
    )


def _facts(observation: Observation) -> list[Record]:
    return [
        item
        for item in observation.records("typing_signals") or ()
        if item.kind == "boundary_type_allowance"
    ]


def _targets(observation: Observation) -> list[Record]:
    return [
        item
        for item in trace_valid_violations(observation)
        if str(item.data.get("qualified_name")).endswith((".prepare", ".dispatch"))
    ]


def _unknowns(observation: Observation) -> tuple[Record, ...]:
    return tuple(
        item
        for item in observation.records("unknowns") or ()
        if item.kind == "boundary_type_position"
    )


@pytest.mark.parametrize("facade", [False, True], ids=["direct", "facade"])
@pytest.mark.parametrize("selected", _SELECTIONS)
def test_four_exact_selectors_are_independent_and_keep_unrelated_evidence(
    tmp_path: Path, facade: bool, selected: tuple[int, ...]
) -> None:
    _fixture(tmp_path, facade=facade, selected=())
    before = _observe(tmp_path)
    assert before.observation is not None and before.diagnostics == ()
    unrelated = tuple(
        item
        for item in trace_valid_violations(before.observation)
        if item not in _targets(before.observation)
    )
    unknowns = _unknowns(before.observation)
    assert len(_targets(before.observation)) == 4 and unrelated and unknowns
    _fixture(tmp_path, facade=facade, selected=selected)
    after = _observe(tmp_path)
    assert after.observation is not None and after.diagnostics == ()
    assert len(_targets(after.observation)) == 4 - len(selected)
    assert (
        tuple(
            item
            for item in trace_valid_violations(after.observation)
            if item not in _targets(after.observation)
        )
        == unrelated
    )
    assert _unknowns(after.observation) == unknowns
    facts = _facts(after.observation)
    assert len(facts) == len(selected)
    evidence = {item.id: item for item in after.observation.evidence}
    symbols = {item.id: item for item in after.observation.records("symbols") or ()}
    for fact in facts:
        pair = fact.data.get("alias_body")
        assert isinstance(pair, RecordData) and dict(pair.entries) == _BINDING
        assert fact.provenance == ("docs/architecture/sample.md",)
        assert fact.rule_ids == ("APP-TYPES-NOT-DICT",)
        locations = [evidence[item].file for item in fact.evidence_ids]
        assert "sample/app/impl.py" in locations and "sample/app/types.py" in locations
        assert any(symbols[item].kind == "type_alias" for item in fact.fact_ids if item in symbols)
        assert any(symbols[item].kind == "method" for item in fact.fact_ids if item in symbols)
        if fact.data.get("container_depth") == 3:
            assert fact.data.get("accepted_opacity") is True
            assert "type closure remains unproven" in fact.title
        else:
            assert fact.data.get("accepted_opacity") is None
    repeat = _observe(tmp_path)
    assert repeat.observation is not None
    assert _facts(repeat.observation) == facts
    assert trace_valid_violations(repeat.observation) == trace_valid_violations(after.observation)


@pytest.mark.parametrize("facade", [False, True])
def test_unbound_alias_keeps_the_original_four_findings(tmp_path: Path, facade: bool) -> None:
    _fixture(tmp_path, facade=facade, bound=False)
    result = _observe(tmp_path)
    assert result.observation is not None
    assert len(_targets(result.observation)) == 4 and _facts(result.observation) == []


_MUTATIONS = [
    {"body": _BODY.replace("dict[str, object]", "dict[int, object]")},
    {"body": _BODY.replace("list[dict[str, object]]]", "list[dict[str, object]], str]")},
    {"body": _BODY.replace("Metadata", "Other")},
    {"body": _BODY.replace("str, list[object], Metadata", "str, Metadata, list[object]")},
    {"prefix": "MetaAlias = Metadata\n", "body": _BODY.replace("Metadata", "MetaAlias")},
    {"body": _BODY.replace("list[dict", "tuple[dict")},
    {"body": _BODY.replace("tuple[", "list[", 1)},
    {"body": _BODY.replace("dict[str, object]", "dict[str, list[object]]")},
    {"body": _BODY.replace("tuple[str, list[object]] |", "tuple[str, list[object], object] |")},
    {"body": _BODY.replace(", list[dict", " | tuple[str, list[object]], list[dict")},
    {"body": _BODY.replace("str, list[object]] |", "str, list[object], ...] |")},
    {"body": _BODY.replace("list[object]", "list[object | None]", 1)},
    {"prefix": "class object: pass\n"},
    {"prefix": "class str: pass\n"},
    {"prefix": "class list: pass\n"},
    {"prefix": "class dict: pass\n"},
    {"metadata_module": "renamed"},
    {"alias_suffix": "Packet.__args__ = ()\n"},
    {"alias_suffix": "unknown(Packet)\n"},
    {"alias_suffix": "if condition: Packet = object\n"},
    {"prefix": "from missing import *\n"},
    {"prefix": "object = Missing\n"},
    {"prefix": "Packet = object\n"},
    {"prefix": f"Inner = {_BODY}\n", "body": "Inner"},
    {"prefix": "from typing import Annotated\n", "body": f"Annotated[{_BODY}, 'tag']"},
    {
        "prefix": "from typing import Annotated\n",
        "annotation": "Annotated[Packet, 'tag']",
        "change": {"annotation": "Annotated[Packet, 'tag']"},
    },
    {"annotation": "list[Packet]", "change": {"annotation": "list[Packet]"}},
    {"body": "factory()"},
    {"alias_module": True},
    {"prefix": "from .types import Other as Metadata\n"},
    {"metadata": "class Metadata:\n    label: str\nclass Metadata:\n    label: str\n"},
    {"metadata": "class Hidden:\n    label: str\nMetadata = Hidden\n"},
    {
        "metadata": (
            "from typing import Generic, TypeVar\nT = TypeVar('T')\n"
            "class Metadata(Generic[T]):\n    label: str\n"
        )
    },
]


@pytest.mark.parametrize("selected", [(0,), (1,), (2,), (3,), (0, 1, 2, 3)])
@pytest.mark.parametrize("mutation", _MUTATIONS)
def test_unchanged_binding_fails_closed_after_source_mutation(
    tmp_path: Path, selected: tuple[int, ...], mutation
) -> None:
    _fixture(tmp_path, facade=True, selected=selected, **mutation)
    result = _observe(tmp_path)
    assert result.observation is not None and result.diagnostics == ()
    assert _facts(result.observation) == []
    assert _targets(result.observation) or _unknowns(result.observation)


@pytest.mark.parametrize(
    "change",
    [
        {"qualified_name": "sample.app.impl.Session.unrelated"},
        {"position": "other"},
        {"container_depth": 1},
        {"container_depth": 2},
        {"container_depth": 4},
        {"alias_body": {**_BINDING, "origin": "sample.app.moved:Packet"}},
        {
            "alias_body": {
                **_BINDING,
                "shape": _SHAPE.replace("sample.app.types.Metadata", "sample.app.types.Other"),
            }
        },
        {"alias_body": {**_BINDING, "shape": _SHAPE.replace(" | ", "|")}},
    ],
)
def test_wrong_coordinates_and_stale_binding_grant_nothing(tmp_path: Path, change) -> None:
    _fixture(tmp_path, selected=(1, 3), change=change)
    result = _observe(tmp_path)
    assert result.observation is not None
    assert _facts(result.observation) == [] and len(_targets(result.observation)) == 4


def test_source_verdict_retains_three_object_occurrences_and_one_map_before_dedup(
    tmp_path: Path,
) -> None:
    _fixture(tmp_path, selected=())
    result = _observe(tmp_path)
    assert result.observation is not None
    raw = observation_payload(result.observation)
    symbols = raw["symbols"]
    imports = raw["imports"]
    bindings, classes = boundary_type_indexes(symbols, imports)
    verdict = _boundary_type_verdict(
        "Packet",
        "sample.app.impl",
        parse_contract(json.loads((tmp_path / "contract.json").read_text())),
        {},
        bindings,
        classes,
        type_shapes=collect_type_shapes(["Packet", _BODY, "str"]),
    )
    assert verdict.violations == (
        ("holding object instead of a typed model", (), "object", 3),
        ("holding object instead of a typed model", (), "object", 3),
        ("holding object instead of a typed model", (), "object", 3),
        ("instead of a typed model", (), "dict[str, object]", 2),
    )
    assert len(verdict.mapping_occurrences) == 1
    assert verdict.mapping_occurrences[0].depth == 2


@pytest.mark.parametrize("opaque", ["object", "Missing"])
def test_metadata_field_findings_and_unknowns_survive_payload_grants(
    tmp_path: Path, opaque: str
) -> None:
    metadata = f"class Metadata:\n    label: str\n    opaque: {opaque}\n"
    _fixture(tmp_path, selected=(), metadata=metadata)
    before = _observe(tmp_path)
    assert before.observation is not None
    before_fields = tuple(item for item in _targets(before.observation) if item.data.get("path"))
    before_unknowns = _unknowns(before.observation)
    _fixture(tmp_path, metadata=metadata)
    after = _observe(tmp_path)
    assert after.observation is not None
    assert len(_facts(after.observation)) == 4
    assert tuple(_targets(after.observation)) == before_fields
    assert _unknowns(after.observation) == before_unknowns
    assert before_fields if opaque == "object" else before_unknowns


def _cli(root: Path, command: str, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "from archkeel.cli import main; raise SystemExit(main())",
            command,
            "--root",
            str(root),
            *(["--output", str(output)] if command == "report" else []),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize("facade", [False, True])
@pytest.mark.parametrize("selected", _SELECTIONS)
def test_ordinary_cli_report_and_validate_preserve_unrelated_fail_and_unknown(
    tmp_path: Path, facade: bool, selected: tuple[int, ...]
) -> None:
    _fixture(tmp_path, facade=facade, selected=selected)
    _commit_report_fixture(tmp_path)
    output = tmp_path / "architecture.json"
    report = _cli(tmp_path, "report", output)
    assert report.returncode == 0, (json.loads(report.stdout)["diagnostics"], report.stderr)
    summary = json.loads(report.stdout)
    assert summary["declared_rules"] == "FAIL" and summary["diagnostics"] == []
    observation = parse_observation(decode_canonical_model(json.loads(output.read_text())))
    assert len(_facts(observation)) == len(selected)
    assert len(_targets(observation)) == 4 - len(selected)
    assert _unknowns(observation)
    validate = _cli(tmp_path, "validate", output)
    assert validate.returncode == 2, (validate.stdout, validate.stderr)
    assert json.loads(validate.stdout)["declared_rules"] == "FAIL"


@pytest.mark.parametrize(
    "mutation",
    [
        {"body": _BODY.replace("dict[str, object]", "dict[int, object]")},
        {"body": _BODY.replace("tuple[str, list[object]] |", "tuple[str, list[object], object] |")},
        {"prefix": f"Inner = {_BODY}\n", "body": "Inner"},
        {
            "prefix": "from typing import Annotated\n",
            "annotation": "Annotated[Packet, 'tag']",
            "change": {"annotation": "Annotated[Packet, 'tag']"},
        },
        {"alias_module": True},
        {"metadata_module": "renamed"},
    ],
)
def test_ordinary_cli_source_mutations_have_no_bound_grant(tmp_path: Path, mutation) -> None:
    _fixture(tmp_path, facade=True, **mutation)
    _commit_report_fixture(tmp_path)
    output = tmp_path / "architecture.json"
    result = _cli(tmp_path, "report", output)
    assert result.returncode == 0, (json.loads(result.stdout)["diagnostics"], result.stderr)
    observation = parse_observation(decode_canonical_model(json.loads(output.read_text())))
    assert _facts(observation) == []
    assert _targets(observation) or _unknowns(observation)


@pytest.mark.parametrize("depth", [None, 1])
def test_present_binding_never_falls_through_to_legacy_direct_map(
    tmp_path: Path, depth: int | None
) -> None:
    annotation = "dict[str, object]"
    change = (
        {"annotation": annotation, "container_depth": depth}
        if depth is not None
        else {"annotation": annotation}
    )
    _fixture(tmp_path, selected=(0,), annotation=annotation, change=change)
    result = _observe(tmp_path)
    assert result.observation is not None
    assert _facts(result.observation) == []
    assert _targets(result.observation)


@pytest.mark.parametrize("facade", [False, True])
def test_direct_imported_alias_uses_its_actual_source_origin(tmp_path: Path, facade: bool) -> None:
    _fixture(
        tmp_path,
        facade=facade,
        alias_module=True,
        change={"alias_body": {**_BINDING, "origin": "sample.app.moved:Packet"}},
    )
    result = _observe(tmp_path)
    assert result.observation is not None
    assert len(_facts(result.observation)) == 4 and _targets(result.observation) == []


def test_union_arm_order_is_preserved_in_the_binding(tmp_path: Path) -> None:
    reversed_body = (
        "tuple[tuple[str, list[object], Metadata] | tuple[str, list[object]], "
        "list[dict[str, object]]]"
    )
    _fixture(tmp_path, body=reversed_body)
    stale = _observe(tmp_path)
    assert stale.observation is not None and _facts(stale.observation) == []
    _fixture(
        tmp_path,
        body=reversed_body,
        change={
            "alias_body": {
                **_BINDING,
                "shape": reversed_body.replace("Metadata", "sample.app.types.Metadata"),
            }
        },
    )
    result = _observe(tmp_path)
    assert result.observation is not None
    assert len(_facts(result.observation)) == 4 and _targets(result.observation) == []


def test_dto_fields_do_not_inherit_direct_alias_permission(tmp_path: Path) -> None:
    _fixture(
        tmp_path,
        annotation="Envelope",
        prefix="",
        alias_suffix="class Envelope:\n    payload: Packet\n",
        change={"annotation": "Envelope"},
    )
    result = _observe(tmp_path)
    assert result.observation is not None
    assert _facts(result.observation) == [] and _targets(result.observation)


@pytest.mark.parametrize("facade", [False, True])
@pytest.mark.parametrize("selected", _SELECTIONS)
def test_ordinary_validate_cli_proves_exact_permission_with_fail_and_unknown(
    tmp_path: Path, facade: bool, selected: tuple[int, ...]
) -> None:
    _fixture(tmp_path, facade=facade, selected=selected)
    _commit_report_fixture(tmp_path)
    result = _cli(tmp_path, "validate", tmp_path / "unused.json")
    assert result.returncode == 2, result.stderr
    summary = json.loads(result.stdout)
    assert summary["declared_rules"] == "FAIL" and summary["observation_complete"] == "PASS"
    assert summary["coverage"]["status"] == "PASS"
    assert summary["rule_assessments"][0]["count"] == 5 - len(selected)
    assert summary["rule_assessments"][0]["undecided"] == 1
    assert all(item["code"] == "rule.violated" for item in summary["diagnostics"])


@pytest.mark.parametrize("suffix", ["Packet.__args__ = ()\n", "unknown(Packet)\n"])
def test_imported_alias_escape_cannot_reuse_the_source_proof(tmp_path: Path, suffix: str) -> None:
    _fixture(
        tmp_path,
        alias_module=True,
        alias_suffix=suffix,
        change={"alias_body": {**_BINDING, "origin": "sample.app.moved:Packet"}},
    )
    result = _observe(tmp_path)
    assert result.observation is not None
    assert _facts(result.observation) == []
    assert _targets(result.observation) or _unknowns(result.observation)


@pytest.mark.parametrize("name", ["Packet", "Metadata"])
def test_reexported_alias_or_metadata_cannot_lend_direct_body_proof(
    tmp_path: Path, name: str
) -> None:
    if name == "Packet":
        _fixture(
            tmp_path,
            alias_module=True,
            change={"alias_body": {**_BINDING, "origin": "sample.app.moved:Packet"}},
        )
        old = "from .moved import Packet"
        source = "from .moved import Packet\n"
    else:
        _fixture(tmp_path)
        old = "from .types import Metadata"
        source = "from .types import Metadata\n"
    (tmp_path / "sample/app/proxy.py").write_text(source)
    path = tmp_path / "sample/app/impl.py"
    path.write_text(path.read_text().replace(old, f"from .proxy import {name}"))
    result = _observe(tmp_path)
    assert result.observation is not None
    assert _facts(result.observation) == []
    assert _targets(result.observation) or _unknowns(result.observation)


def test_applied_proof_links_source_imports_declarations_and_signature(tmp_path: Path) -> None:
    _fixture(
        tmp_path,
        alias_module=True,
        change={"alias_body": {**_BINDING, "origin": "sample.app.moved:Packet"}},
    )
    result = _observe(tmp_path)
    assert result.observation is not None
    imports = {item.id: item for item in result.observation.records("imports") or ()}
    evidence = {item.id: item for item in result.observation.evidence}
    for fact in _facts(result.observation):
        assert {imports[item].data.get("binding") for item in fact.fact_ids if item in imports} == {
            "Packet",
            "Metadata",
        }
        assert {evidence[item].file for item in fact.evidence_ids} == {
            "sample/app/impl.py",
            "sample/app/moved.py",
            "sample/app/types.py",
        }
        assert fact.data.get("source") == "sample.app"
        assert fact.data.get("module") == "sample.app.impl"


@pytest.mark.parametrize("selected", [(0,), (1,), (2,), (3,), (0, 1, 2, 3)])
@pytest.mark.parametrize("mutation", _MUTATIONS)
def test_ordinary_validate_cli_source_mutation_matches_no_permission_control(
    tmp_path: Path, selected: tuple[int, ...], mutation
) -> None:
    _fixture(tmp_path, facade=True, selected=selected, **mutation)
    _commit_report_fixture(tmp_path)
    bound = _cli(tmp_path, "validate", tmp_path / "unused.json")
    contract_path = tmp_path / "contract.json"
    contract = json.loads(contract_path.read_text())
    contract["rules"][0]["allowed_positions"] = []
    contract_path.write_text(json.dumps(contract))
    control = _cli(tmp_path, "validate", tmp_path / "unused.json")
    star_import = mutation == {"prefix": "from missing import *\n"}
    assert bound.returncode == control.returncode == (0 if star_import else 2)
    actual, expected = json.loads(bound.stdout), json.loads(control.stdout)
    for key in (
        "declared_rules",
        "observation_complete",
        "rule_assessments",
        "diagnostics",
        "measurements",
    ):
        assert actual[key] == expected[key], (key, actual[key], expected[key])
    assert actual["observation_complete"] == "PASS"
    assert actual["declared_rules"] == ("UNKNOWN" if star_import else "FAIL")
    if star_import:
        assert actual["rule_assessments"][0]["count"] == 0
        assert actual["rule_assessments"][0]["undecided"] == 8
        result = _observe(tmp_path)
        assert result.observation is not None and _facts(result.observation) == []
        assert {
            (item.data.get("qualified_name"), item.data.get("position"), item.data.get("reason"))
            for item in _unknowns(result.observation)
        } == {
            (f"sample.app.Session.{method}", position, "ambiguous_facade")
            for method, position in (
                ("prepare", "return"),
                ("dispatch", "packet"),
                ("dispatch", "return"),
                ("unrelated", "counts"),
                ("unrelated", "return"),
                ("undecided", "value"),
                ("undecided", "return"),
            )
        }
