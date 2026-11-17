# IDEAL Security Architecture and Assurance

**Status:** Phase 02 architecture baseline — research and design only  
**Recorded:** 17 November 2026  
**Authority:** Owner-approved security direction, recorded as D-021  
**Implementation status:** Not authorised. Phase 02 remains active; Phases 03–19 remain locked.

## 1. Purpose

Security is a foundational system-wide requirement. IDEAL must be designed to resist unauthorised access, credential theft, data leakage, tampering, malicious dependencies, abuse of automation and compromise of individual components. Security applies to the application, data, infrastructure, development process, operators, integrations, backups and AI-assisted workflows.

Security is a distinct fourth pillar alongside risk management, data integrity and system health. It is also integrated into the other three:
- Security protects the confidentiality, integrity and availability of data.
- Security protects risk policies, calculations, permissions and action pathways from tampering or unauthorised use.
- System health monitors the operation and effectiveness of security controls and detects suspicious or abnormal behaviour.

A security dashboard must not equate service availability with security. A compromised component may continue reporting healthy. Security assurance requires independent evidence, detection and investigation.

## 2. Security objectives

The design must preserve:
- **Confidentiality:** only explicitly authorised principals can access private, financial, credential and operational information.
- **Integrity:** unauthorised changes to code, configuration, policies, records, datasets, models and audit evidence are prevented or detectable.
- **Availability and resilience:** attacks, failures and ransomware must not silently destroy the ability to operate safely or recover.
- **Authenticity and accountability:** identities, services, data sources and consequential actions can be verified and attributed.
- **Least privilege:** every human, process, service, agent and integration receives only the minimum permissions and duration required.
- **Privacy and minimisation:** collect and expose only what is necessary for a defined purpose; apply retention, deletion and legal/provider constraints even where data has research value.

No design can guarantee that every vulnerability or attack will be found. The engineering objective is continuous reduction of attack surface, layered prevention, independent detection, bounded blast radius, evidence-led response and tested recovery.

## 3. Threat model and protected assets

Threat modelling must be performed before implementation and revisited whenever trust boundaries, integrations or permissions change. Use STRIDE and abuse-case analysis across the complete data and control flows.

Protected assets include:
- exchange, broker, bank, IRD and other future integration credentials and tokens;
- personal, financial, tax and identity data;
- market data entitlements and licensed datasets;
- balances, positions, ledger records, tax workpapers and portfolio valuations;
- risk policies, limits, permission grants, kill-switches and execution controls;
- source code, build artefacts, dependencies, CI/CD credentials and deployment configuration;
- historical evidence, model artefacts, research datasets and experiment records;
- audit logs, incident evidence, backups and recovery keys.

Threat actors and failure sources include remote attackers, credential phishing, malicious insiders or compromised endpoints, supply-chain compromise, vulnerable dependencies, hostile or compromised data providers, malicious documents/web content, prompt injection, unsafe AI tools, accidental operator mistakes, ransomware and physical/device loss.

Trust boundaries must be explicitly mapped: mobile/PC client, local runtime, server or cloud boundary, network, data providers, external integrations, storage, backups, CI/CD, AI models and retrieval stores. Data remains untrusted based on its origin, even if it arrives through an internal process.

## 4. Security architecture requirements

### 4.1 Identity, authentication and authorisation

- Establish explicit identities for the owner, services, agents and external integrations.
- Require strong authentication for privileged access; evaluate phishing-resistant MFA/passkeys where supported.
- Apply least privilege, deny-by-default permissions, resource-level authorisation and separation of duties.
- Use short-lived, scoped credentials where practical; support revocation and rotation.
- Separate read-only observation from write/action capabilities.
- Require explicit human approval for sensitive permission grants, new external integrations and consequential financial operations.
- Protect sessions against theft, fixation, replay and CSRF; define secure session lifecycle and device revocation.
- No strategy, model or agent may grant itself permissions, change risk policy or expand its own authority.

### 4.2 Secrets and key management

- Never store secrets in source control, ordinary logs, prompts, analytics or unencrypted configuration.
- Define a dedicated secrets-management design, encryption-key hierarchy, rotation, revocation, backup and recovery procedure.
- Separate encryption keys by purpose and data domain. Authentication/session signing keys must not double as financial-data encryption keys.
- Minimise secret exposure to processes and agents; never give an AI model direct access to raw credentials.
- Treat backups and exported configuration as sensitive; protect and test recovery of encryption keys separately.
- Document incident response for suspected secret exposure. Assume a remotely committed secret is compromised and rotate/revoke it.

### 4.3 Data protection and privacy

