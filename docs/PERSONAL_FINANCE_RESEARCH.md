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

---

## 11. Comparative repository audit — pinned evidence checked 16 November 2026

This is a source-level preliminary audit, not a security audit or runtime test. Stable release tags are preferred over development branches. Repository activity and stars are discovery signals, not proof of correctness.

### 11.1 MoneyMatter — feature-complete reference

Repository: https://github.com/letehaha/moneymatter  
Stable release inspected: [v0.33.7](https://github.com/letehaha/moneymatter/releases/tag/v0.33.7), released 30 October 2026; Akahu NZ sync was introduced in v0.33.6 on 29 October 2026. The dev branch has moved beyond the stable tag; do not describe its unreleased work as a stable release.  
Licence: AGPL-3.0-only. README and release history state earlier pre-relicensing versions used CC BY-NC-SA 4.0; do not reuse code from an unverified historical boundary.

**Strengths**
- Broadest all-in-one product fit in this comparison: accounts, transactions, categories, transfers/refunds, budgets, bills, subscriptions, loans, savings/financial goals, investments, portfolio holdings, multi-currency, net worth, CSV/OFX/QFX and other imports, export and backup/restore.
- New Zealand Akahu Personal App integration is in the v0.33.7 source tree. The provider uses the two Akahu tokens and read-only account/transaction endpoints.
- Source inspection shows a 14-day overlap on incremental sync, transaction IDs as provider external IDs, idempotent persistence and an Akahu E2E test suite with mocked API responses. It does not import Akahu's unstable pending feed in the inspected sync path.
- Bank-provider credentials are encrypted before database storage using the application's AES-GCM token encryption utility.
- CI workflow runs frontend lint/test/build/unused-code checks, backend lint/unit tests/typecheck, sharded backend E2E tests, Docker build/smoke checks and related gates.
- Self-hosted mode is documented as keeping analytics/Sentry off and bank sync/AI disabled until configured. Passkey and external identity-provider login options are available.

**Limitations / risks**
- AGPL-3.0-only; unsuitable for copying into IDEAL without a deliberate licence strategy. A separate unmodified instance is a different choice from incorporating code.
- No native two-factor authentication. Project documentation recommends passkeys or an identity provider with its own MFA; if password login remains enabled, password login remains another path.
- No end-to-end encryption. Bank credentials are encrypted at rest, but transaction and balance records are readable by the server operator and database administrator. A compromised live server can access them.
- No published third-party security certification or security audit is disclosed by the project.
- The cloud Plus/free-trial configuration automatically sends selected new bank-transaction fields (amount, currency, account, date, note, payee and category names) to the included AI provider for categorisation; project docs state there is no single global switch to turn that automatic categorisation off. Self-hosted installs keep AI off until a model is configured. For IDEAL evaluation, do not use the cloud service with real financial data; if ever trialled, use self-hosted mode and do not configure AI/MCP access.
- A large feature surface and active migrations increase upgrade/restore review requirements. Some migrations are explicitly irreversible and require restoring a pre-migration backup to roll back. Test restore before trusting the data.
- It is a personal-finance manager, not a broker-grade investment ledger or execution/risk engine. Portfolio holdings and quoted prices must not be treated as authoritative trading accounting.

**Disposition:** best all-in-one feature and workflow reference; a possible synthetic-data evaluation candidate only. Not selected as IDEAL's core, not adopted as a dependency, and not approved for real bank data.

### 11.2 Actual Budget — best envelope-budgeting reference

Repository: https://github.com/actualbudget/actual  
Stable release inspected: [26.11.0](https://github.com/actualbudget/actual/releases/tag/v26.11.0), 2 November 2026.  
Licence: MIT. The repository is active, with a substantial commit/test history and published security policy.

**Strengths**
- Local-first, mobile-friendly budgeting experience with envelope budgeting, transaction rules, scheduled transactions, reports and a mature community.
- Akahu support for New Zealand banks was introduced as an experimental provider in 26.7.0. Bank sync requires actual-server; 26.11 adds scheduled automatic sync while Actual is open.
- Optional end-to-end encryption protects budget data as it leaves the client; local device data still depends on device/disk security.
- Clear published security policy and architecture decision records. The project explicitly says it is designed for a single owner or trusted household, not as a shared server security boundary for unrelated users.
- Strong automated test and release discipline.

**Limitations / risks**
- Official documentation explicitly states native multi-currency is not supported; workarounds use experimental rules and fixed rates. This is a material blocker for IDEAL's NZD base currency plus international investments and foreign-currency accounts.
- Bank-sync API credentials are stored in plaintext on the sync server and are not protected by the budget-file E2EE. Server administrators can read them.
- E2EE has a recovery trade-off: losing the encryption passphrase and local copy can make data unrecoverable.
- Bank sync is not a standalone offline desktop-only feature; it requires the server. Automatic sync runs only while Actual is open and remains constrained by provider/bank refresh policies.
- It is primarily a budgeting/account register, not a full investment holdings or double-entry portfolio-accounting engine.

**Disposition:** excellent envelope-budgeting UX and rules reference; not suitable as IDEAL's main financial ledger while native multi-currency is absent.

### 11.3 Firefly III — strongest personal ledger/accounting candidate

Repositories:
- Core: https://github.com/firefly-iii/firefly-iii
- Data Importer: https://github.com/firefly-iii/data-importer
- Import configuration collection: https://github.com/firefly-iii/import-configurations

Stable versions inspected: Firefly III v6.7.9 (11 October 2026); Data Importer v2.3.5 (23 September 2026). Newer development builds dated 11 and 14 November respectively are explicitly pre-release and warn of possible bugs/duplicate imports.  
Licence: AGPL-3.0-or-later.

**Strengths**
- Mature double-entry personal-finance ledger, multi-currency accounts and transactions, budgets, rules, recurring transactions, savings goals/piggy banks, reports, two-factor authentication and a broad REST JSON API.
- Fully self-hosted by design; README says it does not contact external services unless explicitly configured.
- Data Importer is a separate component, supports CSV and CAMT.052/CAMT.053 files, plus third-party providers. The separation is intentional for security and maintenance.
- Current v2.3.5 source tree contains an enabled Akahu provider and Akahu-specific unit tests. The stable v2.3.5 tag declares the provider. The user-facing configuration documentation has not caught up and still omits Akahu, so treat this as code-level support requiring a pinned-version end-to-end test, not as a fully documented turnkey NZ integration.
- Importer duplicate detection supports content-based hashes and identifier-based matching. Identifier-based matching is preferable when the provider supplies a stable transaction ID.

**Limitations / risks**
- AGPL-3.0-or-later; do not copy code into IDEAL without a separate licence review.
- Firefly's official security documentation states that database data and uploaded attachments are not encrypted at rest. Use full-disk encryption, strict filesystem/database permissions and encrypted backups; do not expose the database port.
- The importer is another service/container with its own API token/configuration and lifecycle. This increases deployment and backup complexity compared with a single application.
- No native investment holdings/portfolio engine. It can track asset accounts and balances, but this is not equivalent to securities lots, corporate actions, derivatives accounting or IDEAL's portfolio ledger.
- Akahu transfer matching has known NZ-specific gaps in the contribution history: NZ domestic account numbers are not IBANs, the transaction type field was initially unused for transfer typing, and dynamic currency precision required attention. These are explicit test items.
- The importer stable release is behind its development branch. The 14 November development build warns that data handling changes may produce duplicates; do not use development images for any financial records.

**Disposition:** leading candidate for a separate private personal-finance ledger or a source of accounting/API patterns. Before any use with real data, test the stable Akahu path, transfer matching, duplicate handling, backups/restores and security configuration using synthetic data. Not adopted or selected.

### 11.4 Money Manager Ex (MMEX) — local/mobile manual-finance option

Repository: https://github.com/moneymanagerex/moneymanagerex  
Stable desktop release: v1.9.4 (31 August 2026). Android app release 5.5.12 was listed by F-Droid in September 2026.  
Licence: GPL-2.0.

**Strengths**
- Local desktop/mobile personal-finance app with checking, credit-card, savings, stock-investment and asset accounts, multi-level categories, budgets, scheduled bills, cash-flow forecasting and reports.
- Uses a local SQLite database with AES encryption; Android supports SQLCipher.
- Can synchronise via user-controlled cloud storage or Syncthing according to its mobile documentation.
- Good fit for a private, manual-first, offline-capable finance workflow and a useful comparison for phone-first usability.

**Limitations**
- No native NZ open-banking/Akahu connector; desktop import is CSV/QIF according to current project documentation.
- No first-party IDEAL integration/API contract identified in this screen.
- Not a web application/server architecture. It is an alternative standalone personal tool, not a foundation for the IDEAL modular monolith.
- GPL-2.0 is a copyleft licence; do not incorporate code without review.

**Disposition:** retain as a possible standalone/manual-only privacy-oriented alternative and mobile UX reference, not as IDEAL's integrated platform.

### 11.5 GnuCash — mature accounting and investment reference

Repository: https://github.com/Gnucash/gnucash  
Stable release: 5.17 (27 September 2026).  
Licence: GNU GPL; exact licence expression to confirm before any reuse.

**Strengths**
- Mature double-entry accounting; multiple currencies; stock and mutual-fund portfolios; QIF and OFX import with transaction matching/duplicate detection.
- Strong accounting semantics and long history; useful reference for investment accounts, lots, realised/unrealised gains and reconciliations.
- Desktop builds for Windows, macOS and Linux.

**Limitations**
- Desktop-first, no suitable integrated phone-first web experience or NZ Akahu path established in this screen.
- XML is the default data store. SQL database support is described by the project as experimental and not fully tested, with some corner cases reported to cause data loss.
- Not a modern multi-engine trading platform.

**Disposition:** accounting and investment-lot reference only; not selected for IDEAL runtime.

### 11.6 Beancount and Fava — auditable ledger model

Repositories:
- https://github.com/beancount/beancount
- https://github.com/beancount/fava

Beancount v3 is the current stable major line (since June 2024); v2 is frozen/obsolete. Beancount is GPL-2.0-only.

**Strengths**
- Plain-text, double-entry accounting with explicit commodities, prices, postings, balances and investment accounting.
- Text ledger and version control make changes inspectable and auditable.
- Fava supplies a web UI and reports.

**Limitations**
- Not a turnkey budgeting/bank-sync/mobile product; bank statement ingestion is primarily importer/script based.
- More technical and text-oriented than the requested personal finance experience.
- GPL-2.0-only is a licence consideration for reuse.

**Disposition:** excellent reference for ledger invariants, auditability and reproducible accounting; not an end-user product foundation.

### 11.7 hledger — multi-currency journal and import reference

Repository: https://github.com/hledger/hledger  
Stable release inspected: 1.52.4 (10 September 2026).  
Licence: GPL-3.0.

**Strengths**
- Text journal accounting, multi-currency, well-documented CSV import rules, CLI, TUI and web UI; supports Windows.
- Strong focus on reliability, real-world practicality and documented formats.
- Good reference for reconciliation, import rules, reports and deterministic ledger calculations.

**Limitations**
- Not a polished consumer budgeting application or native bank aggregation service.
- No integrated investment holdings/portfolio engine or NZ bank connection identified in this screen.
- GPL-3.0.

**Disposition:** accounting/import/reporting reference only.

---

## 12. Revised shortlist and build-versus-adopt recommendation

| Candidate | Best role | Key blocker | Current disposition |
|---|---|---|---|
| Firefly III + Data Importer | Separate personal finance ledger; multi-currency, double-entry, 2FA, REST API | AGPL; no investment holdings; no at-rest encryption; Akahu docs/transfer handling need tests | Leading candidate for isolated synthetic-data evaluation |
| MoneyMatter | Broad all-in-one feature and mobile UX reference; NZ Akahu integration | AGPL; no native 2FA/E2EE; AI privacy defaults in cloud; no external security audit disclosed | Reference and synthetic-data evaluation candidate only |
| Actual Budget | Envelope budgeting UX, local-first workflows, Akahu | No native multi-currency; bank tokens plaintext on server | Borrow UX/rules patterns only |
| Money Manager Ex | Offline/manual, encrypted, mobile personal finance | No NZ bank sync or IDEAL API; standalone desktop/mobile | Optional private manual-only fallback |
| GnuCash | Double-entry, multi-currency, stock accounting | Desktop-centric; SQL storage experimental | Accounting reference |
| Beancount/Fava | Auditable ledger and investment postings | Technical/manual import; no mobile-first bank sync | Ledger semantics reference |
| hledger | Deterministic journal, CSV import, reports | Technical UX; no integrated investment/bank feeds | Accounting/import reference |

**Recommended IDEAL direction (not yet approved as an implementation decision):**
1. Do not make any external personal-finance app the authoritative ledger for all IDEAL engines.
2. Keep Personal Finance as a separate IDEAL domain with its own ledger and account ownership.
3. Reuse established accounting principles (double-entry, reconciliation, currency precision, transaction provenance) and budgeting workflows; do not copy AGPL/GPL code.
4. Use a read-only adapter to consolidate balances/performance from investment and trading engines. Do not pool cash, margin or collateral.
5. Treat Firefly III as the leading external accounting candidate for an isolated comparison; treat MoneyMatter as the broadest product reference. A future decision may still favour a clean, small IDEAL-owned domain if adapter complexity or data ownership outweighs reuse.
6. No bank account, API token, provider, host, runtime dependency or application is selected by this research.

## 13. Akahu-specific data quality and refresh constraints

Official Akahu documentation checked 16 November 2026:
- Personal Apps are free and limited to the owner's own Akahu account; account information only, no payments, no webhooks; scheduled refresh is daily and manual refresh has a one-hour rest period.
- Personal Apps can access up to 730 days of transaction history, subject to any shorter history limits imposed by the financial institution.
- Settled transactions and pending transactions are separate endpoints. Pending transactions are unstable, may change date/description and do not have stable transaction IDs; they should be treated as provisional and rebuilt on each fetch.
- Settled transactions normally have stable Akahu IDs, but a small fraction may be deleted/replaced with new IDs if the bank mutates a transaction beyond recognition. Consumers must handle updates and deletions, not only append new records.
- API timestamps are UTC; pagination is required for larger histories; bank refresh timestamps must be displayed so users can see data freshness.
- Bank transaction data is not a real-time event stream. The Personal App's daily schedule and manual-refresh rest period are incompatible with a promise of live balance/transaction freshness.

References:
- Personal Apps: https://developers.akahu.nz/docs/personal-apps
- Accessing transactional data: https://developers.akahu.nz/docs/accessing-transactional-data
- Transaction model: https://developers.akahu.nz/docs/the-transaction-model
- Data refreshes: https://developers.akahu.nz/docs/data-refreshes
- Pending transactions: https://developers.akahu.nz/reference/get_transactions-pending

## 14. Practical viability for the owner's private-use goals

**Viable without a bank connection**
- Manual accounts, assets and liabilities; CSV/QIF/OFX/CAMT imports; budgets; bills; subscriptions; debt; savings goals; cash-flow forecasts; net worth; investment statements and valuations.
- All imports must be previewed, validated, deduplicated and reconciled before posting. No silent balance corrections.

**Viable with a future read-only Akahu connection**
- Account balances and settled transactions for supported NZ banks, subject to daily refresh and provider/bank historical limits.
- Display last refreshed timestamps and stale-data warnings.
- Handle transaction updates/deletions, pending-vs-settled states and account disconnections explicitly.
- Do not use bank-feed values as permission to spend, transfer or trade.

**Not appropriate for the first version**
- Payment initiation, automated transfers, broker orders, exchange connectivity or live trading.
- Claims of real-time bank data.
- Public multi-user SaaS, commercial open-banking accreditation or financial-advice functionality.
- Cross-engine cash/margin pooling.
- Cloud AI processing of identifiable bank transactions by default.

**Hosting reality**
- A phone is a client, not a dependable always-on server.
- Local/private operation on an existing PC can work while that PC is on; remote/mobile access then requires a deliberate secure network path.
- A VPS or public web app is technically possible later, but introduces ongoing cost, provider access to runtime data, hardening, MFA, TLS, patching, backups and incident response. No free always-on hosting assumption is approved.
- Start with synthetic data and manual workflows. Do not put real bank data into an unreviewed prototype.

## 15. Audit and provenance contract requirements

The future audit record should be structured and reconstructable, not a transcript of hidden internal reasoning. For each event, preserve as appropriate:
- event ID, event type, actor/source, timestamp, correlation/import batch ID;
- source system and source record ID, source timestamps, data freshness and provider/account reference;
- parser, mapping, rule, FX-rate, valuation and software versions;
- before/after references or immutable journal entries, validation result, duplicate decision and reconciliation outcome;
- calculation inputs, output, assumptions, confidence/limitations and concise decision rationale;
- explicit user approval/denial for any action, including the exact scope approved;
- errors, retries, idempotency key, reversal/supersession and recovery references.

Do not log bank tokens, passwords, full unredacted statement payloads, or sensitive personal data unnecessarily. Keep raw evidence in protected storage with explicit retention controls; GitHub stores documentation and source only, never personal financial records. Corrections must be reversible and traceable, not silent mutation.

## 16. Research outcome

The one-package all-in-one ideal is not yet met by a candidate without trade-offs:
- MoneyMatter has the broadest feature coverage but has material security/licence limitations.
- Firefly III has the strongest accounting/API/multi-currency foundations but no native investment holdings and an extra importer component.
- Actual Budget has the best envelope-budgeting UX but lacks native multi-currency.
- MMEX is the best offline/manual privacy alternative but lacks NZ bank sync and web/API integration.

The most viable path for IDEAL is therefore a separated Personal Finance domain plus separate investment/trading engines and a read-only consolidated view. Whether its initial ledger is IDEAL-owned or a private Firefly III adapter remains open and requires further isolated evaluation.

**Approval boundary unchanged:** D-017 Proposed; D-001 unchanged; Phase 02 architecture/contracts only; Phases 03–19 locked. No implementation, dependency adoption, account connection, credentials, bank provider selection, payments or hosting are authorised.


## 17. Pinned-release source audit — Akahu import correctness (17 November 2026)

This section records a source-level inspection of the exact stable tags below. No application was installed or executed; no live Akahu request, account, token or financial record was used. The MoneyMatter E2E tests inspected use mocked HTTP responses. Findings are code-path observations, not a security certification or independent runtime test.

### 17.1 Pinned source and evidence

| Project | Pinned release | Source paths inspected |
|---|---|---|
| Firefly III Data Importer | v2.3.5 | `app/Services/Akahu/Conversion/TransactionConverter.php`; `TransactionFetcher.php`; `Request/GetTransactionsRequest.php`; `Request/AkahuDateRange.php`; `Response/GetTransactions/GetTransactionsResponseBuilder.php`; `Model/Transaction/Transaction.php`; `Services/Shared/Import/Routine/ApiSubmitter.php`; `Services/Shared/Configuration/Configuration.php`; `Services/Akahu/Authentication/SecretManager.php`; `tests/Feature/Akahu/HttpFlowTest.php` |
| MoneyMatter | v0.33.7 | `packages/backend/src/services/bank-data-providers/akahu/akahu.provider.ts`; `api-client.ts`; `types.ts`; `akahu-flow.e2e.ts`; `services/bank-data-providers/utils/credential-encryption.ts` |

Pinned-source links:
- Firefly converter: https://github.com/firefly-iii/data-importer/blob/v2.3.5/app/Services/Akahu/Conversion/TransactionConverter.php
- Firefly fetcher: https://github.com/firefly-iii/data-importer/blob/v2.3.5/app/Services/Akahu/Conversion/TransactionFetcher.php
- Firefly submitter: https://github.com/firefly-iii/data-importer/blob/v2.3.5/app/Services/Shared/Import/Routine/ApiSubmitter.php
- Firefly Akahu flow test: https://github.com/firefly-iii/data-importer/blob/v2.3.5/tests/Feature/Akahu/HttpFlowTest.php
- MoneyMatter Akahu provider: https://github.com/letehaha/moneymatter/blob/v0.33.7/packages/backend/src/services/bank-data-providers/akahu/akahu.provider.ts
- MoneyMatter Akahu API client: https://github.com/letehaha/moneymatter/blob/v0.33.7/packages/backend/src/services/bank-data-providers/akahu/api-client.ts
- MoneyMatter Akahu mocked E2E suite: https://github.com/letehaha/moneymatter/blob/v0.33.7/packages/backend/src/services/bank-data-providers/akahu/akahu-flow.e2e.ts

### 17.2 Transaction import, idempotency and source corrections

**MoneyMatter v0.33.7**
- First connection fetches the available settled transaction feed. Subsequent sync starts 14 days before the newest imported transaction, specifically to catch late-settling NZ bank rows.
- The API client follows every Akahu cursor page and carries the same start/end window to each page.
- Persistence is ordered by transaction date. It checks account + Akahu `_id` against `originalId`; an existing ID is skipped. A second lookup on `externalData.originalSource.originalId` restores the source ID after unlink/relink.
- This is good append idempotency and unlink/relink protection. It is not source reconciliation: an existing ID is skipped even if the bank has since changed amount/date/description/metadata. The inspected code does not reconcile removed Akahu IDs into local reversals/deletions.
- The 14-day overlap catches late-arriving records within the overlap; it is not proof that older transactions are rechecked indefinitely for changes.
- The provider uses Akahu's settled endpoint only. No pending-transaction endpoint is called in the inspected provider/API client.
- Imported amounts are converted to the account's currency precision (Money/cents); direction is stored separately as income/expense. Currency comes from the account balance payload.
- The metadata mapper stores Akahu type, merchant, category, category group, particulars, reference, card suffix and balance-after. It does not persist Akahu `meta.conversion` amount/currency/rate as explicit foreign-currency transaction fields.
- Every imported transaction is explicitly created with `transferNature: not_transfer`. Therefore a bank-to-bank transfer is initially classified as an income/expense row, not automatically paired into a transfer by this connector.
- The current balance is separately written to balance history when Akahu supplies it; if current balance is null, the balance is left unchanged. Balance freshness is taken from Akahu's `refreshed.balance` timestamp when available.
- The 20-hour stale-data threshold may request an Akahu refresh, but the source comments correctly note refresh is asynchronous: the current sync still reads the cached account/transactions; the request can improve the next sync only.
- Mocked E2E tests cover valid/invalid credentials, account selection, signed amounts, cents, repeat-sync idempotency, late-settling rows, cursor pagination, 14-day overlap, transient 5xx recovery, auth-failure handling, stale refresh requests, period imports, pre-link history and unlink/relink. The inspected suite does not test changed-content updates or source deletions.

**Firefly III Data Importer v2.3.5**
- The Akahu request fetcher follows all cursor pages and applies the same date range on each request. Its date-range adapter subtracts one millisecond from the inclusive lower calendar date and adds a day to the upper bound to account for Akahu's exclusive `start` and inclusive `end` semantics.
- The converter stores Akahu `_id` as Firefly `external_id`. For non-file flows, the import configuration defaults duplicate detection to the `cell`/identifier path; the submitter defaults an empty identifier field to `external_id`. A repeat ID is therefore skipped, including when Firefly finds that identifier on a deleted transaction.
- This is identifier-based append idempotency, not update/delete reconciliation. If Akahu changes the contents while retaining the ID, the importer finds the ID and skips the changed record. If Akahu removes and replaces a transaction with a new ID, the new ID can import but the old Firefly entry is not automatically reversed/deleted.
- The converter maps positive amounts to deposits and negative amounts to withdrawals. Optional Akahu other-account data becomes a source/destination name; the inspected Akahu conversion path does not demonstrate robust resolution of both sides to existing Firefly accounts or automatic pairing of opposite-side bank entries.
- Akahu conversion metadata can populate Firefly foreign amount and currency, but the code hard-codes two decimal places for the foreign amount and also uses two decimals for the account amount (the source contains FIXME comments about obtaining account decimal places). This is a precision risk for currencies with zero or three minor-unit decimals.
- The Akahu converter maps the account-side amount and foreign amount, but does not use the Akahu transaction balance as a continuously reconciled account balance. New-account opening balance is separately configured by the user.
- The Akahu response model reads settled transaction records; the inspected request calls the settled transactions endpoint and does not query pending transactions.
- Akahu-specific test coverage is materially thinner than MoneyMatter's: the v2.3.5 `HttpFlowTest` contains a TODO to mock Akahu API responses. There are Akahu model/unit tests, but the inspected Akahu feature test does not exercise the complete import/conversion/submit lifecycle against mocked transactions.
- Akahu credentials are retrieved from server-side session state or environment-backed configuration in the inspected SecretManager. This code path does not itself show an application-level encrypted credential store. Actual exposure depends on session driver, host controls, environment handling and logs; this requires deployment-specific review.

### 17.3 Transfers, pending rows and foreign currency — comparison

| Requirement | MoneyMatter v0.33.7 | Firefly importer v2.3.5 |
|---|---|---|
| Stable-ID repeat import | Yes: account + `originalId`, plus unlink/relink recovery | Yes: Akahu `external_id` and default identifier duplicate path |
| Update same ID when bank changes row | Not in inspected persistence path; existing row skipped | Not in inspected submit path; existing identifier skipped |
| Remove/reverse row deleted upstream | Not in inspected persistence path | Not in inspected import path |
| Pending transactions | Not queried by inspected connector | Not queried by inspected connector |
| Late-settling rows | 14-day incremental overlap; mocked E2E test | Date-window import/pagination; no equivalent tested rolling overlap identified |
| Automatic transfer pairing | No: explicitly imports as `not_transfer` | Not demonstrated; deposit/withdrawal with source/destination names |
| Foreign-currency conversion metadata | Akahu conversion object not mapped into explicit foreign amount/currency/rate fields | Foreign amount/currency mapped, but amount rounded to 2 decimals |
| Current account balance | Explicit balance-history write when current balance is supplied | Not continuously synced by the inspected importer converter |

Akahu's own documentation says settled records can be modified or deleted and that consumers should process additions, modifications and deletions. It also states pending transactions are separate, unstable, lack stable IDs and should be rebuilt on each fetch. Neither pinned connector implements the full Akahu lifecycle described by the provider.

### 17.4 Security, recovery and integration implications

- MoneyMatter encrypts the stored Akahu credential object through its credential-encryption helper before database persistence. This is a meaningful control, but the key-management, backup encryption, rotation and restore procedure still require an isolated deployment review.
- MoneyMatter's provider does not expose webhook/realtime support for Akahu Personal Apps; its code explicitly marks webhooks and realtime unsupported. The 12-hour internal sync schedule cannot make upstream daily Personal App data fresh.
- Firefly's Akahu credentials are supplied via session or environment-backed config in the inspected importer code. No application-level encryption of these tokens is visible in that code path. Firefly's core ledger still has the previously recorded at-rest database encryption limitation.
- MoneyMatter documents a self-hosted PostgreSQL/Redis/Docker stack and backup/restore workflow; this is operationally heavier than a single local database. Restore drills and off-host encrypted backups remain mandatory before any real data.
- Firefly III and its importer are separate services. Their API boundary is useful, but introduces another credential, network and backup boundary. Firefly's AGPL obligations remain a separate reuse decision.
- Neither connector should be treated as an authoritative bank reconciliation engine for IDEAL. The required behaviour is a source-observation ledger with immutable raw-event references, deterministic normalisation, versioned matching, update/supersession handling, explicit deletion/tombstone handling, and a separate pending snapshot lifecycle.

### 17.5 Synthetic fixture acceptance matrix for any future POC

No fixtures were executed in this audit. A future separately approved synthetic-only POC must include at least:

1. Same transaction ID, identical payload imported twice → one economic event.
2. Same transaction ID, changed description/date/amount/balance → update or superseding version, never silent skip.
3. Old transaction removed by provider → explicit tombstone/reversal workflow; no silent historical erasure.
4. Removed ID replaced by new ID → link old/new source records and prevent double counting.
5. Pending row changes date/description/amount, then disappears and settles under a new ID → provisional snapshot is replaced and reconciled once.
6. Two sides of an internal transfer arrive on separate accounts, with different descriptions/fees/settlement dates → candidate match with confidence and user review; never infer transfer solely from equal amounts.
7. Foreign card purchase with NZD base posting and JPY/KWD/GBP conversion → preserve exact source decimal, foreign amount, currency and rate; no binary-float rounding.
8. Pagination with fixed date bounds and a cursor → no missing or duplicated page boundary.
9. Akahu API outage, 401/403, 429 refresh throttle and partial-page failure → no false-success checkpoint; safe retry with idempotency.
10. Account balance null/stale/revised → preserve freshness timestamp and reconcile statement balance against ledger without silently rewriting transactions.
11. Import rollback/replay after interruption → deterministic results and auditable batch state.
12. Backup restore → credentials excluded or separately protected, database and attachments restored, checksums and ledger totals verified.

### 17.6 Revised disposition

**Do not adopt either bank connector as IDEAL's correctness model.** MoneyMatter is the stronger Akahu integration reference because its pinned provider has substantially broader mocked E2E coverage, pagination, incremental overlap, stable-ID idempotency, unlink/relink recovery, auth-failure handling and balance-history handling. Its important gap remains append-only behaviour for upstream edits/deletions, no pending feed, no automatic transfer classification and loss of explicit Akahu FX conversion metadata.

Firefly remains the stronger external double-entry/multi-currency ledger candidate, but its Akahu importer is less mature in the inspected tag: identifier deduplication exists, while full update/delete reconciliation and a comprehensive mocked Akahu flow test are not demonstrated. Its two-decimal conversion and account-currency assumptions require tests before trusting NZD/international accounts.

The architecture recommendation is therefore:
1. Keep the Personal Finance domain separate from trading and investment engines.
2. Keep IDEAL-owned source observations and reconciliation semantics as the eventual authority, rather than relying on either connector's import semantics.
3. If a future external-ledger POC is approved, compare Firefly for double-entry/accounting semantics and MoneyMatter for bank-sync/UX behaviour using synthetic fixtures only. Do not connect a real bank.
4. No runtime, dependency, credential, bank connection, installation, host or implementation is selected by this audit.

**Approval boundary unchanged:** D-017 remains Proposed; D-001 remains accepted and unchanged; Phase 02 architecture/contracts only; Phases 03–19 remain LOCKED.


### 17.7 Backup, restore and credential-key lifecycle follow-up

A second pinned-source pass inspected MoneyMatter v0.33.7 encryption and backup/restore code.

**MoneyMatter credential encryption**
- Akahu credentials are stored as an encrypted JSON object. The pinned encryption helper uses AES-256-GCM with a random IV and authentication tag.
- The AES key is derived as SHA-256 of `APPLICATION_JWT_SECRET`. This means the deployment must preserve this secret securely and include it in disaster-recovery planning. Changing it without a migration/re-encryption process will make existing ciphertext undecryptable. No key-rotation workflow was identified in the inspected source; this remains an open security/operational question.
- This is application-level encryption at rest for the credential field, not end-to-end encryption of the financial database.

**MoneyMatter backup/restore**
- The backup export E2E source explicitly tests that plaintext bank tokens, encrypted credential blobs and AI API keys are absent from every archive file. Bank connection rows remain for account linkage, but credentials are set to null.
- The restore E2E source explicitly tests that a restored bank connection is inactive with a `RESTORED` reason, appears in the reauthentication-required list, and becomes active only after valid credentials are re-entered.
- Restore tests cover same-user round-trip consistency, cross-user remapping, transaction/transfer/holding data, import-batch undo state, foreign-reference handling, checksums, malformed/newer archives and rollback on invalid data. These are source-level test observations; the suite was not executed here.
- Attachments are explicitly excluded from the backup/restore registry because their binary files are not included. They require a separate backup and restore procedure if used.
- The self-hosted deployment is a multi-service PostgreSQL/Redis/Docker stack. Redis is queue-only; database and attachment storage require their own backup strategy. Backup archives should be encrypted off-host by the operator and restore drills should verify ledger totals, balances, transfer pairs, attachment availability and credential reauthentication.

**MoneyMatter transfer capability clarification**
- The product supports manual/explicit transfer records generally, but the pinned Akahu provider still creates bank-imported transactions with `transferNature: not_transfer`. General product transfer capability must not be confused with automatic bank-feed transfer pairing. Any matching service elsewhere in the product would need a distinct provider-path test before relying on it for Akahu.

**Firefly comparison**
- The Akahu note builder preserves other-account details as notes, not as a resolved destination/source account relationship. The converter still maps the bank row to a deposit or withdrawal and does not demonstrate automatic two-sided transfer pairing.
- The Data Importer stores Akahu tokens in server-side session or environment-backed configuration in the inspected path. The deployment must protect session storage, environment secrets, logs and the Firefly API token. No application-level encryption of Akahu credentials is visible in this importer SecretManager.

**Updated security/recovery disposition**
- MoneyMatter has a stronger explicit credential-at-rest and secret-safe backup/restore story in the pinned source than the Firefly Akahu importer path inspected. Its encryption key is deployment-critical and its attachment exclusion must be handled operationally.
- Firefly remains attractive for double-entry accounting but its Akahu connector needs a deployment-specific secrets review and a synthetic restore/reconciliation exercise before any real data is considered.
- Neither backup system has been runtime-tested by IDEAL. No backup was created, no restore executed, and no application installed.

## 18. Additional open-source component audit — 17 November 2026

This audit looked for reusable components that solve the remaining gaps: durable source identity, statement ingestion, exact accounting, correction/reversal handling, portfolio read models, backup/restore, and mobile-first personal-finance UX. Source was inspected through repository READMEs, schemas, license files, official documentation and selected implementation files. No repository was installed or executed.

### 18.1 Shortlist and disposition

| Project | Licence / observed activity | Useful capability | IDEAL disposition |
|---|---|---|---|
| [astt](https://github.com/mike840609/assets_tracker) | MIT; 26 stars and 861 commits in the inspected GitHub snapshot; CI and E2E workflows documented | Mobile PWA, accounts, cash, liabilities, holdings, goals, recurring cash/DCA, net worth, backup/restore | Best permissively licensed product/UI reference; not an authoritative ledger |
| [krbob/portfolio](https://github.com/krbob/portfolio) | 2 stars; 763 commits; activity recorded from 2024-07 to 2026-11-01; no root LICENSE file found in inspected tree | Transactions as canonical source, rebuildable read models, decimal-text persistence, audit trail, backup/restore preview, stale/partial data states | Strongest portfolio-domain architecture reference; do not copy/reuse code unless licence is clarified |
| [Formance Ledger](https://github.com/formancehq/ledger) | MIT; 1.4k stars, 2,289 commits, 18 open issues in inspected repository snapshot; v2.4.18 latest stable, v3.0.0-rc.3 pre-release | Double-entry ledger, immutable log/audit chain, idempotent writes, deterministic state machine and rebuildable projections | Study invariants and API patterns; do not adopt as a single-user runtime dependency now |
| [TigerBeetle](https://github.com/tigerbeetle/tigerbeetle) | Apache-2.0 | Immutable financial transfers, strict account/ledger invariants, pending/post/void and compensating corrections | Excellent correctness reference; purpose-built high-throughput database is excessive for IDEAL's initial personal-finance domain |
| [Akahu JavaScript SDK](https://github.com/akahu-io/akahu-sdk-js) | ISC; package metadata inspected at v2.6.0; 225 commits and 34 stars in repository snapshot | Typed API client, OAuth helpers, cursor pagination, settled and pending transaction methods, webhook signature verification | Potential adapter helper if IDEAL's eventual backend is Node/TypeScript; otherwise use the REST contract. Server-side only. No dependency added |
| [OFX Statement](https://github.com/kedder/ofxstatement) | GPL-3.0; 367 stars, 667 commits; Coveralls reported 95.27% line coverage on 22 Aug 2026 | Plugin-based conversion of bank-specific exports to OFX; sample statement fixtures | Useful import architecture and test-fixture reference; licence review required before reuse or embedding |
| [Beangulp](https://github.com/beancount/beangulp) | GPL-2.0-only; 145 stars, 468 commits; no published GitHub releases in inspected snapshot | Importer framework for Beancount 2.3/3.0 and document ingestion | Importer design reference only; GPL and Beancount coupling make it unsuitable as an assumed IDEAL dependency |
| [rotki](https://github.com/rotki/rotki) | AGPL-3.0; latest inspected release v1.44.2 dated 22 Oct 2026 | Self-hosted crypto portfolio accounting, exchange/blockchain event decoding, PnL and analytics | Specialist crypto accounting reference; not household finance ledger |
| [Ghostfolio](https://github.com/ghostfolio/ghostfolio) | AGPL-3.0; 9.3k stars; release 3.99.0 dated 7 Nov 2026 | Mature investment dashboard, multi-account portfolio views and mobile-first PWA | Strong investment UX reference; not budgeting or a complete double-entry household ledger |
| [Flowfolio](https://github.com/lukasbloom/flowfolio) | AGPL-3.0 | Exact decimal arithmetic, transaction-history performance, multi-currency and backup concepts | Secondary research reference only; no adoption or licence-compatible reuse assumed |

Repository metrics are discovery context, not security or correctness ratings. The inspected source and license files are the controlling evidence for the specific observations below.

### 18.2 astt — best permissive product reference, with ledger limitations

Repository: https://github.com/mike840609/assets_tracker

The inspected root LICENSE is MIT. The repository documents CI, unit/integration/E2E tests, Docker self-hosting, PostgreSQL, a responsive PWA and a private single-owner authentication option. Its product scope covers cash accounts, liabilities, holdings, recurring cash flows, recurring investments, net-worth snapshots, goals and portfolio views.

Important source-level limitations:
- Its README explicitly distinguishes it from Firefly III and Actual Budget: astt does not provide a budgeting/double-entry bookkeeping ledger.
- Its Prisma schema stores Account.cashBalance, CashTransaction and HoldingTransaction as separate product models. This is useful for a tracker but is not a complete double-entry journal.
- The account and holding transaction relations use cascading deletes. The inspected account DELETE route directly deletes the account; dependent holdings and transactions are removed by the database cascade. That behaviour is unacceptable for IDEAL's authoritative audit ledger unless replaced with archival/closure semantics.
- The database stores money/quantity as DECIMAL(28,8), but its API accepts JSON IEEE-754 numbers. Its own database documentation correctly explains that eight fractional decimals are not preserved at every supported magnitude. IDEAL should send canonical decimal strings at financial API boundaries.
- Manual account balance corrections are represented as EDIT cash transactions. This is a useful UX pattern, but IDEAL should model a correction as an explicit, immutable journal adjustment.
- The product is a useful candidate for a synthetic-data UX review, not for importing its persistence model as IDEAL's source of truth.

Disposition: retain as a permissively licensed UI/product reference. Any later code reuse requires a separate compatibility, architecture and security review. No source code was copied.

### 18.3 krbob/portfolio — strong portfolio architecture, reuse blocked pending licence

Repository: https://github.com/krbob/portfolio

The README and financial-methodology document describe a strong pattern: canonical transactions are replayed to derive holdings, allocation, contributions and performance; snapshots/read models can be rebuilt; values are persisted as canonical decimal text; stale, partial and unavailable market data are explicit; backup/restore includes preview and audit records.

The repository reports 763 commits and a low star count (2) in the inspected snapshot. It is active but small and appears to be a single-investor project. It is a portfolio tracker, not a complete budgeting/bank aggregation system. A root LICENSE file was not found in the inspected repository tree; therefore its code is not cleared for reuse. Public visibility is not a licence grant.

Disposition: use its published methodology and operational documentation as architecture study material only. Ask for licence clarification before any code reuse. Do not adopt its application or cross-repository service stack.

### 18.4 Formance Ledger — powerful but wrong-sized runtime dependency

Repository: https://github.com/formancehq/ledger

The inspected LICENSE is MIT. Its current main branch is Ledger v3 architecture, but the releases page identifies v2.4.18 as the latest stable release while v3.0.0-rc.3 remains a release candidate. Do not treat v3 main as a stable release.

The v3 architecture documents a deterministic state machine, replicated audit history, integrity checking and rebuildable read-side projections. Its idempotency implementation hashes request content, returns the original result for a repeated key and rejects reuse of the same key with different content. The default key TTL is 24 hours; policy value zero means no expiry.

Important distinction: an API idempotency key is not the same as a durable external transaction identity. IDEAL still needs a persistent uniqueness mapping keyed by provider + connection + source account + provider transaction ID, together with observation versions and source deletion/replacement handling. A short-lived retry key cannot replace that registry.

Disposition: study its immutability, correction, idempotency conflict and projection patterns. A replicated Raft cluster is unnecessary operational complexity for a private single-user finance system. No runtime dependency selected.

### 18.5 TigerBeetle — correctness reference, not a household ledger application

Repository: https://github.com/tigerbeetle/tigerbeetle

The inspected LICENSE is Apache-2.0. Official documentation describes immutable accounts and transfers, balanced posted/pending debit-credit totals, explicit two-phase pending/post/void transfers and corrections using additional transfers rather than mutation or deletion.

These properties align with IDEAL's audit requirements. However, TigerBeetle is a specialised financial transactions database with its own data model, server process and operational requirements. It does not solve bank-source reconciliation, transaction categorisation, budgeting, investment holdings, statement import or user-facing personal finance. Its amount/ledger primitives also require explicit modelling of currency and scale.

Disposition: use as a source of ledger invariants and correction patterns. Do not add TigerBeetle to the initial stack.

### 18.6 Import standards and libraries

- Akahu's official JavaScript SDK package metadata reports ISC licensing and version 2.6.0. The SDK exposes cursor-paginated settled and pending transaction methods, OAuth helpers and webhook signature validation. App secrets must remain server-side. Personal Apps do not provide webhooks, so webhook-driven reconciliation cannot be assumed for the private Personal App route.
- Akahu's current Getting Started page explicitly says Personal Apps are useful for exploring one's own data but are unsuitable for a production-ready application. The page says a full app and accreditation are required before releasing an Akahu integration to production. This tightens the earlier feasibility assessment: Personal App access may support personal experimentation, but IDEAL must not assume it is a permitted production connector. Obtain provider confirmation before any real account connection or deployed integration.
- OFX Statement is a plugin-based conversion tool for bank-specific exports. Its GPL-3.0 licence means it should not be embedded into an IDEAL-owned distribution without a deliberate licence decision. The ofxstatement-iso20022 plugin README describes its implementation as trivial/naive; it is not a production-ready NZ CAMT parser.
- Beangulp provides a useful importer lifecycle and document-ingestion pattern, but it is GPL-2.0-only and tied to Beancount. Reuse is not assumed.
- Prefer an IDEAL-owned import adapter contract with isolated parsers and golden fixtures. Accept CSV first; add OFX and ISO 20022 CAMT.053/CAMT.054 parsers only when supported statement samples and test fixtures are available. Do not infer that all NZ banks expose these formats.

### 18.7 Overall reuse decision

No inspected repository is a safe, complete drop-in solution for IDEAL's required combination of private single-user operation; NZD-first multi-currency personal accounts and liabilities; robust source-observation reconciliation; immutable double-entry accounting and correction history; bank statement imports and a possible Akahu adapter; investment and crypto portfolio visibility; mobile-first UI; and strict separation from the perpetual-futures trading ledger.

Recommended reuse boundary:
1. Study Formance/TigerBeetle for ledger invariants and idempotency/correction semantics.
2. Study Beancount/Beangulp and OFX Statement for statement ingestion and reconciliation workflows, respecting their licences.
3. Study astt/Ghostfolio/rotki for user experience and investment reporting; astt is the most permissively licensed candidate, but its schema is not IDEAL's ledger.
4. Keep the authoritative source-observation registry, reconciliation policy and accounting journal IDEAL-owned.
5. Do not install or add any dependency during Phase 02.

## 19. Feasibility and proposed IDEAL data contract

### 19.1 Feasibility conclusion

A private single-user personal-finance domain is technically viable within IDEAL's approved modular-monolith direction. It should be a distinct bounded context with its own ledger and permissions, not a feature bolted into the perpetual-futures engine. A read-only net-worth projection may aggregate balances and valuations from separately governed domains; it must not pool cash, collateral, margin or execution permissions.

The largest feasibility risk is not the dashboard or arithmetic. It is source reconciliation and long-term operational responsibility for sensitive financial data. Manual entry and file import are feasible without bank aggregation. Akahu must remain a conditional future adapter until provider terms and the Personal App production limitation are resolved.

### 19.2 Proposed data flow

Source adapter -> import batch -> immutable source observations -> reconciliation decisions -> immutable journal entries/postings -> rebuildable balance, budget and net-worth projections.

Keep three different records separate:
- Source observation: what a bank, statement or user supplied at a particular observation time.
- Reconciliation decision: how IDEAL matched, versioned, ignored, superseded or escalated that observation.
- Accounting journal: the financial effect accepted by IDEAL. It is not silently rewritten when a provider changes its data.

### 19.3 Required contract invariants

1. **Durable source identity:** unique key scoped by provider, connection, source account and external transaction ID. Keep it independently of any short-lived API idempotency cache.
2. **Immutable observations:** retain each changed source payload as a new version with received time, source version/hash, adapter version and import-batch reference. Minimise raw payload retention and protect any retained payload as sensitive data.
3. **Safe retries:** at-least-once fetch plus durable idempotent persistence. Replaying the same page/batch must not create another observation or journal posting.
4. **Correction handling:** same-ID changed data creates a new observation version and reconciliation decision. If the old version has been posted, correct it with a traceable adjustment/reversal, not silent mutation.
5. **Deletion handling:** never infer deletion from absence in an incomplete page, incremental overlap or provider outage. Require an explicit source deletion signal or a complete, bounded authoritative re-fetch before creating a tombstone. A tombstone does not delete the accounting history.
6. **Replacement IDs:** a changed provider ID may represent a replacement of an old transaction. Correlate conservatively; uncertain cases require review rather than automatic duplicate suppression.
7. **Pending/settled separation:** pending rows are provisional snapshots, not posted journal entries. Reconcile them to settled rows; preserve state transitions and avoid double-counting.
8. **Exact numbers:** financial APIs use decimal strings, not binary floating-point JSON numbers. Keep money, asset quantity, unit price and FX rate as separate precision domains. Preserve source scale and ISO currency code; do not hardcode two decimals for all currencies or crypto quantities.
9. **FX provenance:** retain original amount/currency, converted amount/currency, rate, rate source, rate timestamp and any fee where provided. Missing FX makes a valuation incomplete; never guess using today's rate for historical transactions.
10. **Double-entry journal:** posted journal entries are immutable; postings balance per commodity/currency or use explicit FX clearing/conversion accounts. Account balances are derived projections, not independently editable truths.
11. **Transfer matching:** identify candidate cross-account transfers using amount, currency, dates and counterparty metadata. Pairing confidence is explicit; ambiguous matches require review. Never categorise both sides as income/expense.
12. **Balance reconciliation:** provider-reported current/available balances are observations. Compare them with ledger-derived balances and record discrepancies; do not overwrite journal entries to force a match.
13. **Deterministic replay:** same ordered observations, reconciliation decisions, accounting rules and versions must produce the same ledger and projections.
14. **Backup/recovery:** versioned, checksummed backups; restore preview; atomic restore; documented key rotation; tested recovery. Never put bank credentials or private financial records in GitHub.
15. **Credential isolation:** if a bank adapter is ever approved, use a dedicated encryption key separate from authentication/JWT signing secrets, with rotation/re-encryption procedure. Keep credentials out of logs and exports.

### 19.4 Minimum synthetic acceptance matrix

Before any real source is connected, a separately approved synthetic-only prototype must test:
- duplicate page, repeated file and retry after a simulated crash;
- same external ID with unchanged data, corrected amount/date/description and source deletion;
- incomplete pagination, missing page, provider timeout and a full bounded rescan;
- pending -> settled, pending amount change, pending disappearance and settled replacement ID;
- identical same-day purchases, refunds, chargebacks and reversals;
- transfer pairs across accounts, one-sided transfer and ambiguous match;
- NZD/AUD/USD and zero-, two- and three-decimal currencies, fractional crypto quantities and high-precision FX;
- timezone offsets, UTC boundaries, daylight-saving changes and effective dates;
- stale account balance, available-vs-current balance and ledger/provider discrepancy;
- deterministic replay, per-currency debit/credit balance and correction without deletion;
- backup, restore preview, atomic restore, encryption-key rotation and secret-free export.

Required properties: import replay is idempotent; no incomplete fetch can create a deletion; posted journal history is never silently overwritten; decimal values round-trip exactly; journal entries balance; a rebuild reproduces the same projections.

### 19.5 Build-vs-reuse recommendation

Build the source-observation registry, reconciliation engine and journal as IDEAL-owned modules. Reuse only small, licence-compatible provider/parser libraries after a pinned-version audit. Do not adopt a distributed ledger database or an external personal-finance app as the source of truth.

A staged future path, subject to owner approval and phase gates:
1. Complete Phase 02 contracts and ADRs.
2. Later, if separately authorised, implement synthetic fixtures and pure domain tests.
3. Add manual accounts and file imports before any live bank adapter.
4. Evaluate Akahu only after written provider confirmation and an explicit account-connection approval.
5. Add budgets, bills, goals, valuations and consolidated read-only net worth as separate modules/projections.

This recommendation does not accept D-017, unlock Phase 03, select a provider, authorise implementation or permit real financial data.


## 20. Proposed New Zealand tax intelligence domain — 17 November 2026

### 20.1 Concept and feasibility

A dedicated Tax Intelligence and Tax Accounting bounded context is a viable future IDEAL capability. It should consume verified financial events from the separately governed trading, investment and personal-finance domains; calculate and explain tax estimates under versioned New Zealand rules; maintain evidence and reconciliation; and publish tax provisions and payment obligations into Personal Finance.

Tax must not be embedded inside a trading strategy or execution engine. It must not alter trades, positions or accounting records. Its outputs should distinguish:
- calculated estimate / forecast;
- reviewed tax workpaper;
- return prepared but not submitted;
- return submitted and acknowledged;
- IRD assessment / assessed balance;
- payment initiated, pending, confirmed or reconciled.

A calculated estimate is not an IRD-assessed tax debt. Personal Finance should label estimated provisions separately from assessed liabilities.

### 20.2 New Zealand tax complexity: separate instrument tax treatments

Do not apply one generic "crypto tax rate" to every event.

- **Spot cryptoassets:** IRD treats cryptoassets as property. Tax treatment depends on characteristics and use, not the asset label. Amounts from selling, trading or exchanging are generally taxable in many common circumstances; NZD valuation, income and expenses, purpose and activity facts matter. Cryptoassets are generally excepted financial arrangements, except those economically equivalent to debt arrangements. Trading-stock treatment may apply where relevant.
- **Crypto perpetual futures and derivatives:** do not assume spot-crypto guidance automatically determines derivative treatment. IRD material identifies futures contracts as financial arrangements, and the financial-arrangements rules may require accrual spreading and a base-price adjustment. The legal classification of a specific offshore crypto perpetual swap, settlement asset, funding payment, fee, collateral movement and close-out must be researched separately. This is a mandatory specialist tax review item before the engine can produce filing-grade results.
- **Equities and offshore funds:** share and foreign investment fund (FIF) rules can apply. FIF income can arise without cash being received and several calculation methods exist. Do not implement a single default method without establishing residence, transitional-residence status, exemptions, holdings and elections.
- **Other income and assets:** interest, dividends, staking/mining rewards, foreign exchange, lending, airdrops, fees and business income require distinct event classifications and evidence.

IRD sources reviewed:
- https://www.ird.govt.nz/crypto-currency
- https://www.ird.govt.nz/cryptoassets/taxing
- https://www.ird.govt.nz/cryptoassets/individual/buying-selling
- https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-income/interest-and-dividends/financial-arrangements-rules
- https://www.ird.govt.nz/fif
- https://www.ird.govt.nz/-/media/project/ir/home/documents/forms-and-guides/ir1---ir99/ir3g/ir3g-2024.pdf

The 2026–27 annual rates/FIF bill was introduced on 10 September 2026 and was at Select Committee stage in the IRD Tax Policy page snapshot inspected. A proposal to change FIF settings is not enacted law. Rule packs must track enacted effective dates, not draft bills or press summaries. https://www.taxpolicy.ird.govt.nz/bills/2026-fbt-simplification-tax-bill

### 20.3 IRD integration: capability versus permission

IRD publishes Gateway Services for software providers:
- Income tax return service: prepopulate, submit new/amended returns, retrieve return/status/filing obligation and copies of filed returns.
- Income service: retrieve income information reported to IRD for reconciliation.
- Transaction Data Services: retrieve tax financial/transaction data under the documented models.
- Account API: retrieve customer account metadata for appropriately authorised users.
- Gateway services documentation describes OAuth authorisation with user consent and, depending on deployment, additional TLS/client-certificate security.

Crucial constraints:
- Gateway Services Terms of Use IR1269 (February 2026) require registration and IRD approval before use, followed by developer-portal integration, testing and production onboarding.
- IRD performs due diligence and security assessment, including an Operational Security Framework questionnaire. Approval is not automatic.
- IRD documentation permits software to be provided in-house by a client organisation, but it is not yet established that IDEAL's exact private single-user arrangement will be approved. Obtain written clarification before committing to the integration.
- Gateway terms impose confidentiality, security, privacy, consent, audit and notification obligations and restrict changes in approved purpose/use.
- The public payment guidance describes internet banking, myIR direct debit and other payment routes. No public IRD gateway operation for initiating an individual tax payment was identified in this research. Do not assume return-filing APIs imply a payment API.
- The documented "transfer requests" in the income tax return service are tax-account transfer requests, not a general bank-payment initiation API.

Sources:
- https://www.ird.govt.nz/topics/intermediaries/gateway-services
- https://www.ird.govt.nz/digital-service-providers/services-catalogue/returns-and-information/income-tax
- https://www.ird.govt.nz/digital-service-providers/services-catalogue/customer-and-account/income
- https://www.ird.govt.nz/digital-service-providers/services-catalogue/transaction-data-services
- https://www.ird.govt.nz/digital-service-providers/services-catalogue/customer-and-account/customer-services-suite/account-api
- https://www.ird.govt.nz/digital-service-providers/getting-started
- https://www.ird.govt.nz/-/media/project/ir/home/documents/forms-and-guides/ir1200---ir1299/ir1269/gateway-services-terms-of-use.pdf
- https://www.ird.govt.nz/managing-my-tax/make-a-payment/ways-of-paying
- https://www.ird.govt.nz/managing-my-tax/make-a-payment/ways-of-paying/internet-banking

### 20.4 Proposed tax architecture

Financial domain event feeds -> Tax evidence and classification registry -> Versioned tax rule engine -> Tax workpapers and estimates -> Human review/approval -> Tax return package / approved IRD gateway adapter -> IRD acknowledgements and assessments -> Personal Finance tax provision and payment reconciliation.

Tax calculation modules should be separated by regime and asset/event class:
1. Spot crypto property disposals and income.
2. Derivatives/financial arrangements, including perpetuals, only after specialist rule interpretation.
3. Shares, dividends and FIF calculations.
4. Interest, foreign income, withholding and FX.
5. Fees, expenses, adjustments, losses and other income.

Each calculation needs provenance: source event IDs, evidence, exchange rates and source/time, tax year, residence assumptions, classification, applicable legislation/guidance version, method/election, calculation version, exceptions, reviewer and approval. Rule packs must be effective-dated and old calculations reproducible under the exact historical rule version.

### 20.5 Personal Finance interface

Tax domain publishes:
- estimated current-year tax provision (clearly marked estimate);
- reviewed tax provision;
- IRD-assessed amount and balance (where retrieved and authorised);
- due dates and provisional-tax schedule;
- amount reserved in cash;
- payment instructions/reference and payment status;
- submitted return/acknowledgement/assessment references.

Personal Finance owns the cash movement and payment reconciliation. Tax owns the calculation and obligation evidence. The tax engine must never initiate a bank payment automatically.

### 20.6 Payment workflow recommendation

Phase the capability:
- Initial: show tax reserve target, due date, tax type, period, amount and IRD payment reference details; link to IRD/myIR or display the bank's official Pay IRD instructions.
- Later: if a compliant payment initiation mechanism is available, create a payment instruction only after explicit user confirmation, with amount/payee/reference rendered for review.
- Final reconciliation: mark paid only after bank evidence or IRD account data confirms it. A click or browser redirect is not proof of payment.

IRD currently documents payment through internet banking, myIR direct debit and other methods. It advises using bank "Pay Tax"/"Pay IRD" functionality and requires the correct IRD number, tax/payment type and period. No public payment-initiation endpoint was found in this research. https://www.ird.govt.nz/managing-my-tax/make-a-payment/ways-of-paying

### 20.7 Safety and acceptance requirements

- Tax estimates are not tax advice or an assessment; show confidence, unresolved classifications and material assumptions.
- No filing without a reviewed, locked workpaper and explicit final approval.
- No tax payment without explicit amount/payee/reference confirmation and bank/IRD confirmation.
- No unsupported tax classification silently defaults to zero tax or a generic rate.
- Preserve gross proceeds, cost, fees, funding, settlement, collateral, FX, dates and source references separately.
- Never equate unrealised PnL, wallet transfers, collateral movements or deposits with taxable income without a rule-supported classification.
- Support amended returns and reproducible prior-year calculations.
- Include independent test vectors reviewed by a NZ tax professional, tax-year boundary tests, rounding tests, FX provenance, missing-data and correction tests.
- Encrypt taxpayer records, minimise retention, implement access controls, secure backups and audit every rule change, calculation, review, submission and payment status transition.

### 20.8 Disposition

Add a proposed Tax Intelligence and Tax Accounting domain to future scope, with a downstream interface into Personal Finance. Treat IRD filing as a conditional later integration subject to approval. Treat direct payment initiation as unconfirmed and out of scope until a supported mechanism and authorisation path are verified.

This is a research proposal only. It does not accept D-017, approve a new tax decision, authorise code or dependencies, permit IRD account linking, filing, payment or hosting, or unlock any phase.


## 21. User-controlled tax awareness and capital autonomy (17 November 2026)

The owner explicitly rejects a mandatory tax reserve or any mechanism that makes funds unavailable. IDEAL must calculate and display tax estimates and may display a recommended reserve as an informational accounting designation, but it must not:
- lock, escrow, ring-fence or technically segregate the user's money;
- deduct a percentage from income, deposits, realised PnL or investment proceeds;
- prevent or limit trading, spot accumulation, stock investing, hedging or withdrawals because an estimate is unpaid;
- automatically initiate tax payments or silently move funds.

The user may choose to deploy funds shown as a recommended reserve. IDEAL should then update available-balance views and estimated tax coverage/shortfall, explain relevant tax obligations and deadlines, and record the user's decision only where useful and authorised. It must not moralise or obstruct. A tax estimate is not an IRD assessment; a recommended reserve is not money held by IDEAL; software permission is not a statement about legal tax obligations.

Tax Intelligence remains responsible for calculations, classifications, provenance and due-date estimates. Personal Finance remains responsible for representing actual cash movements and confirmed payments. No automatic payment or custody function is implied. This owner clarification is accepted as D-018 and applies across IDEAL, not only the Personal Finance domain.


## 22. Current provider, privacy and NZ tax update — 17 November 2026

### 22.1 Akahu Personal App versus full-app accreditation

A fresh read of Akahu's official developer documentation clarifies the boundary:
- Personal App is free and restricted to one user (the owner's own Akahu account); ongoing account information only; no payments or webhooks; daily scheduled refresh; one-hour manual refresh rest period.
- Creating a Personal App requires an Akahu profile, account connection, developer terms, identity verification and MFA. Advanced settings support IPv4 IP allowlisting, immediate user-token rotation and deletion/revocation of the app.
- Akahu's App Accreditation guide is expressly for enduring connectivity/full apps. It requires a privacy notice, consumer information page, security and penetration testing, application review, server-validated MFA, credential protection, account-access revocation handling, inactive-account alerts and data deletion when no longer reasonably required. First application review is free; subsequent review after the first may cost NZ$1,000.

**Correction/clarification to earlier disposition:** Akahu Personal App is not equivalent to a production full app. It remains a plausible low-cost private one-user research path, but daily/no-webhook freshness is not real-time and its current terms/topology suitability must be confirmed. A full app's Tier 2 enduring account-information accreditation is a separate path with materially greater security and review burden. Do not assume full-app accreditation is automatically required for Personal App use or that a private app is exempt from all provider terms. No provider path is selected or authorised.

Sources:
- https://developers.akahu.nz/docs/personal-apps
- https://developers.akahu.nz/docs/personal-apps-advanced
- https://developers.akahu.nz/docs/app-accreditation
- https://developers.akahu.nz/docs/data-refreshes

### 22.2 New Zealand Privacy Act position

The current legislation includes a personal/domestic affairs exception in section 27 for an individual, subject to conditions and a highly-offensive exception. It is not a blanket exemption for every processor in the system. Third-party providers and agencies retain their own obligations and contractual controls. Architecture should still follow minimisation, purpose limitation, correction, security, retention, access/export and secure deletion. Cross-border processing needs a separate assessment.

Sources:
- https://www.legislation.govt.nz/act/public/2025/53/en/latest/sections/LMS899135/LMS23347/
- https://www.privacy.org.nz/privacy-principles/5/
- https://www.privacy.org.nz/privacy-principles/9/
- https://www.privacy.org.nz/privacy-principles/12/

### 22.3 CARF and crypto-derivative tax classification

IRD's CARF guidance states that New Zealand-connected Reporting Crypto-Asset Service Providers must collect/report from 1 April 2026; the first reporting period ends 31 March 2027 and the first report is due 30 June 2027. IRD states that users do not register for CARF; RCASPs report. CARF reporting is a tax-information visibility regime, not itself a tax charge or a determination of taxable income. IRD's description excludes persons merely trading cryptoassets for their own benefit from being an RCASP, but the role of any counterparty/platform must be assessed separately.

The official IRD cryptoasset overview says cryptoassets are generally excepted financial arrangements except where economically equivalent to debt arrangements. That does not settle the treatment of a futures/perpetual contract over a cryptoasset. The 2022 officials' report discussed crypto futures under the financial-arrangements rules, but this historical policy material must not be hard-coded as current legal advice. Contract terms, current law, residence and taxpayer facts require specialist interpretation.

The 2026–27 Taxation Bill was introduced 10 September 2026 and IRD Tax Policy records it at select-committee stage as at 12 October 2026. Proposed FIF changes must remain tagged PROPOSED until enactment and commencement are verified.

Sources:
- https://www.ird.govt.nz/international-tax/exchange-of-information/crypto-asset-reporting-framework/crypto-asset-reporting-framework-overview
- https://www.ird.govt.nz/updates/news-folder/2026/what-carf-means-for-crypto-asset-users
- https://www.taxtechnical.ird.govt.nz/overviews/cryptoassets
- https://www.ird.govt.nz/crypto-currency
- https://www.taxpolicy.ird.govt.nz/bills/2026-fbt-simplification-tax-bill
- https://www.taxpolicy.ird.govt.nz/publications/2022/officials-report-2021-taxation-bill

No bank connection, credential, tax filing, payment, legal opinion or provider integration was performed or approved.


## 23. Reconciliation and recovery architecture cross-reference — checkpoint 076

Personal-finance provider rows remain source observations until reconciled into the IDEAL-owned journal. Changed/deleted rows, pending-to-posted transitions, transfer legs, pagination overlap, cursor resets and FX corrections require explicit semantics. Provider balance snapshots must retain refresh time and statement coverage; a difference from journal balance is not automatically a missing transaction.

A provider outage or token revocation must not erase the journal. Historical rows, source entitlement and retention/deletion obligations are distinct. Restore requires verification of the journal, source evidence, encryption/key state, provider authorisation status and reconciliation differences before dependent projections are marked current.

See [Reconciliation, Incident Containment and Verified Recovery Architecture](IDEAL_RECONCILIATION_AND_VERIFIED_RECOVERY_ARCHITECTURE.md). No bank account was connected and no real financial data was used.


## 24. Cross-domain accounting examples — checkpoint 078

Synthetic worked examples now cover bank-to-exchange transfers, pending-to-posted rows, collateral, tax estimates versus owner-designated reserves/assessments/payments, and stale FX. The core rule remains that imported bank rows are observations until reconciled, transfers are not income, pending rows are not final postings, and tax reserves do not restrict capital.

See [Cross-Domain Accounting and Valuation Worked Examples](IDEAL_CROSS_DOMAIN_ACCOUNTING_AND_VALUATION_EXAMPLES.md). No real records or bank integration were used.
