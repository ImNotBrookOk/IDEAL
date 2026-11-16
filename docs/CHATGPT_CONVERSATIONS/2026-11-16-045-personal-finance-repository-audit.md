# 2026-11-16-045 — Personal finance repository audit

## Status and scope
Phase 02 architecture research only. This checkpoint continues D-017/F-004 private single-user personal-finance research. D-017 remains Proposed, D-001 is unchanged, and Phases 03–19 remain LOCKED. No software was installed or executed; no code, dependencies, bank accounts, credentials, API tokens, payments, hosting or provider accounts were created.

## User continuation
User replied "Yes" to proceeding with the focused repository audit and alternatives comparison. This authorised research and documentation, not implementation or bank connection.

## Work performed

### Pinned source/repository audit
Inspected official repository README/license/package files, selected source files, release notes, security docs and CI/test configuration for:
- MoneyMatter: stable tag v0.33.7, Akahu provider implementation and E2E tests, credential encryption utility, backup/restore code, CI workflow and current security/privacy documentation.
- Actual Budget: v26.11.0 release notes, bank-sync documentation, security policy, architecture decision record and multi-currency documentation.
- Firefly III: v6.7.9 and Data Importer v2.3.5 release evidence, core README/composer metadata, importer README/config/source, Akahu provider declaration and tests, duplicate-detection docs and security documentation.
- Money Manager Ex: v1.9.4 release, repository README, encryption/mobile documentation and current feature set.
- GnuCash: v5.17 release, multi-currency, stock portfolio and OFX/QIF import documentation.
- Beancount v3: current stable major line, GPL-2.0-only licence and text-ledger model.
- hledger 1.52.4: stable release, GPL-3.0, multi-currency, CSV rules, CLI/TUI/WUI.

### Important findings

#### MoneyMatter
- v0.33.7 is the stable release inspected (30 Oct 2026); NZ Akahu sync introduced in v0.33.6 (29 Oct 2026). Development-branch work beyond the stable tag must not be represented as released.
- Feature breadth is strongest: budgets, transactions, bills, subscriptions, loans, investment holdings, multi-currency, net worth, imports/exports and backup/restore.
- Akahu source uses personal app tokens and read-only endpoints. The sync code uses a 14-day incremental overlap, provider transaction IDs, idempotent persistence and E2E tests with mocked API responses. Inspected settled-transaction sync does not import the unstable pending endpoint.
- Bank provider credentials are encrypted at rest with AES-GCM. Transaction and balance records are not end-to-end encrypted and remain readable by the server operator.
- Project security docs state no native 2FA and no published third-party security audit/certification. Passkeys and external identity providers are supported; password login may remain as another route if configured.
- Cloud Plus/free-trial AI categorisation automatically sends selected new transaction fields to the included AI provider; there is no single global off switch. Self-hosted AI remains off until a model is configured. Self-hosted mode is the only candidate for a synthetic-data trial; do not use cloud with real financial data.
- CI includes lint, unit tests, E2E tests, type checks, frontend build, Docker build/smoke tests.
- AGPL-3.0-only. Earlier pre-relicensing versions were CC BY-NC-SA 4.0; exact historical boundary must be checked before any reuse.
- Disposition: strongest all-in-one feature reference, synthetic-data candidate only; not IDEAL core, no dependency or real data approved.

#### Actual Budget
- MIT, local-first, strong envelope budgeting UX, mobile support, rules and reports.
- Akahu support introduced experimentally in v26.7.0; v26.11.0 adds scheduled automatic sync while Actual is open.
- Official docs explicitly state native multi-currency is not supported.
- Budget data can be E2E encrypted, but bank-sync credentials are stored in plaintext on the sync server and are not protected by budget E2EE. Local device data remains dependent on disk security.
- Security policy says deployment is for one owner or trusted household, not a shared security boundary for untrusted users.
- Disposition: UX/rules reference only; not suitable as IDEAL ledger while native multi-currency is absent.

#### Firefly III and Data Importer
- Firefly III v6.7.9; Data Importer v2.3.5 stable. Newer Nov 2026 development builds are explicitly pre-release and warn of possible duplicate imports.
- AGPL-3.0-or-later.
- Strong double-entry ledger, multi-currency, 2FA, REST API, budgets, recurring transactions, rules and savings goals.
- Data Importer is separate and supports CSV/CAMT files and third-party bank providers.
- Important: the v2.3.5 stable source tag contains an enabled Akahu provider and Akahu unit tests, but current user-facing configuration docs omit Akahu. Treat as code-level support that needs a pinned-version end-to-end test, not turnkey documented NZ integration.
- NZ-specific transfer matching concerns are recorded in contribution history: no IBAN convention, transaction type initially unused for transfer inference, and currency precision work needed.
- Official Firefly security docs say database data and attachments are not encrypted at rest. Full-disk encryption, strict permissions, encrypted backups and database network isolation are mandatory if evaluated.
- No native investment holdings engine.
- Disposition: leading candidate for an isolated synthetic-data ledger comparison; no adoption.

#### Money Manager Ex
- GPL-2.0; v1.9.4 desktop stable release 31 Aug 2026; Android app 5.5.12 listed in Sep 2026.
- Local SQLite with AES encryption; Android supports SQLCipher. Budgets, scheduled bills, cash flow, stock investment accounts, assets and multiple currencies.
- No native NZ Akahu connector or IDEAL API identified; manual CSV/QIF import and local/mobile sync.
- Disposition: private/manual offline alternative and mobile UX reference only.

