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

- [ ] Commit plan and independently authored Target before production.
- [ ] RED: actual three-entry source fails a native raw-control guard; absent owner/port fails the independently authored Target and public API assertions. Existing real-entry, passive-import and exception controls remain passing.
- [ ] Implement the smallest owned marker classification and replace only each direct-start condition.
- [ ] GREEN: native positive source/Target checks, raw-dispatch probes (equality, membership, match, alias, Enum.value) and bool-return/Enum-kind mutation controls.
- [ ] Exercise actual Python/Dart/TypeScript main functions and subprocess module starts, with exact same-snapshot wire bytes and error paths.
- [ ] Run related protocol/native tests, Ruff, Mypy, hygiene, native self-validation and before/after unresolved/PARTIAL/UNKNOWN site comparison.
- [ ] Generate/replay normal v2 amendment against the exact base; keep baseline bytes unchanged.
- [ ] Export clean product carrier, no temporary workflow, and hand off independent Astra/full-regression review.
