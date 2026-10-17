# Atlas deviation boundary design

Part of #542; follows the frozen Scene #573 source at `0aee692c767150847089dbcfdcf1765464837ab6`. This stage owns the two recorded Atlas deviation kinds and their actual pair classification. It does not close all Atlas/UI states.

The current `render/atlas.py` has 829 lines and 20 payload/projection functions. Its `_level_balance` builds five-field deviation dictionaries; `_atlas_levels` reparses their IDs and `atlas_payload` publishes them. The browser `atlasScene` repeatedly rebuilds a level/pair map and compares its values to raw deviation strings.

The coherent extraction is a value boundary with behavior: `render/atlas_deviations.py` owns the immutable deviation value, deterministic declared-minus-used/used-minus-declared derivation, IDs and explicit wire emission. It does not own architecture permission decisions, report packing or any Core Observation. This is more than a separate enum catalog. Its browser consumer owns validation and level/pair classification for that same value.

- `AtlasDeviationKind` owns exactly `allowed_unused` and `undeclared`; the existing generator derives its browser spelling from this Python owner.
- `AtlasDeviation` has `id: str`, `kind: AtlasDeviationKind`, `source_id: str`, `target_id: str` and `level_id: str | None`. `level_deviations` derives immutable rows in the current kind and sorted pair order; `to_wire` emits the existing five-key dictionary in the original order with a plain string kind.
- Browser decoding validates this precise DTO once at the existing cloned Atlas ingress. A checked classic-JS consumer keeps these same row objects and indexes their level/pair identities. Its `isUndeclared` and `unused` operations replace the four raw kind comparisons in `atlasScene`.
- Existing Scene modes and graph domains retain their canonical owners. This cut does not move AssessmentStatus derivation, open actor labels, layers, arbitrary names or IDs.
- Missing legacy `deviations` remains equivalent to an empty list; explicitly malformed rows reject. Input JSON, stable IDs, key order, output scenes/Mermaid and the existing single Atlas clone remain compatible.
- Maximum 160 new manual production lines (generated TS/JS and tests/docs counted separately). Expected 110–140: Python value/derivation ~45, concrete protocol ~20, checked browser consumer ~45, integration/generator ~15. Stop and narrow before exceeding the limit.
- No new compiler, bundler, graph copy, cache framework, cast, any, ignore, spelling registry, historical snapshot or allowance/budget increase.
- Python native intent pins the actual DTO kind and derivation return, with source-widening controls and a whole-module guard on this cohesive new owner. Native JS literal mutation is a positive PARTIAL witness; clean source never proves whole-browser absence.
- The existing IR-owned PermissionStatus Literal and its raw allowed comparison remain a separate pending concern; this stage makes no whole-Atlas absence claim. Root owns final composite native measurement and the exact normal amendment.
