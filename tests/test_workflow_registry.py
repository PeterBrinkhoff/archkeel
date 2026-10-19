# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Only absent file-backed workflows may be disabled against stable live Main."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
MAIN = "a" * 40
TREE = "b" * 40
PREFIX = "repos/example/project/"
KEPT = ".github/workflows/ci.yml"
OLD = ".github/workflows/diagnostic.yml"


def _workflow(identifier: int, path: str, state: str = "active") -> dict[str, object]:
    return {"id": identifier, "path": path, "state": state}


def _ref(sha: str = MAIN) -> dict[str, object]:
    return {"ref": "refs/heads/main", "object": {"type": "commit", "sha": sha}}


def _tree(*paths: str) -> dict[str, object]:
    return {
        "sha": TREE,
        "truncated": False,
        "tree": [{"path": path, "type": "blob", "mode": "100644"} for path in paths],
    }


def _page(*workflows: dict[str, object], count: int | None = None) -> dict[str, object]:
    return {"total_count": len(workflows) if count is None else count, "workflows": workflows}


def _get(path: str, response: object, *, pages: bool = False) -> dict[str, object]:
    return {
        "args": ["api", *(["--paginate", "--slurp"] if pages else []), PREFIX + path],
        "response": response,
    }


def _setup(*, tree: object = None, inventory: object = None) -> list[dict[str, object]]:
    return [
        _get("git/ref/heads/main", _ref()),
        _get(f"git/commits/{MAIN}", {"sha": MAIN, "tree": {"sha": TREE}}),
        _get(f"git/trees/{TREE}?recursive=1", _tree(KEPT) if tree is None else tree),
        _get(
            "actions/workflows?per_page=100",
            [_page(_workflow(1, KEPT), _workflow(2, OLD))] if inventory is None else inventory,
            pages=True,
        ),
    ]


def _disable(identifier: int, path: str = OLD) -> list[dict[str, object]]:
    return [
        _get(f"actions/workflows/{identifier}", _workflow(identifier, path)),
        _get("git/ref/heads/main", _ref()),
        {
            "args": ["api", "--method", "PUT", PREFIX + f"actions/workflows/{identifier}/disable"],
            "response": None,
        },
        {
            **_get(
                f"actions/workflows/{identifier}",
                _workflow(identifier, path, "disabled_manually"),
            ),
            "expect_pending": identifier,
        },
        _get("git/ref/heads/main", _ref()),
    ]


def _run(
    tmp_path: Path, tape: list[dict[str, object]], *, disable: str = "false"
) -> tuple[subprocess.CompletedProcess[str], dict, list[list[str]]]:
    tape_path = tmp_path / "tape.json"
    tape_path.write_text(json.dumps(tape))
    calls_path = tmp_path / "calls.json"
    plan_dir = tmp_path / "plan"
    gh = tmp_path / "gh"
    gh.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, pathlib, sys\n"
        "calls_path = pathlib.Path(os.environ['MOCK_CALLS'])\n"
        "calls = json.loads(calls_path.read_text()) if calls_path.exists() else []\n"
        "tape = json.loads(pathlib.Path(os.environ['MOCK_TAPE']).read_text())\n"
        "step = tape[len(calls)]\n"
        "calls.append(sys.argv[1:])\n"
        "calls_path.write_text(json.dumps(calls))\n"
        "assert sys.argv[1:] == step['args'], (sys.argv[1:], step['args'])\n"
        "if '--method' in sys.argv:\n"
        "    plan = json.loads(pathlib.Path(os.environ['MOCK_PLAN']).read_text())\n"
        "    assert plan['main_sha'] == 'a' * 40\n"
        "    assert plan['disable_ids']\n"
        "if 'expect_pending' in step:\n"
        "    plan = json.loads(pathlib.Path(os.environ['MOCK_PLAN']).read_text())\n"
        "    assert plan['pending_disable_id'] == step['expect_pending']\n"
        "    assert step['expect_pending'] not in plan['disabled_ids']\n"
        "if step.get('exit'):\n"
        "    sys.exit(step['exit'])\n"
        "if step['response'] is not None:\n"
        "    print(json.dumps(step['response']))\n"
    )
    gh.chmod(0o755)
    result = subprocess.run(
        [
            "make",
            "--no-print-directory",
            "prune-workflows",
            f"DISABLE={disable}",
            f"WORKFLOW_PRUNE_DIR={plan_dir}",
        ],
        cwd=ROOT,
        env={
            **os.environ,
            "MAKEFLAGS": "",
            "PATH": f"{tmp_path}:{os.environ['PATH']}",
            "GITHUB_REPOSITORY": "example/project",
            "MOCK_CALLS": str(calls_path),
            "MOCK_TAPE": str(tape_path),
            "MOCK_PLAN": str(plan_dir / "plan.json"),
        },
        capture_output=True,
        text=True,
        timeout=15,
    )
    output = plan_dir / "plan.json"
    plan = json.loads(output.read_text()) if output.exists() else {}
    calls = json.loads(calls_path.read_text()) if calls_path.exists() else []
    return result, plan, calls


