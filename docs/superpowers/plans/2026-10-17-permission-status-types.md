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

- [x] Add actual legacy constructor, invalid-value, producer-state and JSON controls; pin the canonical enum and actual status field in independent authored intent.
- [x] Run the unchanged production source in an isolated Actions checkout; record assertion/type-comparison REDs, not unrelated errors.
- [x] Commit tests/intent independently. Keep the fixed intent unchanged for subsequent source mutations.

## Task 2: Canonical owner and consumers

**Files:** ir/architecture_projection.py; ir/report_projection.py; render/atlas.py; ir/command_view.py; necessary root enum placement/public port declarations.
**Interfaces:** PermissionStatus(StrEnum), PermissionProjection.status: PermissionStatus, existing constructor normalization.
**Shared interface check:** Task1's fixed PermissionStatus/PermissionProjection names are exactly Task2's owner and field; no new module or alternate name.

- [x] Replace the alias with the three-member enum and normalize the real existing DTO constructor once with canonical builtins.object.__setattr__.
- [x] Use the enum in four actual producer branches, four permission decisions, the existing command grouping decision and the single Atlas allowed decision; preserve the existing serializer.
- [x] Run Task1 GREEN; count source changes and native call-site/UNKNOWN deltas before freezing.

## Task 3: Permanent guards, verification and review

**Files:** tests/test_permission_status_types.py; Makefile and only necessary authored Target/guard declarations; generated native baseline/amendment; this ledger.

- [x] Mutate the actual status annotation to str and real constructor controls to raw equality/membership/local-alias/match under unchanged authored intent; require trace-valid native failures.
- [x] Run relevant projection/command/result/Atlas suites, strict checks and the actual required report path; verify predecessor/new permission JSON and balances.
- [x] Generate the ordinary baseline/amendment against the exact 5fc94c10298c4bbcd98fd44f8ac72b321b03a0b4 predecessor; run identical NoWrite, document actual sites and budgets.
- [ ] Run the appropriate project suite, freeze a separate Part-of-542 PR, obtain independent Astra review and hand Root the exact immutable delta for integration.

## Execution ledger

Base: 5fc94c10298c4bbcd98fd44f8ac72b321b03a0b4. Its inherited integration receipt is not assumed valid; this stage generates its own normal receipt against that actual predecessor.

Ruling: the parent requires remote GitHub/Actions only, so isolation uses this dedicated feature branch and fresh Actions checkouts rather than local worktree/scripts. No shared Root/Main/Publisher refs are mutated. The skill's auxiliary writing-good-tests resource is unavailable; the main TDD rules remain applied. Design and inline execution were explicitly authorized before this plan.

Task1 RED: run38987444254 / job117262089955 observed exactly11 assertion failures and1 passing whole-module guard control on unchanged production. Known constructors/actual producers still held plain strings, invalid values were accepted, PermissionStatus was not an enum, and the independent native comparison was genuinely FAIL (not an unrelated parse error or absent-module UNKNOWN). The fixed Target and actual original source are retained for GREEN/mutation proofs.

Task2 ruling: the first GREEN attempt passed115 tests but exposed a real outer IR interface violation and two invalid new test assumptions. The canonical enum must be published at both the existing inner Governance and outer IR facade, because Atlas actually imports it. The established command wire groups target_ids, so the new assertion now reads that real facade rather than inventing target_id rows. An additional existing command_view._permission_groups decision already consumes PermissionStatus and is migrated in the same small boundary; the actual grouped value is checked nominal. No second normalization is added to this derived internal DTO, whose producer already supplies the canonical state. No global fixture/assertion is loosened.

Task2 GREEN: run38987966991 / job117263742098 passed all118 focused/native/projection/Core-command tests, Ruff512 and mypy150. Every authored source mutation passed its negative obligation under unchanged intent. The outer interface violation is repaired through the actual IR PermissionStatus port; no fixture or global verdict was relaxed. Product source is frozen for subsequent required gates and independent review.


Task3 native/report proof: frozen product bcf1d367a2f742ba98cb85d4bad1e4991c1dbd31 was checked by run [38988511389](https://github.com/rapiddweller/archkeel/actions/runs/38988511389). Ordinary baseline writing, amendment writing against exact5fc94c10298c4bbcd98fd44f8ac72b321b03a0b4 and identical NoWrite all exited0 in job117265423455, with838 unresolved calls,52 typing positions,58 UNKNOWN positions and0 violations. The generated baseline is byte-identical to the predecessor baseline; the normal amendment is committed verbatim from the runner. No allowances or budgets changed. Widenings, failures and diagnostics were empty; unresolved_call_changes and unresolved_call_note were null.

Actual site proof: the original job117265423706 established unchanged AD-100 unresolved identities/counts and unchanged PARTIAL count; it did not compare PARTIAL identities or reasons. This evidentiary overstatement was caught during review. A fresh exact5fc→clean-c50 comparison in [run38992741508/job117278462285](https://github.com/rapiddweller/archkeel/actions/runs/38992741508/job/117278462285) explicitly compares the multiset of every unresolved and PARTIAL row over status, path, caller, expression, reason and component. Added/removed semantic rows are empty. Full rows including source line differ at8 positions:6 PARTIAL and2 UNRESOLVED calls in report_projection move forward2 lines; the actual expressions, reasons, ownership, status and multiplicity are unchanged. UNKNOWN record-ID counters have no additions/removals, which does not claim complete UNKNOWN payload equality. Total calls18892→18894; the actual PermissionStatus and builtins.object.__setattr__ calls in the new normalizer are both recorded as resolved. Required report job117265423327 passed5 Publisher tests and81 report tests; the unchanged authentic repository2MB/400KB budget control passed separately. No browser asset or generator changed.

Broader verification exposed inherited test dependencies: required ci-pr-check passed4200 tests with1 skip, but failed the existing NameBudgetKind Literal/get_args catalog assertion and three existing render-direction fixture cases; an auxiliary-only Python script also lacked its license header. Run [38992319771](https://github.com/rapiddweller/archkeel/actions/runs/38992319771), job117277184706, reproduced all four assertion failures on the exact unchanged5fc predecessor, then passed17 Navigation/catalog/hygiene controls after supplying the actual guarded Atlas owner/spec and using nominal enum iteration. The feature carries the separately Astra-reviewed catalog correction exactly from3e50a1764bffa24100892bf231e208e15919dacc, plus the narrowly corrected render fixture from809263d0b311033428b54f05a396032a39da25ef. No expectations, direction assertions, contracts or policies were weakened. These are test-only dependency corrections; Permission product remains frozen. The final required core rerun and independent final Astra review remain pending.

Cost: manual Python product source +24/-13 (net+11), including all real consumers. architecture_projection grows147→156 lines. No new product module, browser domain, asset, generation framework or historical snapshot. Tests and independently authored intent are counted separately from product source. Whole-module raw-literal absence is asserted only for architecture_projection; remaining report/UI/version domains are explicitly pending.


Exact clean receipt check: run38992556299/job117277902840 checked out c50c420b9a8909258864fe1946ba9df7ce039d88, passed34 focused/native/fixture/hygiene cases and512-file Ruff checks, then validated the committed ordinary receipt with --against exact5fc and no writer. Exit0,838/52/58/0, empty diagnostics/failures/widenings, null unresolved_call_changes/note, clean git diff. Required core job117277902619 remains running; no complete-core or merge approval is claimed.
