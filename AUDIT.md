# Technical audit — 2026-10-08

Scope: current `contracts/setlist_bridge.py`, tests, `abi.json`, and the
StudioNet deployment in `deployments/studionet.json`.
Deployed LF-normalized source SHA-256:
`12f990d5f45f6fdff5235e7f209e35cf4695091c8c0a86b9816f43a88217ca60`.

## Findings and fixes

- Earlier this day, a directed-edge key collision was fixed by restricting
  track IDs to bounded ASCII letters, digits, `_`, and `-`; `>` cannot be used
  to alias two directed track pairs.
- Validator consensus checks the closed `FLOW`/`BREATH`/`CLASH` label. The
  short note is leader-generated, not consensus-checked. The view and docs
  disclose that distinction; a direct test proves a conflicting label fails
  validation while a different note with the same label does not.
- Public callers could fill all eight track slots and leave the curator no
  recovery path. The curator can now `remove_track` while `COLLECTING`, freeing
  a slot without changing any already reviewed transition. Removal is barred
  after lock. Direct tests cover unauthorized removal, capacity restoration,
  reusing an ID, and the post-lock barrier; the live test exercises removal.

## Checks actually run

| Gate | Result |
| --- | --- |
| GenVM lint and strict typecheck | PASS, zero diagnostics |
| Direct tests | PASS, 10 tests covering roles, phases, edge collision, malformed output, CLASH, consensus mismatch, note scope, and slot recovery |
| Five-validator GLSim full flow | PASS |
| StudioNet full flow | PASS, 13 finalized execution-successful receipts |
| Independent read-only StudioNet regression | PASS, all 13 receipts rechecked |
| Latest-final state | PASS, `FINAL`, tracks `A → B → C`, 2 reviewed transitions |
| Deployed source and ABI | PASS, deployed LF source matches repository; deployed schema equals `abi.json` |

Current contract: https://explorer-studio.genlayer.com/address/0xe09bbfde9406F625e8766C195115A87a5281184D

AI review transactions:
https://explorer-studio.genlayer.com/tx/0xbafba6c60e144db3248441383282b5b8240fbbf48dc671a90466661cf4f10705
and
https://explorer-studio.genlayer.com/tx/0x4de32cb09dc134860a86b4082c037e0c512b89a0b5ac23708ba9985368a66976

Finalization:
https://explorer-studio.genlayer.com/tx/0x1cfaf0ff8561f8397b8ec768fdf86165d790f8f116bbeab3319d959bd7b2d8a1

The exact transaction order is in `deployments/studionet.json`. Historical
deployments at `0x6516Be0770b1DEb694eAEc102fB19b6C29Bf2b7c` and
`0x37d21A2B2da9E45bF46360F71DD7F8dd76C5483c` do not represent the
current source.

## Remaining boundaries

Track descriptions and the show's rules are public caller-provided text, not
authenticated audio. Anyone may request a transition review after lock; the
first review of a directed pair is final for this deployment, although the
curator alone chooses the final order and cannot append an unreviewed or
`CLASH` pair. Creative AI judgments can vary or fail consensus. The contract
holds no funds. Technical tests do not guarantee steward acceptance or prove
that every conceivable flaw is absent.
