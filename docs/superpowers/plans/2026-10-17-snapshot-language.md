# Snapshot language ingress implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the nine raw language dispatch branches in revision snapshots with the existing canonical Facts Language.
**Architecture:** Keep Git/archive I/O in check.snapshot. Its two existing archive entry points normalize supported legacy spellings to facts.Language; internal selection uses that type. The public context manager retains its validation sequence.
**Tech Stack:** Python 3.11, pytest, existing native Python observer and UML target comparison.
**Spec:** User-approved expanded issue #542: parser/protocol controls use canonical types while names, paths and bytes stay data.

## Constraints and design choice

- Reuse facts.Language; no new vocabulary, helper framework, module, dependency or ratchet ceiling.
- Keep all three supported spellings, archive bytes, selected files, metadata selection and resolver closure.
- Keep SnapshotError messages and roots → revision resolution → language rejection order.
- Invalid spellings remain errors. Normalization is at the existing archive ingress functions, which also retain direct legacy callers.
- Prefer typed ingress over a new dispatch registry or additional language-specific classes: the existing selection algorithm needs neither.
- Do not assert whole-module string-control absence: Git protocol bytes, filename suffixes and path safety still need separate semantic triage.

## Review focus

- Python, Dart and TypeScript enum inputs select the same exact files/bytes as legacy strings.
- Unsupported language spellings fail before archive/member reading.
- Unsafe roots and missing revision keep precedence over invalid language at the public context manager.
- TypeScript resolver inputs outside selected roots and explicit tsconfig paths remain present.
- Widening the public language parameter to str fails the unchanged independently authored Target.

## Task 1: Canonical revision snapshot language

**Files:** check/snapshot.py; tests/test_snapshot_language_types.py; docs/architecture/contracts/check.json; Makefile.
**Consumes:** facts.Language and existing materialize_git_snapshot, _git_archive_bytes, _materialize_archive.
**Produces:** the same archive/snapshot results through canonical Language-annotated ports.

- [ ] Add the nominal API/rejection/real archive tests and the independent public snapshot Target.
- [ ] Run the tests against unchanged production source; verify nominal port/Target assertions fail for the expected str annotation, while existing selection/rejection cases pass.
- [ ] Normalize at both archive ingresses; key suffixes and dispatch on Language; keep public validation order.
- [ ] Run new tests, existing snapshot/revision checks, strict typing, lint and native Target regression.
- [ ] Compare the actual native sites and full fixture report wire data before/after; never infer absence from a textual search.
- [ ] Open a separate draft PR, report exact cost and evidence, request independent Astra review. Root owns combined metadata/full-suite verification and merge.

## Ledger

Ruling: Use a separate remote branch and read-only hosted runner because the shared local executor cannot fork. Never mutate Main or the root integration branch.
Pre-flight: one task, no cross-task interfaces.
