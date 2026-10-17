# Typed component-pair permission values

Part of #542; bounded follow-up to the reviewed Atlas deviation boundary.

The existing owner `archkeel.ir.architecture_projection` must define `PermissionStatus` as a nominal string enum with exactly ALLOWED="allowed", FORBIDDEN="forbidden" and UNDECIDED="undecided". `PermissionProjection.status` uses that canonical type. Its existing valid raw-string constructors normalize once and preserve frozen value semantics; invalid supplied states reject.

The actual four producer branches and four permission-status decisions in `ir.report_projection`, plus the one allowed-permission decision in `render.atlas._level_balance`, use that owner directly. IDs, reasons, rule names and other open data remain strings. Existing ordered JSON, saved-report dictionaries, pair constraints, balances and UNKNOWN behavior remain unchanged.

The native authored Target independently pins the actual enum owner and status field. The complete architecture_projection module gets a native raw-literal-control guard, exercised with real source mutations. A widened status annotation must produce a trace-valid native type failure under unchanged intent.

This is not a whole-report_projection or whole-render absence claim. Their other record/UI domains, the projection format version and browser controls remain pending. Do not add an unused generated browser vocabulary, a second render enum, a new value module, generic conversion framework, allowances or higher budgets. Aim for at most 50 added manual production lines; report tests, authored intent, documentation and generated receipts separately.
