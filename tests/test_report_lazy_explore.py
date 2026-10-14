# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Hidden exploration defers DOM while keeping native evidence routes reachable."""

import pytest
from browser_report_support import _browser_page, _open_health_check
from test_atlas_report import _atlas, _page
from test_module_explore import _sample
from test_uml_rendering import _wait_for_layout


@pytest.mark.parametrize("width", [1440, 400])
def test_offline_explore_builds_matrix_on_open_and_module_links_on_expansion(tmp_path, width):
    api = pytest.importorskip("playwright.sync_api")
    html = _page(
        _sample(
            tmp_path / "source",
            extra_files={f"sample/core/item_{i}.py": "import sample.peer\n" for i in range(24)},
        )
    )
    atlas = _atlas(html)
    level = next(item for item in atlas["levels"] if item["parent_id"] is None)
    report = tmp_path / "report.html"
    report.write_text(html)
    errors = []
    playwright, browser, page = _browser_page(api, html, width=width, errors=errors)
    try:
        page.goto(report.as_uri() + "?theme=dark")
        _wait_for_layout(page)
        matrix = page.locator(".flow-matrix")
        modules = page.locator("details.atlas-module-list")
        for lens in ("Diff", "Target", "As-Is"):
            assert matrix.locator("*").count() == 0
            assert modules.locator("li").count() == 0
            page.get_by_role("button", name=lens, exact=True).click()
            _wait_for_layout(page)
        assert str(len(level["modules"])) in modules.locator("summary").inner_text()
        _open_health_check(page)
        assert matrix.locator(".matrix-cell").count() == len(level["cells"])
        assert modules.locator("li").count() == 0
        page.evaluate("window.originalMatrix = document.querySelector('.flow-matrix svg')")
        modules.locator("summary").press("Enter")
        api.expect(modules.locator("li")).to_have_count(len(level["modules"]))
        assert modules.get_by_role("link", name="item_0.py", exact=True).count() == 1
        page.keyboard.press("Escape")
        _open_health_check(page)
        assert page.evaluate("originalMatrix === document.querySelector('.flow-matrix svg')")
        assert modules.locator("li").count() == len(level["modules"])
        for lens in ("Diff", "Target", "As-Is"):
            page.get_by_role("button", name=lens, exact=True).click()
            _wait_for_layout(page)
            if lens == "Target":
                assert matrix.locator("*").count() == 0
                assert modules.count() == 0
            else:
                assert matrix.locator(".matrix-cell").count() == len(level["cells"])
                assert modules.locator("li").count() == 0
        page.keyboard.press("Escape")
        page.get_by_role("button", name="Diff", exact=True).click()
        _wait_for_layout(page)
        assert matrix.locator("*").count() == 0
        assert modules.locator("li").count() == 0
        _open_health_check(page)
        assert matrix.locator(".matrix-cell").count() == len(level["cells"])
        assert not errors
    finally:
        browser.close()
        playwright.stop()


@pytest.mark.parametrize("width", [1440, 400])
def test_question_selection_reuses_matrix_and_reveals_it_after_details_open(tmp_path, width):
    api = pytest.importorskip("playwright.sync_api")
    html = _page(
        _sample(
            tmp_path,
            extra_files={f"sample/core/item_{i}.py": "import sample.peer\n" for i in range(24)},
        )
    )
    errors = []
    playwright, browser, page = _browser_page(api, html, width=width, errors=errors)
    try:
        _wait_for_layout(page)
        _open_health_check(page)
        page.evaluate("window.originalMatrix = document.querySelector('.flow-matrix svg')")
        page.get_by_role("button", name="Show in matrix", exact=True).first.click()
        assert page.evaluate("originalMatrix === document.querySelector('.flow-matrix svg')")
        api.expect(page.locator(".ak-drawer .flow-matrix")).to_be_visible()
        assert page.locator(".matrix-cell.highlighted").count() > 0
        api.expect(page.locator(".flow-matrix")).to_be_focused()
        assert page.locator(".flow-inspector-content").inner_text()
        page.locator(".matrix-cell").first.press("Enter")
        assert "Permission: UNKNOWN" in page.locator(".flow-inspector-content").inner_text()
        assert not errors
    finally:
        browser.close()
        playwright.stop()
