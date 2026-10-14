# AD-237: Dependency proof issuance and replay share one binding recipe

The Core producer and saved-observation reader separately selected and hashed
the dependency proof content introduced by AD-227. Their input adapters differ,
but maintaining the same fingerprint recipe twice risks accepting different
content at issuance and replay.

Own `dependency_binding_id` in the existing public `ir.decisions` module. Accept
typed sections, coverage failures and evidence. Core converts its raw records
with the existing parsers and Section value; replay supplies recorded values.
The shared recipe selects modules, imports, symbols, component declarations
at both levels and complete-requires declarations, then includes coverage
failures and all evidence.

Keep the existing ID sorting, duplicate entries, typed tuple representation and
`DEPENDENCY-PROOF` stable-ID prefix. Saved proof IDs and JSON formats remain
compatible. Unrelated sections and other declaration kinds remain outside the
binding. No new module, component, proof format or policy allowance is needed.

Reject retaining separate fingerprint definitions or introducing a general
proof framework. Canonical JSON would change existing proof IDs and is outside
this refactor.

Limit: sharing the fingerprint does not share trust decisions. Core issuance
eligibility and replay authentication retain their independent runtime, source,
coverage, ownership and receipt checks. Member-inventory proofs remain separate.

`tests/test_scoped_dependency_proof.py` pins old synthetic and Core-issued IDs,
ordering, duplicate retention, bound-content invalidation and unrelated-content
exclusion. Its existing live/saved negative controls retain proof eligibility
and authentication behavior.