- Classify information by sensitivity and purpose. Financial, tax, identity, location and credential data require strict access controls.
- Encrypt sensitive data in transit and at rest using maintained, standard cryptographic protocols and libraries.
- Define field-level protection where database/storage access alone would otherwise expose secrets or highly sensitive values.
- Minimise personal data and redact secrets/PII from logs, traces, error reports and AI context.
- Maintain access audit trails for sensitive reads and all sensitive writes.
- Preserve research evidence only within legal, contractual and privacy limits; data preservation does not override deletion duties, provider licence or purpose limitation.
- Define retention and secure deletion across primary storage, replicas, caches, exports, model/retrieval stores and backups.
- Avoid placing real account credentials, financial records or personal secrets in GitHub.

### 4.4 Network, application and host hardening

- Minimise exposed network services and administrative interfaces; default-deny inbound access.
- Use authenticated encrypted service-to-service communication and verify peer identity.
- Segment workloads and data domains according to sensitivity and blast radius.
- Validate all external input and file content; use parameterised queries, output encoding and safe deserialisation.
- Protect against injection, SSRF, XSS, CSRF, broken access control, request smuggling, path traversal, insecure file handling, replay and denial-of-service.
- Apply secure headers, restrictive CORS, rate limits, request size limits, timeouts and resource quotas where applicable.
- Run services with non-root identities and minimal filesystem/network permissions; isolate risky tools and untrusted workloads.
- Establish secure OS, container, runtime, firewall, patching and endpoint baselines for eventual PC/server deployment.
- Avoid exposing database, metrics, debug or administrative ports to untrusted networks.

### 4.5 Supply-chain and build security

- Pin and review dependencies; use one authoritative lockfile per install boundary and reproducible builds.
- Review package ownership, maintenance, release provenance, transitive dependencies and install scripts before adoption.
- Run automated dependency and vulnerability scanning; triage by severity, reachability and exploitability; track accepted residual risk and review dates.
- Scan source, secrets, containers, infrastructure configuration and build artefacts as applicable.
- Protect CI/CD identities with least privilege, short-lived credentials and protected branch/release controls.
- Produce provenance for released artefacts and preserve build/test evidence.
- Never apply forced dependency upgrades or auto-remediation without review and regression verification.

### 4.6 AI, agents and automation security

- Treat prompts, retrieved documents, market/provider messages and model outputs as untrusted data.
- Prompt instructions are not an authorisation boundary. Permissions must be enforced by deterministic code and operating-system controls.
- Give agents no direct exchange, bank, broker, tax or payment credentials.
- Expose narrow, allowlisted tools with typed input validation, explicit capability scopes, rate/cost limits and audit logging.
- Separate read, research, propose, approve and execute capabilities. AI must not approve its own consequential actions or alter security/risk policy.
- Isolate shell, browser, code execution and file access in constrained sandboxes; deny by default.
- Require explicit human approval for initial activation of a future execution capability; policy/limit/envelope changes; new accounts, venues or integrations; credential creation or permission expansion; transfers, withdrawals and payments; disabling safeguards; reserved destructive/irreversible actions; and incident recovery/release where specified. Individual financial actions may run without per-action approval only under a separately owner-approved, active, versioned bounded-autonomy envelope and after all deterministic controls pass.
- Protect retrieval stores against cross-domain leakage, poisoning and unauthorised indexing.
- Record model/provider, version, tool calls and relevant input/output hashes without logging secrets or unnecessary personal data.

### 4.7 Audit integrity and tamper detection

- Record authentication events, authorisation failures, permission changes, secret/key lifecycle events, configuration changes, dependency changes, sensitive data access, security alerts and incident actions.
- Use append-only or tamper-evident logging, protected storage and independent replication where justified.
- Synchronise clocks and preserve event/source timestamps.
- Restrict who can read, alter, export or delete security logs; log access to the logs themselves.
- Alert on missing audit continuity, unexpected policy/config changes, disabled controls and suspicious privilege escalation.
- Never rely exclusively on logs produced by a potentially compromised component.

## 5. Security as part of system health

Security monitoring is integrated with the system-health framework, but security remains a separate assurance dimension.

The health/security oversight design should monitor:
- authentication anomalies, repeated failures, unusual sessions and unexpected devices;
- privilege grants, role changes, token creation/use/revocation and key rotation failures;
- unexpected outbound connections, new listening ports, unusual process activity and configuration drift;
- dependency advisories, vulnerable runtime images, unsupported software and patch status;
- integrity of binaries, configuration, policy files, datasets, audit logs and backups;
- disabled, stale or failing security agents, scanners, alerts and monitoring pipelines;
- suspicious data exports, access spikes, unusual retrieval or tool activity and cross-domain access attempts;
- backup encryption, backup age, restore evidence and ransomware indicators;
- failed or overdue security reviews, unresolved findings and exception expiry.

