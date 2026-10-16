# Wire compatibility regression correction

Parent: `7b2a14de58eb18be716c8eadef5c43928ec464a5` (PR 551).
Part of #542. Contract-rule grammar work remains paused.

1. Reproduce the nine full-suite failures (five catalog variants, two opaque-map CLI cases, two member-inventory schema cases) against the actual Wire source; compare the same cases and trace-valid findings with pre-Wire `2f4fd495fadc5c9d7154b8df710b842147d1e784`.
2. Diagnose schema reflection and catalog/opaque-map behavior before changing code. Keep independent schema and catalog expectations unless the observed semantics prove them wrong.
3. Correct the smallest real compatibility consumer defects. Preserve nominal owners, source unknown semantics, wire bytes, and exact evidence. No allowance, test budget, baseline or UNKNOWN expectation increases.
4. Run the nine regressions and related schema/member/opaque-map/native controls, then Ruff, strict mypy and hygiene. Validate the actual repository at 918 unresolved calls / 58 UNKNOWN / zero violations.
5. Freeze a clean correction carrier without auxiliary workflows for independent Astra review and propagation through the stack. Root owns the separate unreferenced-symbol regression.
