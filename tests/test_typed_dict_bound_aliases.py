# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Literal TypedDict headers prove identity without proving member closure."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from test_analyzer import _observe
from test_boundary_type_bound_aliases import _cli, _facts, _fixture, _targets, _unknowns
from test_boundary_types_contained_mapping import _commit_report_fixture

from archkeel.ir.codec import (
    canonical_report_bytes,
    decode_canonical_model,
    observation_payload,
    parse_observation,
)

_CE_METADATA = (
    "from typing import TypedDict\n\n"
    "class ExportMetadata(TypedDict, total=False):\n"
    "    target_entity: str\n    selector: str\n    type: str\n"
)


def _ce_fixture(root: Path, *, facade=False, selected=(0, 1, 2, 3), metadata=_CE_METADATA):
    _fixture(root, facade=facade, selected=selected, metadata=metadata)
    for relative in ("sample/app/impl.py", "sample/app/moved.py", "contract.json"):
        path = root / relative
        path.write_text(path.read_text().replace("Metadata", "ExportMetadata"))


@pytest.mark.parametrize("facade", [False, True], ids=["direct", "facade"])
@pytest.mark.parametrize("selected", [(), (0,), (1,), (2,), (3,), (0, 1, 2, 3)])
def test_ce_total_false_keeps_unrelated_failures_and_grants_only_selected(
    tmp_path: Path, facade, selected
):
    _ce_fixture(tmp_path, facade=facade, selected=())
    before = _observe(tmp_path).observation
    assert before is not None and len(_targets(before)) == 4
    unrelated = [r for r in before.records("violations") if r not in _targets(before)]
    _ce_fixture(tmp_path, facade=facade, selected=selected)
    _commit_report_fixture(tmp_path)
    output = tmp_path / "architecture.json"
    report = _cli(tmp_path, "report", output)
    assert report.returncode == 0, (report.stdout, report.stderr)
    observation = parse_observation(decode_canonical_model(json.loads(output.read_text())))
    assert canonical_report_bytes(observation) == output.read_bytes()
    assert len(_facts(observation)) == len(selected)
    assert len(_targets(observation)) == 4 - len(selected)
    assert [
        r for r in observation.records("violations") if r not in _targets(observation)
    ] == unrelated
    assert _unknowns(observation) == _unknowns(before)
    validate = _cli(tmp_path, "validate", output)
    assert validate.returncode == 2 and json.loads(validate.stdout)["declared_rules"] == "FAIL"
    for fact in _facts(observation):
        data = fact.data
        assert data.get("observed_container_depth") == (3 if data.get("accepted_opacity") else 2)
        assert ("container_depth" in dict(data.entries)) is bool(data.get("accepted_opacity"))
        imports = {r.id: r for r in observation.records("imports")}
        assert any(
            imports[i].data.get("origin_definition") == "typing.TypedDict"
            for i in fact.fact_ids
            if i in imports
        )
        provider = next(
            imports[i]
            for i in fact.fact_ids
            if i in imports and imports[i].data.get("origin_definition") == "typing.TypedDict"
        )
        assert set(provider.evidence_ids) <= set(fact.evidence_ids)
        symbols = {r.id: r for r in observation.records("symbols")}
        source = [symbols[i] for i in fact.fact_ids if i in symbols]
        assert {r.kind for r in source} >= {"class", "type_alias", "method"}
        assert any(r.data.get("name") == "ExportMetadata" for r in source)
        assert all(set(r.evidence_ids) <= set(fact.evidence_ids) for r in source)
    metadata = next(
        r
        for r in observation.records("symbols")
        if r.data.get("qualified_name") == "sample.app.types.ExportMetadata"
    )
    assert metadata.data.get("typed_dict_header_static") is True
    assert metadata.data.get("class_header_static") is False
    assert metadata.data.get("source_member_binding_static") is False


def _collect(root: Path):
    from archkeel.analyzer.python.collect import collect
    from archkeel.ir.protocol import CollectionRequest, PythonSettings, SnapshotInput, SourceScope

    return collect(
        CollectionRequest(
            SnapshotInput(str(root), "a" * 40, False),
            SourceScope((".",), "sample"),
            PythonSettings(),
        )
    )


