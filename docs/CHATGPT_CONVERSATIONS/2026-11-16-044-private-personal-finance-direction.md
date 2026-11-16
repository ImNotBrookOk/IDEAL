# 2026-11-16-044 — Private personal finance platform direction

## Status
Owner confirms a personal-use-first direction for IDEAL's future financial system. D-017 is recorded as Proposed, not Accepted. This is Phase 02 architecture research only. No runtime implementation, account connection, credential use, payment initiation, hosting choice or public release is authorised.

## Available conversation transcript

### User
> Without making it more complicated... But one last part... why not be able to connect to my bank or manually, and be able to handle all my budgeting also so it is an all in one portfolio/investing/budgeting platform build for me to use to get my finances right, track everything and make money all in one??? Heres an example... do not take this as fact and I want to know what you think, but to me looking long term and being compliant and law abiding. This would be valuable for any user ...
> https://github.com/letehaha/moneymatter
> Im not saying this is the only source to look at on github, but it is an idea. What do you think?

### Assistant — initial assessment
> I think this is a strong idea, and I would seriously consider it as part of IDEAL's long-term direction.
>
> The important distinction is that we should not turn IDEAL into one enormous application where budgeting, banking, investing and trading are all tangled together. We should build one personal financial platform, with separate, well-governed engines that work together.
>
> That could give a user one place to understand income, spending, liabilities, assets, bank balances, bills, budgets, cash flow, savings goals, investments, net worth, performance, risk and reasonable savings/investment capacity.
>
> Include bank connectivity and manual entry as first-class capabilities. Keep tracking money, recommending what to do with it, and actually moving or investing it as different permission and regulatory boundaries.

### Assistant — MoneyMatter assessment and architecture
> MoneyMatter is a good example of the personal finance layer. Its feature set includes manual and connected bank accounts, transaction categorisation, budgets, bills, subscriptions, loans, investments, net worth, multi-currency reporting, imports/exports and AI-assisted categorisation. Its stack is Vue/TypeScript, Node/Express, PostgreSQL and Redis.
>
> Study it for budgeting workflows, account aggregation, transaction handling and mobile usability. Do not assume its architecture or financial data model is sufficient for IDEAL's investment, trading, accounting and risk requirements.
>
> Its AGPL-3.0 licence creates obligations if code is incorporated or modified, particularly in a network-hosted service. Treat it as a reference implementation initially, not a dependency.
>
> Proposed platform domains: personal finance/budgeting; wealth/investment portfolio; intelligence/financial planning; controlled actions. Start with read-only bank access. Payment initiation and investment execution are separate capabilities.
>
> New Zealand compliance boundaries include privacy/data protection, CDR accreditation and the distinction between budgeting information and regulated personalised financial advice.

### User
> Yes I like the idea of helping others but there are so many loopholes to jump through and licences to get etc. This for now is just for me. Not to say later if proving to be an amazing software we could look into opening it up to others as their personal platform. So maybe we keep that at the back of our minds but definitely add the financial system, find best path, safe, audit able, honest, data conscious, documented every step, every thought and every action taken so an audit trail will protect us. But I do love this idea. And eventually if built right this can go on a live server and log in through a web app or whatever... but for now you know the goals, roadmap. Lets see what is viable and what isnt for us.

### Assistant — clarified direction
> IDEAL is a private, single-user financial platform first. We can keep the possibility of opening it to other people in the architecture, but we should not build around public-user licensing, onboarding, support or commercial compliance today.
>
> For your own use, we can investigate existing personal-finance software, manual imports and personal bank-data access without immediately taking on the obligations of operating a financial-data service for the public. It does not remove the need to protect your data or follow provider terms, but it avoids solving problems we do not yet have.
>
> The audit trail must record what the system did, what data it relied on, why it reached a conclusion, and who authorised any action. It cannot record hidden internal reasoning, but it can preserve the evidence and decision rationale needed to reconstruct events.

## Research performed

### MoneyMatter
- Repository: https://github.com/letehaha/moneymatter
- README describes account aggregation, transactions, categories, budgets, bills, subscriptions, loans, investments, net worth, imports/exports, multi-currency reporting, AI support, self-hosting and backups.
- Stack shown in README: Vue 3/Vite/TypeScript/Tailwind; Node/Express; Sequelize; PostgreSQL; Redis/BullMQ; better-auth; Docker.
- Licence: AGPL-3.0; README states pre-relicensing versions were CC BY-NC-SA 4.0. Exact relicensing boundary must be checked before any reuse.
- GitHub search snapshot: 227 stars, 90 forks. These are discovery signals only.
- Release v0.33.6 (29 Oct 2026) adds NZ bank sync through Akahu and instructs users to create a Personal App and supply App Token/User Token. v0.33.7 is the next listed release (30 Oct 2026).
- Initial disposition: strong reference and isolated trial candidate; not adopted, no code copied.

