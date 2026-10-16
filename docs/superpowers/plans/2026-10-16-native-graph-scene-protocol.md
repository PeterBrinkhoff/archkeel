# Native graph scene protocol Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Make the complete existing native graph scene projection consume precise nominal protocol values without changing graph identity or visible reports.

**Architecture:** Canonical Python Enums generate wire-identical TypeScript string enums and Map validation ports. A concrete protocol validates unknown input once and returns the original objects. The actual graph projection moves to a strictly checkJs-checked classic-JavaScript owner; Atlas/UI remain unchanged follow-ups.

**Tech Stack:** Python3.11+, TypeScript5.9.3, classic JavaScript, existing pytest/Playwright and GitHub Actions.

**Spec:** docs/superpowers/specs/2026-10-16-native-graph-scene-protocol.md

## Global Constraints

- No any, type-ignore, broad casts, duplicate spelling catalogs, schema-generation framework, bundler or cache framework.
- Canonical vocabularies remain in archkeel.ir.architecture_graph; arbitrary IDs/names/paths remain text.
- Preserve original graph/entity/site identity, full JSON, offline assets and Atlas clone behavior.
- Native JS/TS construct evidence is a separate PARTIAL capability; no whole-browser absence claim.
- No budget/allowance increases or historical JSON snapshots.

## Review Focus

- Same-spelling PASS in different status domains must be rejected statically.
- Unknown and malformed closed values must fail at ingress, including nested member/signature fields.
- Legacy supported graph schemas and valid optional metadata must keep working.
- Repeated projections and separately supplied graphs must retain stable identity without repeated full decoding.
- Full JSON, Mermaid, DOM/CSS, route/filter behavior and packaged asset load order must retain wire text.

## Task 1: Prove the missing real ingress behavior

Files: tests/test_graph_scene_protocol.py; this plan/spec. Auxiliary workflow stays off the product carrier.

- [ ] Write real scene.create runtime tests for invalid origin, entity kind, relationship kind/resolution, presence and comparison status.
- [ ] Run unchanged production source under Chromium. Expected: assertions fail because scene.create currently accepts those invalid values.
- [ ] Record the exact RED run/job and commit tests before product implementation.

Interfaces: consumes the actual current ArchkeelReportScene.create(data); expects unknown input to reject unsupported closed values.

## Task 2: Implement one complete native graph scene boundary

Files: tools/browser_graph_protocol.py; src/archkeel/render/assets/report-graph-vocabulary.ts (generated); report-graph-protocol.ts (concrete DTOs/codecs); report-graph-protocol.js (compiled artifact); report-graph-scene.js (existing projection moved and annotated); report-scene.js (delegate); html.py (asset ordering).

- [ ] Generate only graph Enum domains consumed by this boundary from their canonical classes.
- [ ] Define concrete Graph, Entity, Relationship, Signature, Assessment, SceneContext, SceneNode, SceneEdge and Scene DTOs and predicate-based unknown decoders that return the same objects.
- [ ] Extract existing graph/index/member/containment/projection operations to the actual new classic-JS owner. Replace domain control literals with canonical enum members; keep user string data.
- [ ] Run TypeScript5.9.3 strict checkJs on actual consumer source and protocol. Expected: no compiler errors.
- [ ] Run Task1 tests and existing renderer units. Expected: all valid behavior passes; invalid closed values reject; actual graph objects/full JSON remain unchanged.

Interfaces: protocol decodeReport(unknown), decodeGraph(unknown), decodeViewMode(unknown); projection create(unknown) and the existing native scene methods with concrete inputs/outputs.

## Task 3: Verify source guards, integration and shipping

Files: tests/test_graph_scene_protocol.py; tests/test_report_renderer_units.py (new asset dependency loader); Makefile (deterministic generation/typecheck entry); package acceptance only as necessary; this plan ledger.

- [ ] Mutate actual checked consumer field/return source to raw string, same-spelling wrong domain and widened return. Expected: real compiler errors under the fixed authored API expectations.
- [ ] Verify all generated values encode exactly, reject invalid/foreign inputs and survive structuredClone; zero-token test remains a regression control against accidental numeric migration.
- [ ] Regenerate and compare the actual TS/JS artifacts. Expected: byte-identical output; stale-source mutation fails.
- [ ] Run existing Scene/Mermaid, own graph, navigation, filter Chromium tests; assert original object identity and full JSON before/after repeated projection.
- [ ] Build wheel/sdist and verify the actual protocol/projection assets ship and load offline.
- [ ] Record source cost and same-data initialization/projection timing; run Ruff/mypy/hygiene and the appropriate existing regression gate. Root owns fresh composite native gate, exact amendment and independent final Astra review.

## Pre-flight / ledger

- Task2 produces the precise ports consumed by Task3; Task3 mutations target actual source, not a handwritten substitute.
- The existing Flow/API consumes the same primitive string spellings, so no graph copy or output adapter is needed.
- Pending evidence is explicitly unchecked; no completion claim until actual hosted checks are read.

## Size-budget refinement (accepted by Root)

The measured frozen first candidate was 2,029,535 bytes, above both unchanged 2MB/400KB report budgets. Remove the 24 unused generated per-enum decode/encode wrappers; canonical nominal Enums and concrete membership predicates remain. Test invalid numeric status at the real comparison ingress and primitive wire text at actual JSON serialization. Independently measure an auxiliary AST-only publication print with optimization and mangling disabled; do not introduce a production build artifact or packaging change before separate review. Layout deduplication is an independent Root change and is not included here.