@pytest.mark.parametrize(
    "header",
    [
        "from typing import TypedDict\nclass ExportMetadata(TypedDict, total=True):",
        "from typing import TypedDict as TD\nclass ExportMetadata(TD, total=False):",
        "import typing as t\nclass ExportMetadata(t.TypedDict, total=False):",
        "from typing_extensions import TypedDict\n"
        "class ExportMetadata(\n    TypedDict,\n    total=False,\n):",
        "import typing_extensions\nclass ExportMetadata(typing_extensions.TypedDict, total=True):",
    ],
)
def test_literal_standard_headers_emit_source_proof_and_keep_partial_inventory(
    tmp_path: Path, header
):
    _ce_fixture(
        tmp_path, metadata=header + "\n    target_entity: str\n    selector: str\n    type: str\n"
    )
    facts = _collect(tmp_path)
    metadata = next(
        r
        for s in facts.sections
        if s.name == "symbols"
        for r in s.records
        if r.data.get("qualified_name") == "sample.app.types.ExportMetadata"
    )
    assert metadata.data.get("typed_dict_header_static") is True
    assert metadata.data.get("class_header_static") is False
    assert metadata.data.get("source_member_binding_static") is False
    inventories = metadata.data.get("member_inventories")
    assert inventories and all(i.get("status") == "partial" for i in inventories)
    observation = _observe(tmp_path).observation
    assert observation is not None and len(_facts(observation)) == 4


_HEADER_NEGATIVES = [
    ("class ExportMetadata(TypedDict, total=unknown):", ""),
    ("class ExportMetadata(TypedDict, total=unknown()):", ""),
    ("class ExportMetadata(TypedDict, total=0):", ""),
    ('class ExportMetadata(TypedDict, total="False"):', ""),
    ("class ExportMetadata(TypedDict, metaclass=unknown):", ""),
    ("class ExportMetadata(TypedDict, total=False, metaclass=unknown):", ""),
    ("class ExportMetadata(TypedDict, total=False, closed=True):", ""),
    ("class ExportMetadata(TypedDict, total=False, total=True):", ""),
    ("class ExportMetadata(TypedDict, **options):", ""),
    ("class ExportMetadata(TypedDict, total=False, **options):", ""),
    ("@unknown\nclass ExportMetadata(TypedDict, total=False):", ""),
    ("class ExportMetadata(TypedDict, object, total=False):", ""),
    ("class ExportMetadata(TypedDict[int], total=False):", ""),
    ("if unknown:\n    class ExportMetadata(TypedDict, total=False):", "conditional"),
    ("class ExportMetadata(TypedDict, total=False):", "duplicate-class"),
    ("class ExportMetadata(TypedDict, total=False):", "duplicate-import"),
    ("class ExportMetadata(TypedDict, total=False):", "before-shadow"),
    ("class ExportMetadata(TypedDict, total=False):", "after-shadow"),
    ("class ExportMetadata(TypedDict, total=False):", "after-import"),
    ("class ExportMetadata(TypedDict, total=False):", "star"),
    ("class ExportMetadata(TypedDict, total=False):", "conditional-import"),
    ("class ExportMetadata(TypedDict, total=False):", "reexport"),
    ("class ExportMetadata(TypedDict, total=False):", "provider-write"),
    ("class ExportMetadata(TypedDict, total=False):", "provider-call"),
    ("class ExportMetadata(TypedDict, total=False):", "cross-provider-write"),
    ("class ExportMetadata(TypedDict, total=False):", "cross-provider-call"),
    ("class ExportMetadata(TypedDict, total=False):", "cross-star"),
]


