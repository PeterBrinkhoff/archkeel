# Typed control migration scope

Issue #542 includes domain decisions, parser grammar and protocol dispatch.
Closed kinds, modes, states and versions have a nominal owner. Decode external
values once at the relevant boundary, then share that type between actual
producers and consumers. Parser placement is not an exception. Module names,
paths, symbols, JSON field names and ordinary text remain data.

A constant, imported string alias or `Enum.value` comparison does not establish
a nominal decision. Enum values may be serialized at a real wire boundary.
Supported legacy string inputs normalize once; compatibility is not permission
to keep internal string dispatch.

## Implemented guarantees

These scopes describe the reviewed implementation; the linked PRs and #542
record merge status. A source approval does not replace integration checks.

| Owner | Guarantee |
| --- | --- |
| `ir.dependency` | Shared selector modes, ownership and selections; independent API Target and native raw-comparison guard |
| `ir.state_facts`, `ir.state_codec` | Owned field/event vocabulary, typed input conversion and native guards |
| Collector Facts, protocol, type shapes and observation codec | Canonical language/runtime/shape tags shared by producers and decoders; protected modules and authored API intent |
| `ir.contract_version`, `ir.codec_contract` | Owned supported versions/features and contract grammar; native guards include parser branches |
| Graph, graph codec, Target graph and UML comparison | Shared nominal graph/assessment vocabulary and protected module scopes |
| TypeScript configuration, resolution, parser, collector, syntax and source input | Owned compiler/grammar categories, typed semantic outputs and whole-module native guards without parser allowances |
| Dart syntax, parser, resolver, snapshot and collector | Owned grammar/binding categories and native guards; shadowing is tested separately |
| Python binding and receiver type owners | Nominal compiler/evidence categories and native owner guards; this does not cover all Python implementation modules |
| Shared runtime bootstrap and language entries | One direct-start classification and explicit entry port |
| Diagnostic and amendment owners/codecs | Owned closed tags and typed wire ingress with native guards |
| CLI input and summary-badge owners | Explicit input/display types, actual consumers and scoped native guards |
| Measurement owner | Shared budget/resolution/outcome types and native owner guard |
| DeltaVersion, ParameterKind, method descriptors and Core commands | Shared types in existing owners and independently authored actual field/parameter/return intent; no whole-module migration claim |
| Private boundary reasons | One private vocabulary in the existing boundary checker; actual producer/consumer types and native widening/control mutations |
| Browser Scene ingress | Canonical generated vocabulary, checked consumers, malformed-value tests and preserved public view-mode behavior |

Each native rule protects its declared source scope. An authored API Target pins
intended nominal types independently of observed Source. Actual source mutations
must produce trace-valid failures under that unchanged Target; fixture errors or
missing evidence are not a successful negative control.

Wire compatibility, normal baseline/amendment generation, strict replay, required
CI and independent Astra review remain integration gates. No budget increase,
fabricated resolution or broad parser exemption establishes completion.

## Remaining scope and evidence limits

#542 stays open for remaining closed controls in other Core, Python, presentation
and browser consumers. Definition contexts, comparison status and further
TypeScript expression forms are independent bounded increments. Existing typed
fields do not certify every branch in their containing module. The broader inner
Target work in #340 remains separate.

Python's supported syntactic comparisons are documented in
[string-comparison-observation.md](string-comparison-observation.md).
Imported/dynamic values and arbitrary aliases are not a semantic whole-program
type proof. TypeScript and JavaScript construct observation remains PARTIAL:
witnessed prohibited forms can fail, but absence must not become PASS when the
required coverage is incomplete. Compiler acceptance proves syntax/type
compatibility, not complete native architectural evidence.

At the original Main `63437df6734275850838ba1026b276c2f930bf2f`, the native
audit observed 1,662 string-literal constructs. That is a syntax count, not a
defect count or a count of completed fixes. New source inventories likewise need
ownership and control/data triage before they justify a migration.
