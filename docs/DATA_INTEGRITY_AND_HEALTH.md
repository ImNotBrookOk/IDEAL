# IDEAL Data Integrity, Quality and System Health

**Date:** 17 November 2026  
**Phase:** 02 — architecture/contracts only  
**Status:** Proposed architecture requirements; no runtime implementation authorised  
**Related:** D-019 accepted design principle; F-006 proposed research scope

## 1. Purpose and governing principle

IDEAL's data foundation must be more trustworthy than any strategy, model or engine built on top of it. A sophisticated engine consuming wrong prices, stale order books, missing corporate actions, incorrect FX, incomplete fills or corrupted account state can produce confidently wrong decisions. Data validity is therefore a first-class system safety property.

The goal is not to promise that every source is always live. That is impossible across venue outages, market closures, delayed entitlements, rate limits and provider failures. The goal is to know and expose exactly what is known, how current it is, what is missing, and whether a particular use is safe.

## 2. Scope

This is a shared capability for:
- crypto perpetuals and future crypto spot portfolios;
- future stock/ETF investing and corporate-action processing;
- commodity instruments and cross-asset hedging;
- portfolio-level exposure and risk views;
- Personal Finance and tax evidence;
- future reporting, alerts and research/backtesting.

D-001 remains the only active initial trading scope: crypto perpetual futures. The broader classes are future design/research scope only (D-014/D-016). F-006 is proposed; this document is not implementation approval.

## 3. Data lifecycle and provenance

Proposed pipeline:

1. **Source registry:** record provider/venue, API/feed, instrument identifiers, market/session calendar, data type, entitlement/licence, limits, known coverage and fallback compatibility.
2. **Acquisition adapters:** isolate each external source behind a versioned adapter; record request parameters, response metadata, sequence/cursor and errors without leaking credentials.
3. **Raw observation journal:** preserve received payloads or a privacy-safe canonical evidence form with source ID, source event time, publication time if available, retrieval time, ingest time, adapter version and content hash. Raw and normalised data are distinct.
4. **Normalisation:** deterministic conversion to canonical instruments, units, decimal precision, currency, timestamps and event types. Never erase original source values.
5. **Validation:** run deterministic schema, semantic, temporal, sequence, completeness, precision, range, duplicate and cross-source checks.
6. **Quarantine/reconciliation:** invalid or ambiguous observations are isolated; corrections, cancellations, deletions and replacements are explicit events, not silent overwrites.
7. **Consumption contract:** every downstream consumer declares required fields, acceptable source classes, freshness budget, market-session conditions and failure policy.
8. **Decision lineage:** record the exact observation/version IDs and validation states consumed by each material signal, risk decision, backtest result, simulated/live order (if ever separately authorised), valuation and tax calculation.

## 4. Freshness and quality state model

Do not use a single generic "data is fresh" flag. Freshness is specific to data type, instrument, venue, market session, entitlement and intended use.

Proposed states:
- **LIVE:** source/entitlement is verified for real-time delivery and observation age is within the applicable contract.
- **DELAYED:** source is known to be delayed or the entitlement does not provide real-time data.
- **STALE:** last observation exceeds the applicable freshness budget.
- **INCOMPLETE:** required fields, intervals, sequence ranges or coverage are missing.
- **INVALID:** schema, semantic, precision, timestamp or integrity checks failed.
- **CONFLICTED:** sources disagree beyond a defined tolerance or instrument mapping is ambiguous.
- **UNAVAILABLE:** source or adapter is confirmed unavailable.
- **UNKNOWN:** evidence is insufficient to classify the state.

A value may be numerically present and still be unusable. Every value should carry quality state, observation age and lineage. "Latest available" is not synonymous with "live".

Freshness contracts must be designed separately for:
- streaming trades, quotes, order-book snapshots/deltas and funding/mark/index data;
- historical candles and trades, including gap/coverage validation;
- equities quotes/trades, exchange sessions, auctions, halts and corporate actions;
- FX rates and cross-currency valuation;
- broker positions, balances, orders, fills and statements;
- personal-finance and tax source records, where source update cadence may be daily or periodic.

Market closures must not create false stale alarms; conversely, an open market with a silent feed must not be marked healthy simply because the last timestamp is recent enough under a generic timer. All thresholds remain to be established from actual source contracts and use cases.

## 5. Deterministic validation controls

Candidate controls to specify and test:
- schema and contract version compatibility;
- instrument identity, venue, quote/base/settlement currency and contract multiplier;
- timestamp timezone, monotonicity, future timestamps and clock drift;
- sequence continuity, duplicate events, missing deltas and snapshot rebasing;
- candle interval completeness and OHLC invariants;
- bid/ask ordering, crossed/locked markets and spread/depth sanity;
- trade price/size precision, tick/lot constraints and impossible values;
- funding/mark/index timestamp alignment and settlement coverage;
- FX conversion source, timestamp, direction and precision;
- corporate-action and symbol-change continuity for equities;
- broker/exchange reconciliation of balances, positions, orders and fills;
- data corrections, tombstones, replacement IDs and late-arriving events;
- historical dataset coverage, survivorship/look-ahead leakage and revision tracking;
- content hashes, schema migration, journal continuity and backup integrity.

Checks must be deterministic, version-controlled and reproducible. Statistical anomaly detection may be an additional signal, never the only control for basic validity.

