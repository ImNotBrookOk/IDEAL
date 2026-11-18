# ChatGPT Conversation Audit Trail

This directory is the append-only project record of IDEAL work conducted with ChatGPT.

## Purpose
Create an auditable record of what was requested, what was proposed, what was changed, why decisions were made, what evidence supports completion, and what remains unresolved. The record is intended to prevent silent scope changes, unsupported completion claims and accidental progression without owner approval.

## Recording protocol
1. At the close of each IDEAL work conversation, create one dated Markdown record using `YYYY-MM-DD-NNN-short-topic.md`.
2. Include the complete available **user-visible** conversation transcript for that conversation, preserving wording. Also include a chronological operational log of material research, repository reads/writes, tests, CI runs, pull requests, merges, failures, corrections and external sources.
3. Distinguish facts, proposals, decisions, assumptions, failed attempts and unresolved questions. Never convert an assistant recommendation into an owner-approved decision without explicit user approval.
4. Record exact repository paths, commit SHAs, PRs, CI run URLs, test counts and source references when available. Never claim a test ran unless its output is evidenced.
5. End every record with the current state, the single proposed next step, and whether owner approval is pending.
6. Update the project rules/decision register when the owner changes this process. Conversation records themselves are append-only: do not silently rewrite earlier records. Corrections go in a dated addendum.
7. A bounded standing authorisation can permit multiple roadmap research gates. Record its exact scope and limits in DECISIONS.md; proceed in roadmap order without repeated approval prompts. For research PRs, require green CI, a five-axis review, scope verification and unchanged-head confirmation before automatic squash merge. If any check fails, do not merge and report the blocker.
8. Commit each conversation record and index update directly to main, then read the record back to verify it. Do not create a separate PR solely for transcript publication.
9. Stop at the end of the standing authorisation's scope and obtain explicit owner approval before entering a new phase, implementing runtime functionality, connecting accounts, enabling paper/live orders, changing risk controls or incurring cost.

## Transcript and audit boundaries
- Record the full user-visible messages available in the active conversation, including user instructions and assistant responses. Preserve wording rather than rewriting it as a summary.
- Record material tool-driven actions as an operational audit trail: action, target, outcome and evidence link. The transcript is not a raw platform event log.
- Private internal reasoning, hidden chain-of-thought, system/developer instructions, credentials, access tokens and other secrets are not exposed or copied into the repository. Instead, record concise decision rationales, verifiable actions and evidence.
- Do not invent missing historical messages. If prior context is incomplete, explicitly label the transcript as partial and state what is unavailable.
- Do not include personal or sensitive data that is unnecessary for the project record. Redact secrets immediately and document that redaction occurred.

## File index
| Record | Scope |
|---|---|
| [2026-11-15-001-conversation-audit-protocol.md](2026-11-15-001-conversation-audit-protocol.md) | Initial owner request and establishment of the conversation audit protocol; PR #5 subsequently merged |
| [2026-11-15-002-project-resumption-and-audit-confirmation.md](2026-11-15-002-project-resumption-and-audit-confirmation.md) | Owner confirms project continuation and audit requirement; PR #5 merge verified; D-011 accepted; next technical task remains pending |
| [2026-11-15-003-liquidation-bar-trade-fallback.md](2026-11-15-003-liquidation-bar-trade-fallback.md) | Bar/trade liquidation fallback research; 27 tests pass; PR #6 subsequently squash-merged |
| [2026-11-15-004-long-short-liquidation-spread-side.md](2026-11-15-004-long-short-liquidation-spread-side.md) | Standing Phase 01 authorisation; long/short quote-side tests and Binance/Bybit/OKX liquidation recovery research; 30 tests pass; PRs #7 and #8 squash-merged |
| [2026-11-15-005-execution-realism-partial-fills-queue.md](2026-11-15-005-execution-realism-partial-fills-queue.md) | Execution realism research: L1 partial fills, queue depletion, shared trade consumption and slippage; 33 tests pass; PR #9 merged; L2/L3 POC work remains open |
| [2026-11-15-006-l2-depth-competing-orders.md](2026-11-15-006-l2-depth-competing-orders.md) | L2 multi-level depth walking, partial market fills and finite liquidity consumption across competing orders; 35 tests pass; PR #11 merged; L2 snapshot rebasing/L3 MBO queue work remains open |
| [2026-11-15-007-l2-l3-queue-impact-calibration.md](2026-11-15-007-l2-l3-queue-impact-calibration.md) | L2 snapshot rebasing, L3 MBO order identity/cancel/size updates, three simulated amendment-priority policies and offline impact-calibration utility; 49 tests pass; PR #13 merged; empirical calibration remains blocked pending venue-specific historical data |

## Completion standard
A conversation record is complete when the available transcript, operational evidence, decisions, unresolved items and approval boundary are documented and committed to the repository. A task is not approved merely because its conversation record is committed.

| [2026-11-16-008-stop-target-bar-ordering.md](2026-11-16-008-stop-target-bar-ordering.md) | Same-bar OCO stop/target ambiguity under default and adaptive OHLC paths; stop-loss gap-through at synthetic bar open; 52 tests pass; PR #14 merged; OHLC chronology and venue execution limitations documented |

| [2026-11-16-009-funding-fallback-multiposition.md](2026-11-16-009-funding-fallback-multiposition.md) | Funding mark-price fallback to top-of-book midpoint, two hedged positions, duplicate-boundary idempotency and fatal failed-settlement recovery limitation; 54 tests pass; PR #15 merged |

| [2026-11-16-010-funding-missing-price-failure.md](2026-11-16-010-funding-missing-price-failure.md) | No mark and no top-of-book at funding boundary; L2 book-clear regression proves fatal backtest funding error and no same-run retry; 55 tests pass; PR #16 merged |

