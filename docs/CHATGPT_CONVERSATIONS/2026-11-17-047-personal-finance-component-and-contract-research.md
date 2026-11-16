# 2026-11-17-047-personal-finance-component-and-contract-research

## Scope

Continue IDEAL Phase 02 research following checkpoint 046. Determine whether the proposed private, single-user personal-finance domain is technically viable, identify reusable open-source repositories and standards, inspect licences and source-level design, and define a proposed source-observation/reconciliation/accounting contract.

Constraints retained:
- D-001 remains crypto perpetual futures only for active trading.
- D-017 remains Proposed.
- Phase 02 architecture/contracts only; Phases 03–19 remain LOCKED.
- Synthetic/public-source research only. No real financial records, bank credentials, provider account, runtime, installation, dependency or code changes.
- No external product adopted and no bank connection or hosting authorised.

## User-visible transcript

**User:** I had to start in a new conversation. Here is some context of what we last did. [User supplied the complete checkpoint 046 summary covering the MoneyMatter v0.33.7 and Firefly III Data Importer v2.3.5 source audit, findings, repository commits, governance and next research task.]

**User:** Keep going and see if its viable and we can build it in. Check if theres any repos or documents that'll fix what we need...??

**Assistant (interim):** The next step is to test whether we can build this as a reliable part of IDEAL without inheriting the weaknesses of existing finance applications. The investigation was split into reusable open-source components/accounting standards and an IDEAL-owned financial data layer. No real bank data or implementation was authorised.

## Operational log

1. Read the installed Acumen research skill and queried recent-change intelligence for personal finance/open banking/ledger tooling. The returned brief was not sufficiently relevant to determine current repository selection; no conclusion was based on it.
2. Located the connected IDEAL repository as ImNotBrookOk/IDEAL, default branch main. Read current personal-finance research, roadmap, decision register, future-scope register and conversation index before making documentation changes.
3. Reviewed official Akahu Getting Started and transaction documentation. Confirmed:
   - settled and pending transactions are separate API resources;
   - the official JavaScript SDK exposes cursor-paginated settled and pending transaction methods;
   - the SDK provides OAuth and webhook-signature helpers;
   - app secrets must remain server-side;
   - Personal Apps do not provide webhooks;
   - the current Getting Started page explicitly says Personal Apps are unsuitable for production-ready applications and that a full app/accreditation process is required before release of an Akahu integration to production.
4. Inspected the Akahu JavaScript SDK repository README and package metadata. Package metadata reports version 2.6.0 and ISC licence. No package was installed.
5. Inspected Formance Ledger README, LICENSE, architecture overview, idempotency documentation and release page. Confirmed MIT licence; v2.4.18 latest stable in inspected release page; v3.0.0-rc.3 is pre-release. The inspected v3 idempotency implementation hashes request content, returns historical outcomes for same-key/same-content retries, rejects same-key/different-content requests, and defaults to 24-hour TTL (zero means no expiry).
6. Inspected TigerBeetle README, Apache-2.0 LICENSE and official account/transfer/two-phase-transfer docs. Confirmed immutable account/transfer records, balanced pending/posted debit-credit invariants, pending/post/void lifecycle and correcting transfers rather than mutating/deleting prior transfers.
7. Inspected astt repository README, MIT LICENSE, Prisma schema, database documentation, architecture documentation, deployment/security docs and account API route. Confirmed useful multi-currency/net-worth/PWA product coverage, but no double-entry ledger; JSON financial APIs use IEEE-754 numbers; account deletion cascades through holdings/transactions; manual balance edits create EDIT cash transactions.
8. Inspected krbob/portfolio README, financial methodology and configuration docs. Confirmed transaction-canonical architecture, rebuildable read models, canonical decimal text, explicit stale/partial/unavailable data states, audit trail and restore preview. A root LICENSE file was not found through the repository contents API; code reuse is therefore not cleared.
9. Inspected OFX Statement README and project metadata, Beangulp licence/repository information, and the ofxstatement-iso20022 README. OFX Statement is GPL-3.0 and plugin-based; Beangulp is GPL-2.0-only and has no published GitHub releases in the inspected snapshot; the ISO 20022 plugin itself describes its implementation as trivial/naive.
10. Reviewed rotki, Ghostfolio and Flowfolio public repository/release information for specialist crypto/investment UI and accounting references.
11. No repository was installed or executed. No application tests, benchmark or synthetic fixture were run. Findings are source/documentation review only.
12. Updated IDEAL documentation on main. No source code, runtime dependency, configuration, workflow, secret, financial record or decision status changed.

## Findings and disposition

### Viability

A private single-user personal-finance domain is technically viable inside IDEAL's approved modular-monolith direction, provided it is a distinct bounded context with separate accounting and permissions. Consolidated net worth should be a read-only projection. Cash, collateral, margin and execution permissions must never be pooled across domains.

The difficult part is source reconciliation and secure long-term stewardship of sensitive data, not the dashboard. Manual entry and file import are viable without a bank connector. Akahu Personal App cannot be assumed to be a production integration route: official docs explicitly state it is unsuitable for production-ready applications. Provider clarification and the appropriate access/accreditation path are a gate before any deployed connector.

### Repository selection

