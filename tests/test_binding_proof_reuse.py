# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
import ast
from unittest.mock import patch

import pytest
from test_analyzer import _parsed_module

from archkeel.analyzer.python import source
from archkeel.analyzer.python.source import (
    AliasBinding,
    stable_direct_module_bindings,
    unique_direct_module_bindings,
    unproven_member_bindings,
)


def test_unique_proof_does_not_repeat_ast_walks() -> None:
    with patch.object(ast, "iter_fields", wraps=ast.iter_fields) as visits:
        module = _parsed_module("class Api: pass\nclass Other: pass\n")
        assert unique_direct_module_bindings(module) == frozenset({"Api", "Other"})
        first_visits = visits.call_count
        assert unique_direct_module_bindings(module) == frozenset({"Api", "Other"})
        assert visits.call_count == first_visits


def test_stable_proof_does_not_repeat_namespace_scans() -> None:
    module = _parsed_module("class Api: pass\nclass Other: pass\nalias = Api\n")
    with patch.object(
        source, "exposes_dynamic_namespace", wraps=source.exposes_dynamic_namespace
    ) as visits:
        assert stable_direct_module_bindings(module) == frozenset({"Api", "Other", "alias"})
        first_visits = visits.call_count
        assert first_visits > 0
        assert stable_direct_module_bindings(module) == frozenset({"Api", "Other", "alias"})
        assert visits.call_count == first_visits


def test_alias_changes_invalidate_even_an_empty_stable_proof() -> None:
    module = _parsed_module("from builtins import exec as run\nclass C: pass\nrun('x')\n")
    original = frozenset({"C", "run"})
    assert stable_direct_module_bindings(module) == original
    module.aliases["run"] = AliasBinding("builtins.exec", "symbol", "exec")
    assert stable_direct_module_bindings(module) == frozenset()
    assert stable_direct_module_bindings(module) == frozenset()
    module.aliases["run"] = AliasBinding("safe.run", "symbol", "run")
    assert stable_direct_module_bindings(module) == original
    del module.aliases["run"]
    assert stable_direct_module_bindings(module) == original


def test_alias_kind_change_invalidates_import_origin_proof() -> None:
    module = _parsed_module(
        "import pkg as route\nfrom pkg import X as second\nroute.attr = 1\nclass C: pass\n"
    )
    assert "second" in stable_direct_module_bindings(module)
    module.aliases.update(
        route=AliasBinding("pkg", "module"), second=AliasBinding("pkg.X", "symbol", "X")
    )
    assert "second" not in stable_direct_module_bindings(module)
    module.aliases["second"] = AliasBinding("pkg.X", "module", "X")
    assert "second" in stable_direct_module_bindings(module)


def test_incoming_member_proofs_remain_live() -> None:
    module = _parsed_module("class C: pass\n")
    assert stable_direct_module_bindings(module) == frozenset({"C"})
    assert unproven_member_bindings(module) == frozenset()
    module.incoming_member_escapes.add("C")
    assert stable_direct_module_bindings(module) == frozenset({"C"})
    assert unproven_member_bindings(module) == frozenset({"C"})


def test_same_path_snapshots_have_separate_proofs() -> None:
    original = _parsed_module("class C: pass\n")
    changed = _parsed_module("class C: pass\nclass C: pass\n")
    assert original.path == changed.path
    for module, expected in (
        (original, frozenset({"C"})),
        (changed, frozenset()),
        (original, frozenset({"C"})),
    ):
        assert unique_direct_module_bindings(module) == expected
        assert stable_direct_module_bindings(module) == expected


@pytest.mark.parametrize(
    "expression", ["vars()", "vars(C)", "vars", "locals()", "locals(C)", "exec(C)", "eval(C)"]
)
def test_namespace_access_remains_unproven(expression: str) -> None:
    module = _parsed_module("class C: pass\n" + expression + "\n")
    assert stable_direct_module_bindings(module) == frozenset()
    assert stable_direct_module_bindings(module) == frozenset()


def test_absent_global_does_not_rescan_class_bodies() -> None:
    module = _parsed_module("class Service:\n class Nested:\n  staticmethod = 1\n")
    with patch.object(ast, "walk", wraps=ast.walk) as walks:
        for _ in range(3):
            assert not source.binding_may_exist_before(
                module, module.tree.body, None, "staticmethod"
            )
        assert walks.call_count == 0


