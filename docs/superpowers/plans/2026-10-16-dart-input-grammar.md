# Dart input grammar ownership Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Remove the 31 written prefix/suffix control comparisons from the guarded Dart Python implementation while retaining actual Dart behavior and conservative evidence.

**Architecture:** Existing syntax owns the single name-to-Visibility ingress; immutable bindings carry the resulting nominal value. Existing parser owns comment delimiters and formatting lexemes. Snapshot owns filename and pubspec input grammar; resolver uses semantic path APIs, its existing URI/type domains and actual parser CALL/computed facts. No source module, AST framework or coverage authority is added.

**Tech Stack:** Python 3.11, pinned tree-sitter-dart, standard pathlib, existing HRC Target/native observer, remote GitHub and hosted Actions only.

**Spec:** Root-approved four-owner design and compatible public DTO decision, recorded below; existing docs/architecture/dart-nominal-controls.md and dart-python-target.md remain behavioral constraints.

## Global Constraints

- Source inventory base: 0e3b8a7f62b9b13417cda78e11b52d0de82986cd.
- Native prefix observer is the separate f624d99286983fa0e26aff5e87835c359ba63d55 overlay, not an unclaimed existing Dart-project capability.
- 31 new guarded violations: collect 4, parse 15, resolve 10, snapshot 2 (38966921173/job117195558561). No whitelist, guard reduction, raw Final alias, cast/Any/ignore or accepted new debt.
- Public frozen/slotted ResolvedBinding retains its exact seven positional/keyword fields; visibility is init=False and recomputed once at each binding ingress, including dataclasses.replace(name=...).
- Names, paths, IDs and excerpts remain data. Open filename/URI grammar is decoded at its owner; later closed decisions use actual nominal values or existing semantic APIs.
- No new Site receiver-form field: existing computed and exact CALL inventory own that evidence. Do not invent a call solely from closing punctuation.
- Unknown, ambiguous, incomplete, external and malformed inputs stay conservative. No new resolution/analysis authority or forced UNKNOWN-to-PASS change.
- Product branches contain no auxiliary workflow. Root coordinates final independent Astra and integration.

## Review Focus

- Visibility uses the final written qualified-name segment, including Unicode, named/unnamed private constructors and private owner/public member distinctions.
- Old ResolvedBinding seven-field constructors, replace(name=private/public), frozen and slots behavior remain valid.
- Nested comments, comment-looking string contents, raw/triple strings and unclosed block comments preserve source spans and parser concerns.
- Hidden .dart and malformed *.dart names remain selected for the existing validation/problem path; suffix migration must not silently omit them.
- Constructed receivers must have real bounded parser CALL evidence; computed/index, missing/ambiguous calls, closures and incomplete syntax cannot acquire invented targets.

## Owner ports and consumers

1. syntax.py: Visibility.from_name(spelling: str) -> Visibility, backed by the one private name-start token domain. Parser declaration/member producers, synthetic enum/import/binding Fact producers and ResolvedBinding ingress use this decoder. Resolver construction privacy and accessibility consumers read ResolvedBinding.visibility.
2. resolve.py: ResolvedBinding.visibility: Visibility = field(init=False), set only in __post_init__; existing 9 construction sites retain their seven arguments. Existing _TypeToken handles final generic punctuation. Path.is_absolute/is_relative_to replace prefix safety checks. UriScheme remains at the actual resolver owner: snapshot has no URI consumer.
3. parse.py: private _CommentDelimiter and _comment_delimiter(data: bytes, index: int) -> _CommentDelimiter | None are consumed by the existing unclosed-comment and trivia loops; existing _Lexeme handles parameter delimiters, nullable marker and canonical comma/dot punctuation. Actual CONST node kinds classify constructors. Existing CALL/computed facts are sufficient for resolver receivers.
4. snapshot.py: private nominal source suffix decoder consumes filenames (including .dart); the existing pubspec parser owns complete empty/comment-line grammar. Canonical ResolutionRole and RuntimeRequirementState remain shared unchanged.

No import edge is added: parse -> syntax, resolve -> syntax + snapshot, collect -> all three already exist. No new public module or second vocabulary inventory is introduced. Expected production cost before real measurement: approximately 80-130 net lines, mainly explicit typed ingress; exact diff and runtime cost must be reported.

## Task 1: Native RED and preserved behavior

- [x] Commit this plan and actual behavior/API probes before product code.
- [x] Run the unchanged native Dart guard against the real f624 observer overlay; print trace-valid rows with exact source spans, rules and construct IDs.
- [x] Observe actual missing Visibility ingress/field failures and constructor const-prefix false-positive; retain passing comment/string controls.
- [x] Inventory actual tracked ResolvedBinding/Site construction and documented API usage with git grep, not assumptions.

## Task 2: Minimal owned grammar and authored ports

- [ ] Publish new Visibility ingress/derived binding field in the existing Dart Target before implementing them; actual source-widening mutations must fail under unchanged authored intent.
- [ ] Implement the four owner changes without extra state, reader-side private-name parsing, duplicate enum/string inventories or an AST framework.
- [ ] Run new and existing Dart parser/resolver/directive/snapshot/SDK-free/partial-UML/false-positive/differential controls, Ruff, formatter and strict mypy.
- [ ] Prove all five existing whole-module Python guards pass under the real prefix observer and injected raw literal/Final/prefix/suffix controls remain trace-valid FAIL.

## Task 3: Freeze and independent review

- [ ] Compare complete actual Compass syntax/Facts/targets and relevant UNKNOWN semantics to the exact predecessor; explain any genuine corrections.
- [ ] Run Compass complete reports/browser acceptance, existing project suite and normal baseline/amendment/no-write with no increased budget.
- [ ] Record exact product/Target/test costs and parser/resolver runtime; freeze clean source without workflows.
- [ ] Hand source and genuine RED/GREEN evidence to Root for independent final Astra; create a Part of #542 PR only after approval, no self-merge.

## Decisions

Root explicitly approved inline plan/RED then implementation of these four existing owners. Public ResolvedBinding is exported by DART-RESOLUTION and authored with all seven fields in the Target, so a required eighth constructor argument was rejected. The compatible derived field performs one centralized decode per binding ingress; later resolver checks consume the typed value.
Root approved removal of the redundant receiver.endswith precheck in favor of the existing exact parser CALL inventory, and existing computed for index receivers; no additional Site API/state.

## Execution ledger

Actual RED 38973308034/job117216624183: 11 expected failures and 6 controls passed against unchanged Dart source. Missing owned Visibility ingress/field and the real lowercase constance() false-positive are reproduced. An initial probe used the wrong parser signature; that probe was corrected before this authoritative RED and no product code was written in between. Native job117216623885 reports the same 31 trace-valid existing prefix/suffix violations under the explicit f624 observer overlay. Actual tracked constructor inventory shows nine existing resolver producers and no earlier direct test constructor uses; HRC nevertheless explicitly exports the seven-field DTO, so compatibility is retained.