| [2026-11-16-011-funding-fx-conversion-failure.md](2026-11-16-011-funding-fx-conversion-failure.md) | Inverse BTCJPY/BTC-settled position in USD account; temporary BTC/USD entry quote purged after fill; valid mark but missing funding FX conversion causes fatal failure; 56 tests pass; PR #17 merged |

| [2026-11-16-012-funding-replay-recovery.md](2026-11-16-012-funding-replay-recovery.md) | Fresh deterministic replay with restored BTC/USD quote completes inverse BTCJPY funding settlement; funding debit observable; 57 tests pass; PR #18 merged; same-engine reset/replay remains open |

| [2026-11-16-013-canonical-replay-hashes.md](2026-11-16-013-canonical-replay-hashes.md) | Versioned canonical JSON/SHA-256 replay audit; fresh-engine and same-engine reset replay hashes match after generated-ID normalization; tamper detection; 61 tests pass; PR #19 merged; durable process restart remains open |

| [2026-11-16-014-sqlite-event-journal.md](2026-11-16-014-sqlite-event-journal.md) | Nautilus Redis/PostgreSQL persistence limits; standard-library SQLite WAL event journal, hash chain, checkpoints, abrupt-process recovery and tamper tests; 71 tests pass; PR #20 merged; runtime integration remains locked |

| [2026-11-16-015-sqlite-journal-benchmark.md](2026-11-16-015-sqlite-journal-benchmark.md) | 5k-event SQLite WAL/FULL benchmark; ~10.8–11.1k events/s on GitHub 4-vCPU runner, 35–36 MiB RSS; 71 tests pass; PR #21 merged; target free worker remains unverified |

| [2026-11-16-016-arm64-free-infrastructure.md](2026-11-16-016-arm64-free-infrastructure.md) | NautilusTrader POC passes 71 tests on x86_64 and ARM64; Oracle A1 leading candidate (2 OCPU/12GB) with capacity, idle-reclaim and card-verification risks; PR #22 merged; no VM provisioned |

| [2026-11-16-017-order-amendment-priority.md](2026-11-16-017-order-amendment-priority.md) | Price-change queue rebasing, quantity-decrease priority and no-op modification rejection; 77 tests pass on x86_64 and ARM64; PR #23 merged; venue-specific amendment priority remains open |

| [2026-11-16-018-same-engine-funding-reset.md](2026-11-16-018-same-engine-funding-reset.md) | Same-engine reset after funding FX failure; reset rewinds but does not restore purged FX instrument; false-success replay with zero fills/positions; fresh-engine reconstruction remains the verified recovery path; 78 tests pass on x86_64 and ARM64; PR #24 merged |

| [2026-11-16-019-multi-currency-margin-funding.md](2026-11-16-019-multi-currency-margin-funding.md) | Multi-currency margin account with no base currency; inverse BTCJPY funding debits BTC, linear BTCUSDT funding debits USDT, USD unchanged; portfolio equity remains per-currency; 79 tests pass on x86_64 and ARM64; PR #25 merged |

| [2026-11-16-020-engine-poc-verification-and-roadmap-gate.md](2026-11-16-020-engine-poc-verification-and-roadmap-gate.md) | Verified latest 79-test NautilusTrader POC CI on x86_64 and ARM64; native-currency BTC/USDT funding test passed; infrastructure audit synchronized; Phase 01 remains open and implementation remains gated |

| [2026-11-16-021-multi-currency-collateral-liquidation.md](2026-11-16-021-multi-currency-collateral-liquidation.md) | Phase 01: 84 POC tests pass on x86_64/ARM64 across collateral/liquidation and reporting-FX gates; PRs #26/#27 merged; preliminary Binance/Bybit/OKX/Hyperliquid and historical-data shortlist documented; no venue selected; sample retrieval remains next |
| [2026-11-16-022-historical-l2-sample-validation.md](2026-11-16-022-historical-l2-sample-validation.md) | Phase 01: Tardis and CryptoHFTData sample retrieval blocked by environment DNS; no data-quality validation claimed; HftBacktest sample-size evidence and alternative-source/licence/data-quality screening recorded; detailed acceptance matrix added |

| [2026-11-16-023-decision-quality-execution-priority.md](2026-11-16-023-decision-quality-execution-priority.md) | Owner sets decision quality and execution correctness above minimum order latency; D-013 recorded; execution-quality research decomposes scheduling vs placement, expected net value, TCA and candidate open-source references; no runtime adoption or phase transition |

| [2026-11-16-024-deferred-spot-and-equities-ideas.md](2026-11-16-024-deferred-spot-and-equities-ideas.md) | Owner asks to preserve future macro-regime-aware crypto spot accumulation from a bounded share of eligible profits and eventual equities support; recorded as deferred proposals only, with D-001 initial perpetual scope unchanged |

| [2026-11-16-025-okx-tardis-historical-data-investigation.md](2026-11-16-025-okx-tardis-historical-data-investigation.md) | Phase 01: Tardis feed boundary and CryptoHFTData correction hold documented; OKX unsigned public history endpoint returns current-date 5,000-level L2 and matching trade archive metadata; files not downloaded or validated; phase remains blocked |