## 6. Independent health supervisor and self-audit

Propose a small deterministic supervisor that observes the system from outside the components it monitors. It must not trust a component's self-reported "healthy" status as sufficient proof.

Monitor at least:
- source connectivity, authentication state (without exposing secrets), entitlement, API quota/rate-limit headroom and adapter error rates;
- feed heartbeat, lag, sequence gaps, stale/incomplete/invalid/conflicted observations;
- clock synchronisation and drift;
- ingestion queues, event backlog, consumer lag and scheduler/worker liveness;
- process restarts, crash loops, resource exhaustion and configuration drift;
- database integrity, disk capacity, write latency/failures and journal/hash-chain continuity;
- reconciliation exceptions across source observations, canonical ledger and broker/account snapshots;
- backup age, backup verification and periodic restore-test evidence;
- dependency/SBOM and software-version drift;
- audit-log integrity, alert delivery and unacknowledged incidents.

Health state should be explicit at component, source, domain and whole-system levels. Suggested roll-up states: HEALTHY, DEGRADED, STALE, UNAVAILABLE, UNKNOWN. Do not let a healthy UI conceal a failed data worker. A green global state requires all critical dependencies to satisfy their declared contracts.

Incident lifecycle: detect → persist evidence → classify severity → alert → acknowledge → investigate → recover → verify recovery → close. All transitions, operator acknowledgements, overrides and recovery evidence are auditable. A reconnect alone is not proof of recovery; sequence gaps, missing history and downstream reconciliation must be resolved first.

## 7. Failure policy

- Decision-critical missing, invalid, stale, incomplete or conflicted inputs cause the affected consumer to enter a safe no-action/unknown state.
- Do not silently fill gaps, interpolate prices, reuse stale order books, invent FX, or substitute another venue/source without a prevalidated equivalence policy.
- Last-known values may be displayed for context only with source, timestamp, age and stale/delayed badge; they must not be consumed by a decision contract that disallows them.
- Failover must preserve instrument semantics, timestamps, precision, entitlement and quality. If equivalence is not proven, mark the feed conflicted/unknown.
- On recovery, backfill/replay missing data, reconcile state and verify sequence continuity before restoring normal operation.
- Separate user-facing warnings from execution gates. Only decision-critical data contracts affect the relevant engine; no broad lock on unrelated user finances or domains.

## 8. Automation and AI/token budget

Default to deterministic code and scripts for:
- polling/stream ingestion and retries with bounded backoff;
- schema/quality validation and quarantine;
- heartbeat and freshness monitoring;
- reconciliation and gap detection;
- scheduled reports and alerts;
- backup verification, integrity checks and housekeeping;
- regression tests and reproducible incident bundles.

AI must not be in the critical data path, decide whether data is valid, invent missing values, approve risk or run continuously just to monitor health. Use it only when a bounded task materially benefits from language reasoning (for example, summarising a verified incident or explaining a report). Cache/reuse deterministic outputs and keep prompts/context small. A deterministic rule should never require an LLM call.

## 9. Mobile-first now, portable later

The phone is the preferred current interface, not the required compute host. Separate:
- mobile/web UI and user approval/control surface;
- ingestion and scheduled workers;
- storage/journal and backups;
- deterministic validation/health supervisor;
- domain engines and adapters.

The phone must not need to remain awake, foregrounded or connected for feeds, scheduled tasks, recovery or monitoring to work. Design configuration and deployment as portable, documented units suitable for a later Windows/Linux PC or private server. Avoid phone-specific business logic and avoid committing to cloud hosting, paid services or always-on infrastructure before a separate cost/reliability decision.

## 10. Open research and design questions

1. Which source is authoritative for each data type and market, and what are its legal usage/redistribution limits?
2. Which live and historical feeds are genuinely available at zero or low recurring cost, with what latency, depth, coverage and reliability?
3. What per-data-type freshness budgets are justified by the engine and market session?
4. How should source conflict be resolved without silently selecting the most convenient value?
5. Which deterministic checks can be implemented once as shared contracts and which are venue/instrument-specific?
6. What independent supervisor architecture is proportionate for a single-user modular monolith?
7. How will the supervisor continue operating if the primary app process, database or network fails?
8. What evidence is required before declaring recovery after a gap/outage?
9. How to keep audit records privacy-conscious while retaining enough evidence to reproduce decisions?
10. Which checks run continuously, on schedule, at startup, before a decision, and after recovery?
11. What is the minimum viable alerting route that works from Android without making the phone the worker?
12. How will the same deterministic test suite run on mobile-facing development, PC and server targets?

## 11. Acceptance criteria before runtime work

Before implementation is considered, Phase 02 must define:
- canonical source, observation, quality-state, freshness-contract, incident and lineage schemas;
- deterministic validation rules and explicit consumer failure policies;
- source entitlement/licence and cost matrix;
- supervisor independence and failure-domain model;
- recovery, replay, reconciliation and backup verification contracts;
- security/privacy boundaries and audit retention;
- measurable health SLOs and alert severity/escalation;
- portability/deployment contract;
- tests for stale, missing, duplicate, out-of-order, malformed, contradictory, delayed and corrected data, plus supervisor failure and recovery.

No runtime code, dependencies, source subscriptions, credentials, accounts, hosting or paid services are authorised by this proposal.
