# 2026-11-16-045 — Personal finance open-source comparison

## Status
Follow-on research after owner approved continuing the personal-finance research direction. D-017 remains Proposed; F-004 remains a proposed private-use domain. Phase 02 architecture/contracts only; Phases 03–19 locked. No software installed, no bank account connected, no credentials or real statements used, no dependencies or runtime code changed.

## Conversation
### User
> Yes

This confirmed continuation of the proposed research sequence (MoneyMatter audit, alternatives, Akahu path and data model), not approval to install software or connect financial accounts.

## Research findings

### Actual Budget — leading isolated-trial candidate
- Repository: https://github.com/actualbudget/actual
- MIT licence.
- GitHub snapshot: about 30.2k stars / 3.3k forks; release v26.11.0 dated 2 Nov 2026. Activity/stars are not quality/security proof.
- Local-first personal finance system. Statement import documentation lists CSV, QIF, OFX, QFX and CAMT.
- Server is required for browser/mobile access, multi-device sync and bank sync; file import and core budgeting can work without the server.
- Official bank-sync docs list Akahu for NZ banks.
- Important secret boundary: bank-sync API keys/secrets are stored server-side and are not covered by the budget's end-to-end encryption. Self-hosting and protecting the host/database are important.
- Documentation surfaced in different revisions regarding automatic versus manual sync; exact behaviour must be checked against a pinned release and tested.
- Disposition: best candidate for a later isolated synthetic-data-only budgeting trial, after architecture/security gates. Not adopted.

### MoneyMatter — broadest feature/reference candidate
- Repository: https://github.com/letehaha/moneymatter
- AGPL-3.0; README says versions before relicensing commit were CC BY-NC-SA 4.0. Exact commit boundary requires audit.
- Snapshot: 227 stars / 90 forks.
- v0.33.7 released 30 Oct 2026; v0.33.6 (29 Oct) added NZ Akahu bank sync.
- Broad feature set: accounts, budgets, transactions, investments, debts, net worth, multi-currency, imports and self-hosting.
- Stack: Vue 3/Vite/TypeScript/Tailwind; Node/Express; Sequelize; PostgreSQL; Redis/BullMQ; better-auth; Docker.
- Disposition: study and audit at a pinned commit; not selected as foundation due to AGPL relicensing history, more complex stack and unverified data/security implementation.

### Firefly III — serious alternative
- Repository: https://github.com/firefly-iii/firefly-iii
- AGPL-3.0.
- GitHub snapshot: approximately 25k stars; v6.7.8 released 10 Oct 2026; signed releases; development prerelease dated 11 Nov 2026.
- Personal finance manager with strong transaction and budgeting workflow potential.
- No native NZ Akahu integration established by this first-pass screen.
- Disposition: retain as alternative; audit importer ecosystem, auth/security, data model and backup/restore if Actual is unsuitable.

### Beancount — accounting reference
- Repository: https://github.com/beancount/beancount
- GPL-2.0-only.
- Snapshot: approximately 5.9k–6.1k stars, 461–487 forks; repo shows 6,419 commits and 205 issues at capture.
- Current stable is v3; v2 is frozen/obsolete; v1 halted in 2013.
- Text-based double-entry accounting with multi-commodity model and reports.
- Disposition: valuable reference for canonical ledger semantics and auditability, not a turnkey budgeting UI. GPL-2.0-only obligations require review before embedding/distribution.

### hledger — accounting/import reference
- Repository: https://github.com/hledgerorg/hledger
- GPL-3.0.
- Snapshot: approximately 4.8k stars / 418 forks.
- CLI, TUI and web interface; plain-text accounting; CSV rules and import tooling.
- Disposition: useful for ledger/import semantics, not a turnkey bank-connected budgeting app. GPL-3.0 obligations require review before reuse.

## Akahu documentation verification and correction
Official Personal Apps documentation:
- Free Personal App, limited to one user and that user's own Akahu account.
- Ongoing account connectivity and account information only.
- No payments or webhooks.
- Daily scheduled refresh.
- Manual refresh rest period: one hour.
- Creation requires Akahu profile, connected account, acceptance of developer terms, identity verification and MFA.
- Source: https://developers.akahu.nz/docs/personal-apps

Akahu generic data-refresh documentation describes a default 24-hour scheduled freshness target and 15-minute manual rest period for general apps; the Personal App-specific table states one hour, so use the Personal App-specific limit for this use case.
Source: https://developers.akahu.nz/docs/data-refreshes

Akahu full-app accreditation documentation describes privacy notice, consumer information page, recent security/penetration test and app review. First review is free; subsequent reviews listed at NZ$1,000. This is not the same as the restricted personal-app pathway.
Source: https://developers.akahu.nz/docs/app-accreditation

No claim is made that IDEAL is accredited. The Personal App route remains a candidate subject to terms and provider confirmation.

## Comparative disposition
1. Actual Budget: leading candidate for isolated synthetic-data budgeting trial.
2. MoneyMatter: broader all-in-one reference; audit licence and code before any trial/reuse.
3. Firefly III: fallback alternative.
4. Beancount/hledger: accounting and import design references.
5. No adoption or runtime integration yet.

## Repository updates
1. docs/PERSONAL_FINANCE_RESEARCH.md — comparative project screen, Akahu source verification, security/secret boundaries, trial disposition.
   - Commit: efdda5607f9519342a987a654744bf66bcf955bb
2. docs/FUTURE_SCOPE_IDEAS.md — F-004 comparative research update.
   - Commit: 5fcbd9c5a142f8c322067d74821409de3aff9841
3. ROADMAP.md — Phase 02 research checkpoint, scope gates preserved.
   - Commit: 87024053719601439bc48743ebb293740f33b862
4. Conversation index update pending when this record is created.

## Next research tasks
- Pin Actual Budget v26.11.0 and audit exact code/data model, import pipeline, backup/restore, bank-sync secret storage, API/auth, tests/CI, dependency vulnerabilities and Akahu integration implementation.
- Pin MoneyMatter v0.33.7 and inspect exact licence history, data schema, transaction dedupe/idempotency, bank token handling, tests/CI, Docker provenance, backup/restore and dependencies.
- Compare both against a minimal IDEAL-owned canonical double-entry model. Prefer replaceable adapters over coupling IDEAL's ledger truth to an external app.
- No installation, real data, account connection, credentials, payment actions, public service or hosting until separately approved.
