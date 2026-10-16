# Summary badge ownership

The Summary component owns the Badge value and its display state. BadgeState has exactly pass, fail, info and unknown wire values; these are presentation states. Core's binary Verdict and three-valued AssessmentStatus retain their own identities.

The focused archkeel.render.summary_badges module owns BadgeState, frozen Badge and the badge text projection. The projection decodes known assessment text once through the canonical AssessmentStatus. The legacy n/a marker is decoded at this presentation boundary; arbitrary other text keeps the existing NOT CHECKED display. Symbols and labels remain output data.

Badge normalizes the four previously valid string state arguments once into BadgeState. Summary explicitly reexports the same Badge and badge objects for existing callers. Terminal and HTML consume the direct owner, and their output adapters preserve existing state attributes, symbols, labels and colors.

The authored render Target pins the real Badge.state annotation and badge return type. A native forbidden_construct rule covers the entire focused Python module. Its positive proof and source mutations do not certify remaining Result/Command branches in summary.py, HTML's other grammars, open Record.kind values, actor labels or browser JavaScript.

This adds one focused module within the existing Summary component. It adds no dependencies, accepted debt, historical snapshots or baseline allowances. Diagnostic consumers retain their canonical ir.diagnostics imports when that independent increment is integrated.
