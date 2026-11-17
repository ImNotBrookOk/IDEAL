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


## 12. Historical data collection and learning readiness

The owner is leaning toward IDEAL collecting and retaining its own historical data because the archive may later support research, model evaluation and improvement. This is a design direction for further investigation, not approval to subscribe to feeds, retain unlimited raw data or begin model training.

### 12.1 Archive first; learning second

Treat collected data first as an evidence-grade historical archive. Only later, explicitly curated and versioned subsets become research/training datasets. Never let a model's need for data silently redefine collection, retention, privacy or licensing policy.

The archive should preserve:
- source identity, venue/provider, instrument and contract metadata;
- original source timestamps and separate receive/ingest/process timestamps;
- raw payload or lossless/canonical evidence where legally and economically feasible;
- normalised observations and transformation/version;
- correction, cancellation, replacement, gap and reconciliation events;
- source entitlement, licence, permitted-use and retention constraints;
- content hashes, schema versions and dataset manifests.

Keep market data, account/private financial records, personal data and AI interaction traces logically and access-control separated. A market dataset must not accidentally include account identifiers, credentials, personal transactions, or private conversation content.

### 12.2 Storage tiers and collection economics

Do not assume that storing every full-depth order-book update forever is necessary or affordable. Design retention by data class:
- high-resolution hot window for tick/trade/order-book streams where required by active research questions;
- compact, lossless or carefully specified warm archives for validated bars, funding, mark/index, instrument metadata and selected event streams;
- cold compressed historical partitions with manifests and checksums;
- derived features and labels stored separately and reproducibly, never replacing raw evidence.

Measure data volume, write throughput, compression ratio, query patterns, recovery time and backup cost before selecting storage. Retention must respect provider/exchange terms, exchange redistribution restrictions, data residency/privacy obligations and user-controlled deletion policies. Where a licence prohibits archival or model training, record that restriction and exclude the data from those uses.

### 12.3 Point-in-time research datasets

A research dataset must be reproducible and point-in-time correct. Each dataset version should pin:
- source snapshots and revision/correction state as known at decision time;
- instrument universe and delisted/expired contracts;
- timezone, calendar, bar construction and resampling rules;
- feature definitions and code commit;
- label definition, horizon and label-maturity time;
- train/validation/test windows and purging/embargo rules;
- costs, fees, funding, spread, slippage and execution assumptions;
- data-quality exclusions and missing-data policy.

Do not use revised macro releases, later corporate-action knowledge, future constituents, future labels or any other information unavailable at the simulated decision time. Retain delisted and expired instruments where possible to reduce survivorship bias.

### 12.4 Separate kinds of learning

Do not conflate:
1. Assistant/agent learning: interaction traces can improve retrieval, routing, prompts, tool selection and workflow quality. OpenJarvis demonstrates trace-driven routing and stack/model optimisation concepts.
2. Market-model learning: validated market observations and mature outcome labels can train/evaluate forecasting, regime, risk, execution-cost and portfolio models.
3. Strategy research: deterministic feature/strategy experiments and backtests can use the archive without requiring an LLM.

Agent traces are not market labels. A conversational model improving its tool use does not imply a trading model has learned predictive alpha.

### 12.5 Controlled model lifecycle

All model training and tuning must be offline and reproducible. The process is:
collect → validate → curate dataset → define labels → train/fit → evaluate → walk-forward and regime tests → compare to baselines → shadow/challenger → paper evaluation (only when that phase is separately authorised) → explicit approval gate.

No online weight updates, automatic strategy mutation or self-modifying live engine. A new model version must be immutable and registered with dataset hash, code commit, parameters, seed, environment, metrics, known limitations and approval state. Promotion requires measurable out-of-sample improvement after realistic fees, funding, spread, slippage, latency and position sizing, plus stability across regimes and independent replication. A model that fails or loses its data provenance is rejected or rolled back.

## 13. Local AI and model research — preliminary candidates

This section records research candidates only. No framework, model, package or runtime has been adopted or approved.

### 13.1 Personal assistant / agent frameworks

