# IDEAL Host Trust Topology and Recovery Options

**Status:** Phase 02 architecture research; no host or topology selected  
**Checkpoint:** 080 — 17 November 2026  
**Scope:** Phone-first control plane, Windows PC fallback, local/cloud worker options, trust-domain separation and recovery topology  
**Authority:** D-020, D-021, D-022, D-023; existing hosting disposition in COMPONENT_SELECTION_MATRIX  
**Boundary:** Research only. No device inspection, host provisioning, configuration, account creation, paid service, remote-access tunnel, credential, security scan or deployment is authorised.

## 1. Executive conclusion

The cheapest defensible near-term architecture is **phone as a presentation/owner-control device, with no always-on financial runtime**. Use GitHub Actions only for research CI and manual/scheduled offline jobs. If later work genuinely requires a persistent local worker, evaluate the existing Windows PC as a research/data worker after inspecting its hardware and security posture; do not assume it is suitable as the sole security/authority host.

A Windows PC running WSL2 is convenient for development, but Microsoft explicitly says WSL is not a security sandbox and that code in WSL should be treated at the same trust level as the launching Windows user. WSL distributions are not security boundaries from that Windows user. It must not be treated as the isolation boundary for untrusted AI/strategy code or a protected action gateway.

A full Hyper-V Linux VM offers a more explicit VM boundary than WSL2, but it remains on the same physical Windows host. A host administrator/root compromise can control the VM and its data. It is a useful candidate for isolated research workloads, not independent protection against host compromise.

If IDEAL eventually receives authority to perform consequential external actions, the action gateway, owner/recovery trust and independent watchdog require a separately analysed trust domain. A second physical host is the strongest practical separation candidate, but it increases cost and operational complexity. No such capability is approved now.

## 2. Owner constraints carried into the topology

- Phone-first control and monitoring is the preferred user experience.
- An existing Windows PC/laptop is a fallback only if a concrete requirement needs it; it is not presumed always-on.
- Internet access is via mobile phone data. Treat bandwidth, data caps, tethering, latency, connectivity loss and device battery as material constraints.
- Avoid continuous high-volume feed ingestion over mobile data unless independently justified and explicitly approved.
- Prefer local processing, batch downloads, resumable transfers, compressed datasets and scheduled sync.
- No host provisioning, inbound ports, paid infrastructure or PC configuration is authorised.
- The phone is not the sole trusted clock, durable database, policy root, health supervisor or high-frequency worker.

## 3. Topology options

| Option | Cost profile | Strengths | Material weaknesses | Disposition |
|---|---|---|---|---|
| Android phone only | No new hardware | Best owner UX; mobile authenticator/notification device | OS background restrictions, battery/network dependence, small storage/thermal envelope, device loss; not suitable as sole persistent worker or independent supervisor | Presentation/owner control only |
| GitHub Actions | Existing CI usage; quota-bound | Reproducible ephemeral research/test jobs; no always-on host | Ephemeral, workflow quotas, no durable high-frequency process, no persistent safety supervisor or reliable execution gateway | Keep for research CI/offline jobs |
| Windows PC + WSL2 | Existing hardware; no incremental host cost | Convenient Linux development, low overhead, Windows desktop integration | WSL is explicitly not a security sandbox; same Windows user trust; Windows files/network integration; managed VM may auto-stop; not a production trust boundary | Development/research candidate only |
| Windows PC + Hyper-V Linux VM | Existing hardware; moderate configuration/ops cost | Explicit VM lifecycle, separate guest kernel/filesystem, Secure Boot/vTPM options, resource controls | Same physical host and host administrator; shared power/network/storage; host compromise defeats guest trust; hardware/edition support unknown | Candidate for isolated research worker after inspection; not independent action trust |
| Dedicated Linux PC/mini-PC + KVM | New or repurposed hardware cost; ongoing power/maintenance | Native Linux controls, KVM isolation, local storage, no Windows integration path | Hardware cost, patching/backup responsibility, power/network dependency; host root still controls guests | Future self-hosted worker candidate if justified |
| Linux + Firecracker microVMs | Additional engineering/ops cost on KVM host | Lightweight VM isolation, seccomp, jailer, cgroups/namespaces and privilege drop | Requires KVM and careful host/egress setup; does not itself filter guest network; host/kernel/hardware compromise remains; operational complexity | High-risk workload candidate only after host exists and threat model justifies |
| Cloud VM | Variable recurring cost; free-tier uncertainty | Remote uptime/location separation from home device; managed power/network | Provider control plane, identity/IAM exposure, internet dependency, cost/egress/storage limits, regional availability; no guaranteed $0 production host | Deferred; no account/resource provisioning |
| Two-host worker + action gateway | Highest cost/complexity among local options | Separates untrusted research/data workloads from protected dispatch and recovery trust | More hardware, network partitions, independent patching/monitoring, key management and failure-mode complexity | Preferred future pattern if execution authority is ever approved and threat model requires host-root separation |

