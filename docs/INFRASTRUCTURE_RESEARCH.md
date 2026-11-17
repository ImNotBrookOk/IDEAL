# IDEAL Infrastructure Research — Phase 01

**Status:** Research only. No cloud account, VM, payment method or paid service has been created or connected.

## Executive result

Oracle Cloud Infrastructure (OCI) Always Free Ampere A1 is currently the leading candidate for a persistent, $0 general-purpose worker. It is not yet approved or verified: A1 capacity is region-dependent, idle instances may be reclaimed, and signup requires card verification with a temporary authorisation hold.

The exact IDEAL NautilusTrader POC pin, `nautilus_trader==2.0.0rc9`, now installs and passes all 84 tests on both x86_64 and ARM64 under Ubuntu 24.04 / Python 3.14.10 ([CI run 43762099188](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43762099188)); the prior 81-test run is [CI run 43761762953](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43761762953), and the 79-test run is [CI run 43760637330](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760637330). This removes a major ARM wheel compatibility risk, but does not prove performance on an actual A1 VM.

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
- No exchange credentials, paper or live execution are authorised. Any future paper simulator requires separate explicit owner approval after the architecture and legal/security/risk gates.

If A1 capacity is unavailable, remain in GitHub Actions/manual research mode. No paid VM, PAYG upgrade or alternative provider with expiring credits.

## 6. Outstanding gates

1. Owner decision on whether card verification/temporary authorisation hold is acceptable.
2. Owner-approved home-region choice (Sydney or Melbourne) before account creation.
3. Confirm A1 capacity in the chosen region/AD without upgrading.
4. Confirm persistent boot/block volume stays within Always Free quotas.
5. Run the POC and 100k/1M event benchmarks on the actual A1 VM.
6. Measure CPU, memory, disk IOPS, disk growth, egress, restart time and idle-reclamation risk over a representative period.
7. Verify backups, restore and off-host hash anchoring.
8. Phase 01 is closed, but Phase 02 architecture remains active. No implementation/runtime deployment until Phase 02 architecture acceptance and separate explicit owner approval.

**Decision:** Oracle A1 remains a candidate only. No cloud resources have been provisioned, and $0 operation has not been proven.


### 2.1 Later NautilusTrader POC expansion (15 November 2026)

