# AD-232 Module array constant identities

TypeScript `export const entities = [Article, Comment, Tag, User] as const`
declares a statically named registry. Its independent Target previously remained
UNKNOWN because the collector accepted only identifier/scalar initializers.

Record flat identifier/scalar array constructions and their genuine `as const`
wrapper as existing constant declaration facts. New array identities require a
direct module-level const declaration, preserving ownership, export visibility,
definition-site identity and source evidence. No wire vocabulary changes.

Declaration identity does not evaluate the array, resolve its elements, infer a
runtime value/type or prove call/constructor dispatch. Array facts carry no
evaluated constant value or inferred initializer. Module inventories remain
partial; an absent declaration needs separate complete inventory evidence to fail.

Calls, arrows, spreads, member expressions, nested arrays, arbitrary assertions,
computed bindings and malformed syntax remain unsupported. Conditional,
constructor/function-local, arrow-local and namespace-local arrays cannot become
module declarations. Duplicate declarations retain separate sites and ambiguity.
An omitted direct module variable of the same name vetoes the new array identity,
regardless of declaration order; unrelated names and nested scopes do not.
Value imports and uncollected namespace/import-alias bindings also veto a
same-name array; explicit type-only imports do not. Direct module destructuring
and escaped binding spellings make uniqueness opaque and veto new array facts.
Uncollected direct value declarations, including ambient forms, also remain
competitors. Plain supported declarations retain their original facts and ambiguity.
Existing identifier/scalar handling and TypeScript type/value matching are unchanged.

Rejected: interpreting `as const` as runtime immutability or proof of element
types; accepting every initializer; promoting local bindings; changing the pinned
NestJS source or its independently authored Target to conceal the omission.

Proof: [test_typescript_array_constants.py](../../../tests/test_typescript_array_constants.py)
checks native facts, the unchanged NestJS registry, independent live/saved Target
agreement, complete-absence and wrong-kind failures, duplicate ambiguity and
unsupported syntax/scope controls. The change addresses [#500](https://github.com/rapiddweller/archkeel/issues/500).
