# IDEAL Infrastructure Research — Phase 01

**Status:** Research only. No cloud account, VM, payment method or paid service has been created or connected.

## Executive result

Oracle Cloud Infrastructure (OCI) Always Free Ampere A1 is currently the leading candidate for a persistent, $0 general-purpose worker. It is not yet approved or verified: A1 capacity is region-dependent, idle instances may be reclaimed, and signup requires card verification with a temporary authorisation hold.

The exact IDEAL NautilusTrader POC pin, `nautilus_trader==2.0.0rc9`, now installs and passes all 71 tests on both x86_64 and ARM64 under Ubuntu 24.04 / Python 3.14.10. This removes a major ARM wheel compatibility risk, but does not prove performance on an actual A1 VM.

## 1. Oracle Cloud Always Free

Official sources:
- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
- [Oracle Cloud Free Tier FAQ](https://www.oracle.com/cloud/free/faq/)
- [Oracle Always Free resource documentation](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)
- [Oracle public cloud regions](https://www.oracle.com/cloud/public-cloud-regions/)
- [Oracle OCI region availability and capacity documentation](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm)

| Resource | Current documented Always Free allowance | IDEAL assessment |
|---|---:|---|
| Ampere A1 compute | 2 OCPU total, 12 GB RAM total | Plausible for one modest Python worker |
| Block volume | Up to 200 GB total | Sufficient for early SQLite/event journal if retention is controlled |
| Outbound transfer | Up to 10 TB/month | Likely sufficient for early research; measure actual feeds |
| Object storage | Always Free allowance applies | Candidate for off-host backups, verify exact quota and region |
| Availability | Subject to region/AD capacity | Major blocker; no guarantee of immediate A1 capacity |

### Regional constraints

- The Oracle public commercial region list shows Australia East (Sydney) and Australia Southeast (Melbourne) as the nearest public OCI regions to New Zealand.
- No New Zealand public OCI region is listed on the current public-region page.
- The home region is selected at signup and cannot later be changed. The selected home region determines Always Free resource availability.
- A1 capacity is not guaranteed. An out-of-host-capacity response means the instance cannot currently be created in that AD/region. Do not switch to paid capacity or upgrade to PAYG to bypass it.
- An Always Free A1 instance may be reclaimed if CPU, memory and network utilisation all remain below Oracle's documented idle thresholds for a sustained seven-day period. A continuously operating market-data worker may avoid the condition, but this cannot be assumed. Do not burn CPU artificially to defeat reclamation.
- Free-tier resources do not provide a production uptime SLA.

### Signup and billing boundary

Oracle requires a supported credit/debit card for identity/payment verification and may place a temporary authorisation hold. Oracle describes this as verification rather than a service charge. The account also begins with a time-limited trial-credit period, but Always Free resources can continue after that period if the account is not upgraded.

This still requires entering payment-card details. No signup was attempted. Do not proceed unless the owner explicitly accepts the verification requirement and temporary hold. Never upgrade to Pay As You Go; never create resources outside Always Free quotas.

## 2. NautilusTrader ARM64 compatibility

- PyPI release [NautilusTrader 2.0.0rc9](https://pypi.org/project/nautilus-trader/2.0.0rc9/) publishes a `cp314 manylinux_2_34_aarch64` wheel.
- Ubuntu 24.04 ARM64 provides glibc 2.39, above the wheel's glibc 2.34 baseline.
- IDEAL CI matrix [run 43757287905](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43757287905) verified:
  - x86_64: 71 tests passed.
  - ARM64: 71 tests passed.
  - Both used Python 3.14.10 and exact package version 2.0.0rc9.
- This confirms package/POC compatibility on ARM64. It does not establish Oracle A1 CPU performance, storage durability or capacity.

## 3. SQLite journal benchmark across architectures

Same CI run, 5,000 events per case, one SQLite WAL + synchronous FULL transaction per event:

| Architecture | Payload | Throughput | p50 | p95 | p99 | Peak RSS |
|---|---:|---:|---:|---:|---:|---:|
| x86_64 | 256B | 2,863/s | 0.158 ms | 0.390 ms | 0.896 ms | 35.6 MiB |
| x86_64 | 1,024B | 4,075/s | 0.161 ms | 0.372 ms | 0.694 ms | 35.6 MiB |
| ARM64 | 256B | 2,659/s | 0.320 ms | 0.791 ms | 1.294 ms | 34.4 MiB |
| ARM64 | 1,024B | 2,735/s | 0.326 ms | 0.555 ms | 1.019 ms | 34.4 MiB |

The runner reported four CPUs for both architectures; Oracle A1's Always Free allocation is two OCPU. x86 maximum write-latency outliers exceeded 100 ms in this run. Results vary materially between GitHub-hosted runner executions and are not a production SLO or a target-worker estimate.

## 4. Other free options

| Provider | Free offer | IDEAL suitability |
|---|---|---|
| Google Cloud | e2-micro free allowance restricted to selected US regions | Too small and geographically distant for the full worker |
| AWS | New-account free plan is time-limited, not a permanent general-purpose free VM | Not a long-term $0 worker |
| Cloudflare Workers | Free serverless request/CPU allowance | Useful for small API/control-plane functions, not a persistent NautilusTrader process |
| GitHub Actions | Public-repository CI runners | Good for scheduled/manual research and tests; not a persistent worker or durable data store |

## 5. Provisional architecture

If OCI A1 is available without a paid upgrade:
- One ARM64 Ubuntu 24.04 worker, limited to the Always Free 2 OCPU / 12 GB allocation.
- Python 3.14 and exact pinned dependencies.
- SQLite WAL event journal on persistent local block storage.
- Single-writer journal queue; periodic snapshots and WAL checkpoints.
- Encrypted off-host backups and externally signed hash anchors before any production use.
- GitHub Actions remains CI; Android remains the control plane.
- No direct exchange credentials until separately approved; paper mode only after Phase 01/02 gates.

If A1 capacity is unavailable, remain in GitHub Actions/manual research mode. No paid VM, PAYG upgrade or alternative provider with expiring credits.

## 6. Outstanding gates

1. Owner decision on whether card verification/temporary authorisation hold is acceptable.
2. Owner-approved home-region choice (Sydney or Melbourne) before account creation.
3. Confirm A1 capacity in the chosen region/AD without upgrading.
4. Confirm persistent boot/block volume stays within Always Free quotas.
5. Run the POC and 100k/1M event benchmarks on the actual A1 VM.
6. Measure CPU, memory, disk IOPS, disk growth, egress, restart time and idle-reclamation risk over a representative period.
7. Verify backups, restore and off-host hash anchoring.
8. No implementation/runtime deployment until Phase 01 exit and separate owner approval.

**Decision:** Oracle A1 remains a candidate only. No cloud resources have been provisioned, and $0 operation has not been proven.