- OpenJarvis — Apache-2.0, https://github.com/open-jarvis/OpenJarvis. Strongest architectural research candidate for local-first personal AI: separate Intelligence, Engine, Agents, Tools/Memory and Learning primitives; supports local inference backends including Ollama, vLLM, SGLang and llama.cpp, plus optional cloud; trace-driven routing and learning; on-demand/scheduled/continuous modes; energy, latency and cost telemetry. Its security documentation is useful but requires careful hardening: shell execution can run with host-user privileges unless sandboxed, Docker sandboxing and capability controls are off by default, capability policy defaults need explicit deny-by-default configuration, and a documented tool-confirmation setting is accepted but not enforced in every entry point. Treat as a design reference and sandboxed evaluation candidate, not as IDEAL's trusted financial supervisor or execution authority.
- Hermes Agent — MIT, https://github.com/NousResearch/hermes-agent. Broad self-hosted agent with memory, skill creation, scheduling, multiple channels and pluggable model providers. Useful comparison for user-facing assistant workflows. Its own security model describes a single-tenant agent and a default terminal backend that runs commands directly on the host; any IDEAL evaluation would require strict tool minimisation, isolated execution, least privilege and no access to trading credentials or financial write operations. Its learning loop is agent/skill/memory improvement, not evidence of market-prediction ability.
- OpenJarvis is currently the better fit for architecture study because its composable primitives, trace/evaluation/efficiency focus and local-first routing align closely with IDEAL's low-token, portable design. Neither candidate is adopted.

### 13.2 Local inference runtimes

- llama.cpp — MIT, https://github.com/ggml-org/llama.cpp. Strong portability candidate for quantised CPU/GPU inference across Windows/Linux, Apple Silicon and multiple accelerators; provides an OpenAI-compatible local server, schema-constrained JSON and tool/function calling. Candidate runtime for later PC evaluation.
- Ollama — MIT, https://github.com/ollama/ollama. Simpler local model lifecycle and API; supports tool calls and schema-constrained structured output. Useful usability baseline. Keep model runtime behind an IDEAL-owned interface so it can be replaced.
- OpenJarvis supports several interchangeable backends. Avoid binding IDEAL's domain contracts to a particular inference server or model format.

### 13.3 Hugging Face / open-weight model candidates

- Amazon Chronos-2 — Apache-2.0, 120M parameters, probabilistic quantile forecasting, univariate/multivariate/covariate-aware and CPU/GPU capable. Promising low-compute baseline for general time-series experiments, but not validated as a crypto/equity alpha model.
- Google TimesFM 3.0 — Apache-2.0 repository, pretrained general time-series foundation model. Candidate comparison, not assumed suitable for high-frequency or microstructure data.
- IBM Granite Time Series PatchTST-FM-r2 — dual Apache-2.0/OpenMDW-1.0 licensing per release material, about 385M parameters, probabilistic forecasts and imputation. Candidate for medium-horizon forecasting and missing-data experiments; must benchmark locally and verify exact model artefact licence.
- Salesforce Moirai 2.0-R-Small / MoiraiAgent — Hugging Face model card declares CC-BY-NC-4.0; exclude from any commercial-use-compatible candidate set unless licence terms change or counsel confirms the intended use. Research-only status and licence restrictions must be respected.
- FinGPT — financial-language model research ecosystem, potentially useful for classifying/summarising financial text and sentiment with careful source/time provenance. It is not a replacement for numerical time-series models, and sentiment output is not a trading signal without independent validation.
- Qlib — MIT, https://github.com/microsoft/qlib. Quant research framework with data pipeline, feature/model training, backtesting, portfolio/risk and execution abstractions. Valuable research reference and potential offline experiment harness; not a drop-in IDEAL runtime and not proof of edge. Its defaults/examples have equity-market orientation, so crypto perpetual support and funding/microstructure assumptions need independent assessment.

### 13.4 AI usage policy for IDEAL

