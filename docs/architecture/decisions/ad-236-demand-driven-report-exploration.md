# AD-236: Demand-driven report exploration

The hidden Health check eagerly built every module matrix cell and every link
inside the closed module list. The frozen CE report contained 3,534 matrix DOM
descendants before the drawer opened. This work repeated on lens changes.

Build matrix DOM when Health check opens. Keep the current matrix when closing
and reopening the drawer; discard it with the rest of exploration when a new
scene renders. Build module links only when their native details element opens.
Counts, Core status, findings and question candidates stay available beforehand.

The existing Flow presentation seam exposes the drawer's open state. The
Explorer remains responsible for DOM; scene projection and authenticated data
stay unchanged. Matrix grouping, measurement, coordinates and keyboard actions
use the existing implementation. No network dependency or renderer is added.

Question selection updates highlight classes and the Inspector without replacing
the matrix. It reveals and focuses the matrix after opening Details, including
the narrow-screen path where inspection otherwise closes Health check.

Rejected: eager hidden rendering, which consumes time and DOM before use;
Canvas/WebGL or a new UI framework, which would duplicate existing navigation
and accessibility behavior. Virtualization is unnecessary for this bounded fix.

Limit: opening a large matrix still builds all its cells. Findings and summary
markup remain eager for existing hash routes. A changed scene invalidates the
current matrix and module-list DOM rather than retaining every visited scope.

`tests/test_report_lazy_explore.py` checks structural deferral, counts, native
keyboard expansion, drawer reuse, lens changes and visible question selection
at desktop and mobile widths under offline file navigation. Existing Atlas
tests retain cell statuses, axis geometry, source routes and finding links.

Performance observations use the same frozen CE payload; browser timings are
diagnostics, not CI assertions. Combined-preview acceptance remains required
before merge.
