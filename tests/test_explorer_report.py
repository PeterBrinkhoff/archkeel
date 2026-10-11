# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""ArchQ Explorer is the default, offline architecture report."""

from urllib.parse import parse_qs, urlsplit
from xml.etree import ElementTree

import pytest
from browser_report_support import _browser_page, _open_details
from test_atlas_report import _page, _result
from test_module_explore import _sample
from test_uml_rendering import _wait_for_layout

from archkeel.ir.codec import canonical_report_bytes
from archkeel.render.html import render_architecture_details


@pytest.fixture
def explorer(tmp_path):
    api = pytest.importorskip("playwright.sync_api")
    model = _sample(tmp_path, uml=True, other_component=True)
    index = tmp_path / "architecture.report.html"
    index.write_text(_page(model))
    for name, content in render_architecture_details(
        _result(model),
        canonical_report_bytes(model),
        repository="One target",
        architecture_href="architecture.json",
    ).items():
        (tmp_path / name).write_bytes(content)
    errors = []
    playwright, browser, page = _browser_page(api, "", errors=errors)
    page.goto(index.as_uri())
    _wait_for_layout(page)
    try:
        yield page, index
        assert not errors
    finally:
        browser.close()
        playwright.stop()


def test_explorer_is_default_and_keeps_architecture_evidence(tmp_path):
    api = pytest.importorskip("playwright.sync_api")
    document = _page(_sample(tmp_path))
    errors = []
    playwright, browser, page = _browser_page(api, document, errors=errors)
    try:
        _wait_for_layout(page)
        assert page.locator("html").evaluate("e => e.classList.contains('ak-canvas')")
        assert "ArchQ Explorer" in page.title()
        assert page.locator(".ak-brand").inner_text() == "ArchQ Explorer"
        assert page.locator(".ak-brand").is_visible()
        assert page.get_by_role("button", name="Search", exact=True).is_visible()
        assert page.get_by_role("button", name="Target", exact=True).is_visible()
        assert page.get_by_role("button", name="Diff", exact=True).is_visible()
        assert not errors
    finally:
        browser.close()
        playwright.stop()


def test_search_selects_components_rules_and_declared_modules(explorer):
    page, _ = explorer
    page.get_by_role("button", name="Search", exact=True).click()
    search = page.get_by_role("combobox", name="Search", exact=True)
    search.fill("peer")
    search.press("Enter")
    assert parse_qs(urlsplit(page.url).query)["selected"] == ["peer"]
    assert page.locator('.flow-nodes [data-uml-id="peer"]').get_attribute("aria-pressed") == "true"
    page.keyboard.press("/")
    search.fill("dependencies")
    search.press("Enter")
    assessment = page.locator("#atlas-assessment-dependencies")
    assert assessment.is_visible()
    assert "FAIL" in assessment.inner_text()
    page.get_by_role("button", name="Target", exact=True).click()
    page.keyboard.press("/")
    search.fill("core")
    page.get_by_role("option").filter(has=page.locator(".ak-kind", has_text="M")).click()
    _wait_for_layout(page)
    query = parse_qs(urlsplit(page.url).query)
    assert query["module"] == ["core-module"]
    assert query["origin"] == ["declared"]
    assert "Requested scope unavailable" not in page.locator("body").inner_text()
    assert urlsplit(page.url).path.endswith("architecture.detail.html")


