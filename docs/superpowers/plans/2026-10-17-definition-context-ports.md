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

## RED observation

The first fixture attempts had incomplete nested UML metadata and are not product RED evidence. After correcting only the fixture, hosted run 38986030782/job117257587261 observed 15 expected failures and 39 passing controls on unchanged b06 production. All three native NamedTuple field/return mutation probes passed: the fixed Target observes those real ports and trace-valid violations survive actual written annotation widening. The real Source frame/nominal identity is still missing, as expected. Product implementation starts only after this result.

## Final source and evidence ledger

Production and authored intent are frozen at a79aa22628c7dea56f7bbd89d7d5fe3ef2a6ab4e; the reviewed 898c28e2512bd6fa55a71ffc4d5b64bf72173ddc and test-only successor 08efa0a9578cc71d2ebf1bae2e784b62ab68ca4d have byte-identical production/intent. Measured production cost: +36 net lines in five existing modules. Fourteen duplicated Source control spellings are removed; the five AST field labels remain a distinct, locally owned input grammar. Astra independently approved 898c28 against b06 with no Critical/Important findings.

- Final original 67 native/conditional/hygiene controls, Ruff, formatting, strict mypy (143 files), exact generated browser vocabulary and actual old/new E/F/H/K Core+collector wire pairs passed in 38986751987 (117259895805, 117259896116). Each collector explicitly binds its isolated runtime and verifies all five changed module origins; -I/PYTHONPATH ambiguity is not hidden. The sole payload difference is analyzer.code_digest, then canonical bytes are 5572/145970/56632/1349592. The E-runtime mismatch diagnostic is preserved.
- Same-current-engine observation of both authored revisions passed in 38986494012/117259078030. Scalars remain 0 violations, 52 typing positions, 838 unresolved calls, 58 UNKNOWN positions; total calls 18887→18896. The single ordered observation took 108.0→115.4 seconds; this is not a benchmark or performance-improvement claim.
- Full record/provenance comparison 38987574676/117262503233 preserves all 3345 original unresolved/PARTIAL calls after actual AST-position, scope, symbol and reference correspondence. Two additional PARTIAL _DEFINITION_FIELDS.get sites remain explicit. A native source experiment (38987366098/117261851476) proves that adding a dictionary annotation alone does not resolve that method port; production is not changed to pretend otherwise.
- All 85 complete UNKNOWN records remain equal after the same correspondence plus authenticated derived UML identities. Exactly two assessment/finding IDs change because Facts definitions move; the unchanged stable_id algorithms are re-run against the actual authored IR scopes and raw observed IDs. No ID field, module, reason, target or multiplicity is dropped. This does not assert equality of every complete call AST/argument expression; binding IDs follow their observed call and ordinal while their actual payloads remain compared.
- The broader Python/Graph run 38986398010/117258772000 reported 758 PASS, 24 SKIP and one existing-fixture failure. Its Facts extractor omitted the two newly shared canonical definitions. Causal 38987301608/117261644637 proved only those two missing entities were UNKNOWN; copying their actual definitions restored PASS with unchanged Target bytes. The fixture now collects both real members and the actual spec. The entire corrected Graph/Context fixture suite passed 61 tests plus Ruff/format in 38987636436/117262694201; no expectation was weakened.

Final 69 native/conditional/hygiene controls including actual field-grammar parameter widening, Ruff/format, strict mypy (143 files), generated browser bytes and all four actual Core+collector wire pairs passed in 38987851305 (117263368506, 117263368338) on clean 08efa0a9 source plus one isolated verify workflow. Common full suite, normal receipt and NoWrite gates are tracked separately. Root owns stack integration/receipt/full regression and merge. No new vocabulary migration begins in this stage.
