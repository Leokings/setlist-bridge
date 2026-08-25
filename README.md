# Setlist Bridge

Builds a live set from validator-reviewed transitions between participant-supplied track briefs.

This standalone repository contains one reusable GenLayer Intelligent Contract, direct tests, a five-validator GLSim flow, and an opt-in StudioNet smoke test. It has no frontend, token, payout, proxy, or repository secret.

## GenLayer-native decision

track collection -> directed transition review -> curator-selected path -> deterministic completion.

## Evidence boundary

The show brief, transition rule, and track descriptions are caller-supplied public text. Validators do not hear audio or browse.

## Limits

Transition labels are creative judgments. The curator retains final ordering authority and the contract never books performers or handles money.

## Verify

Run GenVM lint before tests, then direct tests, then the five-validator integration test. StudioNet evidence is written to deployments/studionet.json only after finalized successful execution and final-state readback.

