# Shared runtime bootstrap implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Give the three source collector entry points one nominal owner for the direct-start protocol.

**Architecture:** The existing analyzer Process owner owns a small bootstrap module and its explicit `is_direct_entrypoint(module_name: str) -> bool` port. The module classifies arbitrary incoming names once through a private Enum for the closed `__main__` marker. Each language entry retains its statically known `main()` and `SystemExit`; no callback indirection or resolver authority is introduced.

**Tech Stack:** Python 3.11+, pytest, existing native architecture observation/Target, Ruff and Mypy.

**Spec:** Issue #542 and the approved read-only Python/runtime inventory. The parent explicitly chose decision ownership over a higher-order callback to preserve static call resolution.

## Global constraints

- Base: final collector-wire carrier 6e3913738d95a22cb9b1572f51822892548f2270.
- Preserve resolver checks, request/response bytes, supported protocol versions and exception/exit behavior.
- Preserve CLI __main__, all source proof limits and baseline ceilings (918 unresolved /58 unknown /52 typing /0 violations).
- Add no generic converters, dependency, callback framework, per-language Enum, allowances or budget changes.
- Use an isolated GitHub branch and hosted verification because the execution workspace cannot fork.

## Review focus

- Importing any language entry must not touch stdin/stdout.
- Arbitrary non-main module names remain passive; invalid request and wrong resolver exceptions retain their types.
- Real subprocess entry points and direct main calls produce identical response bytes from the same source snapshot.
- Original statically known main/Exit sites remain explicit; native sites are compared before/after.
- Private nominal marker and public bool signature are authored intent, independent of observed implementation.

## One independent bootstrap increment

**Files:** create src/archkeel/analyzer/bootstrap.py, tests/test_shared_runtime_bootstrap.py, docs/architecture/shared-runtime-bootstrap.md; modify the three analyzer language entry.py files, architecture-contract.json, docs/architecture/contracts/analyzer.json and Makefile.

**Interfaces:** public is_direct_entrypoint(module_name: str) -> bool. Private marker enum _EntryMode.MAIN has wire spelling __main__. The Process component publishes only the function; all three existing language-to-Process edges already authorize it.

- [x] Commit plan and independently authored Target before production.
- [x] RED: actual three-entry source fails a native raw-control guard; absent owner/port fails the independently authored Target and public API assertions. Existing real-entry, passive-import and exception controls remain passing.
- [x] Implement the smallest owned marker classification and replace only each direct-start condition.
- [x] GREEN: native positive source/Target checks, raw-dispatch probes (equality, membership, match, alias, Enum.value) and bool-return/Enum-kind mutation controls.
- [x] Exercise actual Python/Dart/TypeScript main functions and subprocess module starts, with exact same-snapshot wire bytes and error paths.
- [x] Run related protocol/native tests, Ruff, Mypy, hygiene, native self-validation and before/after unresolved/PARTIAL/UNKNOWN site comparison.
- [x] Generate/replay normal v2 amendment against the exact base; keep baseline bytes unchanged.
- [x] Export clean product carrier, no temporary workflow, and hand off independent Astra/full-regression review.

## Verification and rulings

- Ruling: share the protocol decision through a bool port, while each entry retains its statically known main/SystemExit targets — this avoids introducing an unresolved callback solely to deduplicate a start idiom; cost: three explicit launch branches remain, using one marker owner.
- Ruling: GitHub branch isolation and hosted commands replace unavailable local processes — no shared Main edits or local execution; cost: final whole-branch Astra and combined regression remain parent integration gates.
- Ruling: include bootstrap.py in each collector code digest — shared startup is collector source; cost: adapter digests intentionally change when this shared implementation changes, while request/response grammar and same-snapshot main/module bytes remain identical.

RED run38964550700:13 expected missing-owner/Target/raw-dispatch assertions failed,19 behavioral controls passed. The earlier Dart fixture setup omission was corrected before production.
GREEN run38964732019:218 tests and11 hygiene checks passed, Ruff/Mypy133 clean.
Digest RED/GREEN and expanded regression run38965125573:3 expected old-runtime digest failures, followed by316 passing protocol/runtime/native tests and11 hygiene checks. Formatter patch empty, Ruff and Mypy133 clean.
Native run38964875426: normal amendment generation and no-write replay both exit0, diagnostics/failures empty;918 unresolved,58 unknown,52 typing positions,0 violations. Baseline bytes and all ceilings unchanged.

The exact native site comparison reports no added or removed unresolved/PARTIAL site:
918 unresolved and2453 PARTIAL before/after. bootstrap.py and all three entry.py modules have no such sites. Existing runtime.py sites shift by one physical line because the shared digest path is added; their callers, expressions, reasons and counts stay identical. Boundary UNKNOWN positions remain Render29/Check19/Analyzer2; the full native unknown scalar remains58.
No compiler/binding, namespace/member, callback, GenericAlias, property or other proof authority changes.
The umbrella issue542 remains open for the separately inventoried control scopes.

This isolated carrier is ready for independent Astra review and the parent's combined full regression; those integration gates are not claimed complete here.