## 4. Windows PC and WSL2 implications

Microsoft's WSL security guidance states that WSL is not a security sandbox for untrusted code. Code in WSL should be treated with the same trust level as the Windows user that launched it; WSL distributions do not create a security boundary from that Windows user or other distributions running for that user.

Microsoft's WSL FAQ also describes the utility VM's automatic lifecycle and Windows file access/integration. This is useful for development, but those same integration conveniences increase the need to treat WSL as part of the user's Windows trust domain.

**Result:** WSL2 may be used as a developer convenience in a future approved workflow, but not as the sole containment boundary for arbitrary strategy/agent code, secret-bearing services or a protected action gateway.

A conventional Hyper-V VM is a stronger isolation mechanism for research workloads, but it is not independent of the host. Microsoft recommends securing the Hyper-V host, keeping firmware/OS updated, minimising host software, using BitLocker, restricting VM administrator rights, enabling Secure Boot for supported Gen 2 VMs and considering TPM 2.0/guarded-fabric protections. The host still controls VM configuration and virtual disks; host administrator compromise remains a common-mode failure.

## 5. Host security baseline candidates

If a Windows PC is later approved for research-worker use, inspect and verify before storing any C2/C3 data:
- Windows edition/build and supported security updates;
- TPM 2.0 presence and firmware state;
- UEFI Secure Boot status;
- BitLocker/device encryption status and recovery-key custody;
- Windows Defender/endpoint protection and firewall;
- local administrator inventory and separate least-privilege IDEAL service identity;
- startup applications, remote access, exposed ports and installed software;
- patch and reboot policy;
- disk health, free capacity and backup destination;
- power/sleep behaviour and mobile-hotspot failure behaviour.

BitLocker with TPM can help protect data at rest and detect some offline boot tampering. It does not protect against malware or an already compromised logged-in host. Recovery-key storage must be deliberate; a cloud-backed recovery key may create a separate account-security dependency. Secure Boot/TPM are foundations, not proof of a clean host.

Do not run untrusted agent code as administrator. Do not store owner root keys, recovery material or future exchange credentials in the same user profile or VM as strategy/AI code. No credential store or host control is selected.

## 6. Linux KVM and Firecracker implications

Firecracker is not a drop-in security guarantee. Official documentation requires KVM and describes a production jailer that applies cgroups/namespaces and drops privileges. Firecracker uses seccomp filters, but its own production host guide states that network traffic filtering must be implemented by the host; packets are forwarded to the TAP device and a malicious guest may reach restricted destinations unless host firewall rules prevent it. Host and guest kernels, microcode, hardware and egress controls remain in scope.

This makes Firecracker a candidate for isolating untrusted workloads on a future dedicated Linux/KVM host, not a reason to buy hardware or choose it now. It does not solve the host-root compromise problem or the need for an independent action gateway.

