# IDEAL Cross-Domain Accounting and Valuation Worked Examples

**Status:** Phase 02 design fixtures; illustrative only, not accounting advice or owner policy  
**Checkpoint:** 078 — 17 November 2026  
**Scope:** Cross-domain transaction flows, cash/asset/derivative separation, FX, collateral, tax estimates and portfolio projection semantics  
**Boundary:** Synthetic values only. No user financial data, account access, provider connection, payment, tax filing, execution or implementation.

## 1. Purpose

The integrated system must be able to show a coherent capital picture without double-counting balances, confusing transfers with income, treating derivative notional as an owned asset, or converting estimates into restrictions. These examples test the conceptual contracts across Personal Finance, trading/investment domains, Tax Intelligence, Data Integrity and Portfolio & Capital View.

All amounts and prices are synthetic. The examples do not set a risk limit, tax treatment, valuation convention or accounting policy.

## 2. Scenario A — bank cash transferred to an exchange

**Assumptions:** Owner transfers NZD 5,000 from a bank account to an exchange wallet. Bank charges NZD 2.50. Exchange credits USD 3,000 after FX conversion; illustrative conversion rate and provider fees are represented separately.

| Event | Personal Finance journal | Exchange/account view | Portfolio view |
|---|---|---|---|
| Bank transfer initiated | Pending outflow NZD 5,000; not yet posted | No credited exchange asset yet | Show pending transfer separately; do not count as settled exchange cash |
| Bank debit posts | Bank cash decreases NZD 5,002.50 including fee | Still pending until exchange confirms receipt | Economic value decreases only by fee/FX cost once external transfer completes |
| Exchange credit confirms | Record transfer leg / in-transit clearing reconciliation | Exchange wallet increases USD 3,000 | Reclassify asset from bank cash to exchange wallet, convert using evidenced FX; avoid counting both legs as separate wealth |
| Reconciliation closes | Match bank debit, fee and transfer reference | Match deposit/credit and conversion | Close in-transit balance; retain FX spread/fee evidence |

**Invariants**
- A transfer is not income or profit.
- Pending and posted legs are not counted as two assets.
- Fee and FX difference are separate economic effects.
- The exchange credit is not current until source evidence confirms it.
- Bank statement and exchange history remain independent evidence sources.

## 3. Scenario B — crypto spot asset and perpetual position on the same underlying

**Assumptions:** Synthetic BTC reference price NZD 100,000. Owner holds 0.10 BTC spot and separately has a linear BTC perpetual long with 0.10 BTC-equivalent contract exposure. Ignore fees/funding for the initial illustration.

| Measure | Spot holding | Perpetual position |
|---|---:|---:|
| Owned asset market value | NZD 10,000 | Not an owned BTC asset |
| Gross market exposure | NZD 10,000 | NZD 10,000 notional |
| Economic equity contribution | NZD 10,000 before liabilities/valuation haircut | Derivative mark-to-market P&L, notional is not added to net worth as an asset |
| Margin/collateral | Not assumed to be margin | Separate venue/account-specific collateral and margin state |
| Risk reporting | Spot price/custody/liquidity exposure | Derivative directional, leverage, funding, margin and liquidation exposure |

The portfolio view may report NZD 20,000 gross directional exposure and NZD 20,000 long BTC-equivalent exposure for this simplified example, while economic net worth includes the spot asset and derivative mark-to-market only. It must not add the perpetual notional to net worth.

**Invariants**
- Notional is exposure, not asset value.
- Spot and derivative risks remain separate even when their underlying is the same.
- Derivative collateral is not a second copy of the spot asset unless a documented account-level collateral relationship proves it.
- A future hedge/netting model must be explicit; this example has two long exposures, not a hedge.

## 4. Scenario C — derivative funding, fees and mark-to-market

**Assumptions:** A synthetic perpetual position pays NZD-equivalent funding of 12 and incurs an exchange fee of 4 during a period. Unrealised mark-to-market P&L at the end is +80.

