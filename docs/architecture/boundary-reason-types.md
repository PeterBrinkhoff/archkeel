# Boundary position reason ownership

The existing Core boundary_types evaluator owns the closed reasons for one annotated position. This stage gives that existing field and its lexical fallback classifier a nominal type without changing what the checker can prove.

The twelve wire spellings and report order remain missing_annotation, inherited_surface, forward_reference, dotted_name, generic, union, ambiguous_binding, ambiguous_facade, unresolved_name, external_type, nested_type and other. nested_type is currently a historical zero-count slot; retaining it claims no new capability.

A private _UndecidableReason(StrEnum) lives beside _Position in boundary_types.py. The frozen _Position.undecidable field is _UndecidableReason | None; valid legacy string inputs normalize once at that DTO ingress, and unknown reasons fail closed. _unresolvable_shape returns the same owned type. Producers and the four existing consumers use owned members. The existing _UNDECIDABLE_KINDS facade derives plain string values from that one owner for wire/legacy compatibility.

The evaluator's open diagnostic text, annotation/name/path data and other public API limit reasons remain distinct. ir.decisions stays a dynamic historical wire consumer and never imports check. This stage introduces no new analyzer/coverage authority, module-wide string guard, exemption or budget.

The independent authored check Target specifies the actual private field and function-return intent. Native source annotation mutations must fail that unchanged Target. Actual wire, finding/evidence IDs, UNKNOWN semantics, call/PARTIAL sites and budgets are compared against the pinned predecessor.

The 6,305-line evaluator is a measured SoC hotspot: annotation interpretation, inheritance/facade/public API surface traversal and diagnostic/wire aggregation coexist. Splitting those responsibilities needs a separate behavior-preserving plan; this type change does not reorganize them.
