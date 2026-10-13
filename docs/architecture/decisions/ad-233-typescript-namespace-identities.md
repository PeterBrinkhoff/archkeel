# AD-233 TypeScript identity matching separates type and value namespaces

TypeScript can declare a type alias and a constant with the same qualified name.
Their native definition-site IDs and source evidence remain distinct. Core UML
matching selects candidates in the namespace requested by the independent Target,
then applies the existing uniqueness, kind, context and evidence checks.

Interfaces and type aliases occupy the type namespace. Functions, methods, fields,
constants, bindings and enum literals occupy the value namespace. Classes and enums
occupy both. Opaque kinds remain candidates in both namespaces; their namespace is
not guessed. Package/module matching and existing field/value projections retain
their current behavior.

An opposite-namespace declaration does not prove that the requested definition
exists or has the wrong kind. Absence remains UNKNOWN without complete relevant
inventory, and FAIL when that inventory proves absence. A unique wrong kind within
the requested namespace still fails. Same-namespace duplicates, declaration merging,
class/enum overlaps and conditional definitions remain conservative.

Reject exact-kind preference across arbitrary definitions, an all-language fallback,
discarding source sites and inventing runtime alias/call targets. Other languages
keep their existing identity rules. Namespace selection does not resolve uncertain
reference or call sites. External computed MikroORM keys remain unproved.

The collector, SourceFacts/IR schemas, frozen Nest source and independent Targets,
permissions and budgets do not change. Fresh reports record the ordinary comparison;
saved reports consume that comparison without reevaluating source.

Proof: [namespace controls](../../../tests/test_typescript_namespace_identities.py)
and [native declaration controls](../../../tests/test_typescript_inner.py).