def test_make_dry_run_uses_live_main_not_checkout_and_preserves_managed_workflows(tmp_path: Path):
    inventory = [
        _page(_workflow(1, KEPT), _workflow(2, OLD), count=5),
        _page(
            _workflow(3, "dynamic/pages/pages-build-deployment"),
            _workflow(4, ".github/workflows/disabled.yml", "disabled_manually"),
            _workflow(5, "pages-build-deployment"),
            count=5,
        ),
    ]
    tape = [*_setup(inventory=inventory), _get("git/ref/heads/main", _ref())]
    result, plan, calls = _run(tmp_path, tape)
    assert result.returncode == 0, result.stderr
    assert plan["main_paths"] == [KEPT]
    assert plan["disable_ids"] == [2]
    assert plan["disabled_ids"] == []
    assert calls == [step["args"] for step in tape]
    assert "Dry run" in result.stdout


def test_explicit_disable_rechecks_identity_and_main_without_deleting_history(tmp_path: Path):
    tape = [*_setup(), _get("git/ref/heads/main", _ref()), *_disable(2)]
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode == 0, result.stderr
    assert plan["disabled_ids"] == [2]
    assert calls == [step["args"] for step in tape]


@pytest.mark.parametrize("point", ["after_inventory", "before_disable", "after_disable"])
def test_main_changes_abort_with_completed_write_receipt(tmp_path: Path, point: str):
    tape = [*_setup(), _get("git/ref/heads/main", _ref()), *_disable(2)]
    position = {"after_inventory": 4, "before_disable": 6, "after_disable": 9}[point]
    tape[position]["response"] = _ref("c" * 40)
    tape = tape[: position + 1]
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert "Main changed" in plan["error"]
    assert plan["disabled_ids"] == ([2] if point == "after_disable" else [])
    assert calls == [step["args"] for step in tape]


@pytest.mark.parametrize(
    "workflow",
    [
        _workflow(2, KEPT),
        _workflow(2, "dynamic/generated"),
        _workflow(3, OLD),
        _workflow(2, OLD, "disabled_manually"),
        {},
    ],
)
def test_changed_workflow_identity_aborts_before_write(tmp_path: Path, workflow: object):
    tape = [*_setup(), _get("git/ref/heads/main", _ref()), _get("actions/workflows/2", workflow)]
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert plan["disabled_ids"] == []
    assert calls == [step["args"] for step in tape]


@pytest.mark.parametrize(
    "inventory",
    [
        [],
        {},
        [{}],
        [_page()],
        [_page(_workflow(2, OLD), count=2)],
        [_page(_workflow(2, OLD), count=True)],
        [_page(_workflow(True, OLD))],
        [_page(_workflow(2, OLD), _workflow(2, OLD))],
        [_page(_workflow(2, OLD, ""))],
        [_page(_workflow(2, ""))],
        [_page(_workflow(2, ".github/workflows/../ci.yml"))],
        [_page(_workflow(2, OLD), count=2), _page(_workflow(3, OLD), count=3)],
    ],
)
def test_incomplete_or_malformed_inventory_never_writes(tmp_path: Path, inventory: object):
    tape = _setup(inventory=inventory)
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert plan["disabled_ids"] == []
    assert "error" in plan
    assert calls == [step["args"] for step in tape]


@pytest.mark.parametrize(
    "tree",
    [
        {},
        _tree(),
        {**_tree(KEPT), "truncated": True},
        {**_tree(KEPT), "sha": "c" * 40},
        _tree("README.md"),
        {**_tree(KEPT), "tree": [{"path": KEPT, "type": "blob", "mode": "120000"}]},
        _tree(KEPT, KEPT),
    ],
)
def test_untrusted_or_empty_main_tree_never_reads_registry_or_writes(tmp_path: Path, tree: object):
    tape = _setup(tree=tree)[:3]
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert plan["disabled_ids"] == []
    assert calls == [step["args"] for step in tape]