| Component | Amount | Treatment in the model |
|---|---:|---|
| Unrealised mark-to-market | +80 | Valuation projection, time-varying and source-dependent |
| Funding payment | -12 | Separate settled/posted cashflow event when confirmed |
| Trading fee | -4 | Separate fee event when confirmed |
| Net economic change (illustrative) | +64 | Derived view, with components retained separately |

Do not record +80 as a cash receipt. Do not also include -12/-4 in both the account ledger and a duplicate P&L adjustment. When the venue posts a settlement/funding event, reconcile it once against the venue ledger and the IDEAL event journal.

**Invariants**
- Realised cashflows and unrealised valuations are separate.
- Funding estimates and actual funding settlements are separate.
- Venue settlement evidence outranks an internal estimate for the external cash event.
- Historical results retain the funding rate/schedule, event time, settlement currency and source.

## 5. Scenario D — collateral posted and encumbered

**Assumptions:** Owner transfers 0.05 BTC from a free exchange wallet to a derivatives collateral subaccount. Synthetic BTC price is NZD 100,000, so gross market value is NZD 5,000 before haircut.

| View | Before | After |
|---|---:|---:|
| Total BTC owned within exchange | 0.05 BTC | 0.05 BTC |
| Free BTC | 0.05 BTC | 0 BTC |
| Encumbered collateral | 0 BTC | 0.05 BTC |
| Economic asset value | NZD 5,000 | NZD 5,000 before valuation/haircut |
| Available margin | Venue-specific | Venue-specific; cannot infer from nominal market value |

This is an internal account/collateral reclassification, not income, profit or an increase in total wealth. Risk-adjusted collateral value may be lower due to venue haircut, concentration, liquidity and stress assumptions. If the collateral is held under a separate legal or custody arrangement, ownership and counterparty exposure must be represented accordingly.

**Invariants**
- Encumbered collateral remains an asset only to the extent ownership and recoverability are established.
- Free balance and collateral balance cannot both include the same units.
- Venue margin equity and IDEAL risk-adjusted equity are distinct.
- Collateral is not assumed portable across venues/accounts.

## 6. Scenario E — pending bank transaction becomes posted

**Assumptions:** A NZD 120 card purchase first appears as pending and later posts with final amount NZD 123.

1. Import the pending observation with its source status and timestamp.
2. Do not post it as a final expense and then post a second expense when the final row appears.
3. Match the posted row to the pending observation using provider identifiers and documented semantics.
4. Create a revision/reconciliation event showing amount changed from 120 to 123.
5. Post the final journal amount once, retaining both source observations and the reason for the change.
6. If the provider replaces IDs or provides no stable relation, keep an explicit reconciliation case for review rather than guessing.

**Invariants**
- Pending is not posted.
- The same economic transaction is not counted twice.
- Original and final source evidence remain available.
- A missing pending row is not treated as deletion unless source semantics establish that.

## 7. Scenario F — tax estimate, owner-designated reserve and actual payment

**Assumptions:** IDEAL calculates a synthetic estimated tax amount of NZD 2,000. Owner chooses to label NZD 1,000 as a planning reserve, then later spends NZD 600 of that cash. No actual payment has yet been made.

| State | Tax Intelligence | Personal Finance | Owner capital |
|---|---|---|---|
| Estimate calculated | Estimated liability NZD 2,000 with assumptions/confidence | Informational projection only | All funds remain accessible |
| Owner designates NZD 1,000 | Estimate unchanged; designation is not a tax payment | Optional planning label | No lock, escrow, segregation or restriction |
| Owner spends NZD 600 | Update reserve coverage/shortfall display; no punitive action | Record actual cash expense | Owner retains control; IDEAL does not block spending |
| IRD assessment arrives | Record assessed amount/status separately from estimate | Project assessment as a liability/obligation according to reviewed accounting policy | No automatic reserve lock |
| Payment is confirmed | Mark payment only from bank/IRD evidence | Record actual cash outflow and reconcile | No payment is initiated by IDEAL without separate explicit approval |

