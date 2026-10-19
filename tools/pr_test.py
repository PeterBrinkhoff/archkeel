# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Run the existing PR test selection, optionally across two file-preserving shards."""

import argparse
import os
import sys
from collections.abc import Sequence


def select_files(selectors: list[str], shard: int | None) -> list[str]:
    if shard not in (None, 0, 1):
        raise ValueError("shard must be 0 or 1")
    files: dict[str, int] = {}
    selected: list[str] = []
    for selector in selectors:
        filename = selector.partition("::")[0]
        if not filename or selector.startswith("-"):
            raise ValueError("explicit pytest file selectors are required")
        group = files.setdefault(filename, len(files))
        if shard is None or group % 2 == shard:
            selected.append(selector)
    if not selected:
        raise ValueError("the test selection or requested shard is empty")
    return selected


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shard", type=int)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if not args.arguments or args.arguments[0] != "--":
        parser.error("separate pytest options and file selectors with --")
    try:
        separator = args.arguments.index("--", 1)
        selected = select_files(args.arguments[separator + 1 :], args.shard)
    except ValueError as error:
        parser.error(str(error))
    os.execv(
        sys.executable, [sys.executable, "-m", "pytest", *args.arguments[1:separator], *selected]
    )


if __name__ == "__main__":
    main()
