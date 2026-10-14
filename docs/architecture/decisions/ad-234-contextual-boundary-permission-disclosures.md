# AD-234: Contextual boundary permission disclosures

The unselected report fact sheet shows neutral permission counts and a closed
complete audit. Selecting a component, module or entity shows only the recorded
permissions for that scope. Diff also retains the exact declaration/fact
counterparts. Target uses declarations; As-Is uses applied facts.

Group permissions by rule, with a separate unmapped group in the root audit.
Opening a group builds the first 20 record summaries. A native button reveals
the next 20 until every record is reachable. Opening a record builds its full
selector, rationale, opacity caveat, IDs, locations and existing navigation.
Keep disclosures and paging keyboard accessible and usable offline.

Hashes open the exact record and its parent disclosures. A record beyond the
first batch is inserted directly without building all intervening rows. Later
paging does not duplicate it. Rule status stays with the evaluator; a permission
count or accepted fact does not prove PASS. Canonical evidence remains complete.

The published DATAMIMIC CE snapshot has 135 declarations and 132 applied facts.
The previous Diff root created 267 detailed rows while disclosures were closed.
Collapsed HTML therefore did not bound its DOM cost. Defer DOM construction
instead of changing evidence, adding a framework or fetching detail data.

Rejected: truncating evidence, eager hidden bodies, and an unbounded initial
list. The 20-record batch bounds each opening, not the eventual audit size.
Reopening a loaded disclosure retains its contents for the current selection.

Tests: `tests/test_boundary_permission_presentation.py` checks all three lenses,
root counts, selected scopes, deferred bodies, paging, keyboard access and
offline hashes beyond the first batch. The existing boundary/alias regressions
in `tests/test_atlas_report.py` check exact metadata, escaping and routes.
