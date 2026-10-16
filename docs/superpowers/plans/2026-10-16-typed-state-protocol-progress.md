# SDD ledger — plan: docs/superpowers/plans/2026-10-16-typed-state-protocol.md

Pre-flight: one task; shared contract/Makefile updates are supplied to the parent for sequential integration.
Ruling: Remote isolated branch and hosted Actions replace local worktree/scripts because executor cannot fork; no production behavior depends on this adaptation.
Ruling: Keep the existing public state_facts module scope; add owned enum types without creating a parallel API facade. Private codec event tag remains internal.
Task 1 RED: run 38930727279, 9 failed and 40 passed. Nominal type/value assertions, absent authored Target and native guards failed as expected.
Task 1 in progress: implement nominal controls and enum parsing, then verify the actual native own budget.
