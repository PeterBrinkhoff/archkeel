# Dart local callable shadowing (#570)

Root approved an independent fix after identical native source tests proved this defect on both the pre-grammar source and its candidate (run38976296732, two failures and one index control pass per revision).

## Design

Use the existing immutable SiteKind.BINDING port for actual local function declarations and their enclosing lexical scope. Do not add an AST owner, parser wrapper, DTO or runtime return inference. Resolver construction dispatch must respect the same existing lexical-binding test used by direct CALL resolution. A chained receiver must identify its actual contained CALL by physical span and matching lexical scope, with exactly one matching fact; file-wide first-spelling selection is insufficient.

## Steps

- [x] Checkpoint real direct/closure/function-valued-variable/parameter/forward-declaration RED and unshadowed/sibling-scope positives.
- [x] Inspect the pinned Dart grammar and existing Site BINDING fields; keep root/top-level function semantics unchanged.
- [x] Implement the smallest parser producer and resolver consumers after RED.
- [x] Run native focused and existing parser/resolver/false-positive tests; no unsafe global-target expectations.
- [x] Compare actual Compass/H canonical Facts, classify any changed resolution evidence honestly and keep UNKNOWN conservative.
- [ ] Freeze clean source, independent Astra, separate PR closing #570; no self-merge.

## Constraints

The branch starts from actual 0e3b8a7f62b9b13417cda78e11b52d0de82986cd, independently of #542 grammar changes. No borrowed Target/receipt/Source authority, casts, Any, ignores, exemptions or budgets. Auxiliary workflows stay only on verify refs.

## Verified source freeze

Clean source candidate ba73962f96c0a1c76a5bfc0bb88933c1cc7021a3 has two product-file changes: parse.py +21 net lines, resolve.py +1 net line. Local callable declarations use the existing BINDING producer; the existing negative lexical-binding predicate protects construction dispatch, while physical receiver CALL span, matching scope and uniqueness replace first-spelling selection. No DTO, schema, authored Target, budget or inference is added.

Causal native RED38977191644/job117229372821:7 actual failures /4 controls pass. Final native GREEN38977678731/job117230919876:11 pass, Ruff/8 formats/strict mypy139 pass, product/Target checkout unchanged. Existing Dart coverage38977443252/job117230176110:317 pass, including parser/resolver/directives/snapshot/SDK-free/partial-UML/false-positive/acceptance/Target/rules/demo/profile tests.

Complete canonical Fact wire is byte-identical under a shared runtime for H226636B and Compass10669901B (38977678731/job117230920107); no fields are removed or projected. Three alternating collection medians were H0.06484 ->0.06645s (+2.48%,1.61ms) and Compass5.22480 ->5.22010s (-0.09%,noise); no speed advantage is claimed.

Native real-source revision comparison38977678731/job117230920145 keeps violations0, unresolved865, typing52 and UNKNOWN58 unchanged. The full 30-position/20-route/8-UML semantic projections agree; total observed calls18692 ->18702. Artifact12078959407 contains complete before/after observations. No unmeasured UNKNOWN is presented as PASS. This evidence uses the ordinary observer on the pre-prefix base; #542 prefix activation remains separately coordinated.

Independent final Astra and Root integration/normal committed receipt/no-write remain outstanding. No merge is authorized to this implementer.
