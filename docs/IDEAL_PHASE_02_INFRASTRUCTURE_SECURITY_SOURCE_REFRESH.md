# IDEAL Phase 02 — Infrastructure Security Source Refresh

**Checkpoint:** 107 — 18 November 2026  
**Scope:** Linux kernel maintenance, Firecracker lifecycle/security advisories, production host controls  
**Status:** Dated research addendum; no platform or dependency selected  
**Boundary:** No host inspection, provisioning, code, dependency, runtime or execution.

## 1. Executive result

The November source refresh reinforces rather than changes IDEAL's existing position: a microVM is one isolation layer, not a complete security boundary. Host kernel maintenance, jailer/process restrictions, restrictive seccomp, resource ceilings, host-enforced guest egress filtering, bounded logging, watchdog behaviour, microcode and hardware threat assumptions remain necessary.

Two new operational facts are material to future platform evaluation:

1. The upstream Linux kernel archive reported stable 7.3.5 on 17 November 2026, with 7.4-rc3 as mainline. The same archive identifies maintained long-term branches including 6.18, 6.12, 6.6 and 6.1. IDEAL should not automatically select the newest mainline kernel. A future host decision must select a distribution-supported kernel branch, consume security backports, and verify the exact Firecracker/KVM compatibility matrix.
2. Upstream Firecracker's release policy lists v1.18.0 (9 November 2026) as supported, with v1.17.0 (10 September 2026) also supported. v1.16 support is scheduled to end 3 December 2026. Any future adoption must use a currently supported patched release and track its six-month support window; no version is pinned now.

## 2. Firecracker vulnerability evidence

The upstream GitHub security page lists two relevant advisories:

| Advisory | Severity | Affected versions | Patched versions | IDEAL relevance |
|---|---|---|---|---|
| GHSA-36j2-f825-qvgc / CVE-2026-1386 | Moderate | v1.13.1 and earlier; v1.14.0 | v1.13.2 and v1.14.1 | Jailer symlink-following could permit arbitrary host-file overwrite when a local user can write the pre-created jailer directory and the jailer runs privileged |
| GHSA-776c-mpj7-jm3r / CVE-2026-5747 | High | v1.13.0–v1.14.3 and v1.15.0 | v1.14.4 and v1.15.1 | Root-privileged guest could alter virtio PCI queue size after activation; denial of service and out-of-bounds write; host code execution requires additional preconditions |

These advisories demonstrate why IDEAL must assess the complete deployed version, enabled device model, jailer directory ownership, guest privilege assumptions and patch process. They do not imply that currently supported releases are affected. The current v1.18.0 release is newer than the listed patched versions, but no blanket security guarantee is inferred.

The jailer advisory specifically makes directory ownership and non-writable trusted paths important. The PCI advisory is relevant only when virtio PCI is enabled; MMIO is the default and was not affected by that advisory. This does not justify treating MMIO as universally safe or disabling future review.

## 3. Current upstream production-host requirements

The upstream production-host guide explicitly states that Firecracker does not filter guest network traffic; packets pass from the guest virtual interface to the TAP device. Host firewall policy must therefore enforce guest egress restrictions.

The same guide requires or recommends:

- Use the release-matched jailer, or equivalent/more restrictive process constraints.
- Use Firecracker's default restrictive seccomp filters; production use of `--no-seccomp` is not recommended.
- Protect jailer executable, chroot, network namespace paths and all parent directories from untrusted writes.
- Run each Firecracker process as a dedicated non-privileged user/group; use unique identities per instance.
- Apply cgroup and jailer resource limits for CPU, memory, disk/file size and descriptors.
- Apply host firewall rules to prevent guest access to restricted destinations, including cloud instance metadata endpoints where applicable.
- Bound guest-influenced serial and log output; do not allow unbounded host storage consumption.
- Operate an external host-side watchdog capable of detecting and terminating an unresponsive VMM process.
- Patch host and guest kernels and host microcode; account for host hardware vulnerabilities and side channels.
- Treat each Firecracker process as one tenant/workload; do not rely on the microVM to mitigate host hardware vulnerabilities.
- Consider swap data remanence and side-channel mitigations in the selected hardware/host design.

These are future acceptance requirements, not controls currently deployed by IDEAL.

## 4. Linux kernel maintenance interpretation

The upstream archive's stable and long-term branches serve different purposes. A mainline release candidate is not a production maintenance target. A future deployment must choose a distribution and kernel branch with a support commitment, security backports, compatible KVM features and a tested upgrade/reboot procedure.

The exact 7.3.5 stable release is a dated upstream fact, not a recommendation to run kernel 7.3.5. Distribution kernels may carry backported fixes without matching upstream version strings. Vulnerability assessment must therefore use the distribution's package advisories and patch status, not naive version comparison alone.

## 5. Architecture impact

No change to the logical architecture is warranted. Add these explicit future acceptance checks to ODR-09 (host trust topology) and ODR-11 (revocation/supervisor/audit witness):

1. Host OS/distribution and kernel branch have an explicit security support lifecycle.
2. Host and guest patch ownership, vulnerability intake, patch deadlines, reboot windows and exception expiry are documented.
3. Firecracker version is within upstream support and security advisories are monitored.
4. Release-matched jailer, restrictive seccomp, dedicated identities and protected jailer paths are verified.
5. Guest egress is denied by default at the host boundary and allowlisted by workload purpose.
6. Logs, serial output, CPU, memory, disk, descriptors and network are bounded and monitored.
7. An independent host-side watchdog detects VMM hangs and has no authority to grant financial permissions.
8. Recovery and patch rollback cannot restore revoked credentials, permits or policy.
9. The threat model explicitly states that host root/kernel and hardware compromise remain outside same-host VM containment.

Do not create a second host or separate gateway solely because this source refresh identifies these controls. The physical trust-domain choice remains an owner/platform decision.

## 6. Sources checked on 18 November 2026

- Linux kernel archive (latest stable, mainline and long-term branches): https://cdn.kernel.org/
- Linux kernel active releases and LTS lifecycle: https://www.kernel.org/releases.html
- Firecracker release policy: https://github.com/firecracker-microvm/firecracker/blob/main/docs/RELEASE_POLICY.md
- Firecracker releases: https://github.com/firecracker-microvm/firecracker/releases
- Firecracker production host setup: https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md
- Firecracker security advisories: https://github.com/firecracker-microvm/firecracker/security
- GHSA-36j2-f825-qvgc / CVE-2026-1386: https://github.com/firecracker-microvm/firecracker/security/advisories/GHSA-36j2-f825-qvgc
- GHSA-776c-mpj7-jm3r / CVE-2026-5747: https://github.com/firecracker-microvm/firecracker/security/advisories/GHSA-776c-mpj7-jm3r
- Firecracker seccomp guide: https://github.com/firecracker-microvm/firecracker/blob/main/docs/seccomp.md

## 7. Disposition

The existing host trust architecture remains directionally correct. The refresh adds explicit release lifecycle, patch ownership, jailer-path, guest egress, watchdog and bounded-output acceptance checks. It does not select Firecracker, a kernel, Linux distribution, host, cloud provider or topology. No runtime security test or host inspection was performed. Phase 02 remains active; Phases 03–19 remain locked.
