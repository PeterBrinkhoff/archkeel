# Dart local callable shadowing (#570)

Root approved an independent fix after identical native source tests proved this defect on both the pre-grammar source and its candidate (run38976296732, two failures and one index control pass per revision).

## Design

Use the existing immutable SiteKind.BINDING port for actual local function declarations and their enclosing lexical scope. Do not add an AST owner, parser wrapper, DTO or runtime return inference. Resolver construction dispatch must respect the same existing lexical-binding test used by direct CALL resolution. A chained receiver must identify its actual contained CALL by physical span and matching lexical scope, with exactly one matching fact; file-wide first-spelling selection is insufficient.

## Steps

- [x] Checkpoint real direct/closure/function-valued-variable/parameter/forward-declaration RED and unshadowed/sibling-scope positives.
- [x] Inspect the pinned Dart grammar and existing Site BINDING fields; keep root/top-level function semantics unchanged.
- [ ] Implement the smallest parser producer and resolver consumers after RED.
- [ ] Run native focused and existing parser/resolver/false-positive tests; no unsafe global-target expectations.
- [ ] Compare actual Compass/H canonical Facts, classify any changed resolution evidence honestly and keep UNKNOWN conservative.
- [ ] Freeze clean source, independent Astra, separate PR closing #570; no self-merge.

## Constraints

The branch starts from actual 0e3b8a7f62b9b13417cda78e11b52d0de82986cd, independently of #542 grammar changes. No borrowed Target/receipt/Source authority, casts, Any, ignores, exemptions or budgets. Auxiliary workflows stay only on verify refs.

Actual expanded native RED38977191644/job117229372821:7 failed and4 unrelated-scope controls passed. The real pinned grammar reports local_function_declaration -> lambda_expression -> function_signature/function_body. Existing constructor and function-valued variable/parameter bindings are bypassed only by the chained construction path. Forward local callables remain lexical names throughout their written scope; the negative _has_lexical_binding check therefore does not require a preceding declaration, while _lexical_bindings retains its preceding-position requirement for positive binding claims.