- astt (MIT): best permissively licensed mobile/net-worth UX reference; not an authoritative ledger.
- krbob/portfolio: strongest portfolio read-model and operational-methodology reference; no root licence found, so no code reuse.
- Formance Ledger (MIT): ledger invariants/idempotency/projection reference; distributed cluster is wrong-sized; v3 is pre-release in inspected release page.
- TigerBeetle (Apache-2.0): immutable transfer and pending/correction reference; not a personal-finance app and excessive as an initial runtime dependency.
- Akahu SDK (ISC): possible server-side adapter helper if the eventual stack is Node/TypeScript; REST contract is portable. Personal App lacks webhooks.
- OFX Statement (GPL-3.0) and Beangulp (GPL-2.0-only): importer architecture references only pending licence decision.
- rotki (AGPL-3.0): specialist crypto accounting reference.
- Ghostfolio (AGPL-3.0): investment portfolio/mobile UI reference.
- Flowfolio (AGPL-3.0): secondary exact-decimal and portfolio performance reference.
- Firefly III and MoneyMatter remain as recorded in checkpoints 045–046.

No candidate is a complete, licence-clear, low-cost drop-in for IDEAL's requirements.

### Proposed architecture

Keep IDEAL-owned:
1. Source adapters and import batches.
2. Durable source identity registry scoped by provider, connection, source account and external transaction ID.
3. Immutable source-observation versions.
4. Reconciliation decisions for corrections, deletions, pending/settled changes and replacement IDs.
5. Immutable double-entry journal with correction/reversal postings.
6. Rebuildable balance, budget, investment and net-worth projections.

Important safeguards:
- Do not confuse API idempotency keys with permanent provider transaction identity.
- Do not infer deletion from absence in incomplete pagination, an incremental overlap or an outage.
- Pending transactions remain provisional snapshots and are not posted to the accounting journal.
- Correct already-posted entries through traceable adjustment/reversal records.
- Use decimal strings at financial API boundaries; keep currency, quantity, price and FX precision distinct.
- Preserve FX provenance and do not invent missing historical rates.
- Match transfers conservatively and require review for ambiguous cases.
- Reconcile provider balances against ledger-derived balances; do not rewrite journal entries to force agreement.
- Keep credentials out of logs, exports and GitHub. Use a dedicated encryption key with rotation/re-encryption procedure, not an authentication/JWT signing secret.
- Use versioned, checksummed backups, restore preview, atomic restore and tested recovery.

A minimum synthetic acceptance matrix is recorded in research section 19.4.

## Documentation changes

1. docs/PERSONAL_FINANCE_RESEARCH.md — appended sections 18–19 with repository/license/source audit, Akahu Personal App production caveat, feasibility assessment, proposed data contract invariants and synthetic acceptance matrix.
   - Commit: edd0aa5482b2097827d9793c87b0e3ee7007b779
   - Blob: 54726a549f74f6eb58230e09837b4de48b43bb0c
2. docs/FUTURE_SCOPE_IDEAS.md — appended F-004 research update; no proposal accepted.
   - Commit: 63cf252419b916bed381959ddf821b168c2a8a10
   - Blob: bb66d850dbc47be150d299ab6b43ae53abd8b589
3. ROADMAP.md — appended Phase 02 research checkpoint; later phases remain locked.
   - Commit: 493fad7e353782cbab6dec7c16ef960c12ce0b2f
   - Blob: 14ec2ed427235b9f26d9717cadf7a722aa48173e
4. docs/CHATGPT_CONVERSATIONS/README.md — added checkpoint 047 index entry.
   - Commit: 047933568321ec5c2a54dc81f192fdef1e542c45
   - Blob: 1d5889206dc046a7e3dfedcfe6867b4aef16138d

Fetch-back verification is required after this record is committed.

## Sources inspected

- https://developers.akahu.nz/docs/getting-started
- https://developers.akahu.nz/docs/accessing-transactional-data
- https://github.com/akahu-io/akahu-sdk-js
- https://github.com/mike840609/assets_tracker
- https://github.com/krbob/portfolio
- https://github.com/formancehq/ledger
- https://github.com/tigerbeetle/tigerbeetle
- https://github.com/kedder/ofxstatement
- https://github.com/kedder/ofxstatement-iso20022
- https://github.com/beancount/beangulp
- https://github.com/rotki/rotki
- https://github.com/ghostfolio/ghostfolio
- https://github.com/lukasbloom/flowfolio
- https://docs.tigerbeetle.com/reference/account/
- https://docs.tigerbeetle.com/reference/transfer/
- https://docs.tigerbeetle.com/coding/two-phase-transfers/

## Governance state

- D-001: Accepted, unchanged — crypto perpetual futures only.
- D-017: Proposed, unchanged.
- Phase 01: Closed.
- Phase 02: Active — architecture/contracts only.
- Phases 03–19: LOCKED.
- No application or dependency installed.
- No tests or fixtures executed.
- No real bank data, account, token or credential accessed.
- No provider, external product, hosting or runtime adopted.
- No live trading, paper execution or financial transaction authorised.


## Fetch-back verification addendum

Fetched all five changed paths from the GitHub main branch after the commits. Verified:
- research sections 18 and 19 are present;
- F-004 research update is present and D-017 remains Proposed;
- ROADMAP Phase 02 checkpoint is present and Phases 03–19 remain LOCKED;
- conversation index includes checkpoint 047;
- this conversation record is present with the governance state and source list.

Fetched blob SHAs:
- PERSONAL_FINANCE_RESEARCH.md: 54726a549f74f6eb58230e09837b4de48b43bb0c
- FUTURE_SCOPE_IDEAS.md: bb66d850dbc47be150d299ab6b43ae53abd8b589
- ROADMAP.md: 14ec2ed427235b9f26d9717cadf7a722aa48173e
- conversation README: 1d5889206dc046a7e3dfedcfe6867b4aef16138d
- checkpoint 047: 6fbc8594865192abc20390151e58fcae70bc7523

No code, dependencies, tests, runtime, credentials, bank connections or financial records were changed or used.
