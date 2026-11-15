# IDEAL Conversation Record 011 — Missing FX Conversion at Funding Settlement

**Date:** 16 November 2026  
**Scope:** Phase 01 funding research — missing FX conversion from inverse BTC-settled position to USD account base  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #17 merged; 56 tests pass on final PR head. Research only.

## Available user-visible transcript

### User
> Ok keep going

### Assistant
Continued funding settlement research. The no-mark/no-top-of-book failure was already reproduced. The remaining funding gap was conversion from the position's settlement currency into the account base currency. An inverse BTC-settled position in a USD account requires a BTC/USD conversion rate at funding settlement.

## Operational audit log

### 1. Source audit

Inspected pinned NautilusTrader `v2.0.0rc9`:

- `crates/backtest/src/exchange.rs`: funding settlement calls account-currency conversion when position settlement currency differs from account base currency.
- `crates/common/src/cache/mod.rs`: `try_get_xrate` builds a currency-pair graph from cached quote ticks for instruments on the venue. The graph is used to derive the conversion path.
- `crates/common/src/xrate.rs`: direct and multi-hop pair conversion graph; requires a connected, valid quote path.

### 2. Test design and important failed approaches

Added `research/nautilus_poc/test_funding_fx_conversion.py`.

First approach used the BTCUSD inverse perpetual itself. This supplied a BTC/USD quote path, so it did not represent missing conversion. Changing to BTCJPY removed the direct pair, but further issues had to be resolved:

- Without any BTC/USD conversion at order entry, the risk engine denied the order before a position existed: `Account currency conversion failed: No exchange rate from BTC to USD`.
- The first replay did not advance past the funding boundary, so no settlement was attempted.
- A BTCUSD inverse instrument still supplied its own conversion path; it was replaced with BTCJPY.
- A temporary BTC/USD spot quote was then added to permit entry, and purged from the cache after the BTCJPY position filled.
- A valid BTCJPY mark price was retained for settlement valuation, separating missing FX conversion from missing settlement price.
- A later ETH/USD quote was supplied after the boundary to advance the replay. ETH/USD does not connect BTC to USD.

The final fixture:
1. Opens an inverse BTCJPY perpetual (settlement BTC) in a USD-base account.
2. Supplies temporary BTC/USD spot quote data for entry risk validation.
3. Purges the BTC/USD instrument from cache after the BTCJPY position fills.
4. Supplies a BTCJPY mark price, so settlement valuation has a price.
5. Clears the BTCJPY L2 book and advances past the funding boundary.
6. Asserts the fatal funding settlement error and that the position remains open.

This isolates the FX-conversion failure: mark-price valuation exists, but the account conversion graph has no BTC/USD path.

### 3. CI history and corrections

- First attempt: 1 failure, 55 passed. A venue-wide L2 configuration required book data for the ETHUSD trigger instrument; added its L2 book.
- Next attempt: no funding error because the BTCUSD instrument still provided a conversion path.
- A BTCJPY instrument was introduced to avoid self-conversion.
- Another run did not reach settlement because no later event advanced time; a later trigger quote was added.
- An additional attempt was rejected at order entry because no FX quote existed. A temporary BTC/USD quote was added and purged after entry.
- Final test-only suite [CI run 43754511937](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43754511937): **56 passed in 0.20s**.
- Documentation updated in roadmap, POC README and execution realism report.
- Final PR-head CI [run 43754599641](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43754599641): **56 passed in 0.23s**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 / Python 3.14.

### 4. Five-axis review and merge

- **Correctness:** the fixture separates entry risk conversion, funding valuation mark and settlement FX conversion; fatal error is asserted at the boundary.
- **Security:** synthetic data only; no secrets, external calls or production code.
- **Cost:** no dependency or paid service.
- **Maintainability:** standalone test with explicit conversion source lifecycle and comments.
- **Scope:** four files changed: roadmap, POC README, execution realism report and the new FX test.
- Final PR head `25d2da88dbcc2f9a71359c09e26da230a53520fa` matched the branch ref before merge.
- [PR #17](https://github.com/ImNotBrookOk/IDEAL/pull/17) squash-merged under D-012.
- Merge commit: `624eb9bbb54b7bac7e06ddbd624af417b3380053`.

## Documentation updated

- [Roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md): FX conversion failure now covered; explicit replay recovery remains open.
- [POC README](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/README.md): records the missing-FX test and limitations.
- [Execution realism report](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md): test design, source semantics, failure history and evidence.

## Remaining funding work

- Explicit recovery by creating a fresh deterministic replay with corrected FX data remains untested.
- A same-engine reset/replay path remains untested.
- Multi-currency account behavior and mixed settlement currencies remain untested.
- Existing coverage now includes missing mark fallback, no mark/no book fatal failure, two same-currency positions, duplicate update idempotency and missing FX conversion at settlement.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- Isolated POC suite: 56 passing tests.
- No runtime code, dependencies, exchange adapter, credentials, account, testnet, paper/live trading or paid service added.
