# 035 — Zero-cost hosting alternatives comparison

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED  
**Constraint:** no cloud account creation, resource provisioning, credentials, paid services or spend

## Summary

No reviewed free cloud tier is a verified, dependable, full IDEAL production engine host. The strongest compute candidate remains Oracle Ampere A1, but its home-region capacity uncertainty, idle-instance reclamation and lack of SLA are incompatible with treating it as the sole safety-critical host. Other options are useful only for narrower supporting roles.

## Comparison

| Provider | Published free capacity / limits | Suitability |
|---|---|---|
| Oracle Cloud Always Free A1 | 2 OCPU / 12 GB RAM; 1,500 OCPU-hours and 9,000 GB-hours monthly; 200 GB combined block storage; home-region only; can be out of capacity; idle reclaim if CPU p95, network and A1 memory each remain below 20% over seven days; no SLA | Best free VM capacity candidate for bounded experiment, but not reliable sole production host |
| Google Cloud Compute Engine | One non-preemptible e2-micro per month in US regions only; 0.25 vCPU / 1 GB RAM; 30 GB standard persistent disk; 1 GB/month outbound from North America; billing account required | Too small and geographically remote for the full engine; possibly monitoring or low-frequency utility only |
| Render Free Web Service | 750 free instance hours/workspace/month; spins down after 15 minutes without inbound HTTP/WebSocket messages; ephemeral local filesystem; may restart at any time; no persistent disk on free instance | Not suitable for an outbound exchange-WebSocket background worker; incoming WebSocket traffic can keep a web service active but is not a reliable execution-host contract |
| Cloudflare Workers + Durable Objects Free | Workers: 100,000 requests/day, 10 ms CPU per request, 128 MB memory. SQLite-backed Durable Objects: 100,000 requests/day, 13,000 GB-s/day, 5 GB total storage; incoming WebSocket server can hibernate while keeping clients connected. Outgoing WebSocket clients cannot use WebSocket hibernation and consume active duration. | Promising edge/gateway/low-volume data relay, not a general Python/Rust process or full trading engine. Outgoing feed processing must fit 128 MB, request and daily duration quotas; no full-engine benchmark or reliability proof |
| GitHub Actions | Public-repository CI runners are ephemeral jobs; not a persistent service or always-on VM | Suitable for research, tests, scheduled data checks and build automation only |
| Self-hosted existing hardware | No new cloud subscription; actual cost depends on existing hardware, electricity, ISP, UPS and maintenance | Most direct $0 recurring compute path if an always-on host already exists, but user hardware/power/network availability is not confirmed |

Official sources:
- Oracle Always Free: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Google Cloud Free Tier: https://docs.cloud.google.com/free/docs/free-cloud-features
- Google e2-micro specs: https://docs.cloud.google.com/compute/docs/general-purpose-machines
- Render free service limits: https://render.com/docs/free
- Render WebSocket spin-down change (24 Feb 2026): https://render.com/changelog/free-web-services-now-remain-active-while-receiving-websocket-messages
- Cloudflare Workers limits: https://developers.cloudflare.com/workers/platform/limits/
- Cloudflare Durable Objects pricing: https://developers.cloudflare.com/durable-objects/platform/pricing/
- Cloudflare Durable Objects limits: https://developers.cloudflare.com/durable-objects/platform/limits/
- Cloudflare WebSocket hibernation: https://developers.cloudflare.com/durable-objects/best-practices/websockets/

## Architectural implication

A potential zero-subscription hybrid is:
1. A self-hosted always-on machine runs the Python/Rust engine and durable event journal.
2. Cloudflare Workers/SQLite Durable Objects provide optional edge API, notifications, dashboard relay or a low-volume data-gateway role.
3. GitHub Actions handles CI, historical-data research and scheduled offline validation.

This is a candidate topology only. It is not approved or implemented. A single Cloudflare Durable Object maintaining an outgoing exchange WebSocket cannot hibernate; incoming WebSocket hibernation documentation must not be misapplied to an outgoing exchange connection. Free-tier limits and restarts mean it should not be the only execution/risk process.

## Disposition

- No provider is selected as the production worker.
- Oracle A1 remains the highest-capacity free VM experiment candidate, not a dependable sole host.
- GCP e2-micro and Render Free are rejected for the core engine; Cloudflare is supporting infrastructure only.
- $0 persistent worker feasibility remains OPEN until a real host can be benchmarked and failure/recovery tested.
- The only plausible zero-subscription core compute route is self-hosting on existing always-on hardware, whose availability is not yet known.
- No account or resource was provisioned and no spending occurred.
