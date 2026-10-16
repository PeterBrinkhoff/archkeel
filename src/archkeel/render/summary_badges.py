# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Own the display Badge and its projection from existing verdict domains."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from archkeel.ir.architecture_graph import AssessmentStatus


class BadgeState(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    INFO = "info"
    UNKNOWN = "unknown"


class _BadgeMarker(StrEnum):
    NOT_APPLICABLE = "n/a"


@dataclass(frozen=True, slots=True)
class Badge:
    state: BadgeState
    symbol: str
    label: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, BadgeState):
            object.__setattr__(self, "state", BadgeState(self.state))


def badge(value: str) -> Badge:
    """Project recognized verdict text; preserve the legacy fallback for other data."""
    try:
        status = AssessmentStatus(value)
    except ValueError:
        try:
            _BadgeMarker(value)
        except ValueError:
            return Badge(BadgeState.UNKNOWN, "?", "NOT CHECKED")
        return Badge(BadgeState.INFO, "i", "NOT APPLICABLE")
    if status is AssessmentStatus.PASS:
        return Badge(BadgeState.PASS, "✓", "PASS")
    if status is AssessmentStatus.FAIL:
        return Badge(BadgeState.FAIL, "×", "FAIL")
    return Badge(BadgeState.UNKNOWN, "?", "UNKNOWN")
