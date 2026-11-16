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
