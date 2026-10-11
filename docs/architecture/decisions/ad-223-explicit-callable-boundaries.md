# AD-223 Explicit Callable boundaries

Source proves syntax, stdlib Callable origin and every binding/alias hop. IR
transports immutable TypeList facts under SourceFacts 3.0.0. Core reuses its
boundary walker for ordered explicit arguments and result; it never parses
Python or validates runtime callback implementations. These owners follow AD-148.

Only proven typing.Callable or collections.abc.Callable with an explicit argument
list is admitted. Broad leaves remain FAIL beside unresolved leaves; callback
routes retain real DTO paths and depths. Existing map/iterable grants cannot
approve callback leaves. Ellipsis, ParamSpec, Concatenate, unpacking, generic
specialization, cycles and unproven providers remain UNKNOWN.

Source protection covers exact callback type references and joins the existing
escape fixed point. Namespace, provider and alias escapes revoke constructor
proof. Referenced-member uncertainty stays in Core leaf checks, preserving safe
siblings; protection never exempts arbitrary expression descendants.

SourceFacts 1.0.0/2.0.0 preserve byte round trips and reject TypeList at any depth.
The required runtime state belongs to 2.0.0 and later. Architecture contract,
ArchitectureIR, result envelopes, budgets and dependencies do not change.

Proof: tests/test_callable_boundaries.py, tests/test_binding_proof_reuse.py,
tests/test_type_shapes.py and tests/test_collection_protocol.py.