## Verification ledger

- Original unchanged source RED: run38966843115/job117195309326, seven real invalid-ingress assertion failures.
- Nominal string-enum feasibility: run38966562360/job117194361254, four genuine TS2322 controls including identical PASS in different domains.
- Reduced protocol: run38971736988/job117211476277,28 runtime/actual-source compiler mutation tests pass. The follow-on lint identified one embedded JavaScript test line over100 columns; that line is now split without behavior change.
- Actual native source mutation: run38971736988/job117211475912, original0 to mutated1 record at src/scene.js:74, capabilityPARTIAL, no absence PASS claim. The independent observer dependency is auxiliary and is not part of this product carrier.
- Final Python/style/artifact generation check: run38972273073/job117213240384, Ruff484, mypy145 plus strict generator,11 hygiene tests pass. Committed generated bytes come directly from that runner; a final check-only reproduction is required after committing them.
- Actual unchanged size guard remains blocked at2,024,087 bytes total and414,380 bytes without ELK on this source basis. The2MB/400KB limits are unchanged. Separate AST publication measurement is auxiliary only and has not changed packaged assets.
- Same29,834,964-byte OwnGraph (11,589 entities/30,741 relationships/224 cards): five-sample medians before create0.068ms, first187.048ms, repeat150.254ms; after create26.351ms, first178.237ms, repeat139.002ms. Full scene values/Mermaid and original graph/entity/input identity match. Timing varies between runs; no general speedup claim.

## Astra compatibility correction

Astra found that the original exposed projection accepted omitted options, an empty options object, directChildren-only options and an explicit undefined viewMode. Actual old-versus-frozen-source RED run38973113521/job117215992808 proved all four original calls matched explicit diagram mode while the frozen candidate threw TypeError. Test commit8aeff5b pins those real defaults in the independently authored TypeScript consumer and a permanent Chromium regression. Options and its viewMode are genuinely optional again; only absent/undefined mode normalizes to the existing DIAGRAM enum before strict decoding. Explicit invalid modes remain rejected. Source guards target the corrected actual optional declaration.


## Compatibility follow-up: existing Evidence views

Source851 rejected the existing visible Actual/Structure/Review buttons because its new ingress confused the six public report views with the three internal graph projection modes. The actual old/new VM programs prove all three old views valid and all three new calls throwing TypeError (run38978583933/job117233832671). Source851 and source union32d3 are superseded pending this correction; Publisher remains independent.

1. Add real visible-button regression controls against the unchanged851 source and observe their causal RED.
2. Close the actual six-valued public ViewMode domain, then map its three Evidence members explicitly to the existing Diagram projection. Keep ProjectionMode a precise three-member subset of that same nominal Enum, with no duplicated spelling catalog; reject unknown ingress values.
3. Require actual consumer return/subset mutations, legacy defaults, all six views and visible buttons; regenerate committed protocol with the existing official compiler. Run strict Scene and existing Chromium controls, then independent Astra review of this exact delta. Preserve original wire/object identity, no extra graph walk or copy, no Publisher changes.


## Final source freeze and required-gate evidence

The reviewed production source is `43303448ba681991e21f8975f2c3302139041bb0`, compared to the pinned `d08dfaf6a2e6992153a434341465306a88d993a2` review predecessor. Independent Astra approved that exact source after the Evidence-view compatibility and canonical-owner CI corrections. This ledger update changes documentation only.

- Actual public API RED: run 38978583933 / job 117233832671, all three existing Evidence views valid before and rejected by 851. Actual visible-button RED: run 38978975180 / job 117235096769, three corresponding failures.
- Corrected real consumer, compiler mutations, ingress, defaults, identity and visible buttons: run 38979366897 / job 117236335652, 34 PASS; a second actual Chromium job 117236335816 adds 18 PASS. Legacy old/new Evidence JSON remains identical.
- Required routing RED: run 38980587252 / job 117240264357, the actual Python Enum owner failed report classification. Correction GREEN: run 38980779299 / job 117240887586, 75 PASS, Ruff and mypy 145. Source artifact inputs and the real owner now trigger the required report path.
- Final actual required entry on 43303448, run 38980693700 / job 117240613702: unmodified `make ci-pr-report-check` passes 71 tests in 312.07s, with strict generation/checkJs checks, then 86 CI/repository controls pass. Ruff reports 484 formatted files and all checks passing; mypy reports 145 source files clean. The runner verifies no generated asset, independent Target or generator mutation. Auxiliary commit `458add8b7432b41b8bfc3bad879ae570765176cd` differs from 43303448 only by its verification workflow.
- The correction adds 433 bytes to the compiled protocol and 82 to the graph projection, without an extra graph copy, cache or repeated decode. Native written-literal evidence remains PARTIAL and never proves whole-browser absence.

Integration remains separate: Publisher #568 must precede Scene #573; the real combined HTML must satisfy the unchanged 2MB/400KB guards. Root owns the exact composite native measurement, normal amendment and final integration gates. Atlas and UI protocols remain explicitly pending within #542. Superseded 851 and 32d3 must not be used as the final Scene source.
