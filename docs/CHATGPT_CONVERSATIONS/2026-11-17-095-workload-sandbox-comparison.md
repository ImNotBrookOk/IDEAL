# IDEAL Work Audit — Checkpoint 095

**Date:** 17 November 2026  
**Workstream:** Phase 02 — untrusted workload isolation comparison  
**Status:** Read-only research and documentation.

## Research question

Which open-source isolation model is proportionate for future untrusted AI/strategy/research workloads: gVisor, Kata Containers or Firecracker?

## Findings

- **gVisor:** its userspace Sentry implements the application-facing system API rather than passing application syscalls directly to the host. It still relies on host kernel/platform for hardware attack mitigation and cgroups for resource-exhaustion protection. Host networking/passthrough configurations can expand the host API surface. It may be the lower-operational-cost first experiment where a guest kernel is not required, but it is not an independent VM boundary against host-root/kernel compromise.
- **Kata Containers:** runs containers inside a VM with guest kernel and agent, managed through a container runtime and VMM. This supplies a guest-kernel boundary but adds guest assets, VMM, agent, host/guest control channel and lifecycle complexity. Its own threat model includes host kernel, VMM, virtual-device, shared-resource and configuration risks.
- **Firecracker:** provides a minimal KVM microVM with one VM per Firecracker process. It offers a direct guest-kernel boundary but requires KVM, jailer, seccomp, cgroups/namespaces, host TAP egress filtering, bounded logging and external monitoring. Host kernel/hardware remain trusted.

**Disposition:** No runtime selected. For a future single-host research worker, evaluate gVisor first only if untrusted code execution is a real requirement and compatibility supports it. If a guest-kernel boundary is required, compare Firecracker and Kata on the actual host. No sandbox may receive credentials or unrestricted egress.

## Sources

- https://gvisor.dev/docs/architecture_guide/security/
- https://gvisor.dev/docs/architecture_guide/networking/
- https://gvisor.dev/blog/2020/04/02/gvisor-networking-security/
- https://kata-containers.github.io/kata-containers/design/architecture/
- https://github.com/kata-containers/kata-containers/blob/main/docs/threat-model/threat-model.md
- https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md

## Changes and boundaries

Updated host trust topology, infrastructure research, core protection architecture, document map and roadmap; created this audit. No code, runtime, dependency, host, account, credentials, external service, deployment or test was introduced. No owner decision or phase status changed. Phase 02 remains active; Phases 03–19 remain locked.
