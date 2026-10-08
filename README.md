# Setlist Bridge

Builds a live set from validator-reviewed transitions between participant-supplied track briefs.

This standalone repository contains one reusable GenLayer Intelligent Contract, direct tests, a five-validator GLSim flow, and an opt-in StudioNet smoke test. It has no frontend, token, payout, proxy, or repository secret.

Current StudioNet contract: https://explorer-studio.genlayer.com/address/0xe09bbfde9406F625e8766C195115A87a5281184D

Licensed under the [MIT License](LICENSE).

## GenLayer-native decision

track collection -> directed transition review -> curator-selected path -> deterministic completion.

## First-time use in GenLayer Studio

1. Deploy `contracts/setlist_bridge.py` on StudioNet. Enter a public `show_brief` (the intended arc of the performance) and a public `transition_rule` (what should count as a good adjacent move). The deploying wallet becomes the curator.
2. From any wallet, call `submit_track` at least three times. Give each track a short ID using only ASCII letters, digits, `_`, or `-`, plus a 30–1,800 character text description. Descriptions are briefs, not uploaded audio. If unwanted submissions occupy the eight available slots, the curator can call `remove_track` before locking; removed IDs can be resubmitted.
3. The curator calls `lock_tracks`. Anyone can call `review_transition(left_id, right_id)` for each directed pair they want to use. GenLayer validators independently judge the pair as `FLOW`, `BREATH`, or `CLASH`. Read `get_transition` for the label; its short note is not independently consensus-checked.
4. The curator calls `begin_order(first_track_id)`, then `append_track` for each remaining track. Only a previously reviewed `FLOW` or `BREATH` edge can be appended. If a pair is `CLASH`, review and choose another path. Once every track is placed, call `finalize_set` and read `get_set` to confirm `phase` is `FINAL`.

All text and transactions are public. The contract does not play audio, verify that a song exists, book performers, or move funds.

## Evidence boundary

The show brief, transition rule, and track descriptions are caller-supplied public text. Validators do not hear audio or browse.

Track IDs are bounded ASCII letters, digits, `_`, and `-`; this keeps each directed transition key unambiguous. Open submissions can be curated only before `lock_tracks`; after locking, the track set is immutable. Validator consensus checks only the closed transition label. The short note is leader-generated context, not a consensus-checked explanation, and the view marks it as such.

## Limits

Transition labels are creative judgments. The curator retains final ordering authority and the contract never books performers or handles money.

## Verify

Run GenVM lint before tests, then direct tests, then the five-validator integration test. StudioNet evidence is written to `deployments/studionet.json` only after finalized successful execution, final-state readback, deployed-source equality, and ABI equality. The live test uses disposable in-process wallets and does not require a private key in this repository.

