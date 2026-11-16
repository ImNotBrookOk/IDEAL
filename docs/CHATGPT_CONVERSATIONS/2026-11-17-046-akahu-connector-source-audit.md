# 2026-11-17-046-akahu-connector-source-audit

## Scope

Continue the IDEAL private personal-finance research by comparing pinned stable-release source for MoneyMatter v0.33.7 and Firefly III Data Importer v2.3.5. Focus: Akahu transaction ingestion, idempotency, updates/deletions, pending rows, transfer matching, FX precision, balances, credentials, tests and future IDEAL requirements.

## User-visible conversation transcript

**User:** Lets do it and investigate

**Assistant:** We’ll continue with a **source-level comparison of Firefly III v6.7.9 / Data Importer v2.3.5 and MoneyMatter v0.33.7**.

The investigation will use pinned stable-release source, tests, documentation and synthetic/mock transaction fixtures only. The key question is whether either system provides a sufficiently reliable, auditable foundation for IDEAL’s future personal-finance ledger—or whether IDEAL should own that domain from the outset.

No real bank connections, credentials, financial records, runtime installation, dependency changes or phase advancement.

**Assistant (interim finding):** The most important issue is now clear: stable transaction IDs prevent repeated imports, but they do not automatically keep an imported ledger synchronised with later bank corrections or deletions.

- MoneyMatter checks Akahu `_id` against local `originalId` and skips an existing row. It does not update changed fields or reconcile source deletions in the inspected persistence path.
- Firefly stores Akahu's ID as `external_id`; its documented content-hash duplicate mode does not update edited transactions.

This interim statement was subsequently refined after inspecting Firefly's exact configuration and submitter: the pinned non-file flow defaults to the identifier-based `cell` path, and Akahu's external ID is the default identifier field. The corrected detailed finding is recorded below and in section 17 of the research document.

## Operational log

1. Resumed from the prior IDEAL checkpoint. Scope remained Phase 02 architecture/contracts and personal-finance research only.
2. Read the installed Acumen research skill and queried current-change intelligence. The returned brief was off-topic for Firefly/MoneyMatter/Akahu; no project conclusion was drawn from it.
3. Located the IDEAL repository `ImNotBrookOk/IDEAL` and read the current research, future-scope, roadmap and conversation-index documents before writing.
4. Used GitHub source search to locate Akahu integration files and then fetched the pinned release paths, not default-branch source:
   - Firefly III Data Importer v2.3.5.
   - MoneyMatter v0.33.7.
5. Inspected Firefly Akahu conversion, fetcher, request pagination, date range, response builder/model, account model, account creation, API submitter, duplicate-detection configuration, SecretManager, Akahu feature test and configuration.
6. Inspected MoneyMatter Akahu provider, API client, type definitions, credential-encryption helper and mocked Akahu E2E suite.
7. Rechecked official Akahu docs for settled transaction update/delete semantics, pending rows, stable IDs, foreign conversion metadata, timestamps, pagination and endpoint behaviour.
8. No software was installed or run. No test suite or synthetic fixture was executed. The inspected MoneyMatter E2E source contains mocked tests; source inspection is not represented as an executed test.
9. No IDEAL application code, dependency, configuration, workflow, credential, account or runtime was changed. Documentation only.

## Corrected findings

### MoneyMatter v0.33.7

- First sync fetches the available settled feed; later syncs start 14 days before the newest imported row to catch late-settling transactions.
- API client paginates through all cursors and carries the same start/end bounds across pages.
- Deduplication checks account + Akahu `_id` against `originalId`; a secondary source-metadata lookup restores IDs after unlink/relink.
- Existing IDs are skipped, not updated. Source deletions are not reconciled in the inspected path. A 14-day overlap is not a full historical update scan.
- Only settled transactions are fetched; no pending endpoint appears in the pinned provider/client.
- Signed decimal amount is converted into account currency cents; direction is income/expense. Currency is taken from account balance.
- Akahu merchant/category/particulars/reference/card suffix/balance-after/type metadata is retained, but explicit `meta.conversion` foreign amount/currency/rate is not mapped.
- Transactions are explicitly created with `transferNature: not_transfer`; automatic transfer pairing is not implemented in this provider path.
- Current account balance is written to balance history when supplied; stale refresh is asynchronous and only improves a later fetch.
- Mocked E2E coverage is materially broader than Firefly's Akahu integration suite: credentials, account filtering, signed amount, cents, re-sync idempotency, late settlements, pagination, overlap, outages, auth failures, refresh, period load, pre-link history and unlink/relink.
- Stored Akahu credentials are encrypted through the provider's credential-encryption helper. Key management, rotation and encrypted backup/restore still require a deployment-specific audit.

### Firefly III Data Importer v2.3.5

