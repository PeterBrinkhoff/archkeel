# AD-228 Dart constructor identities name the lexical owner once

Named constructor and factory declarations use `module.Class.named`, matching
Dart's source spelling and the independent Compass Target. The former
`module.Class.Class.named` duplicated the lexical owner and left eleven
source-present `fromJson` factories UNKNOWN. Unnamed constructors retain
`module.Class.Class`; their member name is the class name.

Normalize the seven old named-constructor spellings in Compass's domain/utilities
Target to the same language identity: `BookingShareUseCase.{_,custom,withSharePlus}`,
`Result.{ok,error}`, `Ok._` and `Error._`. Only `qualified_name` changes; IDs,
parents, signatures, permissions and responsibilities retain their authored intent.
Keep all source bytes and the eleven already-canonical `fromJson` names unchanged.
Record the representation migration with the updated Target bundle hash.
The Flutter shop Target similarly migrates only its `Order.fromCart` factory's
qualified name; its architecture intent and source remain unchanged.

Normalize the declaration's canonical name in collection. Keep the parsed member
spelling, lexical parent and source span unchanged. Existing span-based joins then
carry the same identity into signatures, references and callable scopes. Prefixed
constructor references use the same proven local constructor lookup as unprefixed
references, preserving library-private access checks.
Check uniqueness across every imported declaration before considering its kind;
conflicting classes, aliases and functions remain ambiguous. Reexports of the
same source declaration share one identity.
Gate only the new constructor-reference fallback on closed visible source
namespaces. Follow import/export combinators for the class name, inspect every
conditional URI and owned part, and terminate local export cycles. Missing,
external or incomplete visible namespaces remain UNKNOWN; excluded names and
unexported external imports do not veto a known local reference.
Conditional alternatives must agree on queried source bindings with traversal
ancestors retained. Equal absence agrees; presence in one alternative alone does
not prove a stable binding.

Reject changing the Target to match faulty observed names or normalizing arbitrary
dotted method names. Constructor identity does not prove a factory's instance
result, resolve aliases, or provide missing inherited types and defaults. Existing
coverage failures and genuine UNKNOWNs remain; budgets and policy do not change.

Native process tests cover generative/factory declarations, private names,
generics, redirects, references, callable scopes, construction relationships,
unknown alias/external/missing targets and repeat-run equality. All four Compass
variants compare against the pinned source and migrated Target digests, with all eleven
named factories present under their declared identities.
