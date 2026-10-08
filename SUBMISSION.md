Contribution Date: 10/08/2026

Title: Setlist Bridge

Notes / Description:
Setlist Bridge is a reusable GenLayer contract for assembling a live set from AI-reviewed directed transitions. First-time use: deploy with a public show brief and transition rule; submit at least three track IDs and text briefs; as curator, lock the tracks. Review each intended adjacent pair with `review_transition`. GenLayer validators independently agree on `FLOW`, `BREATH`, or `CLASH`; only `FLOW` or `BREATH` may enter the final path. Read `get_transition`, then the curator calls `begin_order`, `append_track` for every remaining track, and `finalize_set`. Read `get_set` to confirm `FINAL`. The contract does not hear audio, book performers, verify a track exists, or move funds. A short note is leader-generated, not consensus-checked. Oct 8 re-audit fixed an edge-key collision; lint, strict typecheck, 5 direct tests, five-validator GLSim, and a fresh full-lifecycle StudioNet test passed.

Evidence & Supporting:

GitHub repository: https://github.com/Leokings/setlist-bridge (public; MIT licensed)

Contract file: contracts/setlist_bridge.py

StudioNet evidence: deployments/studionet.json

StudioNet contract: 0x6516Be0770b1DEb694eAEc102fB19b6C29Bf2b7c

Deployment transaction: 0x42872a0c60281ec3e688550de95994da4570c1d652f6469aa78082716d91bc71

Intelligent transactions: 0xfac314eb0353b1b9affb99dd20aab74e8ef401859fbf3e30cc3f437a4c02f132 and 0xde076d56152454f434b5d4407f7883782a638c0ff6e0150f5e8830aac83006f9

Finalization transaction: 0x9c6199e61b4666ae3d5e348ddd5c5cbed982f1e0dcf8a14046bfd14d5c982f75

Audit status: PASS on technical gates; see AUDIT.md and deployments/studionet.json. Reviewer judgment is not guaranteed.