Use deterministic scripts for acquisition, validation, reconciliation, health checks, calculations, backtests, scheduling and routine reporting. A local model may assist with natural-language interaction, document research, bounded incident summaries, tool routing or approved research analysis. LLM output is untrusted input: validate structured output against schemas, treat retrieved content as untrusted, sandbox code/tools, require explicit approval for consequential actions and maintain an independent audit record. No model can authoritatively validate its own input data or silently modify live strategy/execution logic.

### 13.5 Evaluation criteria before any adoption

Evaluate candidates on:
- exact licence for code, weights, tokenizer, training data and intended use;
- hardware and memory requirements at the actual target quantisation/context;
- local latency, throughput, energy and memory use on the eventual PC;
- structured-output and tool-call reliability on IDEAL-specific test sets;
- hallucination, prompt-injection and tool-boundary resistance;
- offline operation, data egress and telemetry behaviour;
- reproducible installation, pinned versions, SBOM and security updates;
- maintenance activity, release cadence, unresolved critical issues and dependency footprint;
- measurable quality versus deterministic scripts and simpler models;
- total cost of ownership, including hardware, power, storage and maintenance.

Do not select hardware or a model before target PC specifications and representative workloads are known.


## 14. Risk, data and health as one protection system

Data integrity and system health are not standalone infrastructure concerns. They are direct prerequisites for valid risk decisions. Risk management is the protection and permission layer; data integrity is the evidence layer; system health is the independent oversight layer. All three must reinforce one another across every authorised domain.

A risk calculation must consume the quality and freshness state of every material input, not just its numeric value. If required prices, balances, positions, FX conversions, contract metadata, funding/mark values or other inputs are stale, incomplete, contradictory or unknown, the risk result must be invalid or conservatively restricted according to a predefined contract. A numeric output must never imply confidence when its evidence is defective.

The health supervisor must monitor whether data validation, risk services, policy versions, reconciliation and downstream interlocks are functioning. A risk service cannot certify its own health; a data adapter cannot certify its own source integrity; and a strategy cannot declare that its own dependencies are safe. Independent checks, external heartbeats and cross-source reconciliation should be proportionate to the failure being detected.

Risk management must be a shared deterministic capability with domain-specific contracts. It should evaluate exposure before an action, monitor it while exposure exists, and reconcile actual outcomes afterwards. A strategy may request an action but cannot alter limits, bypass a restriction or treat unavailable risk controls as approval. The health supervisor may trigger only predefined restrictive interlocks; it must not invent risk limits or authorise financial actions.

Failure handling must be dependency-aware. Invalid market data may suspend strategies that rely on it without disabling unrelated finance reporting. A portfolio-wide risk service failure may restrict every activity that depends on portfolio-wide approval. Every engine must declare its dependencies, acceptable quality states, failure behaviour and recovery requirements.

This integration is specified in [docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md](IDEAL_CORE_PROTECTION_ARCHITECTURE.md). No runtime integration or implementation is authorised by this documentation update.


## 15. Security monitoring and health integration

Security is a separate foundational pillar, but its telemetry and the operational status of its controls must be integrated with system health. Monitor authentication anomalies, permission changes, credential/key lifecycle, unusual access and exports, unexpected outbound connections, process/port/configuration drift, dependency advisories, integrity failures, audit gaps, backup encryption/restore evidence and failures or disablement of security monitoring.

Do not collapse security posture into a single green health indicator. Operational health asks whether components are functioning; security assurance asks what was assessed, against which threats and controls, using what evidence and how recently. A compromised component may remain available and report itself healthy. Security status therefore needs its own scoped states, evidence freshness and independent observation.

The health supervisor itself has only a restrictive interlock channel: it may request suspension of affected risk-increasing actions and, where explicitly designed, isolation of an untrusted workload through a narrowly scoped control. It cannot revoke/issue credentials, change security policy or initiate financial side effects. A separately governed security incident-response authority may revoke compromised identities/credentials or disable integrations under its own audited authority; that security controller is not the health supervisor. Neither authority may grant financial permissions or initiate cancellation, flattening, transfer, withdrawal or payment.