The 71-test compatibility run above is an earlier checkpoint. The isolated POC was subsequently expanded to 84 tests and the exact 2.0.0rc9 pin passed on both x86_64 and ARM64:
- 79 tests: [CI #43760637330](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760637330).
- 81 tests: [CI #43761762953](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43761762953).
- 84 tests: [CI #43762099188](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43762099188).

The additional tests cover FX freshness/fail-closed conversion and a BTC-collateral/USDT-settled liquidation boundary. They do not prove consolidated reporting equity, cross-collateral accounting, exchange-equivalent liquidation or actual Oracle A1 performance. NautilusTrader remains a POC candidate, not an adopted runtime.


## 7. Host trust topology research — checkpoint 080

The host options have been re-evaluated against the current owner preference and threat model. Phone-first control remains the UX direction; the existing Windows PC is a fallback only if required; mobile phone data is a material bandwidth/availability constraint.

Key conclusions:
- Android remains the presentation/approval device, not a persistent high-frequency worker or independent supervisor.
- GitHub Actions remains ephemeral research CI, not a persistent runtime.
- WSL2 is a developer convenience, not a security sandbox or trust boundary from the Windows user.
- A full Hyper-V VM is a better explicit research isolation boundary than WSL2, but remains vulnerable to compromise of the physical host/administrator.
- A dedicated Linux/KVM host is a future self-hosted candidate; Firecracker requires KVM, jailer/cgroups/namespaces/seccomp and host-enforced egress filtering. It does not eliminate host-root or hardware risks.
- A separate physical action gateway/recovery trust domain is the strongest practical future option if host-root compromise is outside the accepted threat model; it adds cost and operational complexity.
- No current deployment is recommended. Inspect actual PC hardware/security posture only if a concrete later requirement justifies it.

See [IDEAL Host Trust Topology and Recovery Options](IDEAL_HOST_TRUST_TOPOLOGY_AND_RECOVERY_OPTIONS.md). No device inspection, configuration, account, purchase, hosting or security scan was performed.

Sources:
- https://github.com/microsoft/WSL/blob/master/doc/docs/technical-documentation/security.md
- https://learn.microsoft.com/en-us/windows/wsl/faq
- https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/plan-hyper-v-security-in-windows-server
- https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/
- https://developer.android.com/develop/background-work/background-tasks/bg-work-restrictions
- https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md


## 8. Infrastructure revalidation — checkpoint 094 (17 November 2026)

### 8.1 SQLite WAL-reset incident: version and test gate

Two primary engineering reports materially change the SQLite assurance checklist:

- Tailscale documented 19 database-corruption incidents over six months in a production single-writer SQLite deployment. The root cause was a WAL-reset race in the checkpoint path; the investigation also found committed writes that were not visible to later transactions in two cases.
- Antithesis reports that SQLite 3.51.3 fixed the WAL-reset bug. A generic concurrent writer/checkpoint workload reproduced the defect against 3.51.2 in 15 minutes; the same instrumented workload passed against 3.51.3.

Implications for IDEAL:
1. Any future SQLite POC must pin a SQLite runtime at or above 3.51.3 and record the actual runtime version from the library used by the application.
2. Python's sqlite3 wrapper version, system SQLite version and bundled/native extension version must not be conflated. Record `sqlite3.sqlite_version` (or equivalent runtime API) from the exact deployed process.
3. Add deterministic/fault-injection tests for concurrent writes and WAL checkpoints, committed-write visibility, process termination at transaction boundaries, `PRAGMA integrity_check`, backup consistency, restore and replay.
4. Keep one authoritative writer per database file unless a separately tested design proves otherwise. Do not assume a single-writer design eliminates engine-level races.
5. Use SQLite's supported backup mechanisms or a proven consistent snapshot procedure; copying a live database file without a consistent snapshot contract is not an acceptable backup design.
6. Keep audit/authority transaction atomicity and independent off-host backup/hash anchoring as IDEAL-owned requirements; WAL mode is not a substitute for them.

This is a design/test requirement, not evidence of corruption in IDEAL. No database was created or tested in this checkpoint.

Sources:
- https://tailscale.com/blog/sqlite-wal-reset-bug
- https://antithesis.com/blog/2026/wal-reset-bug/

### 8.2 OCI Always Free quota documentation conflict

The current Oracle general Always Free resources page states 1,500 OCPU-hours and 9,000 GB-hours per month for A1, equivalent to 2 OCPUs and 12 GB continuously. Oracle's A1-specific compute page states 3,000 OCPU-hours and 18,000 GB-hours. These are conflicting official pages.

The conservative interpretation for any future estimate is the lower general Always Free allowance until Oracle resolves the discrepancy or the tenancy console/contract confirms the applicable quota. The general page also confirms:
- A1 capacity is home-region constrained and can return "out of host capacity";
- idle Always Free compute can be reclaimed when CPU, network and (for A1) memory utilisation remain below 20% at the 95th percentile over seven days;
- a paid-account upgrade does not make an individual A1 shape available by guarantee;
- quota/compartment limits are not a hard spending cap.

No account, region, quota, capacity or pricing was tested for IDEAL. No provisioning or upgrade is authorised.

Sources:
- https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- https://docs.oracle.com/en-us/iaas/Content/Compute/References/arm.htm

### 8.3 NautilusTrader current platform and persistence semantics

Current upstream installation documentation lists Ubuntu Linux ARM64 as a supported platform. This aligns with the isolated POC's x86_64/ARM64 compatibility evidence, but it is not an OCI A1 performance benchmark.

The current architecture documentation also describes a critical persistence boundary: cache insertion/publication may proceed despite synchronous persistence/enqueue errors, and asynchronous database failures do not roll back in-memory cache state. IDEAL must therefore own its durable ledger, audit, intent, reservation, outbox and reconciliation semantics outside the engine's cache. The engine may be a trading-system component, not the system-of-record for financial authority or accounting.

Sources:
- https://nautilustrader.io/docs/latest/getting_started/installation/
- https://nautilustrader.io/docs/latest/concepts/architecture/
- https://nautilustrader.io/docs/latest/concepts/overview/


## 8. Infrastructure revalidation — checkpoint 094 (17 November 2026)

### 8.1 SQLite WAL-reset incident: version and test gate

Tailscale documented 19 database-corruption incidents over six months in a production single-writer SQLite deployment. The root cause was a WAL-reset race in the checkpoint path; two incidents also exposed committed writes that were not visible to later transactions. Antithesis reports SQLite 3.51.3 fixed the bug. A generic concurrent writer/checkpoint workload reproduced the defect against 3.51.2 in 15 minutes and passed against 3.51.3.

Any future SQLite POC must: (1) pin a SQLite runtime >=3.51.3 and record the actual linked runtime version; (2) distinguish Python wrapper, system library and bundled/native extension versions; (3) test concurrent writes/checkpoints, committed-write visibility, process termination at transaction boundaries, integrity_check, backup consistency, restore and replay; (4) retain one authoritative writer per DB file unless a different design is separately proven; and (5) use a supported consistent backup procedure rather than copying a live database file without a snapshot contract. WAL mode and synchronous FULL alone are not a complete durability case.

This is a future test requirement, not evidence of corruption in IDEAL. No database was created or tested.

Sources: https://tailscale.com/blog/sqlite-wal-reset-bug ; https://antithesis.com/blog/2026/wal-reset-bug/

### 8.2 OCI Always Free quota documentation conflict

Oracle's general Always Free resources page states 1,500 OCPU-hours and 9,000 GB-hours per month for A1, equivalent to 2 OCPUs and 12 GB continuously. Oracle's A1-specific compute page states 3,000 OCPU-hours and 18,000 GB-hours. Both are official pages. Use the lower general allowance conservatively until Oracle resolves the discrepancy or tenancy-level evidence confirms the applicable quota. The general page also confirms home-region capacity constraints, seven-day idle reclamation thresholds (CPU/network <20% at p95 and memory <20% for A1), and that PAYG upgrade does not guarantee physical capacity. Quotas/compartment limits are not a hard spending cap.

No account, region, quota, capacity or pricing was tested for IDEAL. No provisioning or upgrade is authorised.

Sources: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm ; https://docs.oracle.com/en-us/iaas/Content/Compute/References/arm.htm

### 8.3 NautilusTrader current platform and persistence semantics

Current upstream installation docs list Ubuntu Linux ARM64 as supported. This aligns with IDEAL's isolated architecture test coverage, but is not an OCI A1 performance benchmark.

Current architecture docs describe asynchronous database persistence from an in-memory cache. Synchronous persistence/enqueue errors may be logged without preventing cache insertion/publication, and later asynchronous database errors do not roll back in-memory state. IDEAL must own its durable ledger, audit, intent, reservation, outbox and reconciliation semantics outside the engine cache. The engine is a component, not the system-of-record for financial authority or accounting.

Sources: https://nautilustrader.io/docs/latest/getting_started/installation/ ; https://nautilustrader.io/docs/latest/concepts/architecture/ ; https://nautilustrader.io/docs/latest/concepts/overview/


## 9. Workload sandbox comparison — checkpoint 095 (17 November 2026)

Official project documentation supports three distinct isolation models:

| Runtime | Model | Main trust assumptions | Operational profile |
|---|---|---|---|
| gVisor/runsc | Userspace Sentry implements Linux system API; guest application syscalls are not passed directly through | Host kernel/platform and cgroups remain trusted; Sentry and Gofer are part of trusted computing base; host-network/passthrough modes expand host API exposure | Potentially less infrastructure than a VM; compatibility/performance trade-offs; still requires host egress/resource policy |
| Kata Containers | Containerd/CRI-managed VM with guest kernel, guest agent and hypervisor/VMM | Host kernel, VMM, virtual devices, guest agent, host/guest control channel and configuration are in the trust boundary | Integrates VM isolation into container orchestration but adds runtime/shim, guest image/kernel, VMM and IPC lifecycle complexity |
| Firecracker | KVM microVM; one VM per Firecracker process, minimal VirtIO device model | Host kernel/KVM, Firecracker VMM, jailer, TAP/network policy, host resource controls and monitoring remain trusted | More direct microVM control and smaller device model, but substantial host-specific setup and operations |

### IDEAL disposition

No runtime is selected. For a future single-host research worker, gVisor is a reasonable first compatibility experiment if untrusted strategy/agent code must be run and the threat model does not require a separate guest kernel. It is not a substitute for VM isolation against host-root/kernel compromise. If a guest-kernel boundary is required, compare Firecracker and Kata on the actual host rather than selecting by general marketing or assumed performance.

A decision requires a bounded benchmark and negative-test plan covering filesystem/IPC exposure, network egress allowlists, metadata/loopback reachability, process/resource exhaustion, kernel attack surface, host/guest compromise assumptions, startup/throughput overhead, observability and recovery. No sandbox receives credentials or unrestricted egress.

Sources:
- https://gvisor.dev/docs/architecture_guide/security/
- https://gvisor.dev/docs/architecture_guide/networking/
- https://gvisor.dev/blog/2020/04/02/gvisor-networking-security/
- https://kata-containers.github.io/kata-containers/design/architecture/
- https://github.com/kata-containers/kata-containers/blob/main/docs/threat-model/threat-model.md
- https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md


## 10. Authorization policy engine review — checkpoint 096 (18 November 2026)

The current official Cedar and OPA documentation and security advisories were rechecked. Cedar 4.15.0 is the current observed release; Cedar's Rust parser memory-exhaustion advisory was fixed in 4.13.0, and 4.15 provides depth-limited parser APIs. Cedar's skip-on-error authorization semantics mean IDEAL must deny if any policy diagnostic is returned, even when the overall decision is Allow. Cedar schema validation is separate from runtime authorization and must be mandatory before activation.

OPA 1.22.4 is the current observed release. Its high-severity bundle signature bypass was fixed in 1.21.3. OPA policy bundles update eventually consistently; undefined decisions may return no result and some evaluation errors become undefined. A future wrapper must require exact Boolean true, reject missing/undefined/error/stale results, require signed snapshots and bind active bundle digest/revision to the action version vector.

CedarJava is a separate binding with a distinct high-severity policy injection advisory (CVE-2026-55773), patched in 2.3.6 / 3.4.1 / 4.9.0. No binding is selected. See [Policy Engine Evaluation](IDEAL_POLICY_ENGINE_EVALUATION.md) for the full comparison, sources and unexecuted acceptance plan.