def test_global_elsewhere_does_not_bind_inside_a_different_class() -> None:
    module = _parsed_module(
        "class First:\n global property\n property = None\nclass Second: pass\n"
    )
    second = module.tree.body[1]
    assert isinstance(second, ast.ClassDef)
    assert not source.binding_may_exist_before(module, second.body, None, "property")
    assert source.binding_may_exist_before(module, module.tree.body, second, "property")


def test_absent_binding_does_not_repeat_statement_scans() -> None:
    module = _parsed_module("def service(value=factory('x')): pass\n")
    with patch.object(ast, "iter_child_nodes", wraps=ast.iter_child_nodes) as visits:
        for _ in range(3):
            assert not source.binding_may_exist_before(
                module, module.tree.body, None, "staticmethod"
            )
        assert visits.call_count == 0


def test_wildcard_import_retains_arbitrary_binding_uncertainty() -> None:
    module = _parsed_module("from unknown import *\n")
    assert source.binding_may_exist_before(module, module.tree.body, None, "staticmethod")


@pytest.mark.parametrize(
    "declaration",
    [
        "del property",
        "property: object",
        "import unknown as property",
        "from unknown import value as property",
        "class property: pass",
        "def property(): pass",
        "async def property(): pass",
        "try:\n pass\nexcept Exception as property:\n pass",
        'match value:\n case {"x": property}: pass',
        "match value:\n case [*property]: pass",
        "match value:\n case {**property}: pass",
        "class First:\n global property",
        "def service(value=(property := 1)): pass",
    ],
)
def test_binding_index_preserves_every_binding_form(declaration: str) -> None:
    module = _parsed_module(declaration + "\n")
    assert source.binding_may_exist_before(module, module.tree.body, None, "property")


_MAP_UNION = "dict[str, float] | dict[tuple[int, int], float] | dict[SexKey, float]"


def _map_union_project(
    *,
    local: bool = False,
    extra: str = "",
    provider_extra: str = "",
    annotation: str = _MAP_UNION,
    body: str = _MAP_UNION,
    prefix: str = "",
    other_importer: str = "",
    provider_source: str = "SexKey = str | None\n",
    importer_source: str = "from .types import SexKey\n",
):
    from archkeel.analyzer.python.imports import collect_imports, resolve_reexports
    from archkeel.analyzer.python.symbols import collect_symbols

    modules = [
        _parsed_module(
            provider_source + provider_extra, "sample.types", rel_path="sample/types.py"
        ),
        _parsed_module(
            ("SexKey = str | None\n" if local else importer_source)
            + prefix
            + f"GroupMask = {body}\n"
            + f"class Session:\n    def prepare(self) -> {annotation}: pass\n"
            + extra,
            "sample.impl",
            rel_path="sample/impl.py",
        ),
    ]
    if other_importer:
        modules.append(_parsed_module(other_importer, "sample.other", rel_path="sample/other.py"))
    evidence = {}
    imports = collect_imports(
        modules, {module.module for module in modules}, evidence, namespace="sample"
    )
    resolve_reexports(imports, {module.module: module.all_exports for module in modules}, modules)
    symbols, _, _ = collect_symbols(modules, evidence)
    return modules, imports, symbols


@pytest.mark.parametrize("local", [False, True])
@pytest.mark.parametrize("named", [False, True])
def test_map_union_proves_both_annotation_and_admitted_assignment(local: bool, named: bool) -> None:
    modules, imports, symbols = _map_union_project(
        local=local, annotation="GroupMask" if named else _MAP_UNION
    )
    for module in modules:
        assert "SexKey" not in unproven_member_bindings(module)
    keys = [item for item in symbols if item["data"].get("name") == "SexKey"]
    assert keys and all(item["data"].get("source_member_binding_static") is True for item in keys)
    key_imports = [item for item in imports if item["data"]["binding"] == "SexKey"]
    assert all(
        item["data"].get("source_member_binding_static") is True
        and item["data"].get("origin_member_binding_static") is True
        for item in key_imports
    )


@pytest.mark.parametrize(
    "change",
    [
        {"extra": "unknown(SexKey)\n"},
        {"extra": "SexKey.__args__ = ()\n"},
        {"extra": "unknown(GroupMask)\n"},
        {"provider_extra": "unknown(SexKey)\n"},
        {"extra": "from . import types\ntypes.SexKey = object\n"},
        {"other_importer": "from .types import SexKey\nunknown(SexKey)\n"},
    ],
)
def test_map_union_cannot_absolve_a_separate_escape(change) -> None:
    modules, imports, symbols = _map_union_project(**change)
    assert "SexKey" in unproven_member_bindings(modules[0])
    assert "SexKey" in unproven_member_bindings(modules[1])
    assert all(
        item["data"].get("source_member_binding_static") is False
        for item in symbols
        if item["data"].get("name") == "SexKey"
    )
    assert all(
        item["data"].get("source_member_binding_static") is False
        for item in imports
        if item["data"]["binding"] == "SexKey"
    )


