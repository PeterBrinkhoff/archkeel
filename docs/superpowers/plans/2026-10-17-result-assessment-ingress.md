# Result assessment ingress and presentation

Part of #542; bounded existing-flow follow-up to the approved closed-control migration.
Base: 68b656668a3fdbbbe482881d0dab41ff89a21ca3.

RunResult already declares AssessmentStatus, but declared_rules legacy constructors retain raw strings. Normalize that field once alongside its existing nominal controls. Summary consumers use AssessmentStatus; the Atlas legend uses existing RuleAssessmentStatus and None for its uncounted explanation, with NOT CHECKED retained only as display text. No enum, helper, DTO, module or Target inventory is added.

- [x] Add legacy valid-value identity/wire and unsupported-value rejection tests to the existing Core result suite; observe real assertion RED on unchanged production.
- [ ] Normalize the one field and change actual summary/legend decisions; preserve legend order, labels, counts, diagnostics and JSON.
- [ ] Run focused/native/summary/renderer/regression tests, strict quality, exact native site counters and before/after real rendered output; independent Astra review and separate draft PR.

Ruling: existing execution authorization applies; isolated GitHub branch/read-only Actions replace unavailable local process execution. The skill's writing-good-tests resource is unavailable. No debt ceilings, legacy public routes or open names change; whole-module absence is not claimed. Root owns final combined metadata/full suite; Main writes remain solely with the merge steward.

RED: actual unchanged-production run38993545257/job117280923662 produced exactly7 expected assertion failures: three retained legacy strings, four unsupported values accepted. No collection errors. Production patch follows only this observed RED. Verification remains pending.
