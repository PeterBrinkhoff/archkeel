# Summary badge ownership

The Summary component owns the Badge value and its display state. BadgeState has exactly pass, fail, info and unknown wire values; these are presentation states. Core's binary Verdict and three-valued AssessmentStatus retain their own identities.

The focused archkeel.render.summary_badges module owns BadgeState, frozen Badge and the badge text projection. The projection decodes known assessment text once through the canonical AssessmentStatus. The legacy n/a marker is decoded at this presentation boundary; arbitrary other text keeps the existing NOT CHECKED display. Symbols and labels remain output data.

Badge normalizes the four previously valid string state arguments once into BadgeState. Summary explicitly reexports the same Badge and badge objects for existing callers. Terminal and HTML consume the direct owner, and their output adapters preserve existing state attributes, symbols, labels and colors.

The authored render Target pins the real Badge.state annotation and badge return type. A native forbidden_construct rule covers the entire focused Python module. Its positive proof and source mutations do not certify remaining Result/Command branches in summary.py, HTML's other grammars, open Record.kind values, actor labels or browser JavaScript.

This adds one focused module within the existing Summary component. It adds no dependencies, accepted debt, historical snapshots or baseline allowances. Diagnostic consumers retain their canonical ir.diagnostics imports when that independent increment is integrated.

Verification uses actual source against independently authored intent. Runtime assertion RED and the legacy-source native RED are recorded in run 38955722943. Final strict/mutation/byte-parity and exact-parent source-site proof are in run 38956930786; Chromium is in run 38956067479/job117159122968. All 17 Badge Target assessments pass, and the complete focused-module guard is proven.

Against 7f99d03afaaea57530c56d688ce84e4b0867152e, native counts remain 918 unresolved calls, 52 typing positions, 58 UNKNOWN positions and zero violations. The native call identity changes contain only line-bearing generator scopes in three unchanged HTML function bodies. UNKNOWN IDs are unchanged, but four Summary positions now expose the existing regressions Comparison alias after Badge.state becomes decidable. This does not prove every Summary field; the subsequent alias limitation remains explicit.
