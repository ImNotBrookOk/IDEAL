# 2026-11-17-048-tax-intelligence-and-ird-integration-research

## Scope

Assess the user's proposal to add automated tax calculation/accounting across IDEAL trading and investing activity, feed tax provisions into Personal Finance, and potentially connect to Inland Revenue (IRD) for filing and payment.

## User-visible transcript

**User:** Honestly, we might aswel add automated tax system, for the investing for all the trading....?????? This will be a big help, it then passes this information into the finance section as tax due ??? Its just an idea? Maybe being able to connect directly into IRD so i can pay with a click of a button? Whats your thoughts?

**Assistant:** Recommended a distinct Tax Intelligence and Tax Accounting domain, not tax logic embedded in the trading engine. Its outputs should feed estimated tax provisions and assessed liabilities into Personal Finance. Filing and payment must be separate later capabilities, subject to IRD approval and explicit user confirmation.

## Research conducted

### 1. Acumen brief

Queried current New Zealand IRD APIs, tax filing/payment capabilities and crypto tax guidance. The brief did not return relevant NZ-specific API facts, so the conclusions below rely on official IRD sources.

### 2. Official IRD tax guidance

- IRD says cryptoassets are treated as property and tax treatment depends on characteristics and use, not the asset label. Cryptoassets are generally excepted financial arrangements except those economically equivalent to debt arrangements.
- IRD says amounts from selling, trading or exchanging cryptoassets are taxable in many common individual cases; taxpayers need NZD values and income/expense calculations for IR3.
- IRD identifies trading cryptoassets as a potential business activity based on frequency, effort, organisation, purpose, holding period and investment size.
- IRD's financial-arrangements guidance explains accrual spreading and base-price adjustments. IR3G material identifies futures contracts as financial arrangements. This means crypto perpetuals cannot safely be assigned the same rule pack as spot crypto. Contract-specific analysis is required for the offshore derivative, settlement asset, funding, collateral and close-out.
- IRD's FIF guidance identifies multiple methods and potential income without cash received. A generic equity tax rule is not adequate.
- A 2026–27 annual rates/FIF bill was at Select Committee stage in the IRD Tax Policy page snapshot; proposals must not be treated as enacted law.

### 3. IRD Gateway Services

Official IRD documentation confirms:
- Income tax gateway can submit new/amended returns, retrieve pre-populated information, filing obligations, status and copies of returns.
- Income service retrieves reported income data for a customer/date range for reconciliation.
- Transaction Data Services retrieve tax account financial and transaction data.
- Account API returns account metadata to appropriately authorised users.
- OAuth authorisation redirects the user to myIR for authentication and consent; access tokens have defined lifetimes.
- An application can be provided in-house by a client organisation, but Gateway Services require registration, IRD due diligence, security assessment, approval, developer portal onboarding and successful testing before production.
- Gateway Services Terms IR1269 (February 2026) impose confidentiality, security, Privacy Act, consent, audit and notification obligations and restrict approved purpose changes.
- No public generic payment-initiation API was identified. Public IRD payment guidance describes bank internet banking/Pay IRD, myIR direct debit and other payment routes. Return-service tax-account transfer requests are not a general bank-payment initiation API.

### 4. Sources

- https://www.ird.govt.nz/crypto-currency
- https://www.ird.govt.nz/cryptoassets/taxing
- https://www.ird.govt.nz/cryptoassets/individual/buying-selling
- https://www.ird.govt.nz/cryptoassets/individual/buying-selling/trading
- https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-income/interest-and-dividends/financial-arrangements-rules
- https://www.ird.govt.nz/fif
- https://www.ird.govt.nz/-/media/project/ir/home/documents/forms-and-guides/ir1---ir99/ir3g/ir3g-2024.pdf
- https://www.taxpolicy.ird.govt.nz/bills/2026-fbt-simplification-tax-bill
- https://www.ird.govt.nz/topics/intermediaries/gateway-services
- https://www.ird.govt.nz/digital-service-providers/services-catalogue/returns-and-information/income-tax
- https://www.ird.govt.nz/digital-service-providers/services-catalogue/customer-and-account/income
- https://www.ird.govt.nz/digital-service-providers/services-catalogue/transaction-data-services
- https://www.ird.govt.nz/digital-service-providers/services-catalogue/customer-and-account/customer-services-suite/account-api
- https://www.ird.govt.nz/digital-service-providers/getting-started
- https://www.ird.govt.nz/digital-service-providers/guides-and-docs/manage-access-tokens-for-gateway-services
- https://www.ird.govt.nz/-/media/project/ir/home/documents/forms-and-guides/ir1200---ir1299/ir1269/gateway-services-terms-of-use.pdf
- https://www.ird.govt.nz/managing-my-tax/make-a-payment/ways-of-paying
- https://www.ird.govt.nz/managing-my-tax/make-a-payment/ways-of-paying/internet-banking

## Proposed architecture

Create a Tax Intelligence and Tax Accounting bounded context. It consumes verified events from trading, investing and Personal Finance; classifies them under versioned tax rules; calculates and explains estimates/workpapers; records evidence and reviewer approval; and publishes tax provisions/assessed obligations to Personal Finance.

Separate regimes:
1. Spot crypto property disposals and income.
2. Derivatives/financial arrangements, including perpetual futures, only after specialist interpretation.
3. Equities, dividends and FIF.
4. Interest, foreign income, withholding and FX.
5. Fees, expenses, adjustments, losses and other income.

Personal Finance should distinguish forecast estimate, reviewed provision, IRD assessment, payment pending and confirmed payment. Tax owns calculations/evidence; Personal Finance owns cash movement and payment reconciliation.

No tax filing without a reviewed locked workpaper and explicit approval. No payment without explicit amount/payee/reference confirmation and independent confirmation. No tax result should silently default unsupported classifications to zero or a generic rate.

## Governance and status

- Added F-005 Tax Intelligence and Tax Accounting as Proposed future scope.
- D-001 remains unchanged: active trading scope is crypto perpetual futures.
- D-017 remains Proposed.
- Phase 02 only; Phases 03–19 remain LOCKED.
- No tax rules were implemented, no tax calculations run, no IRD account linked, no return filed, no payment initiated, no code/dependencies changed and no real financial data used.

## Documentation commits

1. docs/PERSONAL_FINANCE_RESEARCH.md section 20
   - Commit: 1f14eb8d3f8a5ca4506b636fa3d6ab08093779d5
   - Blob: c3a0435d80d5f41f3fb0545b1af027d8cb4e1ac5
2. docs/FUTURE_SCOPE_IDEAS.md F-005
   - Commit: 9510788c6a1d90635ecd4155907da61954f700fb
   - Blob: 60f3bcad1de1dcc0e527a15754d8c70fc6302f82
3. ROADMAP.md Phase 02 checkpoint
   - Commit: b9386b7ba8ea643a597f08d1d451015c5dbb52ee
   - Blob: 1cea7a6838132edb47e6cffd3a97a2452ee71628
4. Conversation index
   - Commit: 4601316524cf5b18401120426902f24905bb1d23
   - Blob: 2447f51eee3b36ad34f665fff519a7c8cfcf259e

Fetch-back verification to follow.


## Fetch-back verification addendum

Fetched all five changed files from GitHub main after commits. Verified tax research section 20, F-005 Proposed, Phase 02-only roadmap checkpoint, Phases 03–19 LOCKED, checkpoint index entry, and this complete research record. No code, dependencies, accounts, filing or payments changed.
