# PermissionStatus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Give component-pair permission states their existing canonical nominal owner and migrate actual consumers.
**Architecture:** Keep PermissionStatus and PermissionProjection together in architecture_projection; normalize existing constructors once using the established canonical builtins pattern. Producers and Atlas consume the same enum; existing JSON serialization remains the wire adapter.
**Tech Stack:** Python 3.11+, dataclasses, StrEnum, native Python observation/HRC, existing pytest/Actions gates.
**Spec:** docs/superpowers/specs/2026-10-17-permission-status-types.md

## Global Constraints

- Preserve exactly allowed/forbidden/undecided and existing valid constructor/wire behavior.
- Keep open identities/text as strings; no Any/casts/ignores or renamed string constants.
- At most 50 added manual product lines; no new module, browser vocabulary or generic framework.
- No allowance/budget increase or manual baseline/receipt editing.
- Whole-module native absence applies only to architecture_projection; other producer/render/version domains remain pending.

## Review Focus

- All three valid legacy strings normalize, retain frozen fields and produce identical ordered JSON.
- A nominal input retains identity; unsupported strings, zero and null reject.
- Open IDs, rule names and reasons may equal status spellings without conversion.
- Explicit forbidden rules and complete_requires both remain forbidden; observed use never closes an undecided pair.
- Root/nested Atlas balances and saved reports preserve their actual permissions and deviations.

## Task 1: Native and behavior RED

**Files:** tests/test_permission_status_types.py; authored additions in docs/architecture/contracts/ir.json; this spec/plan.
**Interfaces:** PermissionProjection(target_id, status, rule_ids, reason); fixed native enum/class/status-field intent.

- [ ] Add actual legacy constructor, invalid-value, producer-state and JSON controls; pin the canonical enum and actual status field in independent authored intent.
- [ ] Run the unchanged production source in an isolated Actions checkout; record assertion/type-comparison REDs, not unrelated errors.
- [ ] Commit tests/intent independently. Keep the fixed intent unchanged for subsequent source mutations.

## Task 2: Canonical owner and consumers

**Files:** ir/architecture_projection.py; ir/report_projection.py; render/atlas.py; necessary root enum placement/public port declarations.
**Interfaces:** PermissionStatus(StrEnum), PermissionProjection.status: PermissionStatus, existing constructor normalization.
**Shared interface check:** Task1's fixed PermissionStatus/PermissionProjection names are exactly Task2's owner and field; no new module or alternate name.

- [ ] Replace the alias with the three-member enum and normalize the real existing DTO constructor once with canonical builtins.object.__setattr__.
- [ ] Use the enum in four actual producer branches, four permission decisions and the single Atlas allowed decision; preserve the existing serializer.
- [ ] Run Task1 GREEN; count source changes and native call-site/UNKNOWN deltas before freezing.

## Task 3: Permanent guards, verification and review

**Files:** tests/test_permission_status_types.py; Makefile and only necessary authored Target/guard declarations; generated native baseline/amendment; this ledger.

- [ ] Mutate the actual status annotation to str and real constructor controls to raw equality/membership/local-alias/match under unchanged authored intent; require trace-valid native failures.
- [ ] Run relevant projection/command/result/Atlas suites, strict checks and the actual required report path; verify predecessor/new permission JSON and balances.
- [ ] Generate the ordinary baseline/amendment against the exact 5fc94c10298c4bbcd98fd44f8ac72b321b03a0b4 predecessor; run identical NoWrite, document actual sites and budgets.
- [ ] Run the appropriate project suite, freeze a separate Part-of-542 PR, obtain independent Astra review and hand Root the exact immutable delta for integration.

## Execution ledger

Base: 5fc94c10298c4bbcd98fd44f8ac72b321b03a0b4. Its inherited integration receipt is not assumed valid; this stage generates its own normal receipt against that actual predecessor.

Ruling: the parent requires remote GitHub/Actions only, so isolation uses this dedicated feature branch and fresh Actions checkouts rather than local worktree/scripts. No shared Root/Main/Publisher refs are mutated. The skill's auxiliary writing-good-tests resource is unavailable; the main TDD rules remain applied. Design and inline execution were explicitly authorized before this plan.