### Akahu and NZ open banking
- Akahu Personal Apps documentation says free, restricted to one user's own Akahu account, ongoing connectivity only, account information yes, payments no, webhooks no, daily scheduled refresh, manual refresh subject to a one-hour rest period.
- Akahu accreditation documentation classifies Personal Apps as Tier 0. It separately classifies ongoing account information for personal finance/budgeting as Tier 2 for full apps, requiring a full app review. Personal Apps are not a multi-user production path.
- Akahu's official open-banking transition documentation says it became an accredited intermediary under NZ CDR in December 2025; customers of Akahu need not independently become accredited for that intermediary route, although Akahu's own accreditation process still applies.
- MBIE says accredited requestors can request customer-authorised account/transaction information and instruct payments, subject to their accreditation classes and obligations. IDEAL is not accredited.
- Personal App route is plausible for a private own-account proof of concept, subject to confirming current provider terms and exact applicability. No account or token was created or connected.

### Architecture and controls proposed
- Separate personal-finance domain from investment/trading engines.
- Manual entry and statement imports independent of bank connectivity.
- Native-currency ledger, traceable FX, source provenance, idempotent imports, reconciliation and correction/reversal semantics.
- Consolidated net worth/exposure is a read-only projection; engine ledgers remain authoritative and separate.
- No implicit cash, margin or collateral pooling.
- Read-only bank data first. No payment initiation, automatic transfers or trading authority.
- No public/multi-user service now. Later web hosting is a separate threat-model, security, backup/restore, cost and approval decision.
- AI can classify/explain/propose, not mutate financial truth or authorise actions.
- Audit log records events, data provenance, timestamps, software/model versions, decision rationale, actor and explicit approvals; it does not attempt to store hidden chain-of-thought or unnecessary raw personal data.

## Repository changes

1. DECISIONS.md
   - Added D-017 as Proposed: private single-user personal finance domain; Phase 02 architecture research only; no account connection, credentials, payments, investment execution, public service or paid provider; multi-user is a distant possibility only.
   - Commit: eadbcda6af1ed8cb12728ef2e22b8d8f7c3dd891

2. docs/FUTURE_SCOPE_IDEAS.md
   - Added F-004 with owner direction, architecture boundaries, Akahu preliminary path, feasibility matrix, MoneyMatter reference assessment, safeguards and approval boundary.
   - Commit: 48e0b867fdb9ad3c84430cdc2f3b3049ae54ad1f

3. docs/PERSONAL_FINANCE_RESEARCH.md
   - Created focused research plan, NZ bank access evidence, MoneyMatter assessment, architecture/security boundaries, hosting constraints and research sequence.
   - Commit: 11458763d97c7f1a7e2068c45c0e6cae87984b83

4. ROADMAP.md
   - Added Phase 02 architecture input note; preserved Phase 02-only scope and Phases 03–19 lock.
   - Commit: 01798f35522b5ab997a86a1aa4497cd025e6275e

5. Conversation index update remains pending at time this record was created.

## Sources checked
- MoneyMatter: https://github.com/letehaha/moneymatter
- MoneyMatter releases: https://github.com/letehaha/moneymatter/releases
- MoneyMatter issues: https://github.com/letehaha/moneymatter/issues
- MoneyMatter self-hosting guide: https://github.com/letehaha/moneymatter/tree/dev/self-hosting
- Akahu Personal Apps: https://developers.akahu.nz/docs/personal-apps
- Akahu app accreditation: https://developers.akahu.nz/docs/app-accreditation
- Akahu CDR transition: https://developers.akahu.nz/docs/official-open-banking
- Akahu pricing: https://www.akahu.nz/pricing
- MBIE accredited requestors: https://www.mbie.govt.nz/business-and-employment/business/consumer-data-right/participating-as-a-data-holder-or-accredited-requestor/accredited-requestors
- MBIE CDR standards: https://www.mbie.govt.nz/business-and-employment/business/consumer-data-right/standards-for-the-consumer-data-right

## Current state and next step
- D-017 Proposed; D-001 unchanged.
- Personal finance is a future private-use domain and Phase 02 architecture research input only.
- Phase 02 is architecture/contracts only. Phases 03–19 remain LOCKED.
- No code, dependency, bank connection, credentials, payment capability, provider, host or public product is approved.
- Next step: complete pinned MoneyMatter audit and compare alternative personal finance/ledger projects, then specify the personal-finance domain contracts. Owner approval remains required before any local prototype or bank-account connection.


## Verification addendum — 16 November 2026

- The conversation index was updated after this record was created; its entry is present in docs/CHATGPT_CONVERSATIONS/README.md.
- Fetch-back from main confirmed D-017 is Proposed, D-001 remains accepted and unchanged, F-004 is present, the personal-finance research plan exists, and ROADMAP.md retains Phase 02 architecture/contracts only with Phases 03–19 locked.
- Verified current blob SHAs: DECISIONS.md ec5ce6c80e098607b62cecc67bf0cb2dfbc833c4; docs/FUTURE_SCOPE_IDEAS.md 26e35de2cc4ed2b38b3770fd7bb44dad444bbf2c; docs/PERSONAL_FINANCE_RESEARCH.md 8b54f06d41cdf95ecd8f31721c9984581ed3f634; ROADMAP.md e4a0767ecefccb3ecb6f9a9dd38743402ab8e156; this conversation record 051a13de85af95b782b963e3be4b75c495abe441; conversation index 05c80fdf4cba7bb9b49dddde829b83415985db5c.
- No code, dependencies, credentials, accounts, external services or hosting resources were created or connected. No tests were run because no executable code changed.