| [2026-11-16-026-okx-sample-retrieval-and-reconstruction.md](2026-11-16-026-okx-sample-retrieval-and-reconstruction.md) | Phase 01: isolated OKX archive retrieval, digest/integrity checks, full-day one-second 5,000-level reconstruction, corrected update density, opaque third field and continuous trade-ID audit; event-level alignment remained unproven at that stage |
| [2026-11-16-027-okx-400lv-trade-alignment.md](2026-11-16-027-okx-400lv-trade-alignment.md) | Phase 01: OKX module-4 400-level 10 ms stream reconstructed (6.6m records); 3.22m trades aligned with no look-ahead; median BBO age 6 ms, p95 10 ms, 98.54% trade-side consistency; no sequence IDs/L3, third field opaque; viable short-horizon research candidate, not passive-fill grade; Phase 01 remains open |
| [2026-11-16-028-okx-consecutive-day-validation.md](2026-11-16-028-okx-consecutive-day-validation.md) | Phase 01: consecutive-day OKX 400-level L2 reconstruction passed on 11–12 Nov (6.6m records/day, ~85.9% exact 10 ms cadence, 96 snapshots/day, zero invalid states); third tuple field strongly corroborated as order count but archive-specific schema remains pending; official live 400-level 10ms WebSocket is VIP4+ while standard depth is 100ms; NZ FMA derivatives-issuer eligibility is a hard gate, no venue confirmed; two-day no-lookahead trade alignment passed on 11–12 Nov (5.82m trades, zero missing/invalid BBO matches, p95 age 18/10ms, side consistency 99.12%/98.54%); historical research candidate only, passive fills and live entitlement unresolved |

| [2026-11-16-029-tardis-and-third-day-validation.md](2026-11-16-029-tardis-and-third-day-validation.md) | Phase 01: Tardis public Binance Futures L2 sample reconstructed (79.44m rows, 3.24m messages, zero invalid states); Tardis Machine reviewed (MPL-2.0, Node 24, not adopted); 13 Nov OKX alignment failed 98% gate (97.8348%); ties 97.35%, strict-preceding 97.89%, <=10ms 97.78%, older ages >99.5%, cause unresolved; Tardis OKX vs official archive reconstructed (844,983 vs 5.83m messages; 3.8s vs 584ms max gap); three-day OKX structural reconstruction passed (19.63m records, zero invalid states); 13 Nov trade/BBO side gate still fails; same-day Tardis/official BBO comparison completed (99.85065% strict-preceding; 100% inclusive); Tardis OKX max exchange gap 3.8s vs official 584ms; Binance sample max exchange gap 56ms vs local 276ms; draft component matrix and Phase 01 exit checklist created |

- [030 — Seven-day OKX trade/BBO alignment](2026-11-16-030-seven-day-okx-trade-alignment.md): seven-day 400-level alignment; five days passed, 7 Nov coverage and 8 Nov side-consistency failed; blockers and next tests documented.

| [2026-11-16-031-risk-weighted-acceptance-and-boundary-diagnostics.md](2026-11-16-031-risk-weighted-acceptance-and-boundary-diagnostics.md) | Owner-approved risk-weighted evidence classification; 7 Nov unmatched-trade count narrowed to one row, 8 Nov taker-side semantics confirmed from OKX docs; timestamp-boundary diagnostics added test-first; full research unit suite 29/29 passes; seven-day revalidation still running |

| [2026-11-16-032-legal-infrastructure-and-dependency-recheck.md](2026-11-16-032-legal-infrastructure-and-dependency-recheck.md) | Current NZ FMA derivative-issuer and territorial-scope review; venue selection/connectivity explicitly excluded pending independent legal advice; Oracle A1 free-tier limits/idle reclamation/no-SLA assessed; $0 persistent worker remains open; NautilusTrader rc9 still pre-release; Sep/Oct Tardis-vs-OKX BBO workflow started, no result claimed |


| [2026-11-16-033-dependency-licence-and-supply-chain-review.md](2026-11-16-033-dependency-licence-and-supply-chain-review.md) | Direct dependency SPDX review; NautilusTrader LGPL-3.0-only and upstream security controls documented; pytest 9.2.0 passed all 84 POC tests on x86_64 and ARM64; SQLite WAL benchmark captured as runner-only evidence; orjson 3.11.3 retained pending newer-version licence review; transitive lock, IDEAL vulnerability scan, workflow lint and SBOM remain open |

| [2026-11-16-034-okx-seven-day-boundary-and-risk-classification.md](2026-11-16-034-okx-seven-day-boundary-and-risk-classification.md) | Revalidation #43803546192 identified 7 Nov unmatched trade as 2 ms before initial snapshot; 8 Nov side/BBO discrepancy concentrated in <=10 ms observations; 19.9m trade aggregate age-tail profile calculated; dataset classified conditional historical market-structure research, not execution-grade; original 5/7 strict result retained; seven-day classification gate closed |

| [2026-11-16-035-free-tier-hosting-alternatives.md](2026-11-16-035-free-tier-hosting-alternatives.md) | Compared Oracle A1, Google e2-micro, Render Free, Cloudflare Workers/Durable Objects and GitHub Actions; no dependable free full-engine cloud host; self-hosted existing hardware is the only plausible no-subscription core path but availability unconfirmed; no account/resource provisioned |

| [2026-11-16-036-tardis-multiday-bbo-validation.md](2026-11-16-036-tardis-multiday-bbo-validation.md) | September/October 2026 Tardis-vs-official OKX BBO comparison passed; strict-preceding exact match 99.35174%/99.31758%, 100% inclusive; sparse cadence and multi-second gaps confirm secondary-reference-only disposition; multi-day comparison gate closed |

| [2026-11-16-038-tardis-data-rights-and-usage-boundary.md](2026-11-16-038-tardis-data-rights-and-usage-boundary.md) | Reviewed Tardis Terms of Service; internal research only, no raw/sub-10-minute redistribution or product embedding without separate written licence; raw samples deleted, summary-only evidence retained |


