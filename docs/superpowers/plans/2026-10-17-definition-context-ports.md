# Definition contexts: one vocabulary, explicit AST frames

Part of #542. Pinned implementation base: b06fd806ae0e76d340cba44eb7b5e84c887384d6.

## Scope and responsibility

Move the existing nine DefinitionContextKind and five DefinitionBranchKind members unchanged from architecture_graph to facts. Graph explicitly reexports the exact classes; its Evidence-ID-based DefinitionContext and pair validation stay separate. Python Source owns AST nodes and field grammar, never imports Graph, and produces the shared nominal values.

Source owns a small immutable DefinitionFrame NamedTuple with node: ast.AST, kind: DefinitionContextKind, branch: DefinitionBranchKind. Symbols and Calls read the named fields. The tuple indexing, unpacking, equality and hashing protocol remains available. The public definition_sites ingress continues accepting valid legacy triples with written string kinds/branches: normalize once in its public wrapper, then recurse through a private typed walker. No generic object widening or second AST model. Open historical Graph/Wire inputs retain their existing decoder and conservative behavior.

A private Source-owned _DefinitionField enum names the five consumed AST fields. A derived value-to-member lookup decodes ast.iter_fields field names once; a mapping from nominal fields produces existing canonical branch values. The grammar is not the wire vocabulary: orelse/handlers/finalbody/cases map to else/handler/finally/case. Unknown fields remain unselected; descendants are traversed exactly as before.

## Inventory and compatibility

Read-only hosted 38985333352/job117255360578 inspected all Python calls and repository references at the pinned base. Only Source recursion supplies contexts explicitly; Symbols calls definition_sites(tree), Calls uses control_flow_contexts, and Scopes tests its truthiness. No in-repository manual triple construction was found. The complete Source module is authored public, so valid legacy triples are still protected by explicit ingress tests. This cannot prove absence of external users.

Browser generation imports twelve domains through Graph, excluding both context enums. Preserve existing facts.py required-report routing from the ParameterKind stage; generated protocol bytes must remain exact. No visibility changes, framework, new capability, whole-Source string-absence claim, schema/receipt/budget changes.

## Cost checkpoint

The enum move itself is net zero. The Frame, small AST grammar and once-only public compatibility wrapper are expected to add roughly 45–60 production lines, plus small named-reader edits in two existing consumers. Record the measured final cost. Source's existing 2,199-line size remains a separate SoC hotspot; do not expand this step into its decomposition.

## RED then GREEN

1. Checkpoint this plan/spec; add focused tests without changing production.
2. Observe failures for shared canonical identity, typed real AST outputs, Frame annotations/tuple protocol, valid old tuple ingress, all fifteen existing conditional-source cases, and private field-decoder ownership.
3. Prove NamedTuple fields and a return annotation are actually observed by native Python collection under a fixed independent Target. First use a tiny real-source probe; do not assume observer support.
4. Implement the move, Frame, ingress and two consumers; add exact owner provenance to the existing placement decision, not a broad allowed namespace.
5. Run actual-source native field/return widening mutations, independent Target unchanged, trace-valid FAIL. Preserve unrelated-owner placement rejection.
6. Run focused conditional/source/Graph/codec tests, Ruff/strict mypy/hygiene, generated-byte identity, and real old/new Python collector runtime wire comparisons (explicit collector_argv must bind each copied runtime because -I ignores PYTHONPATH). Compare source-site changes through actual AST/symbol/reason/target/multiplicity evidence; retain all original records.
7. Independent Astra source review before PR/integration. Root owns shared final receipt, NoWrite/full regression and merge.

## Limits

No claim of complete native whole-module control-string absence. No absence PASS invented for partial language capability. No replacement of Source collector comparison with two Core runtimes that secretly launch the same installed collector.
