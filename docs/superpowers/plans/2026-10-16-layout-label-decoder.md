# Report layout label decoding correction

The complete Graph/Version suite passed 9,643 tests but the unchanged small-report limit failed at 2,000,055 bytes. Both native graph labels and edge labels duplicate the same inventory, duplicate-ID, finite-geometry and absolute-position decoding.

Move those identical bodies into one local readLabels function inside decodeLayout. It retains the same owned inventories, error texts and coordinate arguments. This removes 511 emitted source bytes and reduces runtime source lines; it adds no build step, representation, cache, schema or budget. Existing actual ELK, corrupt output, route and small-report tests must pass. Independent final review and exact branch CI gate integration.
