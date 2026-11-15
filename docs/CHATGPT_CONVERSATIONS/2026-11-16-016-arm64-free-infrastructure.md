# IDEAL Conversation Record 016 — ARM64 Compatibility and Always-Free Infrastructure

**Date:** 16 November 2026  
**Scope:** Phase 01 infrastructure research — ARM64 POC validation, SQLite benchmark comparison and free-tier compute assessment  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #22 merged; 71 tests pass on x86_64 and ARM64. Oracle A1 remains an unprovisioned candidate.

## Available user-visible transcript

### User
> Ok keep going

### Assistant
Continued the infrastructure and capacity research. Oracle Cloud Always Free Ampere A1 is the leading candidate for a $0 persistent worker, but availability, idle reclamation, signup card verification and persistent-volume guarantees remain unresolved. The exact NautilusTrader POC has now been tested on ARM64.

## Operational audit log

### 1. Cross-architecture CI

Updated `.github/workflows/nautilus-poc.yml` to run a matrix:
- `ubuntu-24.04` x86_64
- `ubuntu-24.04-arm` ARM64

[Final PR-head CI run 43757521619](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43757521619):
- x86_64: **71 tests passed in 0.39s**.
- ARM64: **71 tests passed in 0.54s**.
- Exact `nautilus_trader==2.0.0rc9`, Python 3.14.10, Ubuntu 24.04 / glibc 2.39.
- PyPI provides a `cp314 manylinux_2_34_aarch64` wheel; Ubuntu 24.04 glibc 2.39 satisfies the wheel baseline.
- Both jobs completed successfully.

This validates ARM64 package/POC compatibility, not actual Oracle A1 performance.

### 2. Cross-architecture SQLite benchmark

Same CI run, 5,000 events per case, SQLite WAL + synchronous FULL:

| Architecture | Payload | Throughput | p50 | p95 | p99 | Peak RSS |
|---|---:|---:|---:|---:|---:|---:|
| x86_64 | 256B | 2,863/s | 0.158 ms | 0.390 ms | 0.896 ms | 35.6 MiB |
| x86_64 | 1,024B | 4,075/s | 0.161 ms | 0.372 ms | 0.694 ms | 35.6 MiB |
| ARM64 | 256B | 2,659/s | 0.320 ms | 0.791 ms | 1.294 ms | 34.4 MiB |
| ARM64 | 1,024B | 2,735/s | 0.326 ms | 0.555 ms | 1.019 ms | 34.4 MiB |

The runners each reported four CPUs. Oracle Always Free A1 has two OCPU. x86 write-latency maxima exceeded 100 ms in this run, showing noisy hosted-disk behavior. These figures are not a stable architecture ranking or a production SLO.

### 3. Free-tier infrastructure assessment

Added [`docs/INFRASTRUCTURE_RESEARCH.md`](INFRASTRUCTURE_RESEARCH.md), updated `ARCHITECTURE.md`, `ROADMAP.md`, POC README and execution realism report.

Findings:
- Oracle Always Free Ampere A1: 2 OCPU / 12 GB RAM, up to 200 GB block storage and 10 TB monthly outbound transfer within Always Free quotas.
- Oracle public region list shows Sydney and Melbourne as the nearest public OCI regions to New Zealand; no New Zealand public OCI region is listed.
- Home region is selected at signup and cannot later be changed.
- A1 capacity is region/availability-domain dependent; out-of-host-capacity can block instance creation. Do not upgrade to paid capacity.
- Oracle may reclaim A1 instances after all documented CPU, memory and network utilisation metrics remain below idle thresholds over seven days.
- Signup requires supported credit/debit card verification and may place a temporary authorisation hold. Oracle describes it as verification rather than a service charge.
- No account was created, no card details entered and no VM provisioned.
- Google Cloud e2-micro free allowance is US-region restricted and small.
- AWS new-account free plan is time-limited rather than a permanent general-purpose VM.
- Cloudflare Workers Free is useful for lightweight API/control-plane work, not a persistent NautilusTrader Python process.
- GitHub Actions public-repository CI is suitable for tests/research, not an always-on worker or durable storage.

### 4. Infrastructure decision

Oracle A1 remains the leading candidate, not an approved deployment. No home region has been selected and no signup attempted. Before any account creation, the owner must decide whether card verification/temporary hold is acceptable. Capacity must be verified without PAYG upgrade. If capacity is unavailable, remain in GitHub Actions/manual research mode.

### 5. Five-axis review and merge

- **Correctness:** exact pinned package installs and all 71 tests pass on both architectures.
- **Security:** no credentials, account signup, VM creation or network exchange access.
- **Cost:** public-repo CI only; no paid cloud resources or dependencies.
- **Maintainability:** CI matrix is explicit; infrastructure findings and limits are documented.
- **Scope:** workflow/docs only; no runtime implementation or trading permissions changed.
- Final PR head `ec63dfcd5eb78eed8a7999db8fdb3763cb601d76` matched branch ref before merge.
- [PR #22](https://github.com/ImNotBrookOk/IDEAL/pull/22) squash-merged under D-012.
- Merge commit: `32207a1e345aedf1f9698e06e555d0a3a7b024c2`.

## Documentation updated

- [Infrastructure research](https://github.com/ImNotBrookOk/IDEAL/blob/main/docs/INFRASTRUCTURE_RESEARCH.md)
- [Architecture](https://github.com/ImNotBrookOk/IDEAL/blob/main/ARCHITECTURE.md)
- [Roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md)
- [POC README](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/README.md)
- [Execution realism report](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md)

## Remaining Phase 01 work

- Actual Oracle A1 availability, persistent-volume and performance proof (requires owner decision on signup card verification; not yet authorised).
- Extend amendment tests for price changes, quantity decreases and no-op modifications.
- Multi-currency account funding and same-engine recovery after funding FX failure remain open.
- Venue-specific queue priority and empirical market-impact calibration remain blocked on venue/data selection.
- Stable release pin and full component licence review.
- Adapter and final component selection matrix.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- POC: 71 tests passing on x86_64 and ARM64.
- Oracle A1: candidate only; no account or VM.
- No exchange account, adapter, credentials, paper/live trading or paid service introduced.
