# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""The actual Atlas deviation producer and public Scene ingress have a precise boundary."""

import importlib
import importlib.util
import json

import pytest
from test_report_renderer_units import _asset_page

from archkeel.ir.model import stable_id


def _packed_atlas():
    return {
        "reference_ids": [], "rule_assessments": [], "cells": [], "assignments": [],
        "modules": [], "symbol_coverages": [], "levels": [], "components": [],
        "findings": [], "declared_modules": [], "deviations": [],
    }


@pytest.mark.parametrize(
    ("field", "value"),
    [("kind", "unsupported-deviation"), ("source_id", 0), ("level_id", 0)],
)
def test_public_scene_rejects_malformed_recorded_deviation(field, value):
    api = pytest.importorskip("playwright.sync_api")
    playwright, browser, page = _asset_page(api, ["report-scene.js"])
    atlas = _packed_atlas()
    row = {"id": "row", "kind": "undeclared", "source_id": "a",
           "target_id": "b", "level_id": None}
    row[field] = value
    atlas["deviations"] = [row]
    try:
        result = page.evaluate("""data => {
          try { ArchkeelReportScene.create(data); }
          catch (error) { return error instanceof TypeError; }
          return false;
        }""", {"atlas": atlas})
        assert result, f"Actual scene.create accepted malformed deviation {field}"
    finally:
        browser.close()
        playwright.stop()


@pytest.mark.parametrize("omitted", [False, True])
def test_public_scene_preserves_legacy_empty_or_missing_deviations(omitted):
    api = pytest.importorskip("playwright.sync_api")
    playwright, browser, page = _asset_page(api, ["report-scene.js"])
    atlas = _packed_atlas()
    if omitted:
        del atlas["deviations"]
    try:
        assert page.evaluate("""data => {
          const before = JSON.stringify(data);
          const model = ArchkeelReportScene.create(data);
          return model.atlas !== data.atlas && JSON.stringify(data) === before;
        }""", {"atlas": atlas})
    finally:
        browser.close()
        playwright.stop()


def test_real_deviation_producer_preserves_sorted_wire_order_and_stable_ids():
    name = "archkeel.render.atlas_deviations"
    assert importlib.util.find_spec(name) is not None, "The actual deviation value owner is absent"
    owner = importlib.import_module(name)
    declared = {("z", "a"), ("a", "b"), ("shared", "pair")}
    used = {("b", "a"), ("shared", "pair")}
    rows = owner.level_deviations(None, declared, used)
    expected = [
        {"id": stable_id("atlas-deviation", None, kind, source, target), "kind": kind,
         "source_id": source, "target_id": target, "level_id": None}
        for kind, source, target in [
            ("allowed_unused", "a", "b"), ("allowed_unused", "z", "a"),
            ("undeclared", "b", "a"),
        ]
    ]
    assert isinstance(rows, tuple)
    assert all(type(row.kind) is owner.AtlasDeviationKind for row in rows)
    wire = [row.to_wire() for row in rows]
    assert wire == expected
    assert json.dumps(wire, separators=(",", ":")) == json.dumps(expected, separators=(",", ":"))
    assert all(type(item["kind"]) is str for item in wire)
    assert all(list(item) == ["id", "kind", "source_id", "target_id", "level_id"] for item in wire)
    assert owner.level_deviations(None, declared, declared) == ()
    nested = owner.level_deviations("nested", declared, used)
    assert all(row.level_id == "nested" for row in nested)
    assert {row.id for row in rows}.isdisjoint(row.id for row in nested)
