# Architecture

## Flow

track collection -> directed transition review -> curator-selected path -> deterministic completion.

## Responsibility boundary

Frontend or backend: wallet UX, indexing, private drafts, and non-authoritative previews.

GenLayer contract: frozen public evidence, independent validator replay of the bounded semantic decision, deterministic state transitions, and the human-controlled terminal action.

External systems: none are queried by this version.

## Originality boundary

This repository uses a domain-specific state machine and settlement effect. It is not a renamed copy of a check, match, route, or generic approval contract.

