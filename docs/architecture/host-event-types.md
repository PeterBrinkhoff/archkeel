# Host replay event types

The existing host-record owner defines the two supported replay events in
`HostEvent`: expectation publication and candidate submission.
`parse_event(value: object) -> HostEvent` is the single consumed conversion port;
`event: str` remains the legacy constructor and replay-wire field.

`parse_records` converts at its existing SHA, event, timestamp validation boundary.
`check_order` reads the port after validating each timestamp, preserving errors
for legacy records. GitLab retains its replay-wire dictionaries. JSON bytes do not change.

GitHub provider event names are open observations. They are not members of this
local replay domain; unfamiliar provider events retain the existing UNKNOWN path.
