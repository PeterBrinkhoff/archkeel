# Dart nominal control boundaries — implementation plan

> **For agentic workers:** Use superpowers:executing-plans; implement and verify each step before final independent Astra review.

**Goal:** Replace Dart implementation parser/protocol string dispatch with owned nominal values while preserving collected evidence and conservative unknowns.
**Architecture:** The existing parser owns syntax vocabulary and exported immutable syntax DTOs. A private parse-local adapter decodes each Tree-sitter node kind once, preserves raw node identity, and delegates only the Tree-sitter operations already consumed. Resolution owns resolution outcomes; shared facts own runtime-requirement states.
**Tech Stack:** Python 3.11, StrEnum, Tree-sitter Dart, pytest, native ArchKeel contracts.
**Spec:** User #542 expansion and the parent-approved isolated Dart scope.

## Constraints and review focus

- No casts, Any, ignores, rule exceptions, increased debt budgets, or unproved Dart-project construct capabilities.
- Names, paths, source text, and free-form diagnostic payloads remain data. Closed grammar is decoded as grammar or nominal values.
- Unknown node kinds retain traversable children and never become a known default.
- The parse-local node cache must preserve parent/field identity and must not outlive a parse.
- SDK-free collection, URI/part resolution, directive combinators, source spans, and Compass reports preserve their existing meaning.
- Shared RuntimeRequirementState, Language, SourceProfile and SourceSectionName have one owner in ir.facts.

## Task 1: Native RED controls

- [ ] Add actual-source DTO annotation checks and node-boundary tests.
- [ ] Add native literal/equality/membership/match/Final probes and unchanged authored Target annotation mutation controls.
- [ ] Run hosted tests against the unmodified Dart implementation and record expected failures.

## Task 2: Parser and resolution ownership

- [ ] Add parser-owned nominal DTO control values and a private finite syntax vocabulary.
- [ ] Implement the parse-local node view, including unknown-kind, parent and field tests.
- [ ] Convert parser text grammar through real decoders, preserving source text as data.
- [ ] Consume syntax enums in resolver and collection; resolver owns closed binding/outcome categories.
- [ ] Preserve serialized fact bytes and ordering at the existing output boundary.

## Task 3: Snapshot and native contract

- [ ] Reuse canonical RuntimeRequirementState and preserve the shared-wire producer changes.
- [ ] Preserve metadata/root grammar rejection and platform behavior.
- [ ] Publish named Dart ports and independently author nominal field intent in the existing Dart contract.
- [ ] Enable complete module string-control guards only after real positive source evidence.

## Task 4: Verification and handoff

- [ ] Run Dart SDK-free, parser, directives, resolver, partial UML, false-positive, rules, acceptance and Compass demo tests.
- [ ] Run Ruff, mypy, hygiene, exact native Target/mutation controls and full self-observation; retain or tighten the baseline.
- [ ] Regenerate the ordinary architecture amendment against the actual integrated predecessor.
- [ ] Return a clean product-only ref, exact changed-file list, evidence and code-cost explanation for independent Astra review.