#### GnuCash, Beancount, hledger
- GnuCash 5.17: double-entry, multi-currency, stock/mutual-fund portfolios, QIF/OFX import and transaction matching; desktop-first, XML default; SQL backend described as experimental with data-loss corner cases.
- Beancount v3: GPL-2.0-only text-based double-entry accounting and investment ledger; Fava offers web UI; technical/manual import, not a consumer bank-sync app.
- hledger 1.52.4: GPL-3.0, text journal, multi-currency, CSV import rules, CLI/TUI/WUI; not a polished consumer investment/bank-aggregation platform.
- Disposition: accounting model and ledger invariants references only.

### Akahu constraints checked against official documentation
- Personal App: free, one user's own Akahu account, read-only account information, no payments/webhooks, daily scheduled refresh, one-hour manual refresh rest period.
- Personal Apps may access up to 730 days of transactions, subject to shorter financial-institution history limits.
- Settled and pending transactions are separate endpoints. Pending data is unstable and lacks stable IDs; rebuild pending snapshots on each fetch rather than append them as settled records.
- Settled IDs are normally stable, but a small percentage may be deleted/replaced if the bank mutates a transaction beyond recognition; consumers must support updates and deletions.
- UTC timestamps, pagination and visible data-freshness timestamps are required. This is not real-time data.

## Architecture conclusion
No single candidate meets IDEAL's complete all-in-one requirements without trade-offs:
- MoneyMatter has broadest product coverage but meaningful security/licence concerns.
- Firefly III has strongest external accounting/API/multi-currency foundations but no native investment holdings, no at-rest encryption and a separate importer.
- Actual Budget has strong envelope UX but lacks native multi-currency.
- MMEX offers local encrypted mobile/manual finance but no bank sync/API.
- GnuCash/Beancount/hledger provide accounting reference patterns, not an integrated phone-first system.

Recommended direction (not a formal accepted ADR): keep Personal Finance as a distinct IDEAL domain with its own ledger; manual/file import first; read-only bank sync only after separate approval; separate investment/trading ledgers; consolidated net worth/exposure as read-only projection; no implicit cash/margin/collateral pooling. Firefly III is the leading external ledger candidate for an isolated synthetic-data evaluation; MoneyMatter is the broadest product/UX reference. A clean IDEAL-owned domain remains possible if adapter complexity/data ownership outweighs reuse.

## Repository documentation changes
1. docs/PERSONAL_FINANCE_RESEARCH.md — appended sections 11–16 with detailed comparative audit, shortlist, Akahu limits, practical viability, audit/provenance requirements and research outcome.
   - Commit: 75e21ebe5d42f6b30c0825a69c77a59800a5647b
   - Blob SHA: 340917cb0cbd4d2663f2fe7168aa61cb9881c834
2. docs/FUTURE_SCOPE_IDEAS.md — appended comparative audit summary and revised recommendation under F-004.
   - Commit: 61edb473b4bec5fda93646467b59ba21df0fa81b
   - Blob SHA: 39c67b85a732db02b9307f5727eaaf25064718ab
3. ROADMAP.md — appended Phase 02 audit checkpoint and retained all approval gates.
   - Commit: 1f43aafcb2c1f3b51db47a6769a2d2e93dcc3cf9
   - Blob SHA: 1490bc846d896b112b476c720b5ce9242e357514
4. DECISIONS.md unchanged; D-017 remains Proposed, D-001 unchanged.
5. Conversation index update pending at time this record was created.

## Source links
- MoneyMatter repository: https://github.com/letehaha/moneymatter
- MoneyMatter v0.33.7: https://github.com/letehaha/moneymatter/releases/tag/v0.33.7
- MoneyMatter security/privacy: https://github.com/letehaha/moneymatter/blob/main/packages/landing/src/pages/features/security-and-privacy.astro
- Actual Budget: https://github.com/actualbudget/actual
- Actual bank sync docs: https://github.com/actualbudget/actual/blob/master/packages/docs/docs/advanced/bank-sync.md
- Actual multi-currency docs: https://actualbudget.org/docs/budgeting/multi-currency/
- Firefly III: https://github.com/firefly-iii/firefly-iii
- Firefly Data Importer: https://github.com/firefly-iii/data-importer
- Firefly security docs: https://docs.firefly-iii.org/explanation/more-information/security/
- Firefly duplicate detection: https://docs.firefly-iii.org/references/data-importer/duplicate-detection/
- MMEX: https://github.com/moneymanagerex/moneymanagerex
- GnuCash: https://github.com/Gnucash/gnucash
- Beancount: https://github.com/beancount/beancount
- hledger: https://github.com/hledgerorg/hledger
- Akahu Personal Apps: https://developers.akahu.nz/docs/personal-apps
- Akahu transaction history: https://developers.akahu.nz/docs/accessing-transactional-data
- Akahu transaction model: https://developers.akahu.nz/docs/the-transaction-model
- Akahu refreshes: https://developers.akahu.nz/docs/data-refreshes
- Akahu pending transactions: https://developers.akahu.nz/reference/get_transactions-pending

## Verification and next step
Fetch back all modified files and verify exact blob SHAs, section presence, D-017 Proposed, D-001 unchanged and Phase 02 / Phases 03–19 gates. No executable code changed, so no tests were run. Next research step: inspect Firefly v2.3.5 Akahu integration against a synthetic/mock account and compare it with MoneyMatter's pinned Akahu provider and backup/restore model. Do not connect a real bank account or create tokens.