def test_dialog_keyboard_and_object_sorting(explorer):
    page, _ = explorer
    trigger = page.get_by_role("button", name="Search", exact=True)
    trigger.click()
    search = page.get_by_role("combobox", name="Search", exact=True)
    search.fill("no such component")
    search.press("p")
    assert search.input_value().endswith("p")
    assert (
        page.get_by_role("button", name="None", exact=True).get_attribute("aria-pressed") == "true"
    )
    assert not search.get_attribute("aria-activedescendant")
    search.press("Tab")
    assert page.evaluate("document.querySelector('dialog').contains(document.activeElement)")
    page.keyboard.press("Escape")
    assert trigger.evaluate("e => e === document.activeElement")
    page.keyboard.press("o")
    table = page.locator(".ak-table")
    table.get_by_role("button", name="Component").press("Enter")
    assert (
        table.get_by_role("columnheader", name="Component").get_attribute("aria-sort")
        == "descending"
    )
    assert table.locator("tbody tr td:first-child").all_text_contents() == ["peer", "other", "core"]
    page.keyboard.press("Escape")
    page.get_by_role("button", name="Share", exact=True).click()
    page.keyboard.press("End")
    assert page.get_by_role("menuitem", name="Download SVG").evaluate(
        "e => e === document.activeElement"
    )
    page.keyboard.press("Escape")
    assert page.get_by_role("button", name="Share", exact=True).evaluate(
        "e => e === document.activeElement"
    )
    page.get_by_role("button", name="Health check", exact=True).click()
    trigger.click()
    search.press("Escape")
    assert page.locator(".ak-drawer").is_visible()
    page.keyboard.press("Escape")
    assert page.locator(".ak-drawer").count() == 0


def test_perspective_history_and_hover_preserve_verdicts(explorer):
    page, _ = explorer
    statuses = page.locator(".atlas-rule-status").all_text_contents()
    peer = page.locator('.flow-nodes [data-uml-id="peer"]')
    peer.hover()
    assert page.locator('.flow-nodes [data-uml-id="other"]').evaluate(
        "e => e.classList.contains('dim')"
    )
    assert not page.locator('.flow-nodes [data-uml-id="core"]').evaluate(
        "e => e.classList.contains('dim')"
    )
    page.get_by_role("button", name="Decided by", exact=True).click()
    page.keyboard.press("/")
    page.get_by_role("combobox").fill("peer")
    page.get_by_role("combobox").press("Enter")
    page.get_by_role("button", name="Evidence", exact=True).click()
    assert parse_qs(urlsplit(page.url).query)["perspective"] == ["evidence"]
    page.go_back()
    _wait_for_layout(page)
    assert (
        page.get_by_role("button", name="Decided by", exact=True).get_attribute("aria-pressed")
        == "true"
    )
    page.get_by_role("button", name="Zoom in", exact=True).click()
    assert page.locator(".atlas-rule-status").all_text_contents() == statuses


def test_zoom_stays_under_pointer_and_middle_drag_pans(explorer):
    page, _ = explorer
    canvas = page.locator(".flow-canvas")
    box = canvas.bounding_box()
    point = {"x": box["x"] + box["width"] * 0.65, "y": box["y"] + box["height"] * 0.4}
    world = page.evaluate(
        """p => {
          const matrix = document.querySelector('.flow-viewport').getScreenCTM();
          const q = new DOMPoint(p.x, p.y).matrixTransform(matrix.inverse());
          return {x:q.x,y:q.y};
        }""",
        point,
    )
    for delta in (-260, 140):
        canvas.dispatch_event(
            "wheel",
            {"deltaY": delta, "ctrlKey": True, "clientX": point["x"], "clientY": point["y"]},
        )
        after = page.evaluate(
            """p => {
              const matrix = document.querySelector('.flow-viewport').getScreenCTM();
              const q = new DOMPoint(p.x, p.y).matrixTransform(matrix);
              return {x:q.x,y:q.y};
            }""",
            world,
        )
        assert abs(after["x"] - point["x"]) <= 2
        assert abs(after["y"] - point["y"]) <= 2
    peer = page.locator('.flow-nodes [data-uml-id="peer"]')
    position = peer.get_attribute("transform")
    before = page.locator(".flow-viewport").get_attribute("transform")
    peer.hover()
    mouse = peer.bounding_box()
    page.mouse.down(button="middle")
    page.mouse.move(mouse["x"] + 60, mouse["y"] + 80, steps=4)
    page.mouse.up(button="middle")
    assert peer.get_attribute("transform") == position
    assert page.locator(".flow-viewport").get_attribute("transform") != before


def test_perspective_pin_clears_on_untagged_modules_and_invalid_urls(explorer):
    page, index = explorer
    page.get_by_role("button", name="Decided by", exact=True).click()
    page.locator(".ak-chip").first.click()
    page.get_by_role("button", name="Modules (").click()
    _wait_for_layout(page)
    assert page.locator(".flow-nodes .ak-dim").count() == 0
    for value in ("constructor", "__proto__", "toString", "unknown"):
        page.goto(index.as_uri() + f"?perspective={value}")
        _wait_for_layout(page)
        assert (
            page.get_by_role("button", name="None", exact=True).get_attribute("aria-pressed")
            == "true"
        )


