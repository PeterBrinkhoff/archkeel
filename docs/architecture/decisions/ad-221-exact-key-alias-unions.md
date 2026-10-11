# AD-221: Exact key alias unions

For [issue #439](https://github.com/rapiddweller/archkeel/issues/439), opt-in
contract **3.1.0** permits the exact outer typed-map union family in
[rules](../../rules.md). Reuse `BoundaryAliasBody` for one proven direct
nullable-string key alias: `key_alias_body: {origin, shape}`. Keep root and key
identities separate; ordered shape text is opaque.

A named root with an aliased key binds both pairs. Partial inline binds only
the key; fully expanded inline binds neither; expanded named binds only the
root. At least two distinct maps, depth 0, empty field path and proven map
providers are required. Builtin keys are `str`, exact `tuple[int, int]` or
ordered `str | None`; values are `str`, `int` or `float`. Chains, wrappers,
duplicate occurrences, unsupported/native/unknown arms and unproven bindings
fail closed. A present pair never falls through to an older permission.

Python collection proves source safety only: complete intrinsic map expressions
may protect referenced bindings from a false escape. Import resolution joins
direct providers, replaces private snapshot expression identities on each origin
resolution, and only revokes candidates while escapes converge. Symbols publish
immutable binding facts. Core independently proves complete type shapes and matches exact
contract selectors; rendering only projects declarations and applied facts.
Ordinary nullable-map permissions retain their meaning across 3.0 and 3.1.
Nested contracts enforce dependencies; [binding reuse](../../../tests/test_binding_proof_reuse.py),
[union](../../../tests/test_boundary_type_alternative_maps.py) and
[compatibility](../../../tests/test_boundary_type_bound_aliases.py) tests enforce these invariants.

Reuse existing records, selector coordinates and report envelopes. A rationale
joins only one exact valid declaration, including both optional pair identities.
Target uses declarations; Actual/Diff use applied facts and source evidence.
Display both full escaped bindings without truncation. Older payloads and
contract semantics remain unchanged. A static grant certifies no runtime
homogeneity, copy behavior or type closure.

[Proof](../../../tests/test_atlas_report.py).
