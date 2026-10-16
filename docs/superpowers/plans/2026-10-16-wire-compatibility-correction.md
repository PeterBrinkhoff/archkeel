# Wire compatibility regression correction

Parent: `7b2a14de58eb18be716c8eadef5c43928ec464a5` (PR 551).
Part of #542. Contract-rule grammar work remains paused.

1. Reproduce the nine full-suite failures (five catalog variants, two opaque-map CLI cases, two member-inventory schema cases) against the actual Wire source; compare the same cases and trace-valid findings with pre-Wire `2f4fd495fadc5c9d7154b8df710b842147d1e784`.
2. Diagnose schema reflection and catalog/opaque-map behavior before changing code. Keep independent schema and catalog expectations unless the observed semantics prove them wrong.
3. Correct the smallest real compatibility consumer defects. Preserve nominal owners, source unknown semantics, wire bytes, and exact evidence. No allowance, test budget, baseline or UNKNOWN expectation increases.
4. Run the nine regressions and related schema/member/opaque-map/native controls, then Ruff, strict mypy and hygiene. Validate the actual repository at 918 unresolved calls / 58 UNKNOWN / zero violations.
5. Freeze a clean correction carrier without auxiliary workflows for independent Astra review and propagation through the stack. Root owns the separate unreferenced-symbol regression.

## Diagnosis and completed evidence

- Causal RED: [run 38954016347](https://github.com/rapiddweller/archkeel/actions/runs/38954016347), actual pre-Wire `2f4fd495fadc5c9d7154b8df710b842147d1e784` versus actual Wire `7b2a14de58eb18be716c8eadef5c43928ec464a5`. The ten selected controls measured 7 failed / 3 passed before and 9 failed / 1 passed after. Both sources emitted the same additional `CONSTRUCT-NO-STRING-LITERAL-COMPARE` finding in all five catalog variants. The seven catalog/CLI failures therefore predated Wire; the two schema failures were caused by the nominal InventoryVersion consumer migration.
- The schema generator now reads version alternatives from either Literal or StrEnum at its existing owner. Committed schema bytes and equality expectations remain unchanged.
- The shared raw-map demo uses the standard mapping get API with a unique missing sentinel. An executable test of the actual catalog source proves missing input raises and present None or zero returns the identical input object. Existing catalog verdicts and boundary evidence expectations remain unchanged.
- GREEN: [run 38954300654](https://github.com/rapiddweller/archkeel/actions/runs/38954300654), job `117153158663`: 679 tests passed across the full architecture-demo, opaque-map, member-inventory, partial-inventory, schema-drift, type-shape, typed-collector-protocol and typed-collector-native modules.
- Quality job `117153158943`: Ruff passed, strict mypy passed for 138 source files, and all 11 repository-hygiene tests passed. Its sole formatter delta was the new test's line wrap, committed unchanged in `9b9e0f095d598c2b1fb6c61922de6c4bb1d127f4`.
- Native job `117153159053`: actual own validation exit 0, no failures or diagnostics; unresolved calls 918, typing positions 52, UNKNOWN positions 58, violations 0. No src/archkeel source changed in this correction; the measured product schema/fixture bytes remain frozen.
- Bounded cost: net 6 generator lines, 1 shared fixture line and 14 behavior-test lines. No HRC declaration, baseline, schema artifact, allowance, amendment or auxiliary workflow is changed in the clean carrier. The independent references-candidate investigation belongs to Root.

All implementation and verification steps are complete. Product scope is frozen for independent Astra review and propagation; contract-rule grammar remains paused during that review.