def test_existing_finding_links_open_visible_health_check(explorer):
    page, index = explorer
    page.goto(index.as_uri() + "#atlas-rule-dependencies")
    _wait_for_layout(page)
    assert page.locator(".ak-drawer #atlas-rule-dependencies").is_visible()
    page.keyboard.press("Escape")
    _open_details(page)
    page.locator(".atlas-rule-assessments > summary").click()
    page.locator(".atlas-rule-assessments").get_by_role(
        "link", name="dependencies", exact=True
    ).click()
    assert page.locator(".ak-drawer #atlas-rule-dependencies").is_visible()


def test_svg_export_is_standalone_and_evidence_view_is_reachable(explorer):
    page, _ = explorer
    page.get_by_role("button", name="Decided by", exact=True).click()
    page.get_by_role("button", name="Share", exact=True).click()
    with page.expect_download() as download:
        page.get_by_role("menuitem", name="Download SVG").click()
    svg = download.value.path().read_text()
    root = ElementTree.fromstring(svg)
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert "var(--" not in svg
    assert "rgb(" in svg
    assert "peer" in svg and "core" in svg
    assert any('url("#flow-arrow' in node.get("style", "") for node in root.iter())
    page.get_by_role("button", name="Report evidence", exact=True).click()
    page.locator(".atlas-source > summary").wait_for(state="visible")
    assert page.get_by_text("Snapshot and audit", exact=True).is_visible()
    assert not page.locator("html").evaluate("e => e.classList.contains('ak-canvas')")
    page.get_by_role("button", name="Target", exact=True).click()
    _wait_for_layout(page)
    page.get_by_role("link", name="Open ArchQ Explorer", exact=True).click()
    page.locator(".ak-brand").wait_for(state="visible")
    assert parse_qs(urlsplit(page.url).query)["perspective"] == ["decision"]
    assert parse_qs(urlsplit(page.url).query)["view"] == ["target"]


def test_print_retains_the_document_evidence(explorer):
    page, _ = explorer
    page.emulate_media(media="print")
    assert page.locator(".atlas-verdict-grid").is_visible()
    assert page.locator(".atlas-source > summary").is_visible()
    assert page.locator(".report-heading").is_visible()
    assert not page.locator(".flow-section").is_visible()


def test_mobile_matrix_selection_reveals_details(explorer):
    page, _ = explorer
    page.set_viewport_size({"width": 390, "height": 844})
    page.get_by_role("button", name="Health check", exact=True).click()
    page.locator('.flow-matrix [data-cell="0"]').click()
    assert page.locator(".ak-drawer").count() == 0
    assert page.locator(".flow-inspector").is_visible()
    assert "Permission: UNKNOWN" in page.locator(".flow-inspector-content").inner_text()


@pytest.mark.parametrize("width", [390, 768, 1024, 1280, 1440])
def test_explorer_controls_fit_without_overlap(explorer, width):
    page, _ = explorer
    page.set_viewport_size({"width": width, "height": 844})
    page.evaluate("ArchkeelFlow.atlas.components[0].label = 'very_long_component_name'.repeat(8)")
    page.locator('.flow-nodes [data-uml-kind="component"]').first.press("Space")
    controls = [
        page.get_by_role("button", name=name, exact=True)
        for name in ("Search", "Target", "Health check", "Objects", "Share", "Zoom in", "Evidence")
    ]
    boxes = []
    for control in controls:
        assert control.is_visible()
        control.scroll_into_view_if_needed()
        box = control.bounding_box()
        assert box["x"] >= 0 and box["x"] + box["width"] <= width
        boxes.append(box)
    for i, a in enumerate(boxes):
        for b in boxes[i + 1 :]:
            assert (
                a["x"] + a["width"] <= b["x"]
                or b["x"] + b["width"] <= a["x"]
                or a["y"] + a["height"] <= b["y"]
                or b["y"] + b["height"] <= a["y"]
            )
    page.get_by_role("button", name="Target", exact=True).click()