The security architecture, threat model, vulnerability lifecycle, incident response and assurance backlog are specified in [docs/IDEAL_SECURITY_ARCHITECTURE.md](IDEAL_SECURITY_ARCHITECTURE.md). No implementation or external scanning is authorised by this documentation update.


## Independent supervisor authority boundary — checkpoint 069

The health supervisor is an observer and restrictive interlock issuer, not an execution authority. It observes components outside their process boundary and must not rely on self-reported HEALTHY status. It has read-only telemetry access and a narrow, authenticated, scoped channel to request suspension of new risk-increasing actions. It cannot create/change owner envelopes, policy, risk approvals, reservations, credentials, or initiate cancellation, flattening, transfer, withdrawal or payment.

The action gateway validates supervisor identity, message scope, generation, freshness and integrity. Loss of the supervisor heartbeat, invalid state or untrusted monitoring path triggers the defined fail-closed restriction for affected risk-increasing actions. Only independent recovery evidence and the designated owner release process can clear critical latched interlocks.

A separate process identity is the minimum logical separation; it does not protect against shared host root/kernel compromise. Stronger independence requires a separate VM/host or hardware/remote watchdog when that threat is in scope. A compromised supervisor may cause denial of service but must not gain financial authority. It cannot certify its own health or security posture.

Keep operational health, data trust, security posture, financial-state trust and authority state as distinct dimensions. No single supervisor or pillar self-certifies all others. See the autonomy authority architecture §§23–24.


## Evidence lifecycle and point-in-time contract — checkpoint 073

The data architecture now distinguishes source event/publication time, receive time, durable ingest time, processing time, valid/effective time, knowledge/transaction time and decision-as-of time. Corrections are linked revisions, not destructive overwrites. Point-in-time datasets must preserve the exact source revisions and availability cutoff that were knowable at the simulated decision time; event time alone is insufficient to prevent look-ahead leakage.

Quality is a consumer-specific vector covering source authenticity, schema, completeness/sequence, freshness, plausibility, cross-source consistency, revision, licence, reconciliation and clock confidence. Unknown, conflicted, stale, incomplete or unlicensed evidence must not be silently converted into valid data. Market, private-finance, security/audit and AI traces remain separate data planes.

See [IDEAL Data Trust, Temporal Semantics and Point-in-Time Evidence Architecture](IDEAL_DATA_TRUST_TEMPORAL_AND_POINT_IN_TIME_ARCHITECTURE.md) for lifecycle, bitemporal semantics, bank/market/tax-specific rules, retention, verification and current NZ provider/tax evidence. W3C PROV, Apache Iceberg and MLflow are conceptual/candidate references only; none is adopted.


## Reconciliation and verified recovery — checkpoint 076

Reconciliation is a domain-owned comparison between independent state representations, not a generic sync or last-write-wins merge. There is no universal source of truth: venue evidence is required for external order/fill/position facts; IDEAL's journal is the personal-finance accounting record after controlled posting; bank/provider records remain observations; IRD assessments differ from IDEAL tax estimates; raw market observations differ from reconstructed canonical state.

Mismatch, unknown and quarantine states remain explicit. Corrections preserve both source sides and create linked revisions. Recovery requires restore into quarantine, integrity/identity/policy checks, external-state reconciliation, recomputation of dependent projections, scoped attestations from each foundation and owner release where reserved. Restart or reconnect alone never establishes recovery.

See [IDEAL Reconciliation, Incident Containment and Verified Recovery Architecture](IDEAL_RECONCILIATION_AND_VERIFIED_RECOVERY_ARCHITECTURE.md). No runtime recovery or account reconciliation has been performed.


## Cross-authority state and version-vector contract — checkpoint 081

Data quality is a distinct state machine. Each future consequential action binds source revisions, availability cutoff, transformation version, quality state and account/instrument reconciliation version. A later correction creates a new latest-known view and may invalidate dependent current decisions; it does not rewrite the original as-known-then evidence snapshot. Data validity cannot grant authority or risk approval.

See [Integrated State-Machine and Cross-Authority Contract Architecture](IDEAL_INTEGRATED_STATE_MACHINE_AND_CONTRACT_ARCHITECTURE.md).