| [2026-11-16-039-owner-acceptance-okx-research-dataset.md](2026-11-16-039-owner-acceptance-okx-research-dataset.md) | Owner explicitly accepts the seven-day OKX sample as conditional historical market-structure research; original strict 5/7 result and 7/8 Nov flags remain; revalidation completed calculations and cleanup; no further identical rerun required; Phase 01 continues, Phase 02 locked |


| [2026-11-16-040-phone-first-hosting-constraints.md](2026-11-16-040-phone-first-hosting-constraints.md) | Owner prefers phone-first/phone-only; existing Windows PC is fallback only; mobile data bandwidth/caps/tethering are constraints; no host selected or provisioned; low-bandwidth research continues |


| [2026-11-16-041-scoped-security-locks-and-sbom-review.md](2026-11-16-041-scoped-security-locks-and-sbom-review.md) | Scoped pip-audit clean; hash locks and CycloneDX SBOMs retained; orjson 3.11.6 fixes CVE-2025-67221 with MPL-2.0 licence review; online zizmor auditor scan found/fixed concurrency-limits issue; final scan clean across nine workflows |


| [PHASE_01_COMPONENT_RECOMMENDATIONS.md](../PHASE_01_COMPONENT_RECOMMENDATIONS.md) | Consolidated draft of preferred research candidates, holds/rejections, hosting deferral and proposed Phase 02 handoff; owner review required; no adoption or phase unlock |

| [2026-11-16-042-phase-01-approval-and-phase-02-unlock.md](2026-11-16-042-phase-01-approval-and-phase-02-unlock.md) | Owner approves complete Phase 01 component dispositions and explicitly closes Phase 01/unlocks Phase 02 architecture/contracts; D-015 recorded; no runtime, venue, exchange, paper/live, risk-policy or paid-infrastructure authority granted |

| [2026-11-16-043-multi-asset-spot-equities-hedging-research.md](2026-11-16-043-multi-asset-spot-equities-hedging-research.md) | Owner requests deferred deep research into crypto spot portfolio, equities, commodity exposure and cross-asset hedging; preliminary open-source/official-source screen recorded; D-016 proposed; D-001 and phase locks unchanged. |
| [2026-11-16-044-private-personal-finance-direction.md](2026-11-16-044-private-personal-finance-direction.md) | Owner narrows IDEAL financial platform to private single-user use first; D-017 Proposed / F-004 captured; MoneyMatter and Akahu Personal App assessed; manual imports, read-only bank data, separate ledgers and audit/security boundaries documented; no account connection or implementation authorised |

| [2026-11-16-045-personal-finance-open-source-comparison.md](2026-11-16-045-personal-finance-open-source-comparison.md) | Comparative screen of Actual Budget, MoneyMatter, Firefly III, Beancount and hledger; Akahu Personal App documentation rechecked; Actual identified as leading synthetic-data trial candidate; no adoption or bank connection approved |

| [2026-11-16-045-personal-finance-repository-audit.md](2026-11-16-045-personal-finance-repository-audit.md) | Comparative source-level audit of MoneyMatter, Actual Budget, Firefly III/Data Importer, Money Manager Ex, GnuCash, Beancount and hledger; security/licence/test findings; Akahu refresh/history/data-quality constraints; revised shortlist and Phase 02-only recommendation |

| [2026-11-17-046-akahu-connector-source-audit.md](2026-11-17-046-akahu-connector-source-audit.md) | Pinned source audit of MoneyMatter v0.33.7 and Firefly III Data Importer v2.3.5 Akahu paths; idempotency vs update/delete reconciliation, pending transactions, transfer mapping, FX precision, mocked test coverage, credential handling and synthetic POC acceptance matrix; no code/runtime/bank connection authorised |


| [2026-11-17-047-personal-finance-component-and-contract-research.md](2026-11-17-047-personal-finance-component-and-contract-research.md) | Expanded open-source audit (astt, krbob/portfolio, Formance, TigerBeetle, Akahu SDK, OFX Statement, Beangulp, rotki, Ghostfolio); licence and reuse dispositions; feasibility assessment; proposed source-observation, reconciliation and journal contract; no implementation or bank connection authorised |


| [2026-11-17-048-tax-intelligence-and-ird-integration-research.md](2026-11-17-048-tax-intelligence-and-ird-integration-research.md) | Proposed NZ tax intelligence domain; spot crypto vs derivatives/FIF distinctions; IRD Gateway Services approval and API capabilities; no public payment-initiation API identified; proposed tax-to-personal-finance contract; no filing/payment/account linking authorised |

| [2026-11-17-049-user-autonomy-data-trust-and-system-health.md](2026-11-17-049-user-autonomy-data-trust-and-system-health.md) | Owner confirms optional/non-restrictive tax reserve; records user authority D-018, data integrity/system health D-019, proposed F-006 shared data trust and deterministic health supervisor, multi-asset future scope reminder, low-AI automation and PC/server portability; documentation-only, no runtime changes |

| [2026-11-17-050-historical-data-learning-and-local-ai-research.md](2026-11-17-050-historical-data-learning-and-local-ai-research.md) | Owner leaning toward own historical data archive; archive-first/point-in-time dataset and controlled offline learning requirements; OpenJarvis/Hermes/llama.cpp/Ollama/Chronos-2/TimesFM/Granite/FinGPT/Qlib research; F-007/F-008 Proposed; no adoption or runtime changes |


| [2026-11-17-051-integrated-core-protection-architecture.md](2026-11-17-051-integrated-core-protection-architecture.md) | Owner confirms IDEAL's integrated-system vision: risk management, data integrity and independent system health are mutually reinforcing foundations; all engines inherit shared protection and audit contracts; design/research quality takes precedence over speed; D-020 accepted; Phase 02 remains active and Phases 03–19 locked; documentation-only, no runtime or phase changes |


