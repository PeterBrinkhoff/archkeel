# AD-222: Literal mapping arms

[Issue #462](https://github.com/rapiddweller/archkeel/issues/462) needs exact
native map permissions without uncertain sibling or value permission. Contract
**3.2.0** adds one opaque `literal_mapping_arm` string alongside the exact
public position and full annotation. [Rules](../../rules.md) define its two
supported families. Older schemas refuse it; absent fields retain 3.1 policy.

Core enriches its existing pre-dedup mapping occurrences with actual syntax
routes and narrow eligibility. One proven literal occurrence must be the only
contributor to the selected finding; duplicate and later resolved alias
collisions fail closed. Root proves builtin dict/str headers independently of
the value verdict. Contained selection grants only the map, preserving object
leaves and every UNKNOWN. Source facts, collection and finding IDs are unchanged.

Codec owns vocabulary; Core owns proof; declarations, widening and rendering
preserve exact selector identity and applied depth. Existing responsibilities
remain. [Controls](../../../tests/test_boundary_type_literal_mapping_arms.py)
cover migration, collisions, missing proof and ordinary direct/facade reports.
