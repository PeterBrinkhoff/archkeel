# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Native comparison observations cover protocol literals without inferring runtime values."""

import ast

import pytest
from test_analyzer import _observe_one_rule, _parsed_module

from archkeel.analyzer.python.constructs import (
    _LiteralComparisons,
    _literal_import_origins,
    collect_constructs,
)
from archkeel.analyzer.python.imports import collect_imports, resolve_reexports
from archkeel.ir.trace import trace_valid_violations

RULE = {
    "kind": "forbidden_construct",
    "source": "sample.core",
    "constructs": ["string_literal_compare"],
}

ENUM = 'from enum import Enum as ProtocolEnum\nclass Token(ProtocolEnum):\n    IMPORT = "import"\n'


@pytest.mark.parametrize(
    ("source", "form"),
    [
        ('def parse(value):\n    return value == "import"\n', "compare"),
        (
            'from typing import Final\nIMPORT: Final[str] = "import"\n'
            "def parse(value):\n    return value == IMPORT\n",
            "compare",
        ),
        (
            'TOKENS = ("import", "export")\ndef parse(value):\n    return value in TOKENS\n',
            "membership",
        ),
        (
            'TOKENS = {"import", "export"}\ndef parse(value):\n    return value in TOKENS\n',
            "membership",
        ),
        (
            'TOKENS = ["import", "export"]\ndef parse(value):\n    return value in TOKENS\n',
            "membership",
        ),
        (
            'TOKENS = ("import", "export")\ndef parse(value):\n    return value not in TOKENS\n',
            "membership",
        ),
        ('def parse(value):\n    return value == b"import"\n', "compare"),
        ('def parse(value):\n    return value in (b"import", b"export")\n', "membership"),
        (
            'def parse(value):\n    match value:\n        case b"import":\n'
            "            return True\n        case _:\n            return False\n",
            "match",
        ),
        (ENUM + "def parse(value):\n    return value == Token.IMPORT.value\n", "compare"),
        (
            ENUM + "def parse(value):\n    return value in (Token.IMPORT.value,)\n",
            "membership",
        ),
        (
            ENUM + "def parse(value):\n    match value:\n        case Token.IMPORT.value:\n"
            "            return True\n        case _:\n            return False\n",
            "match",
        ),
        ('if __name__ == "__main__":\n    pass\n', "compare"),
    ],
    ids=[
        "literal",
        "final",
        "named-tuple",
        "named-set",
        "named-list",
        "named-not-in",
        "bytes-equality",
        "bytes-membership",
        "bytes-match",
        "enum-value",
        "enum-value-membership",
        "enum-value-match",
        "entry-protocol",
    ],
)
def test_native_protocol_literal_comparison_has_trace_valid_failure(tmp_path, source, form):
    result = _observe_one_rule(tmp_path, RULE, {"core.py": source})
    assert result.diagnostics == () and result.observation is not None
    comparisons = [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert [row.data.get("form") for row in comparisons] == [form]
    violations = trace_valid_violations(result.observation)
    assert [(row.kind, row.rule_ids) for row in violations] == [("forbidden_construct", ("RULE",))]


@pytest.mark.parametrize(
    "source",
    [
        ENUM + "def parse(value):\n    return value is Token.IMPORT\n",
        "def parse(module: str, expected: str):\n    return module == expected\n",
        'TOKEN = "import"\ndef parse(value, TOKEN):\n    return value == TOKEN\n',
        'TOKEN = "import"\ndef parse(value):\n    TOKEN = value\n    return value == TOKEN\n',
        'TOKENS = ("import",)\ndef parse(value, TOKENS):\n    return value in TOKENS\n',
        'TOKENS = ("import",)\nTOKENS = read_tokens()\n'
        "def parse(value):\n    return value in TOKENS\n",
        'TOKENS = {"import"}\nTOKENS.add(read_token())\n'
        "def parse(value):\n    return value in TOKENS\n",
        'TOKENS = ["import"]\nother = TOKENS\nother.append(read_token())\n'
        "def parse(value):\n    return value in TOKENS\n",
        ENUM + "def parse(value, Token):\n    return value == Token.IMPORT.value\n",
        'class Other:\n    value = "import"\n'
        "def parse(value, Other):\n    return value == Other.value\n",
        'def parse(value):\n    match value:\n        case {"kind": _}:\n'
        "            return True\n        case _:\n            return False\n",
    ],
    ids=[
        "enum-identity",
        "name-data",
        "shadowed-scalar",
        "local-scalar",
        "shadowed-collection",
        "reassigned-collection",
        "mutated-set",
        "escaped-list",
        "shadowed-enum",
        "shadowed-class",
        "mapping-structure",
    ],
)
def test_native_controls_do_not_infer_literal_runtime_values(tmp_path, source):
    result = _observe_one_rule(tmp_path, RULE, {"core.py": source})
    assert result.diagnostics == () and result.observation is not None
    assert not [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert trace_valid_violations(result.observation) == ()


@pytest.mark.parametrize("expression", ["value == TOKEN", "TOKEN in value", "TOKEN not in value"])
def test_proven_imported_literal_constants_have_native_failure(tmp_path, expression):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {
            "core.py": "from sample.cli import TOKEN\n"
            f"def parse(value):\n    return {expression}\n",
            "cli.py": 'TOKEN = "import"\n',
        },
    )
    assert result.diagnostics == () and result.observation is not None
    assert (
        len(
            [
                row
                for row in result.observation.records("constructs")
                if row.kind == "string_literal_compare"
            ]
        )
        == 1
    )
    assert [(row.kind, row.rule_ids) for row in trace_valid_violations(result.observation)] == [
        ("forbidden_construct", ("RULE",))
    ]


def test_record_ids_are_distinct_and_collection_order_does_not_change_evidence():
    source = 'TOKENS = ("import",)\nvalue in TOKENS\nvalue == b"import"\n'
    parsed = _parsed_module(source)
    first = collect_constructs([parsed], {})
    second = collect_constructs([parsed], {})
    records = [row for row in first if row["kind"] == "string_literal_compare"]
    assert sorted(row["data"]["form"] for row in records) == ["compare", "membership"]
    assert len({row["id"] for row in records}) == 2
    assert first == second


@pytest.mark.parametrize(
    ("prefix", "base"),
    [
        ("class Enum:\n    pass\n", "Enum"),
        ("from enum import Enum as ProtocolEnum\nProtocolEnum = other_base\n", "ProtocolEnum"),
    ],
    ids=["unrelated-base", "rebound-import"],
)
def test_enum_value_requires_a_direct_stdlib_enum_base_import(tmp_path, prefix, base):
    source = (
        prefix + f'class Token({base}):\n    IMPORT = "import"\n'
        "def parse(value):\n    return value == Token.IMPORT.value\n"
    )
    result = _observe_one_rule(tmp_path, RULE, {"core.py": source})
    assert result.diagnostics == () and result.observation is not None
    assert not [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]


@pytest.mark.parametrize(
    "source",
    [
        'TOKENS = alias = ["import"]\nalias.clear()\n'
        "def parse(value):\n    return value in TOKENS\n",
        'holder.tokens = TOKENS = ["import"]\nholder.tokens.clear()\n'
        "def parse(value):\n    return value in TOKENS\n",
        'TOKENS = ("import",)\n'
        "def parse(value, expected):\n    return value in TOKENS == expected\n",
        'TOKENS = ("import",)\ndef parse(value, others):\n    return value in TOKENS in others\n',
    ],
    ids=[
        "chained-name-assignment",
        "chained-attribute-assignment",
        "equality-role",
        "membership-left-role",
    ],
)
def test_native_collection_alias_and_chained_roles_are_unclassified(tmp_path, source):
    result = _observe_one_rule(tmp_path, RULE, {"core.py": source})
    assert result.diagnostics == () and result.observation is not None
    assert not [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert trace_valid_violations(result.observation) == ()


@pytest.mark.parametrize(
    "source",
    [
        'def parse(path):\n    return "node_modules" in path.split("/")\n',
        'def parse(text):\n    return "import" not in text\n',
        'def parse(content):\n    return b"import" in content\n',
        'def parse(content):\n    return b"import" not in content\n',
        'NEEDLE = "import"\ndef parse(values):\n    return NEEDLE in values\n',
        'from typing import Final\nNEEDLE: Final[str] = "import"\n'
        "def parse(values):\n    return NEEDLE not in values\n",
        'NEEDLE = b"import"\ndef parse(values):\n    return NEEDLE in values\n',
        'class Words:\n    IMPORT = "import"\n'
        "def parse(values):\n    return Words.IMPORT in values\n",
        ENUM + "def parse(values):\n    return Token.IMPORT.value in values\n",
    ],
    ids=[
        "parser-literal-needle",
        "not-in-text",
        "bytes-needle",
        "not-in-bytes",
        "module-scalar",
        "final-scalar-not-in",
        "module-bytes",
        "class-scalar",
        "enum-value",
    ],
)
def test_native_literal_membership_needles_have_trace_valid_failures(tmp_path, source):
    result = _observe_one_rule(tmp_path, RULE, {"core.py": source})
    assert result.diagnostics == () and result.observation is not None
    comparisons = [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert [row.data.get("form") for row in comparisons] == ["membership"]
    assert [(row.kind, row.rule_ids) for row in trace_valid_violations(result.observation)] == [
        ("forbidden_construct", ("RULE",))
    ]


@pytest.mark.parametrize(
    "source",
    [
        ENUM + "def parse(values):\n    return Token.IMPORT in values\n",
        "def parse(needle: str, values: tuple[str, ...]):\n    return needle in values\n",
        'NEEDLE = "import"\ndef parse(NEEDLE, values):\n    return NEEDLE in values\n',
        'NEEDLE = "import"\ndef parse(values):\n'
        "    NEEDLE = read_word()\n    return NEEDLE in values\n",
        "NEEDLE = read_word()\ndef parse(values):\n    return NEEDLE in values\n",
    ],
    ids=["enum-needle", "data-needle", "shadowed-scalar-needle", "local-needle", "dynamic-needle"],
)
def test_native_typed_or_unproven_membership_needles_have_no_literal_claim(tmp_path, source):
    result = _observe_one_rule(tmp_path, RULE, {"core.py": source})
    assert result.diagnostics == () and result.observation is not None
    assert not [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert trace_valid_violations(result.observation) == ()


@pytest.mark.parametrize(
    "source",
    [
        "from enum import Enum\n"
        "class Mixin:\n    @property\n    def value(self):\n        return 7\n"
        'class Token(Mixin, Enum):\n    IMPORT = "import"\n',
        "from enum import Enum\nclass Token(Enum):\n"
        "    def __new__(cls, written):\n"
        "        obj = object.__new__(cls)\n        obj._value_ = len(written)\n"
        '        return obj\n    IMPORT = "import"\n',
        "from enum import Enum\nclass Token(Enum):\n"
        "    def __init__(self, written):\n        self._value_ = len(written)\n"
        '    IMPORT = "import"\n',
        "from enum import Enum\nclass Token(Enum):\n"
        "    def __getattribute__(self, name):\n"
        '        return {"value": 7}.get(name, object.__getattribute__(self, name))\n'
        '    IMPORT = "import"\n',
        "from enum import Enum\nclass Token(Enum):\n"
        "    def __setattr__(self, name, value):\n"
        '        object.__setattr__(self, name, {"_value_": 7}.get(name, value))\n'
        '    IMPORT = "import"\n',
        "from enum import Enum, EnumType\nclass ChangingEnumType(EnumType):\n"
        "    def __new__(cls, name, bases, namespace):\n"
        '        dict.__setitem__(namespace, "IMPORT", 7)\n'
        "        return super().__new__(cls, name, bases, namespace)\n"
        'class Token(Enum, metaclass=ChangingEnumType):\n    IMPORT = "import"\n',
        "from enum import Enum\ndef change(cls):\n"
        "    cls.IMPORT._value_ = 7\n    return cls\n"
        '@change\nclass Token(Enum):\n    IMPORT = "import"\n',
        'from enum import IntEnum\nclass Token(IntEnum):\n    IMPORT = "1"\n',
        "from enum import Enum\nclass Token(Enum):\n"
        "    @property\n    def value(self):\n        return 7\n"
        '    IMPORT = "import"\n',
        "from enum import Enum\nclass Token(Enum):\n"
        '    _ignore_ = "IMPORT"\n    IMPORT = "import"\n',
    ],
    ids=[
        "mixin-value",
        "custom-new",
        "custom-init",
        "custom-getattribute",
        "custom-setattr",
        "metaclass-keyword",
        "class-decorator",
        "intenum-conversion",
        "own-value",
        "namespace-ignore",
    ],
)
def test_native_custom_enum_does_not_establish_string_value(tmp_path, source):
    source += "def parse(values):\n    return Token.IMPORT.value in values\n"
    result = _observe_one_rule(tmp_path, RULE, {"core.py": source})
    assert result.diagnostics == () and result.observation is not None
    assert not [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert trace_valid_violations(result.observation) == ()


@pytest.mark.parametrize("base", ["Enum", "StrEnum"])
def test_native_simple_enum_retains_literal_value_evidence(tmp_path, base):
    source = (
        f"from enum import {base}\nclass Token({base}):\n"
        '    """Ordinary literal enum members."""\n    IMPORT = "import"\n'
        '    EXPORT = "export"\n'
        "def parse(values):\n    return Token.IMPORT.value in values\n"
    )
    result = _observe_one_rule(tmp_path, RULE, {"core.py": source})
    assert result.diagnostics == () and result.observation is not None
    assert [
        row.data.get("form")
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ] == ["membership"]
    assert [(row.kind, row.rule_ids) for row in trace_valid_violations(result.observation)] == [
        ("forbidden_construct", ("RULE",))
    ]


@pytest.mark.parametrize(
    ("prefix", "expression", "form"),
    [
        ("from sample.cli import Token\n", "value == Token.IMPORT.value", "compare"),
        ("from sample.cli import Token as Alias\n", "value != Alias.IMPORT.value", "compare"),
        ("import sample.cli as vocabulary\n", "value == vocabulary.Token.IMPORT.value", "compare"),
        ("from .cli import Token\n", "Token.IMPORT.value in value", "membership"),
        ("from sample.bridge import Token\n", "value == Token.IMPORT.value", "compare"),
        (
            "import sample.bridge as vocabulary\n",
            "value == vocabulary.Token.IMPORT.value",
            "compare",
        ),
        ("from sample.cli import Token\n", "value in (Token.IMPORT.value,)", "membership"),
        ("from sample.cli import Token\n", "value.startswith(Token.IMPORT.value)", "startswith"),
        ("from sample.cli import Token\n", "value.endswith((Token.IMPORT.value,))", "endswith"),
    ],
    ids=[
        "symbol",
        "symbol-alias",
        "module-alias",
        "relative",
        "stable-reexport",
        "module-reexport",
        "membership",
        "prefix",
        "suffix",
    ],
)
def test_imported_enum_value_leaf_reaches_native_scoped_policy(tmp_path, prefix, expression, form):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {
            "core.py": prefix + f"def parse(value):\n    return {expression}\n",
            "cli.py": ENUM,
            "bridge.py": 'from sample.cli import Token\n__all__ = ["Token"]\n',
        },
    )
    assert not result.diagnostics and result.observation is not None
    records = [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert [row.data.get("form") for row in records] == [form]
    assert [row.subjects for row in trace_valid_violations(result.observation)] == [
        ("sample.core.parse",)
    ]


@pytest.mark.parametrize(
    "body,form",
    [
        (
            "def parse(value):\n    match value:\n        case Token.IMPORT.value:\n"
            "            return True\n        case _:\n            return False\n",
            "match",
        ),
        (
            "TOKENS = {Token.IMPORT.value}\ndef parse(value):\n    return value in TOKENS\n",
            "membership",
        ),
        (
            "TOKENS = [Token.IMPORT.value]\ndef parse(value):\n    return value in TOKENS\n",
            "membership",
        ),
        (
            "TOKENS = (Token.IMPORT.value,)\n"
            "def parse(value):\n    return value.startswith(TOKENS)\n",
            "startswith",
        ),
        ("def parse(value):\n    tag = Token.IMPORT.value\n    return value == tag\n", "compare"),
    ],
)
def test_imported_value_cannot_hide_in_existing_literal_forms(tmp_path, body, form):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {"core.py": "from sample.cli import Token\n" + body, "cli.py": ENUM},
    )
    assert not result.diagnostics and result.observation is not None
    records = [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert [row.data.get("form") for row in records] == [form]
    assert len(trace_valid_violations(result.observation)) == 1


@pytest.mark.parametrize(
    "provider,prefix,body",
    [
        (
            'class Token:\n    IMPORT = "import"\n',
            "from sample.cli import Token\n",
            "return value == Token.IMPORT.value",
        ),
        (
            'from enum import IntEnum\nclass Token(IntEnum):\n    IMPORT = "1"\n',
            "from sample.cli import Token\n",
            "return value == Token.IMPORT.value",
        ),
        (
            "from enum import Enum\nclass Token(Enum):\n"
            '    IMPORT = "import"\n    @property\n    def value(self):\n        return 1\n',
            "from sample.cli import Token\n",
            "return value == Token.IMPORT.value",
        ),
        (
            'from enum import Enum\n@change\nclass Token(Enum):\n    IMPORT = "import"\n',
            "from sample.cli import Token\n",
            "return value == Token.IMPORT.value",
        ),
        (ENUM, "from external import Token\n", "return value == Token.IMPORT.value"),
        (
            ENUM,
            "from sample.cli import Token\nToken = other\n",
            "return value == Token.IMPORT.value",
        ),
        (
            ENUM,
            "import sample.cli as vocabulary\nvocabulary = other\n",
            "return value == vocabulary.Token.IMPORT.value",
        ),
        (
            ENUM,
            "if condition:\n    from sample.cli import Token\n",
            "return value == Token.IMPORT.value",
        ),
        (ENUM, "from sample.cli import Token\n", "return value is Token.IMPORT"),
        (ENUM, "from sample.cli import Token\n", "return Token.IMPORT.value"),
        (
            ENUM,
            "from sample.cli import Token\n",
            "TOKENS = {Token.IMPORT.value}\n    TOKENS.add(value)\n    return value in TOKENS",
        ),
    ],
    ids=[
        "non-enum",
        "intenum",
        "custom-value",
        "decorated",
        "unscanned",
        "rebound-symbol",
        "rebound-module",
        "conditional-import",
        "enum-identity",
        "wire-serialization",
        "mutated-local-set",
    ],
)
def test_imported_value_observation_does_not_guess_runtime_types(tmp_path, provider, prefix, body):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {"core.py": prefix + "def parse(value):\n    " + body + "\n", "cli.py": provider},
    )
    assert not result.diagnostics and result.observation is not None
    assert not [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert not trace_valid_violations(result.observation)


def test_imported_value_named_collection_escape_is_not_a_literal_proof(tmp_path):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {
            "core.py": "from sample.cli import Token\nTOKENS = {Token.IMPORT.value}\n"
            "other = TOKENS\nother.clear()\ndef parse(value):\n    return value in TOKENS\n",
            "cli.py": ENUM,
        },
    )
    assert not result.diagnostics and result.observation is not None
    assert not result.observation.records("constructs")
    assert not trace_valid_violations(result.observation)


@pytest.mark.parametrize(
    "prefix,expression",
    [
        ("from sample.facade import Token as Event\n", "value == Event.IMPORT.value"),
        ("import sample.facade as vocabulary\n", "value == vocabulary.Token.IMPORT.value"),
    ],
)
def test_transitive_import_value_routes_keep_the_canonical_provider(tmp_path, prefix, expression):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {
            "core.py": prefix + f"def parse(value):\n    return {expression}\n",
            "cli.py": ENUM,
            "bridge.py": 'from sample.cli import Token\n__all__ = ["Token"]\n',
            "facade.py": 'from sample.bridge import Token\n__all__ = ["Token"]\n',
        },
    )
    assert not result.diagnostics and result.observation is not None
    assert [row.subjects for row in trace_valid_violations(result.observation)] == [
        ("sample.core.parse",)
    ]


@pytest.mark.parametrize(
    "prefix,expression",
    [
        ("from sample.cli import TOKEN as WORD\n", "value == WORD"),
        ("import sample.cli as words\n", "value != words.TOKEN"),
        ("from sample.bridge import TOKEN\n", "TOKEN in value"),
        ("from sample.cli import Words\n", "value == Words.IMPORT"),
    ],
)
def test_imported_scalar_leaves_reuse_the_existing_literal_provider_proof(
    tmp_path, prefix, expression
):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {
            "core.py": prefix + f"def parse(value):\n    return {expression}\n",
            "cli.py": 'TOKEN = b"import"\nclass Words:\n    IMPORT = "import"\n',
            "bridge.py": 'from sample.cli import TOKEN\n__all__ = ["TOKEN"]\n',
        },
    )
    assert not result.diagnostics and result.observation is not None
    assert len(trace_valid_violations(result.observation)) == 1


@pytest.mark.parametrize(
    "provider",
    [
        ENUM + "Token = other\n",
        ENUM.replace("class Token", "ProtocolEnum = other\nclass Token"),
        ENUM.replace('IMPORT = "import"', 'IMPORT = "im" + "port"'),
        "if condition:\n    from enum import Enum\n"
        '    class Token(Enum):\n        IMPORT = "import"\n',
    ],
    ids=["rebound-provider", "rebound-stdlib-base", "computed-member", "conditional-class"],
)
def test_module_alias_does_not_turn_an_unproven_provider_into_an_enum(tmp_path, provider):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {
            "core.py": "import sample.cli as vocabulary\n"
            "def parse(value):\n    return value == vocabulary.Token.IMPORT.value\n",
            "cli.py": provider,
        },
    )
    assert not result.diagnostics and result.observation is not None
    assert not [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert not trace_valid_violations(result.observation)


@pytest.mark.parametrize(
    "provider,expression",
    [
        (
            'TOKEN = "import"\ndef replace():\n    global TOKEN\n    TOKEN = read()\n',
            "words.TOKEN",
        ),
        (
            'class Words:\n    IMPORT = "import"\n'
            "def replace():\n    global Words\n    Words = read()\n",
            "words.Words.IMPORT",
        ),
    ],
)
def test_module_import_does_not_skip_the_providers_global_rebinding(tmp_path, provider, expression):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {
            "core.py": "import sample.cli as words\n"
            f"def parse(value):\n    return value == {expression}\n",
            "cli.py": provider,
        },
    )
    assert not result.diagnostics and result.observation is not None
    assert not [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert not trace_valid_violations(result.observation)


@pytest.mark.parametrize(
    "mutation,expression",
    [
        ("words.TOKEN = 123\n", "words.TOKEN"),
        ("words.Token = other\n", "words.Token.IMPORT.value"),
        ("alias = words\nalias.TOKEN = 123\n", "words.TOKEN"),
        ("globals()['words'] = other\n", "words.Token.IMPORT.value"),
    ],
    ids=[
        "module-literal-write",
        "module-enum-write",
        "aliased-module-write",
        "dynamic-alias-write",
    ],
)
def test_visible_consumer_namespace_writes_invalidate_imported_literal_proof(
    tmp_path, mutation, expression
):
    result = _observe_one_rule(
        tmp_path,
        RULE,
        {
            "core.py": (
                "import sample.cli as words\n"
                + mutation
                + f"def parse(value):\n    return value == {expression}\n"
            ),
            "cli.py": ENUM + 'TOKEN = "import"\n',
        },
    )
    assert not result.diagnostics and result.observation is not None
    assert not [
        row
        for row in result.observation.records("constructs")
        if row.kind == "string_literal_compare"
    ]
    assert not trace_valid_violations(result.observation)


@pytest.mark.parametrize(
    "prefix,expression",
    [
        ("import sample.cli as vocabulary\n", "vocabulary.Token.IMPORT.value"),
        ("from sample.bridge import Token as Event\n", "Event.IMPORT.value"),
    ],
    ids=["module-suffix", "imported-symbol-suffix"],
)
def test_canonical_name_replaces_the_longest_origin_once(tmp_path, prefix, expression):
    module = _parsed_module(
        prefix + f"result = {expression}\n", "sample.core", rel_path="sample/core.py"
    )
    parsed = [
        module,
        _parsed_module(ENUM, "sample.cli", rel_path="sample/cli.py"),
        _parsed_module(
            'from sample.cli import Token\n__all__ = ["Token"]\n',
            "sample.bridge",
            rel_path="sample/bridge.py",
        ),
    ]
    imports = collect_imports(parsed, {row.module for row in parsed}, {}, namespace="sample")
    resolve_reexports(imports, {row.module: row.all_exports for row in parsed}, parsed)
    literals = _LiteralComparisons(module)
    literals.origins = _literal_import_origins(imports)
    assignment = module.tree.body[-1]
    assert isinstance(assignment, ast.Assign)
    assert literals._canonical_name(assignment.value) == "sample.cli.Token.IMPORT.value"

    # Synthetic overlap tests only this lookup contract, not native import binding evidence.
    # The native provider/consumer tests above exercise actual resolved import routes.
    literals.origins.update(
        {
            "sample.cli": "short.Route",
            "sample.cli.Token": "short.Owner",
            "sample.cli.Token.IMPORT": "long.Member",
            "long.Member.value": "must.not.chase",
        }
    )
    assert literals._canonical_name(assignment.value) == "long.Member.value"