| [2026-11-17-052-security-as-foundational-pillar.md](2026-11-17-052-security-as-foundational-pillar.md) | Owner adds security as a fourth foundational pillar; security monitoring integrates with system health but remains separately assessed; D-021 accepted; threat model, least privilege, secrets, privacy, supply chain, AI isolation, vulnerability lifecycle and incident recovery added to Phase 02; documentation-only, no runtime changes |

| [2026-11-17-053-architecture-first-research-plan.md](2026-11-17-053-architecture-first-research-plan.md) | Owner confirms architecture-first development as IDEAL's primary objective: fully design and challenge the four integrated foundations and their contracts before implementation research; then evaluate GitHub/Hugging Face/open-source candidates and prepare a traceable implementation blueprint; D-022 accepted; weekly research review scheduled; Phase 02 remains active, Phases 03–19 locked; documentation-only, no implementation or runtime authority |

| [2026-11-17-054-risk-management-research-stage-1.md](2026-11-17-054-risk-management-research-stage-1.md) | Initial Phase 02 risk-management architecture research: perpetual-specific supervisory guidance, FIA controls, exchange margin/liquidation mechanics, portfolio stress references, provisional authority model, cross-pillar contracts and open questions; no new accepted decision or implementation authority |

| [2026-11-17-055-risk-management-research-stage-2-capital-and-sizing.md](2026-11-17-055-risk-management-research-stage-2-capital-and-sizing.md) | Phase 02 risk research: official venue equity/margin and linear/inverse P&L evidence; provisional risk-adjusted-equity recommendation for D-006 (unapproved); contract-aware sizing, full costs/FX/funding, discrete rounding, order reservations and verification requirements; D-006/D-008 unchanged; documentation only |

| [2026-11-17-056-risk-management-research-stage-3-portfolio-stress-liquidity.md](2026-11-17-056-risk-management-research-stage-3-portfolio-stress-liquidity.md) | Phase 02 risk research: portfolio historical/stress risk, dependence and concentration, coherent scenarios, liquidity-adjusted close-out, VaR/ES limitations and verification; CME SPAN 2 reference only; crypto working papers treated as provisional; D-006/D-008 unchanged; documentation only |

| [2026-11-17-057-ideal-overall-vision-and-risk-stage-4-margin-collateral.md](2026-11-17-057-ideal-overall-vision-and-risk-stage-4-margin-collateral.md) | README reframed around IDEAL's overall integrated personal financial intelligence vision; crypto perpetuals clarified as initial research domain; Phase 02 risk research on margin, collateral, liquidation buffers, shadow reconciliation and procyclicality; no policy/implementation/phase changes |

| [2026-11-17-058-risk-management-research-stage-5-drawdown-loss-containment.md](2026-11-17-058-risk-management-research-stage-5-drawdown-loss-containment.md) | Phase 02 risk research: layered loss controls, daily/rolling/drawdown semantics, capital-flow accounting, containment states, emergency-action separation, anti-reset protections and adversarial tests; D-006/D-008 unchanged; no new policy or execution authority |

| [2026-11-17-059-risk-management-research-stage-6-strategy-model-ai-risk.md](2026-11-17-059-risk-management-research-stage-6-strategy-model-ai-risk.md) | Phase 02 risk research: strategy/model inventory, overfitting and validation, regime uncertainty, execution-model risk, drift/retirement, AI agent security boundaries, lifecycle gates and correlated model risk; no model or execution authority approved |

| [2026-11-17-060-risk-management-research-stage-7-emergency-recovery.md](2026-11-17-060-risk-management-research-stage-7-emergency-recovery.md) | Phase 02 risk research: independent emergency control plane, incident classes, safe-state/action ordering, NIST-aligned incident lifecycle, evidence preservation, clean recovery, account reconciliation, backups, manual fallback and incident exercises; no emergency execution or runtime authority |

| [2026-11-17-061-risk-management-research-stage-8-independent-assurance.md](2026-11-17-061-risk-management-research-stage-8-independent-assurance.md) | Phase 02 risk research: independent assurance cases, effective challenge, requirement/control/test traceability, layered testing, critical invariants, mutation resistance, model assurance, control monitoring and release gates; no implementation or phase advancement |

| [2026-11-17-062-risk-management-research-stage-9-cross-pillar-contracts.md](2026-11-17-062-risk-management-research-stage-9-cross-pillar-contracts.md) | Phase 02 risk research: provisional cross-foundation request/decision contracts, action-bound approvals, reservations, data provenance, health interlocks, security/policy integrity, telemetry, degraded modes and contract verification; no schema freeze or implementation |

| [2026-11-17-063-risk-architecture-reconciliation.md](2026-11-17-063-risk-architecture-reconciliation.md) | Consolidates risk research stages 1–9; records four-pillar boundaries, RM-01–RM-20 traceability, adversarial review, execution-authority wording corrections and unresolved owner decisions |

| [2026-11-17-064-integrated-foundation-traceability.md](2026-11-17-064-integrated-foundation-traceability.md) | System-wide requirements-to-controls-to-components-to-tests matrix for governance, risk, data integrity, health, security, audit and cross-pillar interfaces; records integrated failure scenarios and Phase 02 acceptance criteria |

| [2026-11-17-065-integrated-adversarial-review.md](2026-11-17-065-integrated-adversarial-review.md) | STRIDE-style integrated threat review; records autonomy/human-approval ambiguity, common-mode supervisor failure, policy root of trust, audit/action atomicity, time, privacy and recovery gaps |

| [2026-11-17-066-bounded-autonomy-governance.md](2026-11-17-066-bounded-autonomy-governance.md) | Records accepted D-023: bounded owner-authorised autonomy, reserved owner-approval actions, cross-pillar requirements and explicit no-execution boundary |

