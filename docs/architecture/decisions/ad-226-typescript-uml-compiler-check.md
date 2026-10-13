# AD-226 TypeScript UML compiler acceptance

The TypeScript UML demo must pass a genuine compiler check as well as Archkeel's
source-fact and independent-Target checks. Python collector tests alone cannot
certify TypeScript type correctness.

`make typescript-compiler-check` invokes `tsc` from pinned `typescript@5.9.3`
against `fixtures/H-uml-typescript/tsconfig.json` with explicit `--noEmit`.
The pin matches the existing TypeScript compiler reference snapshots, including
this UML fixture. The Nest real-world snapshot's 6.0.3 pin belongs to that separate
upstream fixture; changing this demo's compiler/configuration is a later decision.

Full CI runs the compiler after the policy/package gate and before demo acceptance.
Release tags reuse that full verification workflow. `make demo-uml` runs the same
compiler before generating its three-language reports. A compiler error stops
later acceptance/report work, including parallel Make invocations.

This is a development prerequisite requiring Node and npm. It adds no package
runtime dependency: TypeScript source collection and `make typescript-native`
remain Python-hosted, and Dart collection remains SDK-free. Compiler success does
not establish UML conformance; the independent PASS/FAIL/UNKNOWN checks still own
that result.

Rejected: counting pytest as a compiler check; restoring a Node collector; adding
a package/plugin framework for one compiler invocation; requiring Dart's former
SDK path. The check covers the checked-in UML fixture, not every generated
negative demo variant or the separate Nest application.

Proof: `tests/test_make_gate.py` runs Make's ordering/failure paths and verifies
the full/release workflow route. Run `make typescript-compiler-check` for the real
compiler; a copied fixture with `const invalid: number = 'text';` must fail with
TS2322 and emit no JavaScript.