**Invariants**
- Estimate, owner designation, assessed liability and confirmed payment are four different facts.
- A planning reserve is not cash held by IDEAL.
- D-018 prohibits mandatory lock, deduction, segregation or forced payment.
- A click, payment instruction or browser redirect is not payment confirmation.

## 8. Scenario G — stale or missing FX conversion

**Assumptions:** Portfolio view combines NZD bank cash, USD exchange wallet and a EUR-denominated ETF. The USD/NZD rate is current; the EUR/NZD rate is stale beyond the future consumer threshold.

The portfolio view must:
- show NZD and USD amounts in their native currencies;
- show the source/time/method for the valid USD conversion;
- mark EUR exposure and any total requiring EUR conversion as stale/incomplete;
- not use zero, a silent last-known value or an unlabelled estimate;
- retain partial totals and explicitly state excluded/unknown amounts.

No all-up net-worth figure may be presented as complete when material components lack usable FX evidence.

## 9. Scenario H — portfolio projection after a source correction

A venue corrects a historical funding event after an earlier risk snapshot and backtest were created.

- Preserve original raw observation and the corrected observation.
- Record source publication/availability time and IDEAL receipt time for the correction.
- Keep the original decision's as-known-then evidence snapshot unchanged.
- Recompute a latest-corrected projection under a new version.
- Invalidate affected later calculations only where lineage proves they depend on the corrected fact.
- Do not rewrite an earlier backtest as if the corrected funding value was available at the time.

This separates historical reproducibility from current best-known truth.

## 10. Scenario I — tax law changes after a calculation

A tax rule is published on one date, enacted on another and effective for a tax year that may differ from both.

The Tax Intelligence context must record:
- source type and authority (Act, bill, binding ruling, public guidance, issues paper or non-binding technical summary);
- publication, enactment, commencement and effective dates;
- applicable tax year and transitional rules;
- rule version used for the original calculation;
- current rule version and any recalculation/reassessment;
- reviewer and unresolved interpretation.

A bill or consultation paper must not silently become an enacted rule. Previous workpapers remain reproducible under their original version.

## 11. Scenario J — data completeness versus consolidated capital confidence

One provider returns a valid account snapshot but another connected domain has stale positions. The portfolio view can show a partial subtotal, but must mark the overall projection incomplete and identify the missing scope. It cannot infer that missing positions equal zero or that all capital is available.

## 12. Acceptance criteria for future synthetic fixtures

Every worked example should become deterministic synthetic fixtures before any runtime design is approved. Tests must assert:
- no double-counting of transfer legs, pending/posting states, collateral or derivative notional;
- all values carry currency, units, source, ownership and valuation/observation time;
- event-time and knowledge-time queries return different correct views after a late correction;
- tax estimates never create a capital restriction or payment side effect;
- portfolio totals disclose stale/missing FX and excluded scopes;
- reconciled external facts update the correct domain without mutating another domain's ledger;
- all corrections and derived recalculations retain provenance and audit references.

No synthetic fixture tests were executed as part of this checkpoint.

## 13. Disposition

These examples make cross-domain accounting and valuation assumptions explicit enough for review, but they do not establish a final chart of accounts, tax treatment, valuation policy, FX source, portfolio risk model or accounting standard. They are illustrative design tests only.

Phase 02 remains active; Phases 03–19 remain locked. No implementation, provider integration, real records, financial action or execution is authorised.


## Canonical asset identity for worked examples — checkpoint 093

The synthetic labels NZD, USD, BTC and USDT in these examples are display labels only. A future implementation must bind each amount to a canonical AssetId: NZD/USD to their fiat identities; BTC to the native asset identity; USDT to a distinct stablecoin identity on its specific network/contract where relevant. No ticker-only identity, stablecoin par assumption or implicit 1:1 conversion is permitted. All conversion and valuation examples require explicit source, side, timestamp, spread/haircut and completeness. See [Critical Contract Field Schemas](IDEAL_CRITICAL_CONTRACT_FIELD_SCHEMAS.md).