## 7. Android and mobile-data implications

Android's current background-work documentation explains that excessive background processes can be restricted, and device-manufacturer behaviour can further limit background jobs, alarms and network access. Android 16 also applies runtime quotas to jobs started from foreground services. A phone can provide the owner UI, notifications, approval ceremony and user-initiated data transfer, but should not be treated as a guaranteed persistent ingestion or supervision node.

Given metered mobile data:
- keep large historical downloads resumable and scheduled;
- use compression and incremental cursors;
- separate low-volume control/alert traffic from bulk market archives;
- do not stream full-depth/high-frequency feeds to the phone;
- preserve local queues and explicit stale/unknown status when connectivity drops;
- avoid inbound port forwarding as a default remote-access solution;
- evaluate any future remote tunnel as a separate security dependency and owner decision.

## 8. Trust-domain patterns

### Pattern A — research-only local worker

Phone UI → authenticated read-only control/API → Windows/Linux research worker → local data store. Research and AI/strategy workers have no credentials and no generic egress. This is suitable only for research/data workflows after host review. If the host is compromised, treat all local state as suspect.

### Pattern B — protected gateway on a separate host

Untrusted research worker → typed proposal channel → separate action gateway host → venue adapter. The gateway host owns credentials and final permission/risk checks. Owner root/recovery anchor and health/security watchdog must be independent enough for the claimed threat model. No strategy/AI network path to the venue.

This is a future pattern only. It still needs a secure owner ceremony, key custody, revocation high-water state, network segmentation, audit transaction design, failure-mode tests and a manual recovery process. Two machines do not automatically make a secure system.

### Pattern C — cloud worker with local owner control

Local phone/PC owner control → outbound-authenticated cloud worker. This provides remote compute availability but introduces provider IAM, account recovery, metadata, billing, region, backup and third-party processing dependencies. Cloud agent-only data processing and own-purpose data use require separate Privacy Act analysis. No cloud provider is selected.

## 9. Provisional recommendation by phase

| Stage | Recommendation | Why |
|---|---|---|
| Current Phase 02 | No deployment. Keep GitHub research CI and documentation only | No runtime authority or host choice exists |
| Later research/data collection (if separately approved) | Inspect existing Windows PC first; compare a conventional Hyper-V VM against a dedicated Linux host only if WSL limitations matter | Cheapest evidence-gathering path without buying hardware |
| Future private read-only finance (if separately approved) | Prefer local storage/processing and manual imports first; assess provider and processor roles before any bank API | Reduces privacy, mobile-data and provider dependencies |
| Future untrusted AI/strategy workloads | Isolated VM/microVM with no secrets and host-enforced egress; evaluate against actual hardware | Defence in depth, not trust in prompt instructions |
| Future consequential execution (separate owner approval required) | Separate physical action gateway/recovery trust domain if host-root compromise is outside accepted risk | Same-host separation cannot satisfy that threat model |

**No new hardware, cloud account, provider or service is recommended for purchase now.** A security architecture that cannot be operated, patched, backed up and recovered reliably is not an improvement over a simpler dormant system.

## 10. Required future host inspection and tests

Before selecting a host:
- record exact model/CPU/RAM/storage/NIC/firmware and Windows edition/build;
- verify TPM, Secure Boot, BitLocker and recovery-key location;
- inspect virtualization support and Hyper-V availability;
- measure idle/peak CPU, memory, disk IOPS, storage growth and power/sleep behaviour;
- test mobile tethering bandwidth, latency, data usage, outage and reconnect;
- validate encrypted backup and restore without restoring stale authority;
- test network egress restrictions and absence of inbound exposure;
- test workload isolation and host/guest compromise assumptions;
- measure supervisor independence and alert delivery;
- establish RPO/RTO only after the actual workload and owner tolerance are known.

No such inspection or test was performed.

## 11. Open owner decisions — defer until full architecture pack