Security posture must be reported independently from operational availability. Suggested states include SECURE/ASSESSED, DEGRADED, AT_RISK, INCIDENT and UNKNOWN, with explicit scope, timestamp, evidence and assessment freshness. These are not absolute guarantees: an assessment only describes what was checked and when.

A health/security monitor may trigger predefined containment actions such as disabling a compromised integration, revoking a token, isolating a workload or restricting affected actions. These controls require carefully defined authority, safeguards against false positives, recovery procedures and owner visibility. Monitoring must not silently change financial policy or initiate financial transactions.

The monitor itself must be protected and independently observed. A compromised host may falsify local telemetry; eventual architecture should consider external heartbeat, independent log destination, immutable backup, host integrity and out-of-band alerting proportionate to deployment risk.

## 6. Vulnerability discovery and assurance lifecycle

Security cannot be proven by one scan or one penetration test. Use overlapping methods throughout design and delivery:

1. Threat modelling and abuse-case review before interface and trust-boundary design.
2. Secure design review and attack-surface inventory.
3. Static analysis, secret scanning, dependency/SBOM analysis and configuration scanning.
4. Dynamic application and API testing once a runtime exists.
5. Fuzzing and malformed-input testing for parsers, data adapters and protocol boundaries.
6. Permission/authorization tests, including negative tests and cross-domain isolation.
7. Independent penetration testing and adversarial review before any external exposure or financial write capability.
8. Continuous vulnerability monitoring and patch triage after deployment.
9. Incident exercises, credential revocation drills, backup restoration and compromise recovery.
10. Retest findings and preserve evidence of remediation.

No scan can establish that all vulnerabilities have been found. Findings must include severity, exploitability, affected assets, exposure, compensating controls, owner, remediation target, verification evidence and residual risk. Exceptions require explicit approval, expiry and review; critical exploitable findings must block release or the affected capability.

## 7. Incident response and recovery

Define playbooks for suspected credential theft, unauthorised access, data exfiltration, tampering, malware/ransomware, vulnerable dependency exploitation, AI/tool abuse and compromised data sources.

The lifecycle must cover detection, triage, containment, credential revocation, evidence preservation, eradication, recovery, reconciliation, notification obligations and post-incident review. Containment actions must preserve forensic evidence where safe and must not create further financial exposure.

Recovery is not complete when services restart. Verify identity and permissions, code/configuration integrity, data and ledger consistency, audit continuity, key validity, backup provenance and downstream state. Reconcile any potentially affected financial or research records before restoring dependent activity.

## 8. Phase 02 design work required

Before implementation, research and specify:
1. Threat model, assets, adversaries, trust boundaries and abuse cases.
2. Identity, authentication, authorisation, session and device trust model.
3. Secrets management, encryption/key hierarchy, rotation, revocation and recovery.
4. Data classification, privacy, retention, deletion and secure export rules.
5. Network segmentation, service identity and host/container hardening.
6. Secure development lifecycle, dependency provenance, CI/CD and release integrity.
7. AI/agent sandboxing, tool capabilities and prompt-injection boundaries.
8. Security telemetry, independent monitoring, alerting and tamper-evident audit design.
9. Vulnerability management, testing strategy, severity policy and exception governance.
10. Incident response, forensic evidence, credential compromise and disaster recovery playbooks.
11. Security acceptance criteria and requirement-to-test-to-evidence traceability.
12. Independent review of the complete design and its highest-risk assumptions.

Keep the implementation proportionate to a private single-user system, but do not confuse single-user with low-risk. A private system may hold highly valuable financial data and credentials. Prefer simple, well-maintained, open standards and a small attack surface over unnecessary security products or services.

## 9. Explicit non-authorisations

This document does not authorise implementation, new dependencies, security product subscriptions, external scans against third-party systems, hosting, remote access, external integrations, credential collection, account connections or financial operations. Any external penetration test must be limited to assets the owner controls and separately authorised.

Phase 02 remains active. Phases 03–19 remain locked.


The cross-pillar STRIDE-style challenge and prioritised residual findings are maintained in [IDEAL Integrated Adversarial Architecture Review](IDEAL_INTEGRATED_ADVERSARIAL_REVIEW.md). This is a design review draft, not a penetration test or security certification.


## 9. Bounded owner-authorised autonomy (D-023)

IDEAL's future execution-capable operating model is bounded autonomy, not unrestricted agent authority and not mandatory per-action human approval.

### 9.1 Owner-approved operating envelope

