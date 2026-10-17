# TypeScript written-literal wrappers (#542)

## Scope and design

Approved bounded follow-up to the read-only native coverage audit on b15822a9. The frozen 97-case proof remains artifact 12082543676; it is evidence, not a golden fixture or a claim of complete construct absence.

Keep the single parser owner and the existing _sites pass. Extend only _written_string so a directly written string or static template can be reached through known value-preserving TypeScript as/satisfies/non-null expression wrappers, including ordinary parentheses. Use the canonical _NodeKind vocabulary and the grammar's actual expression-child shape. Keep the original literal Span, excerpt, UTF-16 column and existing named owner. A type annotation containing a string literal is not an expression value. Dynamic templates, identifiers, nominal enum members, unknown/malformed wrapper shapes and imported constants remain unproven. No second AST walk, resolver or wrapper framework; no method/membership expansion.

The Syntax.StringComparison port, wire schema, Core projection, authored Target and construct support remain unchanged. ConstructSupport.PARTIAL still prevents an absence PASS. Existing TypeScript input ownership and valid Python legacy aliases/helpers are preserved.

## Sequence and verification

1. Commit this note and actual collector -> strict wire -> Core regression tests before implementation. Confirm assertion-only RED on the unchanged parser, plus passing conservative negatives and original literal evidence controls. Inspect actual Tree-sitter wrapper child shapes without inferring grammar from text.
2. Add only the necessary canonical node kind and known wrapper expression decoding in _written_string. Preserve literal evidence; run the focused tests, existing native construct suite, strict wire replay and compiler-valid source controls.
3. Run all TypeScript tests/compiler differential controls, source compatibility/wire comparisons for H-uml-typescript and the Nest demo, the native authored API/guard controls, Ruff/mypy/hygiene. Compare actual self UNKNOWN and unresolved/PARTIAL sites with the same final engine; no budget or allowance increase.
4. Measure the actual product source delta and a bounded repeated parser/collector cost comparison. Run the repository regression command, reporting any unrelated failure explicitly. Freeze a clean source-only branch and request independent Astra review before integration.

## Deliberate boundaries

This increment does not identify protocol meaning from literal spelling. Names, paths and JSON keys remain data. A blanket forbidden_construct rule also selects data-literal comparisons; policy must follow actual module/component responsibility. Imported value flow, aliases, named collections, methods and nominal erasure remain separate reviewed follow-ups within #542.

## Initial receipts

- Genuine native RED: [38985799039 / 117256856602](https://github.com/rapiddweller/archkeel/actions/runs/38985799039/job/117256856602), parser unchanged: 8 missing-construct assertion failures, 62 passes, zero errors. All 14 compiler inputs passed TypeScript 5.9.3. Actual wrapper children and absence of obsolete cross-component import paths were printed.
- First focused GREEN: [38986456716 / 117258963489](https://github.com/rapiddweller/archkeel/actions/runs/38986456716/job/117258963489), 71 native construct cases passed. Its formatter step exported the canonical formatting subsequently applied to product source and tests; it is not the final quality gate.
