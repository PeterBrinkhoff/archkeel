# AD-230 Named constructor parameter properties are direct attributes

TypeScript constructor parameters marked public, private, protected or readonly
declare instance properties. Their names, owners, visibility and annotations are
source syntax. Omitting them left fifteen Nest attributes unobserved, and readonly
alone incorrectly allowed a complete empty inventory.

Collect supported identifier parameter properties into the existing Member facts.
Use the identifier's physical source span and the existing attribute identities,
visibility and annotation projection. Keep the constructor parameter and signature
unchanged. Literal defaults remain parameter defaults: a caller can supply another
value, so they do not prove a constant attribute initializer.

Ordinary parameters, inherited members and assignments in constructor bodies do
not become direct attributes. Reject destructured/rest or malformed property
patterns and properties on overload signatures without an implementation body.
Supported plain quoted instance constructors use semantic constructor identity;
their source span, parent and parameter signature remain intact. Static constructor
names and ordinary/accessor/async/generator methods never produce parameter fields.
Escaped names remain partial. Simple quoted field names compare semantically for
duplicate detection while their existing raw identities are preserved.
Duplicate declaration names and multiple constructor sites keep inventories partial;
do not emit duplicate parameter-property attributes. Computed and other unsupported
members, including standalone decorators, remain partial in this separate change.

Reject changing Core to infer fields from Target names, removing the completeness
veto without collecting declarations, and editing independent Targets. Existing
source/evidence binding, global coverage, policies, budgets and schema versions stay
unchanged. Scoped proof of complete inventories remains the separate AD-229 repair.

[Native controls](../../../tests/test_typescript_parameter_properties.py) verify
all property modifiers, precise evidence, preserved parameter defaults/signatures,
ordinary-parameter exclusion, ambiguous/malformed forms, missing/extra member FAIL,
and fresh/saved report agreement. The readonly-only negative control formerly
reported PASS for an empty closed attribute Target despite a declared property.
