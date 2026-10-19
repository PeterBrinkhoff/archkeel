# AD-242: Explicit browser module ports

First-party browser dependencies use named ES imports and exports. The existing
nine source identities, ownership boundaries and exact port restrictions remain.
Compatibility globals remain for existing callers; internal calls use lexical ports.

A pinned build-time bundler produces one inline offline explorer asset. Terser
still verifies Flow publication independently. Generated output must match its
sources and locked tools before publication; installed reports need no Node or
network. Standalone report entry points retain their separate behavior.

ELK remains a pinned external dependency with verified source bytes and license.
Lexical imports establish dependency identity, not vendor runtime purity. Classic
UMD probes continue to report UNKNOWN after unproved calls or constructors.

Native named-import evidence requires an actual source binding. Missing, competing
or unsupported bindings remain UNKNOWN; spelling alone cannot certify a port.
A handwritten module rewriter or an ELK purity whitelist would add weaker machinery.

Alex expressly accepts an unresolved-call ceiling of 840, replacing 832 after the
eight additional Source/browser calls. The canonical baseline amendment binds this
specific change. No other rule, debt budget or performance gate changes.

Required checks: actual-source PASS, forbidden-port FAIL, missing-publication
UNKNOWN or build failure, stale-output rejection, offline browser navigation,
layout/export behavior and wheel/sdist source parity. All existing quality gates
and other budgets remain unchanged.
