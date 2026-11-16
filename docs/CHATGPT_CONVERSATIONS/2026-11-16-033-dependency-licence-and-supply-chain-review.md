# 033 — Dependency licence and supply-chain review

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED

## Direct dependencies in the isolated research tooling

| Package | Current IDEAL pin | Current upstream version checked | Licence | Use / disposition |
|---|---|---|---|---|
| `nautilus_trader` | 2.0.0rc9 | 2.0.0rc9 latest v2; stable 1.231.0 | LGPL-3.0-only | Isolated engine POC only; not runtime adopted |
| `pytest` | 9.2.0 (upgrade CI running) | 9.2.0, released 27 Oct 2026 | MIT | Development/test-only |
| `orjson` | 3.11.3 | 3.13.0, released 7 Oct 2026 | 3.11.3: Apache-2.0 OR MIT; 3.13.0: MPL-2.0 AND (Apache-2.0 OR MIT) | Research parser / CI only; not runtime dependency |

Sources:
- NautilusTrader PyPI release and SPDX: https://pypi.org/project/nautilus-trader/2.0.0rc9/
- NautilusTrader upstream licence: https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/LICENSE
- pytest 9.2.0: https://pypi.org/project/pytest/9.2.0/
- orjson 3.11.3: https://pypi.org/project/orjson/3.11.3/
- orjson 3.13.0: https://pypi.org/project/orjson/3.13.0/

### Deliberate version decisions

- `pytest==8.4.2` was replaced with `pytest==9.2.0` (MIT) in commit `48358298ebf1bff0cef427a384e1cce3bac4d392`. CI [#43805067024](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43805067024) is verifying the full POC suite on x86_64 and ARM64. No pass is claimed until both jobs complete.
- Keep `orjson==3.11.3` for the current research workflows. Version 3.13.0 is newer, but its PyPI licence expression includes MPL-2.0 for some source files in addition to Apache-2.0 OR MIT. The current 3.11.3 version page reports Apache-2.0 OR MIT. Do not upgrade a research-only parser merely for recency without reviewing the changed licence expression and rerunning the high-volume alignment workloads.
- NautilusTrader `2.0.0rc9` is LGPL-3.0-only and a pre-release. Linking/combining obligations and any modification of the library require licence review before distribution. It remains an isolated POC and no source has been copied into IDEAL runtime.

## Upstream security and release posture — NautilusTrader

The upstream repository publishes a detailed security policy. It describes:
- signed and attested release artifacts;
- pinned Rust and Python dependency lockfiles and dependency publication cooldowns;
- CodeQL, OSV Scanner, pip-audit, cargo-audit, cargo-deny, cargo-vet and Zizmor workflows;
- Gitleaks and private-key screening;
- OpenSSF Scorecard reporting;
- SLSA-style build provenance and PyPI Trusted Publishing;
- immutable release tags and CODEOWNERS controls.

The 2.0.0rc9 release is signed with GitHub's verified release signature; PyPI states all 13 release files have provenance metadata. These are positive supply-chain controls, not a guarantee that the package is vulnerability-free or suitable for IDEAL. The upstream security policy also states that users extending the engine with their own dependencies must audit their own dependency trees.

Sources:
- https://github.com/nautechsystems/nautilus_trader/blob/develop/SECURITY.md
- https://nautilustrader.io/security/
- https://github.com/nautechsystems/nautilus_trader/releases
- https://pypi.org/project/nautilus-trader/2.0.0rc9/

## IDEAL gaps found

1. IDEAL POC requirements pin direct packages but do not currently lock all transitive Python dependencies with hashes. This is acceptable for a disposable research POC but not for a reproducible production build.
2. The research CI workflows pin direct `orjson` but do not commit a full resolved dependency lock or run a vulnerability scanner on the research parser dependency set.
3. No full SBOM or automated licence inventory has been generated for IDEAL's complete future dependency graph.
4. No IDEAL-specific `pip-audit`, OSV, secret scanning or GitHub Actions workflow lint/security scan has been run as a complete Phase 01 gate. Upstream NautilusTrader controls do not cover IDEAL's own code, workflows or future dependencies.
5. The direct dependencies are research-only and should not be interpreted as selected runtime dependencies.

## Disposition

- NautilusTrader remains the leading engine research candidate, LGPL-3.0-only, pre-release, not adopted.
- pytest 9.2.0 is a development/test dependency; awaiting x86_64/ARM64 POC CI.
- orjson 3.11.3 remains pinned for current high-volume research runs due to a simpler current licence expression and known-tested parser behaviour; evaluate 3.13.0 separately.
- Full transitive locking, IDEAL-specific vulnerability scanning, workflow security lint and complete licence/SBOM inventory remain open Phase 01 exit items.
- No runtime integration, paid service, exchange access, paper/live execution or phase unlock is authorised.
