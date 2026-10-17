# Result assessment ingress and presentation

Part of #542; bounded existing-flow follow-up to the approved closed-control migration.
Base: 68b656668a3fdbbbe482881d0dab41ff89a21ca3.

RunResult already declares AssessmentStatus, but declared_rules legacy constructors retain raw strings. Normalize that field once alongside its existing nominal controls. Summary consumers use AssessmentStatus; the Atlas legend uses existing RuleAssessmentStatus and None for its uncounted explanation, with NOT CHECKED retained only as display text. No enum, helper, DTO, module or Target inventory is added.

- [x] Add legacy valid-value identity/wire and unsupported-value rejection tests to the existing Core result suite; observe real assertion RED on unchanged production.
- [x] Normalize the one field and change actual summary/legend decisions; preserve legend order, labels, counts, diagnostics and JSON.
- [x] Run focused/native/summary/renderer/regression tests, strict quality, exact native site counters and before/after real rendered output.
- [x] Receive bounded independent Astra production/API review.
- [ ] Complete permanent exact-owner guards with their engine dependency, final feature review, normal metadata and required combined gates.

Ruling: existing execution authorization applies; isolated GitHub branch/read-only Actions replace unavailable local process execution. The skill's writing-good-tests resource is unavailable. No debt ceilings, legacy public routes or open names change; whole-module absence is not claimed. Root owns final combined metadata/full suite; Main writes remain solely with the merge steward.

RED: actual unchanged-production run38993545257/job117280923662 produced exactly7 expected assertion failures: three retained legacy strings, four unsupported values accepted. No collection errors. Production patch follows only this observed RED. Verification remains pending.

GREEN behavior: exact source51f5a3938284ee42187f1336fabcf36268a4feb0 passed268 tests/11 skips, Ruff514/mypy150, actual native owner/form counters27→22 (five removed controls, none added), and27 byte-identical result/summary/legend outputs over nine real DTO inputs in run38993915666/job117282080213. Product cost is eleven net lines in three existing modules; no new type/helper/module. This is not whole-module absence proof.

Permanent contract follow-up: five exact owner guards protect RunResult and the four migrated presentation functions. Existing independently authored RunResult.declared_rules annotation intent is now included in its native fixture and has its own real widening mutation. On unchanged contracts, run38994690700/job117284535873 produced six expected assertion failures because all five guards were absent, with no test errors. Native positive/actual-owner literal mutations and final strict checks follow. No policy allowances or budget edits.

Owner-scope dependency: real qualified class/function rules exposed the existing module-only preflight and receipt bug. Six Core guard cases and three existing direction cases initially failed actual run_report, not a mocked evaluator. The separate rules.py fix observes real symbol owners and preserves missing/clipped/incomplete UNKNOWN. With that fix, run38997783754/job117294030739 passes all55 Core/Target-navigation/hygiene checks on preview024e0bc7aab57188075a0920bb5eab85e2e4de8b. Production remains byte-identical to bounded Astra-approved4ba. The only later UI correction is a fixture source newline before its backward import; all direction assertions stay unchanged. The workflow's later quality step was invalidly scoped over intentional negative fixtures and also included the engine's already corrected line wrapping; final quality uses repository make lint/typecheck on the clean engine successor. No global quality or standalone feature-green claim is made here.
