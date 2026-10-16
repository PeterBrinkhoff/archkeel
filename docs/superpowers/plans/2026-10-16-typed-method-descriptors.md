# Typed Method Descriptor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Share nominal method kinds and Python descriptor proof without changing wire data or receiver semantics.

**Architecture:** facts.py owns five-valued MethodKind and frozen MethodDescriptor. Source produces the typed descriptor; facts_codec writes the old dict, and Core/graph/validators consume one conservative scalar decoder. Arbitrary provider identities remain keys in one Source data table.

**Tech Stack:** Python3.11+, Enum, frozen dataclasses, pytest/native Target and guard mutations, Ruff/mypy; isolated remote GitHub branch and hosted Actions.

**Spec:** [typed-method-descriptors.md](../../architecture/typed-method-descriptors.md); approved base `4493b0a944e6caf0c56802c6333d9fd0090041b4`.

## Global Constraints

- MethodKind has instance/static/class/constructor/factory; no global Python-only three-value validation.
- Existing method_decorator_data returns real dicts with unchanged keys/values and keyword calls.
- No schema/protocol tightening, parameter/visibility/DefinitionContext/typing-role scope, provider enum or converter/tuple framework.
- Missing/future/off-shape wire tags remain data; no new INSTANCE/UNKNOWN/reject fallback or resolver authority.
- Property never resets a preceding STATIC/CLASS effect; descriptor counts and proof predicates are unchanged.
- No budget increase; preserve independent source-grammar work by changing only this isolated base's focused hunks.
- Parent owns final independent Astra review and combined full regression before merge.

## Review Focus

- Multiple/transparent/called/custom decorators preserve exact previous descriptor order and proof.
- Alias/shadowing and module/class rebinding never gain provider proof.
- Unknown tags, JSON null/numbers/bools/arrays/objects and missing keys keep wire compatibility and existing receiver behavior.
- Dart constructor/factory and TypeScript method tags remain valid with unchanged graph modifiers.
- Legacy dict/kwargs/JSON behavior and exact Python/TS/Dart wire bytes remain valid.

---

### Task 1: Author consumed ports and establish actual RED

**Files:** this plan/spec; tests/test_typed_method_descriptors.py; docs/architecture/contracts/{ir,python}.json.

**Interfaces:** MethodDescriptor.method_kind:MethodKind; signature_decorators_proven/source_final_method_binding:bool; property_binding:PropertyBinding|None. parse_method_kind(value:JsonValue | RawJson | MethodKind)->MethodKind|None; method_descriptor(module,node,parent)->MethodDescriptor; method_descriptor_data(descriptor:MethodDescriptor)->RawData.

- [x] Add independent Target entities for the DTO, fields, decoder, writer and actual Source return.
- [x] Add nominal Source/strict DTO/native annotation mutation RED tests and actual scoped dispatch observations.
- [x] Add baseline compatibility controls for decorator ordering, receiver selection, graph modifiers and opaque wire tags.
- [x] Run hosted RED; inspect expected assertions without collection/fixture errors, and commit.

### Task 2: Implement only descriptor controls

**Files:** src/archkeel/ir/{facts,facts_codec,facts_validation,source_graph}.py; src/archkeel/analyzer/python/source.py; src/archkeel/check/evaluation/boundary_types.py.

- [x] Add nominal enum/DTO and conservative reader in facts without a codec import.
- [x] Add thin writer preserving property-field omission; keep old Source raw port as wrapper.
- [x] Convert Source proof consumers to descriptor fields and one provider identity table, retaining proof/order.
- [x] Convert only method-kind decisions in Core/graph/property/Dart validation to the same nominal reader.
- [x] Run new and existing method/property/protocol/native tests, exact wire checks, Ruff/mypy.

### Task 3: Freeze measured evidence for independent review

**Files:** this plan's evidence; normally generated amendment, with only resolved baseline debt ratcheted if needed.

