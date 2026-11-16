# 040 — Hosting constraints: phone-first, Windows PC as fallback

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED

## Owner-provided operating constraints

The owner can make an existing Windows PC/laptop available if genuinely required, but prefers to operate IDEAL from a phone and does not want to depend on the PC unless a material technical requirement makes it necessary. Internet access is via mobile phone data; this must be treated as a constrained/variable connection rather than assumed fixed broadband.

## Phase 01 hosting disposition

- Phone-first remains the operating preference. A phone is suitable as a control/monitoring client, not presumed to be the persistent core compute host.
- The existing Windows PC/laptop is a **fallback candidate**, not selected or provisioned. No Windows service, WSL, Docker, remote-access agent, port forwarding or always-on process is authorised by this note.
- Do not assume unlimited or unmetered mobile data, stable public IP, inbound reachability, low latency, or continuous tethering. Measure actual data use and connection stability before any host experiment.
- Avoid continuous high-volume exchange feeds or repeated large historical downloads over mobile data. Prefer CI/offline research, bounded scheduled jobs, incremental transfer, compression, local caching and small summaries.
- Do not expose a self-hosted machine directly to the public internet. If remote access is later required, evaluate an authenticated outbound tunnel/VPN and least-privilege controls separately.
- No need to use the PC for the remaining Phase 01 research or documentation work. Revisit only if a measured requirement cannot be met by phone control plus existing free CI/cloud research infrastructure.
- Hosting is still unresolved: a Windows PC on mobile data is not yet proven to be a reliable always-on, low-cost runtime. If mobile data is capped or unstable, self-hosting could be more expensive or less reliable than expected.

## Next evidence required before any host selection

1. Determine whether mobile data is metered/capped, typical monthly allowance, and whether tethering is permitted by the plan (owner can provide later if a host test becomes necessary).
2. If justified, measure idle and representative workload bandwidth before leaving any process running.
3. Confirm Windows hardware resources, power/thermal behaviour, sleep/hibernation settings and restart recovery only if the PC becomes a candidate.
4. Test outbound-only connectivity and safe remote administration; no public inbound ports.
5. Benchmark persistence, backup/restore and failure recovery before calling any host viable.

## Boundaries

No spend, cloud provisioning, Windows setup, remote-access configuration, exchange credentials, venue selection, runtime integration, paper/live execution or Phase 02 work is authorised. The decision is to **defer host selection** and continue Phase 01 with phone-first, low-bandwidth assumptions.
