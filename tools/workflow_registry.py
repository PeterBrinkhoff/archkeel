# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Disable obsolete file-backed Actions registrations; retain every historical run."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import NotRequired, TypedDict

_FILE = re.compile(r"\.github/workflows/[^/\\]+\.ya?ml")
_SHA = re.compile(r"[0-9a-f]{40}")


class _Registration(TypedDict):
    id: int
    path: str
    state: str


class _Receipt(TypedDict):
    repository: str
    disabled_ids: list[int]
    main_sha: NotRequired[str]
    main_paths: NotRequired[list[str]]
    observed_count: NotRequired[int]
    disable_ids: NotRequired[list[int]]
    workflows: NotRequired[list[_Registration]]
    pending_disable_id: NotRequired[int]
    error: NotRequired[str]


def _api(repository: str, path: str, *, pages: bool = False, disable: bool = False) -> object:
    flags = ["--method", "PUT"] if disable else ["--paginate", "--slurp"] if pages else []
    result = subprocess.run(
        ["gh", "api", *flags, f"repos/{repository}/{path}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return None if disable else json.loads(result.stdout)


def _sha(value: object) -> str:
    if not isinstance(value, str) or not _SHA.fullmatch(value):
        raise ValueError("expected a full Git object SHA")
    return value


def _main_sha(repository: str) -> str:
    ref = _api(repository, "git/ref/heads/main")
    if not isinstance(ref, dict) or ref.get("ref") != "refs/heads/main":
        raise ValueError("expected the live Main ref")
    target = ref.get("object")
    if not isinstance(target, dict) or target.get("type") != "commit":
        raise ValueError("Main must reference a commit")
    return _sha(target.get("sha"))


def _main_paths(repository: str, main_sha: str) -> list[str]:
    commit = _api(repository, f"git/commits/{main_sha}")
    if not isinstance(commit, dict) or commit.get("sha") != main_sha:
        raise ValueError("Main commit identity mismatch")
    tree_ref = commit.get("tree")
    if not isinstance(tree_ref, dict):
        raise ValueError("Main commit tree is missing")
    tree_sha = _sha(tree_ref.get("sha"))
    tree = _api(repository, f"git/trees/{tree_sha}?recursive=1")
    if (
        not isinstance(tree, dict)
        or tree.get("sha") != tree_sha
        or tree.get("truncated") is not False
        or not isinstance(tree.get("tree"), list)
        or not tree["tree"]
    ):
        raise ValueError("expected a complete nonempty Main tree")
    paths: set[str] = set()
    seen: set[str] = set()
    for entry in tree["tree"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ValueError("tree entry must have a path")
        path = entry["path"]
        if not path or path in seen or any(part in ("", ".", "..") for part in path.split("/")):
            raise ValueError("tree paths must be unique and relative")
        seen.add(path)
        if _FILE.fullmatch(path):
            if entry.get("type") != "blob" or entry.get("mode") not in ("100644", "100755"):
                raise ValueError("Main workflow must be a regular file")
            paths.add(path)
    if not paths:
        raise ValueError("Main must contain workflow files")
    return sorted(paths)


def _workflow(value: object) -> tuple[int, str, str]:
    if not isinstance(value, dict):
        raise ValueError("workflow must be an object")
    identifier, path, state = value.get("id"), value.get("path"), value.get("state")
    if isinstance(identifier, bool) or not isinstance(identifier, int) or identifier <= 0:
        raise ValueError("workflow id must be a positive integer")
    if not isinstance(path, str) or not path or not isinstance(state, str) or not state:
        raise ValueError("workflow path and state must be nonempty strings")
    if path.startswith(".github/workflows/") and not _FILE.fullmatch(path):
        raise ValueError("file-backed workflow path must be a direct YAML file")
    return identifier, path, state


def _obsolete(inventory: object, main_paths: list[str]) -> tuple[int, list[tuple[int, str, str]]]:
    if not isinstance(inventory, list) or not inventory:
        raise ValueError("expected nonempty paginated workflow responses")
    total: int | None = None
    seen: set[int] = set()
    selected: list[tuple[int, str, str]] = []
    for page in inventory:
        if not isinstance(page, dict) or not isinstance(page.get("workflows"), list):
            raise ValueError("workflow page must contain a workflows list")
        count = page.get("total_count")
        if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            raise ValueError("workflow total_count must be a positive integer")
        if total is not None and total != count:
            raise ValueError("workflow total_count changed during pagination")
        total = count
        for value in page["workflows"]:
            workflow = _workflow(value)
            identifier, path, state = workflow
            if identifier in seen:
                raise ValueError("workflow ids must be unique across pages")
            seen.add(identifier)
            if state == "active" and _FILE.fullmatch(path) and path not in main_paths:
                selected.append(workflow)
    if len(seen) != total:
        raise ValueError("workflow pagination is incomplete")
    return len(seen), sorted(selected)


def _require_main(repository: str, expected: str) -> None:
    if _main_sha(repository) != expected:
        raise ValueError("Main changed; stop and regenerate the plan")


def _write(output: Path, receipt: _Receipt) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    temporary.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output)


def reconcile(repository: str, output: Path, *, disable: bool) -> _Receipt:
    receipt: _Receipt = {"repository": repository, "disabled_ids": []}
    try:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) or any(
            part in (".", "..") for part in repository.split("/")
        ):
            raise ValueError("repository must be owner/name")
        main_sha = _main_sha(repository)
        receipt["main_sha"] = main_sha
        paths = _main_paths(repository, main_sha)
        inventory = _api(repository, "actions/workflows?per_page=100", pages=True)
        count, obsolete = _obsolete(inventory, paths)
        receipt["observed_count"] = count
        receipt["main_paths"] = paths
        receipt["disable_ids"] = [item[0] for item in obsolete]
        receipt["workflows"] = [
            {"id": item[0], "path": item[1], "state": item[2]} for item in obsolete
        ]
        _write(output, receipt)
        _require_main(repository, main_sha)
        if disable:
            for workflow in obsolete:
                identifier = workflow[0]
                current = _workflow(_api(repository, f"actions/workflows/{identifier}"))
                if current != workflow:
                    raise ValueError("workflow identity or state changed; regenerate the plan")
                # GitHub offers no transaction joining the ref check and disable request.
                _require_main(repository, main_sha)
                receipt["pending_disable_id"] = identifier
                _write(output, receipt)
                _api(repository, f"actions/workflows/{identifier}/disable", disable=True)
                disabled = _workflow(_api(repository, f"actions/workflows/{identifier}"))
                if disabled != (identifier, workflow[1], "disabled_manually"):
                    raise ValueError("workflow disable readback did not confirm identity and state")
                receipt["disabled_ids"].append(identifier)
                del receipt["pending_disable_id"]
                _write(output, receipt)
                _require_main(repository, main_sha)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        receipt["error"] = str(error)
        _write(output, receipt)
        raise
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--disable", action="store_true")
    args = parser.parse_args()
    try:
        receipt = reconcile(args.repository, args.output, disable=args.disable)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        parser.error(str(error))
    print(
        json.dumps(
            {
                "main_sha": receipt["main_sha"],
                "disable_ids": receipt["disable_ids"],
                "disabled_ids": receipt["disabled_ids"],
            }
        )
    )
    if not args.disable:
        print(f"Dry run: review {args.output}; rerun with DISABLE=true to disable selected IDs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