@pytest.mark.parametrize("header,mutation", _HEADER_NEGATIVES)
def test_unproven_header_or_provider_never_emits_proof_or_permission(
    tmp_path: Path, header, mutation
):
    prefix = "from typing import TypedDict\n"
    suffix = ""
    if mutation == "before-shadow":
        prefix += "TypedDict = unknown\n"
    if mutation == "after-shadow":
        suffix += "TypedDict = unknown\n"
    if mutation == "duplicate-import":
        prefix *= 2
    if mutation == "after-import":
        prefix, suffix = "", prefix
    if mutation == "star":
        prefix += "from unknown import *\n"
    if mutation == "conditional-import":
        prefix = "if unknown:\n    from typing import TypedDict\n"
    if mutation == "reexport":
        prefix = "from .provider import TypedDict\n"
    if mutation == "provider-write":
        prefix += "import typing\ntyping.TypedDict = unknown\n"
    if mutation == "provider-call":
        prefix += "import typing\nunknown(typing)\n"
    fields = (
        "        target_entity: str\n" if mutation == "conditional" else "    target_entity: str\n"
    )
    if mutation == "duplicate-class":
        suffix += header + "\n" + fields
    _ce_fixture(tmp_path, metadata=prefix + header + "\n" + fields + suffix)
    if mutation == "reexport":
        (tmp_path / "sample/app/provider.py").write_text("from typing import TypedDict\n")
    if mutation == "cross-provider-write":
        (tmp_path / "sample/app/evil.py").write_text("import typing\ntyping.TypedDict = unknown\n")
    if mutation == "cross-provider-call":
        (tmp_path / "sample/app/evil.py").write_text(
            "from typing import TypedDict as TD\nunknown(TD)\n"
        )
    if mutation == "cross-star":
        (tmp_path / "sample/app/evil.py").write_text(
            "from typing import *\nTypedDict.__call__ = unknown\n"
        )
    facts = _collect(tmp_path)
    assert not any(
        r.data.get("typed_dict_header_static") is True for s in facts.sections for r in s.records
    )
    result = _observe(tmp_path)
    assert result.observation is not None and _facts(result.observation) == []
    assert _targets(result.observation) or _unknowns(result.observation)


@pytest.mark.parametrize("flag", [None, False])
def test_missing_or_false_source_flag_cannot_grant_keyword_header(tmp_path: Path, flag):
    from archkeel.analyzer.python.type_shapes import collect_type_shapes
    from archkeel.check.evaluation.boundary_types import (
        _boundary_type_verdict,
        boundary_type_indexes,
    )
    from archkeel.ir.codec import parse_contract

    _ce_fixture(tmp_path)
    observation = _observe(tmp_path).observation
    assert observation is not None
    raw = observation_payload(observation)
    metadata = next(
        r
        for r in raw["symbols"]
        if r["data"].get("qualified_name") == "sample.app.types.ExportMetadata"
    )
    metadata["data"].pop("typed_dict_header_static")
    if flag is not None:
        metadata["data"]["typed_dict_header_static"] = flag
    bindings, classes = boundary_type_indexes(raw["symbols"], raw["imports"])
    body = (
        "tuple[tuple[str, list[object]] | tuple[str, list[object], ExportMetadata], "
        "list[dict[str, object]]]"
    )
    verdict = _boundary_type_verdict(
        "Packet",
        "sample.app.impl",
        parse_contract(json.loads((tmp_path / "contract.json").read_text())),
        {},
        bindings,
        classes,
        type_shapes=collect_type_shapes(["Packet", body, "str"]),
    )
    assert verdict.bound_alias is None


@pytest.mark.parametrize("flag", [0, 1, "true", None, [], {}])
def test_source_protocol_rejects_nonboolean_header_proof(tmp_path: Path, flag):
    from archkeel.ir.facts_codec import ProtocolError, decode_response, encode_response
    from archkeel.ir.protocol import CollectionResponse

    _ce_fixture(tmp_path)
    raw = json.loads(encode_response(CollectionResponse(_collect(tmp_path))))
    metadata = next(
        r
        for s in raw["facts"]["sections"]
        if s["name"] == "symbols"
        for r in s["records"]
        if r["data"].get("qualified_name") == "sample.app.types.ExportMetadata"
    )
    metadata["data"]["typed_dict_header_static"] = flag
    with pytest.raises(ProtocolError, match="boolean"):
        decode_response(json.dumps(raw).encode())


