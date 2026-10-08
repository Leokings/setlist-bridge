Contribution Date: 10/08/2026

Title: Setlist Bridge

Notes / Description:
Setlist Bridge assembles a live set from AI-reviewed transitions between public track briefs. First time: deploy with a show brief and transition rule, then submit at least three short track IDs and descriptions. The curator can remove unwanted submissions before locking the tracks. Call `review_transition` for each intended adjacent pair; validators agree on `FLOW`, `BREATH`, or `CLASH`. Only a `FLOW` or `BREATH` edge can be appended. Read `get_transition`; then the curator calls `begin_order`, `append_track` for every remaining track, and `finalize_set`. Read `get_set` to confirm `FINAL`. The contract does not hear audio, prove a track exists, or move funds. The short note is leader-generated, not consensus-checked. Oct 8 audit: edge-key and slot-lockup fixes, lint/typecheck, 10 direct tests, five-validator GLSim, and a complete 13-transaction StudioNet lifecycle.

Evidence & Supporting:

GitHub repository: https://github.com/Leokings/setlist-bridge (public; MIT licensed)

Contract file: contracts/setlist_bridge.py

StudioNet evidence: deployments/studionet.json

StudioNet contract: https://explorer-studio.genlayer.com/address/0xe09bbfde9406F625e8766C195115A87a5281184D

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x2090a989e08e51812fd947f5c0ea8ccece47cba90842e9db5be0f3ba72ad505f

Intelligent transactions: https://explorer-studio.genlayer.com/tx/0xbafba6c60e144db3248441383282b5b8240fbbf48dc671a90466661cf4f10705 and https://explorer-studio.genlayer.com/tx/0x4de32cb09dc134860a86b4082c037e0c512b89a0b5ac23708ba9985368a66976

Finalization transaction: https://explorer-studio.genlayer.com/tx/0x1cfaf0ff8561f8397b8ec768fdf86165d790f8f116bbeab3319d959bd7b2d8a1

Audit status: PASS on tested technical gates; see AUDIT.md and deployments/studionet.json. Reviewer judgment is independent.
