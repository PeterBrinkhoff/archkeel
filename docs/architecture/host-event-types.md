# Host replay event types

The existing host-record owner defines the two supported replay events in
`HostEvent`: expectation publication and candidate submission.
`HostRecord.ordering_event() -> HostEvent` is the consumed ordering port;
`event: str` remains the legacy constructor and replay-wire field.

`parse_records` converts at its existing SHA, event, timestamp validation boundary.
`check_order` reads the port after validating each timestamp, preserving errors
for legacy records. GitLab emits the same replay values. JSON bytes do not change.

GitHub provider event names are open observations. They are not members of this
local replay domain; unfamiliar provider events retain the existing UNKNOWN path.
