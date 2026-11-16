# IDEAL — Personal Finance and Banking Research

**Status:** Proposed private single-user domain; Phase 02 architecture research only  
**Recorded:** 16 November 2026  
**Owner intent:** Personal use first. Public/multi-user release is only a distant possibility and is not an active requirement.

## 1. Objective

Evaluate the safest, lowest-cost, auditable path to a personal financial management system integrated with IDEAL. Desired capabilities include bank-account visibility, manual and statement-based records, transaction categorisation, budgets, bills, subscriptions, debt, savings goals, cash-flow forecasting, net worth and consolidated investment visibility.

This is not approval to build, connect accounts, store credentials, move money, place investments or trade.

## 2. Initial feasibility

| Capability | Assessment | Evidence still required |
|---|---|---|
| Manual accounts, assets, liabilities and transactions | High feasibility | Canonical data model, corrections/reversals, reconciliation |
| CSV/OFX/QFX imports | High feasibility | Real bank statement samples, duplicate detection, transfer matching |
| Budgets, bills, subscriptions, debt and savings goals | High feasibility | Calendar/period semantics, recurrence, forecast assumptions |
| Net worth and investment aggregation | High feasibility | Native currency ledger, price/FX provenance, stale data handling |
| Own-bank read-only aggregation via Akahu Personal App | Plausible; highest-priority integration candidate | Verify supported banks/fields, exact token handling, current terms, sync cadence and MoneyMatter integration semantics |
| Payment initiation / automatic transfers | Defer | Separate provider accreditation/tier, consent, strong confirmation, fraud and legal controls |
| Public multi-user service | Not in scope | Separate CDR/privacy/licensing/security/business review |
| Always-on web deployment | Possible later, not yet justified | Hosting, threat model, identity/MFA, TLS, backups, monitoring, patching, incident response and recurring cost |

## 3. New Zealand bank access — Akahu