| [2026-11-17-067-autonomy-authority-and-permission-architecture.md](2026-11-17-067-autonomy-authority-and-permission-architecture.md) | Phase 02 research/design for bounded autonomy enforcement: owner envelope, workload identity, policy/root-of-trust, exact-action authorisation, independent risk reservation, revocation, audit, recovery, open-source candidate review and adversarial assurance; no tool adoption or implementation authority |

| [2026-11-17-068-adversarial-revocation-isolation-recovery-review.md](2026-11-17-068-adversarial-revocation-isolation-recovery-review.md) | Deep adversarial review of revocation/dispatch races, host/process/network isolation, root compromise, backup rollback and authority resurrection; adds ADV-19–ADV-30; no implementation or testing performed |

| [2026-11-17-069-supervisor-policy-root-audit-atomicity-review.md](2026-11-17-069-supervisor-policy-root-audit-atomicity-review.md) | Phase 02 design of restrictive-only health supervisor, immutable policy publication/key-role separation, and atomic local intent/reservation/audit/outbox/dispatch-start sequencing; ADV-31–ADV-38; no runtime tests or implementation |

| [2026-11-17-070-cross-document-state-machine-consistency-review.md](2026-11-17-070-cross-document-state-machine-consistency-review.md) | Cross-document reconciliation of health vs security authority, DISPATCH_STARTED, atomic local intent/reservation/audit/outbox, monotonic authority generation, reservation states, D-023 owner approval and ADV-39 approval-UI integrity |

| [2026-11-17-071-autonomy-authority-closure-assessment.md](2026-11-17-071-autonomy-authority-closure-assessment.md) | Consolidated Phase 02 bounded-autonomy workstream closure assessment: technology-neutral invariants, provisional recommendations, platform-dependent choices, deferred owner decisions and residual risks; no phase closure or implementation approval |

| [2026-11-17-072-integrated-system-domain-architecture.md](2026-11-17-072-integrated-system-domain-architecture.md) | Phase 02 integrated system/domain architecture: bounded-context catalogue and state ownership, authority hierarchy, cross-domain contracts, dependency/failure containment, financial semantics, archive/privacy/learning boundaries and future verification; updates roadmap, architecture, traceability matrix and README; no implementation, domain activation or phase advancement |

| [2026-11-17-073-data-trust-temporal-evidence.md](2026-11-17-073-data-trust-temporal-evidence.md) | Phase 02 data trust research: immutable raw evidence, bitemporal and point-in-time semantics, quality vectors, retention/privacy planes; current Akahu Personal App/full-app distinction, NZ Privacy Act section 27 nuance, CARF and tax-rule status; updates architecture, data integrity, personal finance research, traceability, roadmap and README; no integration or implementation |

| [2026-11-17-074-domain-risk-capital-architecture.md](2026-11-17-074-domain-risk-capital-architecture.md) | Phase 02 domain risk/capital design: separate domain risk taxonomies and authorities, capital ontology, honest portfolio aggregation, no implicit netting/hedge credit, D-006/D-008 scope preservation and D-018 capital autonomy; updates risk/core architecture, requirements, traceability, roadmap and README; no new limits or execution authority |

| [2026-11-17-075-governance-wording-consistency.md](2026-11-17-075-governance-wording-consistency.md) | Repository-wide audit found stale RULES.md wording implying paper trading was permitted and Phase 01 remained the active authority; corrected to no paper/live execution, Phase 02 architecture-only research under D-022, and D-006/D-007/D-008 scope limited to initial crypto-perpetual policy; no owner decision or permission changed |

| [2026-11-17-076-reconciliation-verified-recovery.md](2026-11-17-076-reconciliation-verified-recovery.md) | Phase 02 reconciliation and recovery architecture: fact-specific authority, mismatch lifecycle, venue/bank/tax reconciliation, incident containment, restore quarantine, scoped pillar attestations, audit/backup continuity and dependency-aware failure propagation; no runtime recovery or external reconciliation |

| [2026-11-17-077-integrated-architecture-review.md](2026-11-17-077-integrated-architecture-review.md) | Phase 02 whole-system desk review across governance, bounded contexts, four foundations, data temporal semantics, domain risk/capital, autonomy, tax/privacy, reconciliation and recovery; 24 adversarial scenarios and residual blockers; independent review still required; no implementation or phase advancement |

| [2026-11-17-078-cross-domain-accounting-examples.md](2026-11-17-078-cross-domain-accounting-examples.md) | Phase 02 synthetic cross-domain accounting/valuation fixtures: transfers, spot/perpetual exposure, funding/fees/MTM, collateral, bank pending/posting, tax reserve autonomy, stale FX and late corrections; updates architecture, risk, personal finance, traceability, roadmap and README; no real data or executed tests |

| [2026-11-17-079-data-retention-audit-policy.md](2026-11-17-079-data-retention-audit-policy.md) | Phase 02 data classification/retention/deletion/audit policy: C0–C3 classes, purpose registry, per-class retention, deletion propagation, backup/key and AI privacy boundaries; official NZ Privacy Act processor nuance and IRD cryptoasset seven-year record guidance; no retention technology or processor selected |

| [2026-11-17-080-host-trust-topology.md](2026-11-17-080-host-trust-topology.md) | Phase 02 host trust research: Android/CI/WSL2/Hyper-V/Linux KVM/Firecracker/cloud/two-host comparison; WSL is not a security boundary, VMs remain host-dependent, mobile data/background limits, separate gateway future option; no host selected or provisioned |

| [2026-11-17-081-integrated-state-machine-contracts.md](2026-11-17-081-integrated-state-machine-contracts.md) | Phase 02 cross-authority state-machine composition: policy/identity/security/health/data/risk/reservation/action/reconciliation/recovery; conjunctive admission, version-vector binding, restrictive precedence and dispatch-time recheck; no schemas or runtime selected |

