# Evidence class consumer plan and evidence

> **For agentic workers:** Use superpowers:executing-plans for this bounded refactor.

**Goal:** Part of #542: keep eleven existing declaration dispatch decisions in the shared nominal evidence domain.

**Architecture:** `archkeel.ir.facts.EvidenceClass` already owns the vocabulary and `Record.evidence_class` annotation. `facts_codec.parse_record` validates the wire string into that enum. The published `model.EvidenceClass` alias is the same object. Consumers compare the existing enum; no new domain, constructor, wrapper or target declaration is needed.

**Spec:** #542 and the approved eleven-site follow-up; base `c725df96543d1dd7ec4e20887a486ec9a7143c8a`.

## Scope and checks

- [x] Inspect actual Record ingress, canonical owner, facade identity and existing interface ports.
- [x] Replace seven UML authentication comparisons, two Target record authentication comparisons, one permission projection comparison and one rule assessment comparison. Three new imports stay private; decisions reuses its existing EvidenceClass import.
- [x] Verify exact before/after native sites, meaningful existing UML/projection/record/decision/codec regressions, strict Ruff/mypy and real old/new fullReport serialization profiles.
- [x] Obtain independent Astra source review and leave integration and fresh combined writer/receipt/NoWrite/full-suite evidence to the Main steward.

**Ruling:** Reuse existing behavior regressions and native before/after evidence for this behavior-preserving refactor, as explicitly authorized; do not add tests that mirror the eleven implementation lines.

**Limits:** This change does not activate native guards for all four modules. TypeScript/JavaScript coverage remains PARTIAL. The inherited combined metadata is stale for this target and is not fresh evidence. Existing serialization uses of `.value` remain at their wire boundaries. No ratchet budget or contract changes.

## Verification evidence

Source head: `1a0fba765ef01b270dd7b7a38dd329fb544076a4`; base above. [Native/quality/regression steps](https://github.com/rapiddweller/archkeel/actions/runs/38993155229) / job `117279730328`; the later profile initializer in that run failed because the harness omitted the repository fixture import path.

- `ruff format --check` and `ruff check` for the four consumers; `mypy --strict src/archkeel`: PASS (144 files).
- Native `collect_constructs` over actual before/after source: 752 → 741 string-comparison observations, exactly eleven semantic observations removed and zero added. Scoped sites: eleven → zero; existing nominal comparison count increases by eleven. The four modules retain 60 other observations. This is a syntax census, not a defect count.
- Existing regressions: 597 passed on each revision across Target/UML authentication, projection, decisions, record/codec/protocol and saved/full report behavior.
- Fixed real inputs: 2.1 governance, 2.2 nested UML and nested legacy 2.1; compact/full architecture queries. [Report-byte proof](https://github.com/rapiddweller/archkeel/actions/runs/38994101160) / job `117282674578`: six graph outputs match raw bytes; eighteen packet/command-result/saved-replay outputs differ only at `analyzer.code_digest` or its projected `analyzer_digest`. Exact recursive differences are checked before normalizing those eighteen known identity fields for byte comparison; codec round trips pass. `check.observation` deliberately combines `package_digest()` with the adapter identity, and `package_digest()` hashes the changed Python sources. Loaded Core paths/hashes prove actual old/new execution. This is not raw parity for those eighteen identity-bearing outputs.
- Independent Astra: source-approved `226538de2fe92d223f32d4be271550edbc314a14`; approval carried after exact review of the two Ruff-only import-order swaps to `1a0fba765ef01b270dd7b7a38dd329fb544076a4`. No blocking findings.
- Harness corrections stayed on the separate verification branch: match native AST forms, preserve repeated-expression multiplicity, and include the repository fixture import path. Production changed only the two Ruff-required import orders after the initial candidate.

Fresh combined metadata, NoWrite, full-suite and Main integration remain with Root and the Main steward; this PR does not claim those gates.
