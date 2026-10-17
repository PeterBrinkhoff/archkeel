# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Python classifier decisions share their actual source-fact vocabulary."""

import json

import pytest
from test_analyzer import _parsed_module

from archkeel.analyzer.python.imports import collect_imports
from archkeel.analyzer.python.symbols import collect_symbols
from archkeel.ir import facts, model
from archkeel.ir.facts_codec import parse_record, record_payload

TAGS = ("protocol", "enum", "pydantic_model", "dataclass", "class")


def _api():
    kind = getattr(facts, "SymbolClassKind", None)
    reader = getattr(facts, "parse_symbol_class_kind", None)
    assert kind is not None and reader is not None, (
        "Facts must own the shared classifier vocabulary"
    )
    assert model.SymbolClassKind is kind
    assert kind.__module__ == facts.__name__
    assert tuple(item.value for item in kind) == TAGS
    return kind, reader


@pytest.mark.parametrize("tag", TAGS)
def test_one_reader_accepts_actual_legacy_tags_and_identical_nominal_members(tag):
    kind, reader = _api()
    assert reader(tag) is kind(tag)
    assert reader(kind(tag)) is kind(tag)


@pytest.mark.parametrize("value", (None, "", "ENUM", "future", "mixin", 1, False, [], {}))
def test_foreign_or_opaque_classifiers_remain_unclassified(value):
    _, reader = _api()
    assert reader(value) is None


def test_actual_fixpoint_produces_nominal_values_without_changing_classifier_records():
    kind, reader = _api()
    module = _parsed_module(
        "from typing import Protocol\n"
        "from enum import Enum\n"
        "from dataclasses import dataclass\n"
        "from pydantic import BaseModel, ConfigDict\n"
        "class Child(Later): pass\n"
        "class Later(Enum): VALUE = 1\n"
        "class Port(Protocol): pass\n"
        "class Client(Port): pass\n"
        "class Extended(Port, Protocol): pass\n"
        "@dataclass\n"
        "class Data: value: int\n"
        "@dataclass\n"
        "class Mixed(Port, Protocol): pass\n"
        "class Plain: pass\n"
        "class Model(BaseModel):\n"
        " model_config = ConfigDict(frozen=True)\n"
        "if enabled:\n"
        " class Conditional(Enum): VALUE = 1\n"
    )
    collect_imports([module], set(), {}, namespace="sample")
    records, _, _ = collect_symbols([module], {})
    classes = {row["title"]: row for row in records if row["kind"] == "class"}
    expected = {
        "Child": kind.ENUM,
        "Later": kind.ENUM,
        "Port": kind.PROTOCOL,
        "Client": kind.CLASS,
        "Extended": kind.PROTOCOL,
        "Data": kind.DATACLASS,
        "Mixed": kind.DATACLASS,
        "Plain": kind.CLASS,
        "Model": kind.PYDANTIC_MODEL,
    }
    assert set(classes) == set(expected) | {"Conditional"}
    assert "class_kind" not in classes["Conditional"]["data"]
    for name, member in expected.items():
        row = classes[name]
        assert row["data"]["class_kind"] is member
        frozen = parse_record(json.loads(json.dumps(row)))
        assert reader(frozen.data.get("class_kind")) is member
        assert json.loads(json.dumps(record_payload(frozen))) == json.loads(json.dumps(row))
    assert classes["Later"]["data"]["enum_members"] == ["VALUE"]
    assert classes["Model"]["data"]["frozen_object"] is True
