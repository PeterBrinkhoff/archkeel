# Delta version types

Part of #542. The existing model owns the four supported Delta format identities and the typed ArchitectureDelta version field. One direct nullable-count policy is shared by codec and expectation ports. Public version grammar text, historical bytes/errors and valid legacy constructors remain compatible. Public dimension/change strings and all other protocol domains remain open or separately pending as before; no entire Model/codec raw-string absence is claimed.

Production cost is 26 net lines (+43/-17) in four existing files, below the initial estimate. Six independently authored Target entries reuse the existing model anchor; 40 native controls cover the real enum/field/parameter/return ports, exact supported wire versions, constructor normalization, raw-decision reversions and open extension values. Existing parity hashes are unchanged.
