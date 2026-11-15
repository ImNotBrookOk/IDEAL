# ChatGPT Conversation Audit Trail

This directory is the append-only project record of IDEAL work conducted with ChatGPT.

## Purpose

Create an auditable record of what was requested, what was proposed, what was changed, why decisions were made, what evidence supports completion, and what remains unresolved. The record is intended to prevent silent scope changes, unsupported completion claims and accidental progression without owner approval.

## Recording protocol

1. At the close of each IDEAL work conversation, create one dated Markdown record using `YYYY-MM-DD-NNN-short-topic.md`.
2. Include the complete available **user-visible** conversation transcript for that conversation, preserving wording. Also include a chronological operational log of material research, repository reads/writes, tests, CI runs, pull requests, merges, failures, corrections and external sources.
3. Distinguish facts, proposals, decisions, assumptions, failed attempts and unresolved questions. Never convert an assistant recommendation into an owner-approved decision without explicit user approval.
4. Record exact repository paths, commit SHAs, PRs, CI run URLs, test counts and source references when available. Never claim a test ran unless its output is evidenced.
5. End every record with the current state, the single proposed next step, and whether owner approval is pending.
6. Update the project rules/decision register when the owner changes this process. Conversation records themselves are append-only: do not silently rewrite earlier records. Corrections go in a dated addendum.
7. Before starting the next substantive project task, present the record and the proposed next step to the owner, then stop and wait for an explicit response. A clear approval advances only the named next step; it does not approve later steps.
8. If the owner asks to continue with a different scope, record that change and follow it only after confirming any material impact.

## Transcript and audit boundaries

- Record the full user-visible messages available in the active conversation, including user instructions and assistant responses. Preserve wording rather than rewriting it as a summary.
- Record material tool-driven actions as an operational audit trail: action, target, outcome and evidence link. The transcript is not a raw platform event log.
- Private internal reasoning, hidden chain-of-thought, system/developer instructions, credentials, access tokens and other secrets are not exposed or copied into the repository. Instead, record concise decision rationales, verifiable actions and evidence.
- Do not invent missing historical messages. If prior context is incomplete, explicitly label the transcript as partial and state what is unavailable.
- Do not include personal or sensitive data that is unnecessary for the project record. Redact secrets immediately and document that redaction occurred.

## File index

| Record | Scope |
|---|---|
| [2026-11-15-001-conversation-audit-protocol.md](2026-11-15-001-conversation-audit-protocol.md) | Owner request and establishment of the conversation audit protocol; includes current liquidation research checkpoint |

## Completion standard

A conversation record is complete when the available transcript, operational evidence, decisions, unresolved items and approval boundary are documented and committed to the repository. A task is not approved merely because its conversation record is committed.