- Whether the existing Windows PC is allowed to become an always-on worker at all.
- Whether any new local hardware is acceptable and what budget/power limits apply.
- Whether a separate gateway host is mandatory before any future execution capability.
- Whether cloud hosting is acceptable given privacy, cost and account-recovery dependencies.
- Whether the phone should act as a passkey/approval authenticator or whether a separate hardware key is required.
- Whether mobile-data usage should cap bulk data ingestion.
- Which recovery anchor and external witness topology is acceptable.

Do not ask these questions until the complete architecture pack is ready.

## 12. Sources

- Microsoft WSL security model: https://github.com/microsoft/WSL/blob/master/doc/docs/technical-documentation/security.md
- Microsoft WSL overview: https://learn.microsoft.com/en-us/windows/wsl/about
- Microsoft WSL FAQ: https://learn.microsoft.com/en-us/windows/wsl/faq
- Microsoft Hyper-V security planning: https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/plan-hyper-v-security-in-windows-server
- Microsoft BitLocker overview: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/
- Microsoft TPM recommendations: https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/tpm-recommendations
- Android background task restrictions: https://developer.android.com/develop/background-work/background-tasks/bg-work-restrictions
- Android foreground service changes: https://developer.android.com/develop/background-work/services/fgs/changes
- Firecracker getting started/KVM requirements: https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md
- Firecracker production host setup: https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md
- Firecracker design/security: https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md
- NIST SP 800-207 Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final

## 13. Disposition

This document narrows future host research but selects no deployment. The current correct choice is to remain undeployed while Phase 02 architecture is completed. Any future topology must be evaluated against the actual host, mobile-data constraints, privacy model, threat tier, operational capability and total cost.

Phase 02 remains active; Phases 03–19 remain locked. No provisioning, configuration, purchase, account, credentials, integration, implementation or execution is authorised.


## 14. Checkpoint 094 — Firecracker operational controls and cloud caveats

A fresh read of the Firecracker production host guidance adds operational controls that must be explicit in any future deployment assessment:

- Run the matching Firecracker release's `jailer`, or enforce constraints at least as restrictive. Use a dedicated unprivileged UID/GID; preferably unique identities per microVM.
- Protect every jailer input path and parent directory from unprivileged modification. The jailer treats its paths as trusted inputs.
- Retain default seccomp filters; upstream does not recommend `--seccomp-filter` overrides or `--no-seccomp` for production.
- Bound CPU, memory, disk I/O, file size and file descriptors using cgroups/resource limits.
- Apply host-enforced TAP-interface egress filtering (nftables/iptables). Firecracker does not filter guest network traffic itself.
- Bound guest-influenced serial/log output to prevent disk exhaustion. Consider disabling the serial device in production and use bounded log rotation/ring buffers.
- Operate a host-side overwatcher for unresponsive Firecracker processes; the upstream guide describes a possible signal-handler deadlock.
- Patch host and guest kernels and CPU microcode; Firecracker does not mitigate host hardware vulnerabilities or eliminate side-channel risks.

These details increase the operational burden. Firecracker remains a future candidate only if the actual threat model justifies a dedicated Linux/KVM host and the owner can operate its patching, monitoring, egress, backup and recovery controls. It is not a lightweight shortcut to a secure host.

### OCI free-tier caution

The official general Always Free resources page currently states 1,500 OCPU-hours and 9,000 GB-hours per month for A1, while Oracle's A1-specific page states 3,000 OCPU-hours and 18,000 GB-hours. Until clarified, use the lower allowance for planning. The general page also confirms home-region capacity constraints and seven-day idle reclamation thresholds. Neither a nominal free quota nor a PAYG account guarantees physical capacity or caps all possible charges.

Sources:
- https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md
- https://github.com/firecracker-microvm/firecracker/blob/main/docs/seccomp.md
- https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- https://docs.oracle.com/en-us/iaas/Content/Compute/References/arm.htm
