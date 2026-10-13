# AD-225 Compact validation decisions

`validate --json` keeps its full open-pair list by default. The explicit
`--compact-open-decisions` option lists observed undecided crossings instead, using
the same IR summary as `init`. Both modes report exact `open_decision_count` and
`open_decisions_complete`; unavailable summaries remain null. Completeness means
every counted pair is listed, including when dense observation covers all open pairs.

Validation previously materialized every ordered pair twice: once to count the
single open-decision diagnostic, and again for the result. Count that diagnostic
with the exact summary so compact retrieval never constructs unobserved options.

Omitted pairs remain undecided. Compact output changes no contract, verdict,
UNKNOWN evidence, measurement, diagnostic or exit code. A positive total with
an empty list still rejects the open contract. Existing full retrieval remains
available by omitting the compact flag.

Rejected: changing validate's default to compact breaks full-list consumers;
truncating without totals hides missing decisions; deriving permissions from
observed imports invents architectural intent. No arbitrary cap or pagination
is needed for the observed-crossing summary already available in IR.

Limit: dense observed crossings can still require a quadratic list. The summary
covers root component pairs, following the existing full-list semantics, and
does not replace scoped rule assessment or prove whole-architecture conformance.

Proof: sparse 39/100-component retrieval and full 39-component enumeration,
dense/empty observations and retained UNKNOWN evidence in
[test_cli.py](../../../tests/test_cli.py); supported JSON schema checks in
[test_result_schema.py](../../../tests/test_result_schema.py).
