# Evidence class consumer plan and evidence

> **For agentic workers:** Use superpowers:executing-plans for this bounded refactor.

**Goal:** Part of #542: keep eleven existing declaration dispatch decisions in the shared nominal evidence domain.

**Architecture:** `archkeel.ir.facts.EvidenceClass` already owns the vocabulary and `Record.evidence_class` annotation. `facts_codec.parse_record` validates the wire string into that enum. The published `model.EvidenceClass` alias is the same object. Consumers compare the existing enum; no new domain, constructor, wrapper or target declaration is needed.

**Spec:** #542 and the approved eleven-site follow-up; base `c725df96543d1dd7ec4e20887a486ec9a7143c8a`.

## Scope and checks

- [x] Inspect actual Record ingress, canonical owner, facade identity and existing interface ports.
- [x] Replace seven UML authentication comparisons, two Target record authentication comparisons, one permission projection comparison and one rule assessment comparison. Three new imports stay private; decisions reuses its existing EvidenceClass import.
- [ ] Verify exact before/after native sites, meaningful existing UML/projection/record/decision/codec regressions, strict Ruff/mypy and real old/new fullReport serialization profiles.
- [ ] Obtain independent Astra source review and leave integration and fresh combined writer/receipt/NoWrite/full-suite evidence to the Main steward.

**Ruling:** Reuse existing behavior regressions and native before/after evidence for this behavior-preserving refactor, as explicitly authorized; do not add tests that mirror the eleven implementation lines.

**Limits:** This change does not activate native guards for all four modules. TypeScript/JavaScript coverage remains PARTIAL. The inherited combined metadata is stale for this target and is not fresh evidence. Existing serialization uses of `.value` remain at their wire boundaries. No ratchet budget or contract changes.

## Verification evidence

Pending hosted read-only verification; record exact source head, commands and run link here after results.