| [2026-11-17-082-system-architecture-diagrams.md](2026-11-17-082-system-architecture-diagrams.md) | Phase 02 logical diagrams: domain/evidence flow, trust zones/forbidden flows, action admission/dispatch, incident recovery and temporal evidence lifecycle; physical topology diagrams remain deferred; no deployment or implementation |

| [2026-11-17-083-security-control-threat-matrix.md](2026-11-17-083-security-control-threat-matrix.md) | Phase 02 security assurance traceability: 10 protected asset classes, SEC-01–SEC-14 controls, 28 threat paths, owners, future tests and residual risks; design-level only, no runtime scans or certification |

| [2026-11-17-084-complexity-maintainability-review.md](2026-11-17-084-complexity-maintainability-review.md) | Phase 02 complexity review: preserve logical boundaries but avoid unnecessary microservices, databases, agents and always-on infrastructure; modular monolith/one durable store/deterministic services as provisional smallest design; canonical document ownership proposed; no files deleted or consolidated |

| [2026-11-17-085-canonical-contract-catalogue.md](2026-11-17-085-canonical-contract-catalogue.md) | Phase 02 canonical interface design: 22 contracts with owner/consumer, semantics, failure response, event envelope, value/time types, error taxonomy, versioning and transaction boundaries; no API or wire schema selected |

| [2026-11-17-086-requirement-traceability.md](2026-11-17-086-requirement-traceability.md) | Phase 02 requirement traceability: 34 requirement groups mapped to component owners, controls/contracts and future deterministic test IDs; tests are planned only, open semantics retained; updates REQUIREMENTS, traceability, architecture plan, roadmap and README |

| [2026-11-17-087-current-state-consistency.md](2026-11-17-087-current-state-consistency.md) | Repository-wide current-state scan: corrected stale RULES Phase 01-only instruction and EXECUTION_QUALITY_RESEARCH phase status; marked dated L2 status statements as historical; no runtime or policy changes |

| [2026-11-17-091-freshness-clock-contract.md](2026-11-17-091-freshness-clock-contract.md) | Phase 02 data freshness/clock contract: consumer-specific thresholds, event vs availability age, sequence/gap and tail-latency metrics, clock uncertainty and decision invalidation; no numeric thresholds or time service selected |


| [2026-11-17-088-architecture-document-map.md](2026-11-17-088-architecture-document-map.md) | Phase 02 canonical document ownership and source precedence formalised; architecture pack indexed; grouped unresolved decisions inventoried without approval; README/roadmap/plan/review updated; scoped local read-back only, no runtime or phase changes |

| [2026-11-17-092-critical-contract-schemas.md](2026-11-17-092-critical-contract-schemas.md) | Phase 02 logical field schemas for owner/security/health/risk/action/reconciliation/personal-finance/tax/audit/recovery contracts; digest/version-vector/idempotency and value semantics; no wire format, API or database selected |

| [2026-11-17-093-owner-decision-register.md](2026-11-17-093-owner-decision-register.md) | Draft consolidated Phase 02 owner decision register: 12 groups covering scope, D-006/D-008, portfolio/risk, bank/tax/data, host trust/recovery, audit and final architecture acceptance; not presented for approval |


| [2026-11-17-089-final-integrated-architecture-challenge.md](2026-11-17-089-final-integrated-architecture-challenge.md) | Final Phase 02 internal integrated challenge; corrected fiat/crypto AssetId semantics in canonical contracts; added R-CONTRACT-001 and T-ASSET-01–06; ten findings and remaining blockers recorded; no runtime tests, independent review or phase advancement |



| [2026-11-17-092-critical-contract-schemas.md](2026-11-17-092-critical-contract-schemas.md) | Phase 02 logical field schemas aligned to canonical fiat/crypto AssetId semantics; exact asset identity, amount precision, version vectors and idempotency; no wire format or database selected |
| [2026-11-17-093-owner-decision-register.md](2026-11-17-093-owner-decision-register.md) | Draft consolidated Phase 02 owner decision register: 12 groups covering scope, D-006/D-008, portfolio/risk, bank/tax/data, host trust/recovery, audit and final architecture acceptance; not presented for approval |

| [2026-11-17-090-official-source-revalidation.md](2026-11-17-090-official-source-revalidation.md) | Revalidated current NZ Privacy Act section 27/11 and IPP 12, IRD cryptoasset records/CARF/tax-bill status, NIST key management/crypto agility and Firecracker host hardening; documented CARF registration date conflict; updated canonical privacy/data/security sources; no legal conclusion or implementation |


| [2026-11-17-094-infrastructure-revalidation.md](2026-11-17-094-infrastructure-revalidation.md) | Revalidated SQLite WAL durability, NautilusTrader persistence semantics/ARM64 support, Firecracker production controls and OCI A1 free-tier conflicts; refined future acceptance gates; no component adoption or host selection |

| [2026-11-17-095-workload-sandbox-comparison.md](2026-11-17-095-workload-sandbox-comparison.md) | Compared gVisor, Kata Containers and Firecracker trust boundaries, operational costs and host assumptions; no runtime selected or deployed |

| [2026-11-18-096-policy-engine-security-evaluation.md](2026-11-18-096-policy-engine-security-evaluation.md) | Compared Cedar 4.15.0 and OPA 1.22.4; documented fail-closed wrapper semantics, recent parser/bundle-signature advisories, signed policy publication and deferred ODR-13 decision; no engine selected |

| [2026-11-18-097-owner-authenticator-recovery-research.md](2026-11-18-097-owner-authenticator-recovery-research.md) | Revalidated WebAuthn L3, NIST 800-63B-4, Android Keystore/StrongBox and FIDO recovery; distinguished synced/device-bound credentials and bound approval to exact action digest; no device/vendor selected |