@pytest.mark.parametrize("opaque", ["object", "Missing"])
def test_typed_dict_member_findings_remain_after_grants(tmp_path: Path, opaque):
    metadata = _CE_METADATA + f"    opaque: {opaque}\n"
    _ce_fixture(tmp_path, selected=(), metadata=metadata)
    before = _observe(tmp_path).observation
    _ce_fixture(tmp_path, metadata=metadata)
    after = _observe(tmp_path).observation
    assert before is not None and after is not None
    assert len(_facts(after)) == 4
    assert _unknowns(after) == _unknowns(before)
    assert _targets(after) == [r for r in _targets(before) if r.data.get("path")]
    assert _targets(after) if opaque == "object" else _unknowns(after)


def test_unrelated_local_call_does_not_invalidate_typed_dict_provider(tmp_path: Path):
    _ce_fixture(tmp_path)
    (tmp_path / "sample/app/helper.py").write_text("def identity(value): return value\n")
    (tmp_path / "sample/app/caller.py").write_text("from .helper import identity\nidentity(1)\n")
    observation = _observe(tmp_path).observation
    assert observation is not None and len(_facts(observation)) == 4


@pytest.mark.parametrize("route", ["symbol", "module", "qualified", "metadata", "local-metadata"])
def test_unresolved_runtime_routes_do_not_claim_future_provider_closure(tmp_path: Path, route):
    _ce_fixture(tmp_path)
    (tmp_path / "sample/app/provider.py").write_text(
        "from typing import TypedDict\nimport typing as provider\n"
    )
    attacks = {
        "symbol": "from .provider import TypedDict\nunknown(TypedDict)\n",
        "module": "from .provider import provider\nprovider.TypedDict = unknown\n",
        "qualified": "from . import provider\nprovider.TypedDict.__call__ = unknown\n",
        "metadata": "from .types import ExportMetadata\nunknown(ExportMetadata)\n",
    }
    if route == "local-metadata":
        path = tmp_path / "sample/app/types.py"
        path.write_text(path.read_text() + "unknown(ExportMetadata)\n")
    else:
        (tmp_path / "sample/app/evil.py").write_text(attacks[route])
    observation = _observe(tmp_path).observation
    assert observation is not None and len(_facts(observation)) == 4
    metadata = next(
        r
        for r in observation.records("symbols")
        if r.data.get("qualified_name") == "sample.app.types.ExportMetadata"
    )
    assert metadata.data.get("typed_dict_header_static") is True
    assert metadata.data.get("source_member_binding_static") is False
    assert _unknowns(observation)


@pytest.mark.parametrize("provider", ["typing", "typing_extensions"])
def test_proven_reexport_provider_escape_rejects_source_proof(tmp_path: Path, provider):
    _ce_fixture(tmp_path, metadata=_CE_METADATA.replace("typing", provider))
    (tmp_path / "sample/app/provider.py").write_text(
        f"from {provider} import TypedDict\n__all__ = ['TypedDict']\n"
    )
    (tmp_path / "sample/app/evil.py").write_text(
        "from .provider import TypedDict\nunknown(TypedDict)\n"
    )
    facts = _collect(tmp_path)
    assert not any(
        r.data.get("typed_dict_header_static") is True for s in facts.sections for r in s.records
    )
    observation = _observe(tmp_path).observation
    assert observation is not None and _facts(observation) == []


def test_other_typing_symbols_do_not_prove_header_factory_escape(tmp_path: Path):
    _ce_fixture(tmp_path)
    (tmp_path / "sample/app/annotations.py").write_text(
        "from typing import Annotated, Literal, SupportsInt, SupportsIndex\n"
        "Intent = Annotated[int, unknown()]\n"
        "Kind = Literal['one', 'two']\n"
        "isinstance(value, str | SupportsInt | SupportsIndex)\n"
    )
    observation = _observe(tmp_path).observation
    assert observation is not None and len(_facts(observation)) == 4
    assert _unknowns(observation)
