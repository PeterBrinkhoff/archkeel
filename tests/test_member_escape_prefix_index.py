"""Preserve dotted import-escape decisions without rescanning every escape per import."""

from pathlib import Path

import pytest

from archkeel.analyzer.python.imports import _propagate_member_escapes, collect_imports
from archkeel.analyzer.python.source import parse_sources, stable_direct_module_bindings
from archkeel.ir.facts import in_scope
from archkeel.ir.reexports import resolve_reexports


def _imports(tmp_path: Path, statement: str):
    package = tmp_path / "sample"
    package.mkdir()
    (package / "user.py").write_text(statement)
    (package / "owner.py").write_text("class User: pass\n")
    parsed = parse_sources(
        tuple(sorted(package.glob("*.py"))), root=tmp_path, namespace="sample"
    ).modules
    modules = {module.module: module for module in parsed}
    imports = collect_imports(parsed, set(modules), {}, namespace="sample")
    resolve_reexports(
        imports,
        {module.module: module.all_exports for module in parsed},
        {module.module: stable_direct_module_bindings(module) for module in parsed},
    )
    return imports, modules


@pytest.mark.parametrize("namespace", [False, True])
@pytest.mark.parametrize(
    "escaped",
    [
        set(),
        {"sample"},
        {"sample.owner"},
        {"sample.owner.User"},
        {"sample.owner.User.field"},
        {"sample.ownerish.User"},
        {"sample.owner.Userish"},
        {"sample.owners"},
    ],
)
def test_escape_matches_canonical_dotted_scope(tmp_path, namespace, escaped):
    statement = (
        "import sample.owner as Visible\n"
        if namespace
        else "from sample.owner import User as Visible\n"
    )
    imports, modules = _imports(tmp_path, statement)
    origin = "sample.owner" if namespace else "sample.owner.User"
    expected = any(
        in_scope(origin, name) or (namespace and in_scope(name, origin)) for name in escaped
    )
    incoming = {name: set() for name in modules}
    _propagate_member_escapes(
        imports,
        modules,
        {"sample.owner": {"User"}},
        escaped,
        {name: set() for name in modules},
        incoming_escapes=incoming,
    )
    assert ("Visible" in incoming["sample.user"]) is expected


def test_ambiguous_origin_candidates_keep_escape_evidence(tmp_path):
    imports, modules = _imports(tmp_path, "from sample.owner import User as Visible\n")
    imports[0]["data"]["origin_definition"] = None
    imports[0]["data"]["reexport_candidates"] = ["sample.owner.User", "other.User"]
    incoming = {name: set() for name in modules}
    _propagate_member_escapes(
        imports,
        modules,
        {},
        {"sample.owner"},
        {name: set() for name in modules},
        incoming_escapes=incoming,
    )
    assert incoming["sample.user"] == {"Visible"}


def test_new_escape_origins_are_visible_on_the_next_pass(tmp_path):
    imports, modules = _imports(tmp_path, "from sample.owner import User as Visible\n")
    incoming = {name: set() for name in modules}
    escaped = set()
    _propagate_member_escapes(imports, modules, {}, escaped, incoming, incoming_escapes=incoming)
    assert incoming["sample.user"] == set()
    escaped.add("sample.owner.User")
    _propagate_member_escapes(imports, modules, {}, escaped, incoming, incoming_escapes=incoming)
    assert incoming["sample.user"] == {"Visible"}


def test_escaped_origins_are_not_rescanned_for_every_import(tmp_path):
    class CountedOrigins(set):
        visited = 0

        def __iter__(self):
            for origin in super().__iter__():
                self.visited += 1
                yield origin

    size = 128
    imports, modules = _imports(
        tmp_path, "".join(f"from sample.owner import User as value{i}\n" for i in range(size))
    )
    origins = CountedOrigins(f"unrelated.module{i}.Value" for i in range(size))
    incoming = {name: set() for name in modules}
    _propagate_member_escapes(
        imports, modules, {}, origins, {name: set() for name in modules}, incoming_escapes=incoming
    )
    assert incoming["sample.user"] == set()
    assert origins.visited <= 4 * (len(imports) + len(origins))


def test_cyclic_imports_keep_incoming_bindings_live_within_a_pass(tmp_path):
    package = tmp_path / "sample"
    package.mkdir()
    (package / "user.py").write_text("from sample.owner import User as Visible\n")
    (package / "owner.py").write_text("class User: pass\nfrom sample.user import Visible as Back\n")
    parsed = parse_sources(
        tuple(sorted(package.glob("*.py"))), root=tmp_path, namespace="sample"
    ).modules
    modules = {module.module: module for module in parsed}
    imports = collect_imports(parsed, set(modules), {}, namespace="sample")
    imports.sort(key=lambda item: item["data"]["source_module"] == "sample.owner")
    for item in imports:
        data = item["data"]
        data["origin_definition"] = f"{data['target_module']}.{data['symbol']}"
    incoming = {"sample.owner": {"User"}, "sample.user": set()}
    _propagate_member_escapes(imports, modules, {}, set(), incoming, incoming_escapes=incoming)
    assert incoming == {"sample.owner": {"User", "Back"}, "sample.user": {"Visible"}}