@pytest.mark.parametrize(
    "annotation",
    [
        "dict[SexKey, float] | Missing",
        "Missing | dict[SexKey, float]",
        "dict[str, int] | dict[SexKey, float] | Missing",
        "dict[SexKey, float] | factory()",
        "factory()[SexKey] | dict[str, float]",
        "Unknown[SexKey] | dict[str, float]",
        "dict[SexKey, Custom] | dict[str, float]",
        "dict[Custom, float] | dict[SexKey, float]",
        "dict[SexKey, float] | Custom",
        "Custom | dict[SexKey, float]",
    ],
)
def test_unsafe_union_operand_or_argument_keeps_alias_escaped(annotation: str) -> None:
    prefix = (
        "class Meta(type):\n"
        "    def __or__(self, other): return other\n"
        "    def __ror__(self, other): return other\n"
        "    def __eq__(self, other): return True\n"
        "class Custom(metaclass=Meta): pass\n"
    )
    modules, imports, _ = _map_union_project(annotation=annotation, body=annotation, prefix=prefix)
    assert "SexKey" in unproven_member_bindings(modules[0])
    assert "SexKey" in unproven_member_bindings(modules[1])
    assert all(
        item["data"].get("source_member_binding_static") is False
        for item in imports
        if item["data"]["binding"] == "SexKey"
    )


def test_fresh_map_union_snapshot_does_not_inherit_an_old_proof() -> None:
    safe, _, _ = _map_union_project()
    unsafe, _, _ = _map_union_project(provider_extra="unknown(SexKey)\n")
    assert safe[1].path == unsafe[1].path
    assert "SexKey" not in unproven_member_bindings(safe[1])
    assert "SexKey" in unproven_member_bindings(unsafe[1])
    assert "SexKey" not in unproven_member_bindings(safe[1])


def test_rerunning_import_origins_replaces_the_map_union_proof() -> None:
    from archkeel.analyzer.python.imports import resolve_reexports

    modules, imports, _ = _map_union_project()
    assert "SexKey" not in unproven_member_bindings(modules[1])
    imported = next(item for item in imports if item["data"]["binding"] == "SexKey")
    imported["data"]["target_module"] = "sample.missing"
    modules[1].aliases["SexKey"] = AliasBinding("sample.missing.SexKey", "symbol", "SexKey")
    resolve_reexports(imports, {module.module: module.all_exports for module in modules}, modules)
    assert "SexKey" in unproven_member_bindings(modules[1])


@pytest.mark.parametrize(
    "change",
    [
        {"provider_source": "class str: pass\nSexKey = str | None\n"},
        {"provider_source": "SexKey = None | str\n"},
        {"provider_source": "Key = str | None\nSexKey = Key\n"},
        {"provider_source": "SexKey = str | None\nSexKey = str | None\n"},
        {"provider_source": "if flag:\n    SexKey = str | None\n"},
        {"provider_source": "from opaque import *\nSexKey = str | None\n"},
        {"provider_source": "SexKey = str | None\nunknown(globals())\n"},
        {"provider_source": "from .provider import SexKey\n"},
        {"importer_source": "from .missing import SexKey\n"},
        {"importer_source": "if flag:\n    from .types import SexKey\n"},
        {"importer_source": "from .types import SexKey\nfrom .types import SexKey\n"},
        {"importer_source": "from .types import *\n"},
        {
            "importer_source": (
                "from typing import TYPE_CHECKING\n"
                "if TYPE_CHECKING:\n    from .types import SexKey\n"
            )
        },
    ],
)
def test_map_union_requires_an_intrinsic_direct_provider(change) -> None:
    modules, imports, _ = _map_union_project(**change)
    assert not modules[1]._proven_map_union_expressions
    assert "SexKey" in unproven_member_bindings(modules[1])
    assert all(
        item["data"].get("source_member_binding_static") is False
        for item in imports
        if item["data"]["binding"] == "SexKey"
    )


def test_local_map_union_protection_revokes_without_an_import_edge() -> None:
    modules, _, _ = _map_union_project(local=True, extra="unknown(SexKey)\n")
    assert not modules[1]._proven_map_union_expressions
    assert "SexKey" in unproven_member_bindings(modules[1])
