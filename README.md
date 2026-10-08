# Setlist Bridge

Builds a live set from validator-reviewed transitions between participant-supplied track briefs.

This standalone repository contains one reusable GenLayer Intelligent Contract, direct tests, a five-validator GLSim flow, and an opt-in StudioNet smoke test. It has no frontend, token, payout, proxy, or repository secret.

## GenLayer-native decision

track collection -> directed transition review -> curator-selected path -> deterministic completion.

## First-time use in GenLayer Studio

1. Deploy `contracts/setlist_bridge.py` on StudioNet. Enter a public `show_brief` (the intended arc of the performance) and a public `transition_rule` (what should count as a good adjacent move). The deploying wallet becomes the curator.
2. From any wallet, call `submit_track` at least three times. Give each track a short ID using only ASCII letters, digits, `_`, or `-`, plus a 30–1,800 character text description. Descriptions are briefs, not uploaded audio.
3. The curator calls `lock_tracks`. Anyone can call `review_transition(left_id, right_id)` for each directed pair they want to use. GenLayer validators independently judge the pair as `FLOW`, `BREATH`, or `CLASH`. Read `get_transition` for the label; its short note is not independently consensus-checked.
4. The curator calls `begin_order(first_track_id)`, then `append_track` for each remaining track. Only a previously reviewed `FLOW` or `BREATH` edge can be appended. If a pair is `CLASH`, review and choose another path. Once every track is placed, call `finalize_set` and read `get_set` to confirm `phase` is `FINAL`.

All text and transactions are public. The contract does not play audio, verify that a song exists, book performers, or move funds.

## Evidence boundary

The show brief, transition rule, and track descriptions are caller-supplied public text. Validators do not hear audio or browse.

Track IDs are bounded ASCII letters, digits, `_`, and `-`; this keeps each directed transition key unambiguous. Validator consensus checks only the closed transition label. The short note is leader-generated context, not a consensus-checked explanation, and the view marks it as such.

## Limits

Transition labels are creative judgments. The curator retains final ordering authority and the contract never books performers or handles money.

## Verify

Run GenVM lint before tests, then direct tests, then the five-validator integration test. StudioNet evidence is written to deployments/studionet.json only after finalized successful execution and final-state readback.