Akahu's current Personal Apps page distinguishes:
- **Personal App:** free; one user only (restricted to the owner's own Akahu account); ongoing connectivity; account information allowed; payments and webhooks unavailable; daily scheduled refresh; manual refresh rest period of one hour. Creating one requires an Akahu profile, connecting an account, accepting developer terms, identity verification and MFA.
- **Full App:** usage-based pricing and customisable refresh; payments and webhooks available. Akahu's accreditation guide says public/production integrations require application review, including a privacy notice, consumer information page, recent security/penetration testing and review of security, authentication and consumer controls. The first review is free; subsequent reviews are listed at NZ$1,000 each.
- Akahu's general refresh documentation says default full-app data freshness is at most 24 hours and its general manual-refresh rest period is 15 minutes, but the Personal App table explicitly sets a one-hour limit. Apply the Personal App-specific rule to that route.
- **Official CDR:** an accredited intermediary can access customer-authorised banking data under New Zealand's Consumer Data Right. IDEAL is not accredited and must not represent itself as such.

The Personal App route is promising for a private single-user experiment, but it is a provider-specific developer product, not a general permission to operate a bank-data service. Confirm that the intended personal/self-hosted use is permitted before connecting. A personal token is a secret: do not paste it into chat, commit it, place it in plain-text config or log it.

References:
- Akahu Personal Apps: https://developers.akahu.nz/docs/personal-apps
- Akahu refresh behaviour: https://developers.akahu.nz/docs/data-refreshes
- Akahu app accreditation: https://developers.akahu.nz/docs/app-accreditation
- Akahu app accreditation/tier classification: https://developers.akahu.nz/docs/app-accreditation
- Akahu official open-banking transition: https://developers.akahu.nz/docs/official-open-banking
- Akahu pricing: https://www.akahu.nz/pricing
- MBIE accredited requestors: https://www.mbie.govt.nz/business-and-employment/business/consumer-data-right/participating-as-a-data-holder-or-accredited-requestor/accredited-requestors
- MBIE regulated open banking standards: https://www.mbie.govt.nz/business-and-employment/business/consumer-data-right/standards-for-the-consumer-data-right

## 4. MoneyMatter — preliminary assessment

Repository: https://github.com/letehaha/moneymatter

Observed repository facts (16 November 2026):
- README advertises accounts, budgets, transactions, imports, loans, investments, net worth, multi-currency reporting, AI categorisation/statement parsing, self-hosting and export/backup.
- Stack: Vue 3, Vite, TypeScript, Tailwind; Node.js/Express; Sequelize; PostgreSQL; Redis/BullMQ; better-auth; Docker.
- Licence: AGPL-3.0. README states earlier versions before the relicensing commit were CC BY-NC-SA 4.0; exact commit/version boundary must be checked before reuse.
- GitHub search snapshot: 227 stars and 90 forks. These are discovery metrics, not a quality or security verdict.
- Release v0.33.6 (29 October 2026) added New Zealand bank sync via Akahu. Release notes instruct a user to create an Akahu Personal App and enter App Token and User Token.
- Release v0.33.7 (30 October 2026) is the next listed release.

Initial disposition: strong reference implementation and possible isolated self-hosted evaluation candidate; not adopted, not a dependency, and no source copied. Before any trial or reuse, audit exact commit, licence history, Docker images/provenance, dependency lock and vulnerability state, authentication/session model, secret storage, database schema, transaction idempotency, import/export/backup restore, migration safety, tests/CI, open issues and data deletion. AGPL-3.0 network-use obligations matter if modified code is exposed as a service.

References:
- Repository/README: https://github.com/letehaha/moneymatter
- Releases: https://github.com/letehaha/moneymatter/releases
- Issues: https://github.com/letehaha/moneymatter/issues
- Self-hosting guide: https://github.com/letehaha/moneymatter/tree/dev/self-hosting

## 5. Proposed architecture boundaries

Personal Finance should be its own domain. It must not become a shared mutable ledger with trading engines.

- Personal Finance owns bank accounts, cash, liabilities, budgets, bills, categories, transactions and savings goals.
- Each investment/trading engine owns its authoritative positions, fills, fees, funding, cash and realised/unrealised PnL.
- A consolidated read-only projection calculates net worth, exposure and cash-flow context with timestamps, native currency and valuation provenance.
- No implicit cash, margin or collateral pooling.
- Transfers between accounts/engines are explicit, matched, reconciled and auditable.
- AI can suggest categories or explain a budget variance, but cannot silently mutate source records, approve transfers or authorise trades.
- Every source import/sync, classification, correction, FX conversion, price mark, forecast and user-approved action receives a timestamp, source/version, actor and immutable audit reference.
- Corrections are represented by reversals or superseding entries; never silently overwrite financial history.

## 6. Privacy, security and audit requirements

Before any real data is connected:
1. Threat-model the local/private deployment and all data flows.
2. Keep secrets outside GitHub, chat transcripts, logs and ordinary exported backups.
3. Encrypt data at rest and backups; restrict file/database permissions.
4. Use MFA where supported; bind local access to loopback/LAN unless a hardened remote design is approved.
5. Define data minimisation, retention, export, deletion and backup lifecycle.
6. Make bank sync read-only; no payment scopes.
7. Validate source records and duplicate/idempotency behaviour; surface missing, stale and conflicting data.
8. Test backup restore, not merely backup creation.
9. Preserve append-only decision/action evidence without retaining unnecessary raw personal data.
10. Do not send identifiable bank transactions to external AI providers by default. Any AI use must be opt-in, minimised and documented.

## 7. Hosting direction

The user's preferred operating model is phone-first and low-cost, with an existing Windows PC as fallback only. A phone is a control surface, not a dependable always-on database/server. A future web app can be hosted privately, but a free always-on host is not assumed to exist. First prove a local/private workflow and reliable backups. Public internet exposure is a separate threat-model and cost decision.

MoneyMatter's self-host guide states a 2 GB RAM minimum and uses Docker, PostgreSQL and Redis. That is a useful comparison point, not an IDEAL hosting decision. No server, domain, paid plan or cloud resource is selected or provisioned.

## 8. Research sequence

1. Complete a focused MoneyMatter code/licence/security/data-model audit at a pinned commit.
2. Compare at least two alternatives (e.g. Actual Budget, Firefly III, maybebeancount/Beancount or hledger) for single-user budgeting, ledger integrity, import/export, mobile UX, licence and maintenance.
3. Verify Akahu Personal App coverage and current terms for the owner's own bank accounts; no credentials or accounts are created during research.
4. Define canonical transaction/account/ledger/FX/provenance contracts in Phase 02.
5. Compare build-versus-adopt using total cost, data ownership, auditability, security, maintainability and phone-first usability.
6. Only after the architecture and security review, seek explicit approval for a local isolated prototype. No account connection until separate approval.

## 9. Scope and approval boundary

- D-001 remains unchanged: crypto perpetual futures are the active initial trading scope.
- D-017 is Proposed, not Accepted.
- This document is research/architecture input only. No code, dependency, provider, bank account, token, payment capability, host or public product is approved.
- Phase 02 remains architecture/contracts only. Phases 03–19 remain LOCKED.
- Future public/multi-user use would require a new owner-approved scope review and independent NZ legal/privacy/security analysis.

## 10. Source notes and uncertainty

Web evidence checked 16 November 2026. Provider terms, bank coverage, API fields, fees, supported institutions and accreditation requirements can change. Confirm directly with Akahu/MBIE before relying on them. This document is technical issue-spotting, not legal, tax or financial advice.


## 11. Comparative project screen — 16 November 2026

This is a first-pass repository and documentation screen, not a full source-code/security audit. Stars/forks are discovery signals only. Pin exact commits before any isolated trial.

| Project | Licence / activity evidence | Strongest fit | Main limitation / disposition |
|---|---|---|---|
| [Actual Budget](https://github.com/actualbudget/actual) | MIT; GitHub snapshot about 30.2k stars / 3.3k forks; release v26.11.0 dated 2 Nov 2026; high visible activity | Local-first envelope budgeting, reports, schedules, CSV/QIF/OFX/QFX/CAMT imports, mobile/browser access with server, API, Akahu provider | **Best initial candidate for an isolated budgeting trial.** Not a complete investment/trading platform. Bank-sync credentials are stored server-side and are not protected by budget end-to-end encryption; self-hosting is therefore important. Documentation versions differ on whether syncing is automatic or manual; verify pinned release behaviour. |
| [MoneyMatter](https://github.com/letehaha/moneymatter) | AGPL-3.0; snapshot 227 stars / 90 forks; v0.33.7 released 30 Oct 2026; NZ Akahu support added in v0.33.6 | Broad all-in-one feature set: budgets, accounts, investments, net worth, debts, multi-currency, imports and Akahu | **Best breadth/reference candidate, not first default foundation.** More complex Docker/Postgres/Redis stack; AGPL and relicensing boundary need exact audit; bank token storage, data model, accounting correctness, security and restore process not yet verified. |
| [Firefly III](https://github.com/firefly-iii/firefly-iii) | AGPL-3.0; 25k+ stars; v6.7.8 released 10 Oct 2026; signed releases; active development snapshot | Detailed personal-finance transaction management, budgets, recurring transactions, rules, reports and API/importer ecosystem | Strong alternative for tracking/accounting; no evidence yet of native NZ Akahu integration; AGPL; verify security fixes, importer compatibility and backup/restore. |
| [Beancount](https://github.com/beancount/beancount) | GPL-2.0-only; 5.9k–6.1k stars; v3 current stable, v2 maintenance/frozen | Explicit double-entry ledger, native multi-currency accounting, reproducibility and text-based auditability | **Accounting reference, not end-user budgeting app.** Requires technical workflow and separate UI/importers; GPL obligations if embedding/distributing. |
| [hledger](https://github.com/hledgerorg/hledger) | GPL-3.0; about 4.8k stars / 418 forks; active repo and release history | Double-entry ledger, CSV rules/import, CLI/TUI/web reporting, lots/cost basis | **Accounting/import reference.** Not a turnkey bank-connected budgeting experience; GPL-3.0 and command-line orientation. |

### Actual Budget details worth testing

- Official documentation lists Akahu as a New Zealand bank provider and supports importing CSV, QIF, OFX, QFX and CAMT statement files.
- Actual's installation documentation says file import and budgeting work without a server; browser/mobile access, device sync and bank sync require the server.
- Bank-sync credentials are held on the server and are not covered by Actual's budget end-to-end encryption. This is a material secret-management boundary, not a reason to assume the product is unsafe. Self-host and protect the host/database.
- Actual is MIT-licensed, so it is the cleanest licensing candidate among the turnkey apps screened here. Any fork still requires normal licence notices and dependency review.

### Preliminary disposition

1. **Trial Actual Budget first** in a disposable, offline/local test environment with synthetic data only. Test the budgeting experience, data export, account model, CSV/OFX imports, mobile access and backup/restore. No bank credentials or real statements yet.
2. **Audit MoneyMatter second** at a pinned release/commit. Focus on exact AGPL relicensing boundary, database schema, bank integration implementation, secret storage, transaction deduplication, tests, dependency vulnerabilities and restore.
3. **Use Beancount/hledger as accounting design references**, not necessarily as the user interface or embedded ledger. Determine whether IDEAL needs a canonical double-entry ledger underneath either app.
4. **Keep Firefly III as a serious alternative** if Actual's envelope-budget model or transaction/account model proves unsuitable.
5. Do not integrate any of these into IDEAL yet. First define the canonical financial contracts and establish whether an external app can safely remain a replaceable adapter/view.

### Important uncertainty and corrections

- Akahu's Personal App page explicitly states the one-hour manual refresh rest period. Akahu's generic refresh page describes 15 minutes as the general default for apps; these statements apply to different app classes, so the Personal App-specific limit governs the proposed personal route.
- Actual's bank-sync documentation surfaced in more than one revision: one describes automatic scheduled syncing and another says manual sync only. The exact behaviour must be checked against a pinned current release and tested before relying on it.
- This screen does not establish that any project is secure, bug-free, accounting-correct or suitable for IDEAL. No security audit, dependency scan, restore test or live integration has been performed.

Sources:
- Actual repository: https://github.com/actualbudget/actual
- Actual bank sync: https://github.com/actualbudget/actual/blob/master/packages/docs/docs/advanced/bank-sync.md
- Actual transaction imports: https://github.com/actualbudget/actual/blob/master/packages/docs/docs/transactions/importing.md
- Actual install modes: https://github.com/actualbudget/actual/blob/master/packages/docs/docs/install/index.md
- MoneyMatter repo/releases: https://github.com/letehaha/moneymatter ; https://github.com/letehaha/moneymatter/releases
- Firefly III repo/releases: https://github.com/firefly-iii/firefly-iii ; https://github.com/firefly-iii/firefly-iii/releases
- Beancount: https://github.com/beancount/beancount
- hledger: https://github.com/hledgerorg/hledger ; https://github.com/hledgerorg/hledger/releases
- Akahu Personal Apps: https://developers.akahu.nz/docs/personal-apps
- Akahu refresh: https://developers.akahu.nz/docs/data-refreshes
- Akahu accreditation: https://developers.akahu.nz/docs/app-accreditation
