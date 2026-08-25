# Audit

Status: PASS — final review and submission-blocker audit completed on 08/25/2026.

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