- [x] Run normal writer and NoWrite/replay without --accept-new or increased budgets.
- [x] Compare unresolved/PARTIAL sites, targets, multiplicity and full UNKNOWN payloads against the exact base.
- [x] Export/apply formatting; freeze a clean carrier without hosted verification workflows.
- [x] Hand off exact SHA/blob/run evidence for independent Astra and parent full integration regression.

## Execution ledger

Native execution is explicitly authorized after the read-only design. Remote branches substitute for local worktrees because the executor cannot fork; hosted Actions run all checks. The plan is the durable ledger.
Pre-flight: Task2 consumes Task1's exact nominal fields/ports; names and signatures agree. Legacy Source writer and optional property omission are shared constraints, not a second decision authority.

Port correction after actual native measurement: the initially authored object input
added one object_annotation signal (52→53). The approved input domain is the existing
raw/frozen JSON value types plus MethodKind. Move the existing RawJson definition to
facts and preserve facts_codec.RawJson as the identical public reexport. Add an
independent Target parameter constraint and establish RED before this correction.
No measurement policy, ceiling, wire validation or conservative None behavior changes.

Verified evidence before clean freeze:
- Original actual RED: 38975040658 / 117222331986, 42 expected failures,
  30 compatibility controls and 227 existing proof/graph tests passed.
- Honest JSON-port RED: 38976685328 / 117227707123, two expected failures
  (missing upstream RawJson and mismatching authored parameter), 30 controls passed.
- Corrected focused GREEN: 38976831326 / 117228178997, 984 passed / 5 skipped;
  Ruff format/check and mypy 148 source files passed.
- Native/writer: 38976852782 / 117228251144, NoWrite and normal writer exit0,
  diagnostics/failures empty, widenings empty. Scalars 865 unresolved calls,
  52 typing positions, 58 unknown positions, 0 violations. Baseline bytes unchanged.
- Deep comparison: same run / 117228250734, complete Python/Dart/TypeScript wire
  bytes equal after only adapter.code_digest normalization. Known Dart method tags
  include constructor/factory as well as static/instance.
- Full UNKNOWN identity/kind/subjects/rule_ids/data payloads: 77 unchanged.
  Typing signal kind/subjects/data payloads: 56 unchanged.
- Calls: total 18721→18736, resolved 15327→15343, PARTIAL 2529→2528,
  unresolved 865 unchanged. Existing properties.get partial moves from old raw
  producer to typed producer; one repeated graph data.get partial disappears.
- References: total 7565→7596, resolved 6609→6638, PARTIAL 956→958.
  The two new descriptor.property_binding references have the conservative
  same-name candidate archkeel.ir.facts.property_binding; this is a function,
  not proof of the DTO field. No resolver authority is added.
- Counters retain target lists, status/reason and multiplicity; only synthetic
  comprehension/lambda physical line suffixes are normalized for site comparison.
- Only six production files change. The canonical RawJson alias moves unchanged
  upstream and is explicitly reexported by the existing codec port. No historical
  JSON, new component, converter framework, schema tightening or budget increase.

Final frozen verification: run 38977434453 on auxiliary carrier
58123fb3587dfc1c25d24744c3d8e849c97bf2ad, with all six production, two Target,
new-test and receipt blobs identical to reviewed clean Source freeze 3bb8816683cf.
- frozen-source job 117230148327: 105 descriptor/property tests passed, Ruff and mypy148 passed.
- receipt-replay job 117230148154: exact NoWrite exit0, amendment_status valid,
  diagnostics/failures/widenings empty; 865/52/58/0 and clean working-tree diff.
- frozen-evidence job 117230148250: three exact canonical wire profiles equal;
  77 full UNKNOWN payloads and 56 typing payloads unchanged; same documented
  PARTIAL target/multiplicity deltas. Counter proof covers its explicit named
  fields, not full AST or every possible Site record field.
Independent Astra Source review approved 3bb8816683cf with no Critical/Important findings.
Combined parent integration/full regression and merge remain separate gates.
