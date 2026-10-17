# Python receiver origins

Issue: #542. Base: 6fba15000baaeff6a274058291654b7301f2077a.
Branch: fix/542-python-receiver-origin.

## Approved bounded design

The existing receiver_types module owns ReceiverOrigin with LITERAL, ANNOTATION and
DOCUMENTED values. ReceiverType stays in that module, retains its constructor shape,
and normalizes valid legacy strings once in its frozen post-init. The Origin import
name remains an alias of the nominal type. Invalid values raise ValueError.

Calls produces and merges nominal origins; resolve keys its existing verdict table
by ReceiverOrigin. Type names, method tables and wire status/reason text stay data.
No additional UNKNOWN origin, namespace inference or method-resolution authority.
Ambiguous and shadowed receiver bindings retain their existing unresolved outcomes.

## Steps

- [x] Commit this plan before production changes.
- [x] RED: nominal field/producer identity, real calls._bind_receiver raw dispatch,
  invalid legacy inputs, and actual Source versus an independently authored origin Target.
  Pin valid legacy verdicts, merge order and ambiguous/shadowed controls at the same time.
- [x] Replace the origin Literal with the owned Enum, retain Origin as an alias,
  normalize ReceiverType inputs once with builtin-qualified object.__setattr__,
  and migrate calls/resolve without changing their algorithms.
- [x] Keep one whole-module guard only for the completely migrated receiver_types
  module; verify raw equality/membership/Enum.value source mutations and
  origin-to-str widening against unchanged Targets.
- [x] Run receiver/call/lexical/source/binding regressions, Ruff, Mypy and native
  validation against this exact base with 918 unresolved / 58 unknown / 52 typing / 0
  violations. Generate/replay the normal v2 amendment without changing budgets.
- [ ] Deliver an isolated PR and freeze the exact product source for final Astra.

## Isolation

Property operation/origin and its legacy Dict/wire port remain a separate increment.
The Source physical-line correction in #553 remains independent and must be preserved
when the branches are combined. Temporary verification workflows stay outside product.

RED evidence: hosted run 38955338212, candidate d0bba4984dd1ad9f3218ab3e02827a2e8f0d3fae:11 expected assertion/validation failures, no setup errors. Actual Source fails the authored origin Target and native observations expose the raw literal-merge comparison.

GREEN evidence: hosted run38955611416, candidate 9e25120a338bfd6b37b85644526a46c817cd95cd:
552 passed; Ruff and Mypy 133 clean. Native validation and normal v2 amendment
replay against 6fba15000baaeff6a274058291654b7301f2077a both retain 918 unresolved /
58 unknown / 52 typing / 0 violations, without diagnostics or failures.
The canonical formatter patch is applied to the product sources/tests.

Wire proof: hosted run38955775524 compares actual complete call records from the
base and candidate across five scenarios/ten calls, including ambiguous/shadowed
controls. Payloads are byte-identical: 6662 bytes, SHA256
d3b300b179ed68cb0b783dd6a73cc9632ff2dbfc77ad49a82c8366d953be51b0.
No JSON payload snapshots or temporary verification workflows enter the product.
