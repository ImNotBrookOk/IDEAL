# IDEAL Work Audit — Checkpoint 096

**Date:** 18 November 2026  
**Workstream:** Phase 02 — Cedar vs OPA authorization policy engine review  
**Status:** Research and documentation only.

## Work performed

Reviewed current official Cedar policy language authorization, validation and security documentation; Cedar Rust releases and GitHub advisories; OPA integration, bundle management and error documentation; OPA release history and GitHub advisories. Queried current-state research for dated changes, then verified relevant findings against primary project sources.

## Material findings

1. Cedar 4.15.0 was released 16 Nov 2026. Its authorization algorithm is default-deny and forbid-overrides-permit, but policy evaluation errors are skipped. A permit can still produce Allow while another policy errors. IDEAL's wrapper must reject any diagnostics/error, not consume the bare decision.
2. Cedar schema validation is a separate pre-publication/pre-activation operation, not automatically repeated during authorization. Schema changes can invalidate previously validated policies and cause evaluation errors. Validation must be bound to immutable schema and policy digests.
3. Cedar parser memory-exhaustion advisory GHSA-m84h-6f26-p3p7 (22 Oct 2026) affected Rust Cedar >=4.3,<4.13 and was fixed in 4.13.0. A crafted ~258-byte input could trigger ~29 GB allocation. v4.15 adds depth-limited parsing APIs. Future acceptance needs input size/depth/resource limits.
4. CedarJava is a distinct binding and had high-severity policy injection advisory CVE-2026-55773 / GHSA-qmch-v2q9-wg4p, patched at 2.3.6, 3.4.1 and 4.9.0. Do not infer binding security from the Rust crate.
5. OPA 1.22.4 was released 12 Nov 2026. OPA is general-purpose; a safe authorization decision must be explicitly authored. Undefined queries can return HTTP 200 without result, and some evaluation-time builtin errors become undefined by default. IDEAL must require exact Boolean true and reject undefined, missing, wrong-typed or error results.
6. OPA bundles are eventually consistent across instances. Built-in bundle persistence is best-effort and does not itself satisfy IDEAL's monotonic authority/revocation requirements. Bind the exact bundle digest/revision to action intent and independently fence stale dispatchers.
7. OPA high-severity GHSA-g2pf-6v5v-qcc8 (19 Oct 2026) affected versions through 1.21.2: missing keyid could bypass configured signature verification, and unsigned delta bundles could replace signed snapshots. Fixed in 1.21.3. Any future use requires signed snapshot policy bundles, explicit signer/key config, rollback tests and signature-negative tests.

## Disposition

No engine selected. Cedar is a narrower semantic fit for authorization if the trusted core is Rust; OPA is credible if the core is Go or a general policy plane is needed. Both require an IDEAL-owned fail-closed wrapper and immutable version/digest binding. Do not run both by default. Final choice remains deferred until language/runtime and topology are known.

## Repository changes

Created docs/IDEAL_POLICY_ENGINE_EVALUATION.md; updated component selection matrix, infrastructure research, owner decision register, Phase 02 architecture document map, roadmap and README; indexed this audit.

## Boundaries

No code, package, policy, runtime, host, account, credentials, exchange connectivity, financial record, paper/live execution, hosting or paid service was introduced. No tests, benchmarks, penetration tests or deployment validation were performed. No owner decision was accepted and no phase advanced. Phase 02 active; Phases 03–19 locked.