Before any future execution capability can be activated, the owner must explicitly approve a versioned capability envelope. Its scope must define, at minimum:
- authorised domain, account, venue and instrument scope;
- permitted action classes and prohibited/reserved action classes;
- operating mode and whether autonomous submission is permitted;
- hard risk policy, exposure/position limits and maximum permissions;
- strategy eligibility and required deterministic gates;
- data-quality, freshness, reconciliation and system-health prerequisites;
- security identity, credential scope and allowed tool capabilities;
- stop conditions, drawdown/restriction behaviour, duration/expiry and revocation method;
- audit/evidence requirements and owner notification/escalation rules.

The envelope is an upper bound, not an entitlement to use the full capacity. Independent risk evaluation may approve less, restrict, or reject an action. A strategy's requested size, AI confidence or model output cannot expand the envelope or risk budget.

### 9.2 Autonomous in-envelope actions

A future separately authorised engine may submit individual actions without per-action human approval only when all of the following are true:
1. The envelope is active, unexpired, correctly signed/versioned and not revoked.
2. The actor/service identity is authenticated and authorised for the exact action and scope.
3. The request is within every envelope and venue constraint.
4. Decision-critical data, account/order state and instrument parameters are sufficiently fresh, complete, reconciled and trusted.
5. Required health and security interlocks are clear; UNKNOWN, stale or compromised states restrict the dependent action.
6. Independent deterministic risk evaluation approves the exact action payload and reserves its potential exposure.
7. The action is idempotent, attributable and covered by required durable audit evidence.
8. The approval is unexpired and has not been consumed, revoked or invalidated by a material state/policy change.

No AI model or strategy component is itself an authority. Models may research, propose and explain; deterministic policy and externally enforced permissions govern action.

### 9.3 Actions reserved for owner approval

Human approval remains mandatory for:
- initial activation or reactivation of any future execution capability;
- creation, expansion, renewal or material modification of the operating envelope;
- changes to hard risk limits, permissions, account/venue/instrument scope or operating mode;
- credential creation, secret/key trust changes or privilege expansion;
- transfers, withdrawals, payments and movement of funds between accounts;
- disabling, bypassing or weakening safeguards;
- new external integrations and materially new data permissions;
- reserved destructive or irreversible operations;
- security-incident recovery, restoration of trust and release from critical restrictions where owner approval is required by incident policy.

An owner may explicitly reserve additional action classes. This list is a minimum design boundary, not an exhaustive grant of authority.

### 9.4 Enforcement, revocation and failure behaviour

- The envelope is immutable to strategies, models and agents. Changes require an authenticated owner-authorised workflow, independent validation, a new version and tamper-evident audit.
- Every action is checked against the current envelope at the action boundary; UI-only or prompt-only restrictions are insufficient.
- A changed action payload, expired/revoked envelope, missing approval, unknown permission state or stale critical evidence requires denial and a fresh evaluation.
- Owner suspension/revocation must propagate to the action boundary. Revocation cannot rely solely on a possibly compromised strategy process.
- Failure to establish envelope validity, risk approval, required data quality, health or security status means no risk-increasing action.
- Emergency restrictions may reduce authority. They cannot silently grant new financial authority or initiate a financial liquidation.

### 9.5 Approval and activation boundary

D-023 records the future governance model only. It does not activate any operating envelope or execution capability. A later proposal must separately define and verify the policy schema, signing/root-of-trust model, identity and permission enforcement, risk reservation/approval protocol, audit durability, health interlocks, recovery and manual fallback. The owner must explicitly approve the complete capability and its operating scope before implementation or use.


## Autonomy authority and permission enforcement (D-023 technical design)

The owner-approved operating envelope is a cryptographically verifiable, immutable, versioned and revocable authority artefact. Its signature is necessary but not sufficient: semantic validation, authenticated owner approval, protected key custody, anti-rollback, independent enforcement and current revocation checks are also required. Keep owner root/recovery, owner approval, policy publication, workload identity, audit checkpoint and data-encryption keys separate.

Every privileged service receives a distinct workload identity; identity is not permission. All consequential actions pass through an action boundary outside strategy/AI processes. It verifies the exact canonical action, owner envelope, policy, caller identity, current revocation epoch, data trust, health/security interlocks, deterministic risk decision/reservation and audit preconditions. Deny by default; any missing, stale, malformed, ambiguous or unverifiable prerequisite blocks risk-increasing actions. The boundary must be the only route to adapters.

Owner approval must be bound to the exact envelope/policy digest and reserved action. Any material parameter change invalidates prior authorisation. Revocation must propagate independently of the strategy/agent process, have a measurable maximum delay and invalidate outstanding capabilities. See [Autonomy Authority and Permission Architecture](IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md) for candidate tooling, key lifecycle, exact-action contract, threat cases, recovery and assurance requirements. No identity/policy/key tool is adopted and no runtime or execution authority is granted.
