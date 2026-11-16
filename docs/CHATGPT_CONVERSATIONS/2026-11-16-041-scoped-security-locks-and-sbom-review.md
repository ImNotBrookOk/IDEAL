# 041 — Scoped dependency security, hash locks and SBOM review

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED

## Audit execution

Latest completed security audit: [GitHub Actions #43807450930](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43807450930), commit `b9eacf48e71989a3ba873179393acdadc9af9e38`, artifact [14198233799](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43807450930/artifacts/14198233799), 14,799 bytes, SHA-256 `ea5097519b5938528b4f7ecdc583f58a76e393938ebfaec2112ea0cecac6d2b9`.

Tools were pinned for the audit run: Python 3.14.10, uv 0.13.8, pip-audit 2.10.1, zizmor 1.32.0 and cyclonedx-bom 7.5.0.

## Results

| Control | Result | Scope / limitation |
|---|---|---|
| Parser dependency vulnerability scan | PASS — 0 known vulnerabilities | One resolved package: orjson 3.11.6 |
| Nautilus POC dependency vulnerability scan | PASS — 0 known vulnerabilities | Six resolved packages: NautilusTrader 2.0.0rc9, pytest 9.2.0 and four transitive packages |
| Hash-pinned dependency locks | PASS | Universal Python 3.14 locks generated, installed with uv sync, committed on research branch, and compared against regenerated locks by the successful workflow |
| CycloneDX SBOM | PASS — generated and retained | Parser and Nautilus POC environments; current research environments only, not a future complete product SBOM |
| Zizmor workflow scan | PASS WITH LIMITS | No findings reported across nine workflow files; ran offline by default and reported one suppressed finding. Offline mode omits some audits; do not treat as complete online analysis |
| Full repository / future dependency inventory | OPEN | These reports cover only the two explicitly resolved research environments |

The previous preliminary note about four findings in two packages is superseded for the current lockfiles by this completed scan: the latest reports contain zero vulnerability records. Do not infer that each earlier finding was individually remediated without matching the earlier report to the final package set. Current evidence is the final locked environment scan.

## Hash-lock and SBOM files

The following files exist on `research/okx-l2-sample-2026-11-16` and were regenerated/compared successfully by the audited workflow:

- `research/requirements.lock`
- `research/nautilus_poc/requirements.lock`
- `research/sbom/2026-11-16-parser.cdx.json`
- `research/sbom/2026-11-16-nautilus-poc.cdx.json`

The SBOMs describe the exact resolved environments. Parser environment contains orjson only. Nautilus POC contains NautilusTrader 2.0.0rc9 (LGPL-3.0-only), pytest 9.2.0 (MIT), iniconfig 2.3.1 (MIT), packaging 26.3 (Apache-2.0 OR BSD-2-Clause), pluggy 1.7.0 (MIT), and Pygments 2.21.0 (BSD-2-Clause).

## orjson licence/security trade-off

The final parser pin is `orjson==3.11.6`, not the earlier `3.11.3` pin. PyPI reports 3.11.3 as Apache-2.0 OR MIT, whereas 3.11.6 adds MPL-2.0-covered source files and declares `MPL-2.0 AND (Apache-2.0 OR MIT)`. The upstream changelog states 3.11.6 added code licensed under MPL-2.0.

This is a deliberate security trade-off: orjson 3.11.3 is in the affected range for CVE-2025-67221 (uncontrolled recursion / denial-of-service in `dumps()`); the advisory's fixed version is 3.11.6. The final pinned version has zero known vulnerabilities in the current pip-audit report. Keep 3.11.6 for the current internal research parser; do not downgrade solely to simplify the licence expression. Before distribution or product integration, review MPL-2.0 file-level obligations and preserve corresponding notices/source-offer compliance where applicable.

Sources:
- PyPI 3.11.3 licence: https://pypi.org/project/orjson/3.11.3/
- PyPI 3.11.6 licence: https://pypi.org/project/orjson/3.11.6/
- Upstream changelog: https://github.com/ijl/orjson/blob/master/CHANGELOG.md
- CVE-2025-67221 advisory summary: https://security.snyk.io/package/pip/orjson/3.11.3

## Zizmor residual

The successful run audited nine workflow files and reported no findings, with one suppressed finding. It ran in offline mode by default; some checks are unavailable offline. Preserve this as a successful preliminary workflow lint, not a complete online security review. Before Phase 01 closes, inspect the suppression's identity and decide whether online mode is warranted; keep action references pinned to full commit SHAs and least-privilege token permissions.

## Disposition and remaining work

- **Scoped dependency vulnerability gate: PASS** for the parser and Nautilus POC lockfiles at the audited commit.
- **Scoped hash-lock gate: PASS**; permanent lock files are present on the research branch and the workflow verifies reproducibility.
- **Scoped SBOM/licence inventory: PASS WITH LIMITS**; two environment SBOMs retained on the research branch.
- **Workflow security lint: PASS WITH LIMITS**; offline scan, one suppressed finding to inspect.
- **Phase 01 security/supply-chain gate: PARTIALLY CLOSED**, not globally closed. Remaining work: inspect the suppressed finding, decide on online workflow analysis, review the full repository's other scripts/tooling and document whether they are in-scope dependencies, and ensure the audit workflow itself is covered by its own policy.

No runtime dependency adoption, paid service, exchange access, paper/live execution or Phase 02 work is authorised.


## Follow-up: online auditor-persona workflow scan and remediation

The initial regular-persona online scan [#43825525763](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43825525763) passed: both pip-audit environments had zero vulnerability records and zizmor reported no findings. To remove the offline-mode limitation and inspect the earlier suppressed result, the audit workflow was updated to pass the least-privilege `GITHUB_TOKEN` (contents: read) and run zizmor in its `auditor` persona.

The auditor-persona run [#43825594880](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43825594880) surfaced one low-severity `concurrency-limits` finding in `.github/workflows/nautilus-poc.yml`: multiple superseding POC runs could run concurrently. This was a genuine efficiency/race-control weakness, not dismissed as noise. Added a workflow concurrency group keyed by workflow and ref with `cancel-in-progress: true`.

Final verification on commit `2911ec3bd05221b7434257d528bf8a7ccee19ffa`:
- Security audit [#43825684618](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43825684618): **SUCCESS**. Hash-lock regeneration/comparison, locked installs, both SBOM generations, both pip-audit scans (zero vulnerability records) and online zizmor auditor-persona scan all passed. Zizmor reported **no findings** across nine workflow files.
- Nautilus POC CI [#43825684604](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43825684604): **SUCCESS**, 84 tests passed on x86_64 and 84 on ARM64; SQLite journal benchmark step also completed.
- The temporary malformed workflow edit in commit `ccf4a91963fd43a7db796fb31cf6d4a065615e32` failed before any job started; corrected in the next commit and superseded by successful online run #43825525763. No research code or dependency lock was changed by that transient failure.

## Updated disposition

- Scoped parser/POC vulnerability scan: **PASS**.
- Hash-pinned research dependency locks: **PASS**.
- Scoped CycloneDX SBOMs and package licence inventory: **PASS WITH LIMITS**; only the two current research environments, not a future product dependency graph.
- Online zizmor auditor-persona scan: **PASS** after fixing the low-severity concurrency finding.
- Research CI concurrency: bounded for Nautilus POC by workflow/ref group; no overlapping superseded runs.
- Remaining supply-chain boundary: runtime/product dependencies do not yet exist and are not certified by this scoped audit. Retain the orjson 3.11.6 MPL-2.0 notice review before distribution.
