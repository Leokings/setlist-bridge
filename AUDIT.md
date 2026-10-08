# Audit

Historical status: the original August 25, 2026 source passed the checks below. Its StudioNet deployment is archived in `deployments/studionet-2026-08-25.json` and is not evidence for the revised October source.

Verification:

- GenVM lint and semantic validation: PASS
- Pyright typecheck: PASS, zero errors
- Direct-mode tests: PASS, 3/3
- Five-validator GLSim: PASS, 1/1
- StudioNet finalized execution and LATEST_FINAL readback: PASS
- ABI-to-source schema comparison: PASS
- Workspace originality: PASS; 162 contracts scanned, new-corpus maximum 0.4276
- Runner pin, prompt-injection boundary, source policy, state/role/bounds, forbidden-operation, repository-shape, and secret scans: PASS

StudioNet:

- Batch: 1
- Public batch wallet: 0xaeFBE9faf54c2916E5257B8AD99200918DD32DA8
- Contract address: 0x37d21A2B2da9E45bF46360F71DD7F8dd76C5483c
- Deployment transaction: 0x4b98a08cfc8650f99612ae95f5147292f3f881cd606eefc02e557c238f3f037e
- Intelligent transaction: 0x19aed73b7806218317c1b5888c2e734441794e4ba1dffba4ce8917c99919c19f

Reviewed scope: contracts/setlist_bridge.py, repository tests, source policy, security boundary, and deployments/studionet.json.

## October 8, 2026 re-audit of revised source

Status: PASS on technical gates; reviewer judgment remains independent.

- Fixed a directed-edge key collision: IDs containing `>` could make two different track pairs share a transition key. Track IDs now accept only bounded ASCII letters, digits, `_`, and `-`.
- Made the trust boundary explicit: validator consensus checks the closed `FLOW`/`BREATH`/`CLASH` label, while the short explanatory note is leader-generated and not consensus-checked.
- GenVM lint and strict typecheck: PASS.
- Direct tests: 5/5 PASS, including malformed model output, unauthorized curator, key-collision rejection, CLASH rejection, and full set assembly.
- Five-validator GLSim full lifecycle: PASS.
- Fresh StudioNet full lifecycle: 11/11 receipts finalized and execution-successful. Two intelligent transition reviews returned `FLOW`; final state is `{"ordered_tracks":["A","B","C"],"phase":"FINAL","review_count":2,"track_count":3}`.
- Independent read-only StudioNet regression: PASS. The LF-normalized Git source bytes match deployed bytes at `0x6516Be0770b1DEb694eAEc102fB19b6C29Bf2b7c`, SHA-256 `ae90602a5b3a9655319b4d5e7e3e453d91ae5826dd829be9b6185bc800e551e4`.
- Repository history secret scan: no credential patterns found. No private key was stored in this repository; the test used a disposable in-process wallet.
- Public GitHub release: source, tests, StudioNet evidence, and MIT license are accessible without signing in.

Remaining limits: track descriptions, show brief, and transition rule are caller-supplied public text, not authenticated audio evidence. A `FLOW` label is a creative judgment, not proof that a live performance will work. The curator decides the final order. No funds are handled. These limits are stated in the README, source policy, and security notes.