- Akahu request follows all cursor pages and preserves date bounds. The date-range adapter accounts for Akahu's exclusive start/inclusive end.
- Akahu `_id` is mapped to Firefly `external_id`. The non-file flow defaults to `cell`/identifier duplicate detection; an empty identifier field defaults to `external_id`. Thus the correct finding is identifier-based idempotency by default, not merely hash-only duplicate checking.
- A repeated identifier is skipped, including an identifier found on a deleted Firefly transaction. An existing ID with changed source content is therefore not updated. An upstream replacement with a new ID can be inserted without automatically reversing the old record.
- Positive/negative signed amounts become deposit/withdrawal. Optional other-account details become names, but automatic resolution and pairing of the two sides of internal transfers is not demonstrated by the inspected converter.
- Foreign conversion is represented, but hard-coded to two decimal places; account amount is also formatted to two decimals, with FIXME comments about obtaining account precision. This requires tests for zero- and three-decimal currencies.
- Inspected importer path does not continuously sync the Akahu current account balance and does not fetch pending transactions.
- Akahu-specific feature test `HttpFlowTest` has a TODO to mock Akahu API responses. Model/unit tests exist, but the inspected test does not demonstrate a full mocked Akahu import/submit lifecycle.
- Akahu credentials are read from server-side session or environment-backed config in the inspected SecretManager; no application-level encrypted credential store is visible in this code path.

### Akahu provider contract

Official docs explicitly require consumers to handle additions, modifications and deletions. Pending transactions are separate, unstable and lack stable IDs; rebuild the pending snapshot each fetch. Stable settled IDs may be replaced when a bank mutation cannot be confidently matched. Neither pinned connector implements the complete provider lifecycle.

## Comparative disposition

- MoneyMatter: stronger Akahu connector implementation and product/UX reference; not a ledger correctness authority.
- Firefly: stronger external double-entry/multi-currency accounting reference; its Akahu importer needs more integration evidence and precision testing.
- Neither connector meets IDEAL's required source reconciliation contract.
- Eventual IDEAL design should preserve immutable source observations, versioned normalisation, idempotency keys, update/supersession links, deletion tombstones/reversals, separate pending snapshots, transfer-match confidence/review, exact source decimal/FX values and auditable reconciliation.

## Synthetic fixture requirements for a separately approved POC

The acceptance matrix is recorded in `docs/PERSONAL_FINANCE_RESEARCH.md` section 17.5: identical replay, same-ID correction, source deletion, replacement ID, pending-to-settled lifecycle, cross-account transfer matching, foreign-currency precision, pagination, API outage/auth/throttle/partial failure, stale/revised balance, interrupted import replay and backup/restore.

No fixtures were executed in this conversation.

## Repository documentation updates

Pending commit and fetch-back verification in this record:
- `docs/PERSONAL_FINANCE_RESEARCH.md` — section 17 added.
- `docs/FUTURE_SCOPE_IDEAS.md` — F-004 audit disposition update added.
- `ROADMAP.md` — Phase 02 checkpoint added.
- `docs/CHATGPT_CONVERSATIONS/README.md` — this record indexed.

## Decisions and approval boundary

- D-017 remains Proposed.
- D-001 remains accepted and unchanged.
- Phase 02 architecture/contracts only.
- Phases 03–19 remain LOCKED.
- No external app selected, no code/dependency adopted, no runtime installed, no account connected, no credentials used, no real bank data processed, no host or paid service selected.
- No implementation, bank connection, provider selection or phase advancement is authorised.

## Current state and next step

Pinned source audit is complete at research level. The next useful research task is to inspect transfer semantics and backup/restore/credential-key lifecycle in both pinned projects, then produce a tighter architecture contract for source-observation reconciliation. Any executable POC remains separately gated and synthetic-only.

Owner approval pending for any implementation, installation, account connection, provider adoption or phase advancement.


## Dated addendum — backup, restore and credential-key review (17 November 2026)

Further pinned-source inspection was completed after the initial record:

- MoneyMatter v0.33.7 credential encryption uses AES-256-GCM; the key is SHA-256-derived from `APPLICATION_JWT_SECRET`. Preserve this secret securely. A key change without re-encryption would make existing stored tokens undecryptable; no rotation workflow was found in the inspected source.
- MoneyMatter backup export tests prove bank credentials and AI keys are stripped from archives. Bank connection rows remain but with null credentials.
- MoneyMatter restore tests prove bank connections return disabled with a `RESTORED` reason and require fresh credentials before reactivation.
- Restore test source covers same-user consistency, cross-user remapping, transaction/transfer/holding round-trip, import-batch undo, foreign-reference handling, checksum validation and rollback cases. These tests were inspected, not executed.
- Attachments are excluded from the backup archive and need a separate backup path.
- Firefly's AkahuNoteBuilder writes other-account details into notes; it does not establish a resolved two-sided transfer. The Akahu importer SecretManager still uses session or environment-backed credentials without visible application-level encryption in that path.
- MoneyMatter's product-wide transfer support does not change the Akahu provider's explicit `transferNature: not_transfer` import behaviour.

Research document section 17.7 contains the detailed evidence. This addendum does not change any approval boundary: D-017 remains Proposed; Phase 02 only; no app installation, credential use, bank connection, runtime, provider selection or implementation.
