# Summary Badge Types Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Give the actual Badge value and display derivation one nominal Summary owner, preserving valid constructor and rendering behavior.
**Architecture:** render.summary_badges owns BadgeState, Badge and badge; render.summary explicitly reexports existing objects. The existing Summary component owns both modules; terminal and HTML use the direct canonical owner.
**Tech Stack:** Python 3.11+, StrEnum, frozen dataclasses, pytest, native Archkeel observation and Chromium.
**Spec:** docs/architecture/summary-badges.md and the approved bounded #542 Presentation scope.

## Global constraints

- Preserve valid Badge string arguments, badge input text, labels, symbols, HTML attributes and terminal colors.
- Reuse architecture_graph.AssessmentStatus and RuleAssessmentStatus; never merge binary Verdict and presentation states.
- No casts, Any, ignored errors, generic decoder facade, raw/Final-string control comparisons, .value comparisons or increased budgets.
- No whole-summary, whole-HTML, whole-render or JavaScript absence claims.
- Preserve independently changed canonical Diagnostic imports and Root/Makefile/IR additions when integrating.
- Remote GitHub isolation and Actions only.

## Review focus

- Invalid legacy wire text must keep NOT CHECKED rather than raise.
- Known direct Badge string states remain accepted and normalized.
- Declaration assessments retain info styling independently from three-valued assessments.
- Existing summary.Badge and summary.badge remain exact object identities.
- A source field or return widened to str must fail against unchanged authored intent.

### Task 1: Own the Badge value and real derivation

**Files:** create src/archkeel/render/summary_badges.py, tests/test_summary_badge_types.py and tests/test_summary_badge_target.py; modify render/summary.py, render/terminal.py, render/html.py and docs/architecture/contracts/render.json. Root enum placement and Makefile deltas are additive.

**Interfaces:** BadgeState(StrEnum): PASS=pass, FAIL=fail, INFO=info, UNKNOWN=unknown. Badge.state: BadgeState; symbol: str; label: str. badge(value: str) -> Badge. Existing summary Badge/badge names explicitly reexport the same objects; State remains a compatibility alias.

- [x] Write direct constructor/projection identity and legacy-wire tests; run unchanged production and observe assertion RED.
- [x] Author a bounded independent Badge Target plus complete-module guard; run actual unchanged source and observe native intent RED.
- [x] Implement the focused value, normalization and derivation using the canonical AssessmentStatus and a bounded private n/a projection marker.
- [x] Move real consumers to the direct owner; use canonical RuleAssessmentStatus.DECLARATION for its info presentation.
- [x] Observe actual source; mutate Badge.state and badge return to str and replace real factory control with literal equality, membership, match, Final and local aliases while intent bytes stay fixed.
- [x] Run compatibility, native mutations, strict mypy/Ruff and hierarchy/public-interface checks.

### Task 2: Verify presentation and freeze the independent increment

- [x] Compare real before/after HTML and terminal bytes for existing pass/fail/unknown/not-applicable and declaration cases; run affected Chromium checks.
- [x] Run native own observation without extra allowances or budget increases and log actual measurements/sites. Root owns the fresh exact-parent normal amendment after targeted stack union.
- [x] Deliver the frozen feature-only carrier, Part of #542, with explicit dependency and hosted receipts; Root owns final union, PR and normal amendment before independent Astra review.

## Pre-flight ruling

A class/method-only construct scope cannot currently prove absence. The focused module must therefore own the actual Badge model and derivation; an enum-only side module would leave the real control unguarded. Remaining result/command formatting stays a separately named follow-up.