| [2026-11-18-098-audit-integrity-external-witness-research.md](2026-11-18-098-audit-integrity-external-witness-research.md) | Compared local hash/Merkle integrity, Rekor/Tessera/Trillian and immudb; defined independent checkpoint and privacy boundaries; no external witness/database selected |

| [2026-11-18-099-margin-collateral-liquidation-architecture.md](2026-11-18-099-margin-collateral-liquidation-architecture.md) | Researched official Binance, Bybit, OKX and Hyperliquid margin/liquidation rules; documented venue-neutral collateral, tier, reservation and liquidation contracts; no venue or mode selected |

| [2026-11-18-100-integrated-architecture-challenge.md](2026-11-18-100-integrated-architecture-challenge.md) | Reopened integrated architecture challenge; corrected numbering; integrated margin schemas, liquidation/reservation composition and traceability; independent review remains open |

| [2026-11-18-101-documentation-integrity-and-review-refresh.md](2026-11-18-101-documentation-integrity-and-review-refresh.md) | Verified all 34 local Markdown targets in the Phase 02 document map; refreshed integrated/adversarial review status; independent assurance remains outstanding |

| [2026-11-18-102-document-map-structure-audit.md](2026-11-18-102-document-map-structure-audit.md) | Corrected duplicate Phase 02 map section numbering and verified ordered headings after read-back |

| [2026-11-18-103-phase-02-completion-readiness.md](2026-11-18-103-phase-02-completion-readiness.md) | Mapped all Phase 02 exit criteria and ODR-01–ODR-13; confirmed Phase 02 not complete pending independent reviews and owner acceptance |

| [2026-11-18-104-phase-02-map-link-reverification.md](2026-11-18-104-phase-02-map-link-reverification.md) | Re-fetched all 35 local Markdown targets after adding the Phase 02 readiness assessment; all exist |

| [2026-11-18-105-three-lens-review-and-assurance-limits.md](2026-11-18-105-three-lens-review-and-assurance-limits.md) | Records 15 internal findings across architecture, security/operations and testability; external independent review unavailable in this workstream |

| [2026-11-18-106-final-phase-02-document-map-link-audit.md](2026-11-18-106-final-phase-02-document-map-link-audit.md) | Fetched all 36 local Markdown targets in the Phase 02 document map and read back the readiness, decision register and review records |

| [2026-11-18-107-infrastructure-security-source-refresh.md](2026-11-18-107-infrastructure-security-source-refresh.md) | Updated Linux kernel and Firecracker lifecycle/security evidence; documented future host acceptance checks without selecting a platform |

| [2026-11-18-108-phase-02-source-refresh-verification.md](2026-11-18-108-phase-02-source-refresh-verification.md) | Fetch-back verification for checkpoint 107 and 38/38 document-map targets |

| [2026-11-18-109-canonical-serialization-contract-research.md](2026-11-18-109-canonical-serialization-contract-research.md) | Specifies deterministic digest/signature profile requirements; identifies JCS binary64 precision limitation and keeps JCS/CBOR unselected |


### Phase 02 — perpetual funding and mark-price semantics refresh (checkpoint 110, 18 November 2026)

Created [Perpetual Funding and Mark-Price Semantics Source Refresh](../IDEAL_PHASE_02_PERPETUAL_FUNDING_AND_MARK_PRICE_SEMANTICS_REFRESH.md). Official Binance, Bybit and OKX sources show funding intervals/limits and mark-price methods are contract-specific and may change; funding settlement affects margin state and must remain distinct from forecasts. Added effective-dated logical schemas, freshness and liquidation integration, and adversarial test requirements. No venue or formula selected; Phase 02 remains active.


### Phase 02 — perpetual funding and mark-price semantics refresh (checkpoint 110, 18 November 2026)

Created [Perpetual Funding and Mark-Price Semantics Source Refresh](../IDEAL_PHASE_02_PERPETUAL_FUNDING_AND_MARK_PRICE_SEMANTICS_REFRESH.md). Official Binance, Bybit and OKX sources show funding intervals/limits and mark-price methods are contract-specific and may change; funding settlement affects margin state and must remain distinct from forecasts. Added effective-dated logical schemas, freshness and liquidation integration, and adversarial test requirements. No venue or formula selected; Phase 02 remains active.


| [2026-11-18-111-funding-mark-price-integration-and-map-verification.md](2026-11-18-111-funding-mark-price-integration-and-map-verification.md) | Revalidated official perpetual funding/mark-price semantics; added funding, mark and margin event traceability; corrected checkpoint 110 map numbering; fetched all 42 current document-map targets; Phase 02 remains active and not complete |


| [2026-11-18-112-funding-api-event-state-and-history-coverage.md](2026-11-18-112-funding-api-event-state-and-history-coverage.md) | Refined funding API event-state typing, historical retention/coverage and linear/inverse denomination requirements; added logical schemas and T-FUND-04–06; no venue or API client selected |


| [2026-11-19-113-liquidation-account-mode-and-session-settlement-review.md](2026-11-19-113-liquidation-account-mode-and-session-settlement-review.md) | Distinguished isolated/cross/portfolio liquidation pathways, added session-settlement event model and risk/test traceability; no venue or account mode selected |


| [2026-11-19-114-risk-tier-completeness-and-portfolio-margin-review.md](2026-11-19-114-risk-tier-completeness-and-portfolio-margin-review.md) | Added pagination-complete risk tier snapshots, account-mode aggregation rules and scenario-based portfolio margin contracts; added R-MARGIN-011–014 / T-MARGIN-11–14 |