def test_api_failure_stops_later_disable_and_retains_completed_ids(tmp_path: Path):
    inventory = [_page(_workflow(2, OLD), _workflow(3, ".github/workflows/old.yml"))]
    tape = [*_setup(inventory=inventory), _get("git/ref/heads/main", _ref()), *_disable(2)]
    tape.append({**_get("actions/workflows/3", None), "exit": 1})
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert plan["disabled_ids"] == [2]
    assert calls == [step["args"] for step in tape]


@pytest.mark.parametrize("disable", ["yes", "1", "TRUE"])
def test_invalid_disable_flag_never_calls_github(tmp_path: Path, disable: str):
    result, plan, calls = _run(tmp_path, [], disable=disable)
    assert result.returncode != 0
    assert "DISABLE must be true or false" in result.stderr
    assert plan == {}
    assert calls == []


def test_no_obsolete_workflows_requires_no_mutation(tmp_path: Path):
    second = ".github/workflows/full.yaml"
    tape = [
        *_setup(
            tree=_tree(KEPT, second), inventory=[_page(_workflow(1, KEPT), _workflow(2, second))]
        ),
        _get("git/ref/heads/main", _ref()),
    ]
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode == 0, result.stderr
    assert plan["disable_ids"] == plan["disabled_ids"] == []
    assert calls == [step["args"] for step in tape]


@pytest.mark.parametrize(
    ("position", "response"),
    [
        (0, {}),
        (0, {**_ref(), "ref": "refs/heads/other"}),
        (0, {"ref": "refs/heads/main", "object": {"type": "tag", "sha": MAIN}}),
        (0, _ref("not-a-sha")),
        (1, {}),
        (1, {"sha": "c" * 40, "tree": {"sha": TREE}}),
        (1, {"sha": MAIN, "tree": {"sha": ""}}),
    ],
)
def test_invalid_live_main_metadata_aborts_before_registry(
    tmp_path: Path, position: int, response: object
):
    tape = _setup()[: position + 1]
    tape[position]["response"] = response
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert plan["disabled_ids"] == []
    assert calls == [step["args"] for step in tape]


def test_failed_disable_records_uncertain_request_and_stops(tmp_path: Path):
    tape = [*_setup(), _get("git/ref/heads/main", _ref()), *_disable(2)[:3]]
    tape[-1]["exit"] = 1
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert plan["disabled_ids"] == []
    assert plan["pending_disable_id"] == 2
    assert calls == [step["args"] for step in tape]


@pytest.mark.parametrize(
    "readback",
    [
        _workflow(2, OLD),
        _workflow(2, OLD, "disabled_inactivity"),
        _workflow(3, OLD, "disabled_manually"),
        _workflow(2, KEPT, "disabled_manually"),
        _workflow(2, "dynamic/generated", "disabled_manually"),
        {},
    ],
    ids=["still-active", "other-reason", "wrong-id", "wrong-path", "dynamic-path", "malformed"],
)
def test_disable_requires_confirmed_readback_before_clearing_pending(
    tmp_path: Path, readback: object
):
    tape = [*_setup(), _get("git/ref/heads/main", _ref()), *_disable(2)[:4]]
    tape[-1]["response"] = readback
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert plan["disabled_ids"] == []
    assert plan.get("pending_disable_id") == 2
    assert "error" in plan
    assert calls == [step["args"] for step in tape]


def test_failed_readback_retains_pending_and_stops_without_retry(tmp_path: Path):
    tape = [*_setup(), _get("git/ref/heads/main", _ref()), *_disable(2)[:4]]
    tape[-1]["exit"] = 1
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert plan["disabled_ids"] == []
    assert plan["pending_disable_id"] == 2
    assert "error" in plan
    assert calls == [step["args"] for step in tape]


def test_later_readback_failure_preserves_prior_confirmed_disable(tmp_path: Path):
    second = ".github/workflows/old.yml"
    inventory = [_page(_workflow(2, OLD), _workflow(3, second))]
    tape = [
        *_setup(inventory=inventory),
        _get("git/ref/heads/main", _ref()),
        *_disable(2),
        *_disable(3, second)[:4],
    ]
    tape[-1]["response"] = _workflow(3, second)
    result, plan, calls = _run(tmp_path, tape, disable="true")
    assert result.returncode != 0
    assert plan["disabled_ids"] == [2]
    assert plan["pending_disable_id"] == 3
    assert "error" in plan
    assert calls == [step["args"] for step in tape]
