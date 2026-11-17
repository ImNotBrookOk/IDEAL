# IDEAL Security Control and Threat Traceability Matrix

**Status:** Phase 02 security design matrix; provisional, not implementation evidence  
**Checkpoint:** 083 — 17 November 2026  
**Scope:** Protected assets, threat classes, control families, owning authority, evidence and future verification  
**Authority:** D-020, D-021, D-022, D-023  
**Boundary:** Design/research only. No runtime security tests, external scan, penetration test, host inspection, account access, credentials, deployment or phase advancement is authorised.

## 1. Assurance statement

This matrix connects the Security Architecture and Integrated Adversarial Review to explicit control owners and future verification. It does not claim that controls exist in a running system or that vulnerabilities have been eliminated.

Current status is **design specified / not implemented / not runtime verified** unless a row explicitly says otherwise. Earlier Phase 01 dependency/workflow scans and POC tests are limited to their recorded scope and do not establish whole-system security.

## 2. Protected assets and trust boundaries

| Asset ID | Protected asset | Sensitivity / impact | Primary owner |
|---|---|---|---|
| AST-01 | Owner identity, approval ceremony and operating envelope | Critical authority | Owner Authority / Security |
| AST-02 | Root/recovery keys, policy signing keys and revocation anchor | Critical trust root | Security |
| AST-03 | Future venue credentials, account identifiers and action gateway | Critical financial capability | Security / Action Boundary |
| AST-04 | Risk policies, decisions, reservations and account exposure state | Critical financial safety | Risk |
| AST-05 | Raw market evidence, canonical data and point-in-time datasets | High decision integrity | Data Integrity |
| AST-06 | Personal bank/ledger/tax records | High confidentiality/privacy | Personal Finance / Tax |
| AST-07 | Audit events, incident evidence and recovery checkpoints | Critical accountability | Audit / Security |
| AST-08 | Strategy/model artefacts, AI agents, generated code and plugins | High integrity/untrusted execution | Research / Security |
| AST-09 | Health telemetry, watchdog and restrictive interlocks | High availability/safety | Health |
| AST-10 | Backups, exports, caches and derived datasets | High confidentiality/recovery | Data owner / Security |

Trust zones Z0–Z4 are defined in the autonomy and system architecture documents. Physical placement remains undecided; same-host process/VM separation does not survive host-root/kernel compromise.

## 3. Security control catalogue

| Control ID | Control family | Required controls | Authority owner | Evidence / assurance status |
|---|---|---|---|---|
| SEC-01 | Owner identity and approval | Phishing-resistant authentication candidate; exact canonical digest; challenge bound to operation/environment/audience/nonce/expiry; visible scope/diff; separate owner approval from publisher signature | Owner / Security | Design specified; authenticator and UI not selected or tested |
| SEC-02 | Workload identity and authorisation | Unique service identities; short-lived credentials; default deny; exact principal/action/resource scope; policy enforcement outside untrusted caller; no self-grant | Security / Policy Registry | Design specified; identity platform and policy engine not selected |
| SEC-03 | Root of trust and key lifecycle | Separate root/recovery, policy signing, owner approval, workload identity, audit checkpoint, encryption and future venue key purposes; offline/hardware-backed root candidate; rotation/revocation/anti-rollback | Security | Design specified; hardware, ceremony and anchor not selected |
| SEC-04 | Secrets and credential isolation | No venue credentials in AI/strategy/research/parser processes; no secrets in GitHub, prompts, logs or generic config; least-privilege storage; rotation and incident revocation | Security | Design specified; no credentials or secret store exists |
| SEC-05 | Network and workload containment | Default-deny inbound; no generic venue egress from Z0; narrow typed IPC; explicit source egress; host-enforced egress; namespaces/cgroups/seccomp/LSM/VM layers where supported | Security / Host Operations | Design specified; OS profile and topology not selected |
| SEC-06 | Application and input security | Schema/type/range validation; safe deserialisation; parameterised queries; SSRF/path traversal/injection/XSS/CSRF/replay/rate-limit controls; file quarantine | Application Security / Data Integrity | Requirements documented; no runtime tests |
| SEC-07 | Supply-chain/build integrity | Pinned dependencies; licence and transitive dependency review; SBOM; provenance/signature verification; CI least privilege; workflow permissions and concurrency controls; vulnerability/advisory monitoring | Build/Release Security | Scoped Phase 01 checks completed; future stack not selected |
| SEC-08 | AI/agent security | Treat models/tools/generated code as hostile; no credentials or direct ledger/adapter writes; sandbox/capability restrictions; prompt injection and data exfiltration controls; human approval for authority changes | Security / AI Boundary | Design specified; no framework/runtime selected |
| SEC-09 | Data privacy and retention | C0–C3 classification; purpose/owner registry; C2/C3 exclusion from default prompts/training; processor/subprocessor assessment; retention/deletion across replicas/backups/derived data | Data Owner / Security | Policy design specified; no retention schedule or processor selected |
| SEC-10 | Audit integrity and accountability | Durable local pre-dispatch intent/reservation/audit/outbox; dispatch-start atomic with audit; event ordering, digest/checkpoint, redaction and retention; external witness optional | Audit / Security | Transaction pattern specified; no durability/anchor test |
| SEC-11 | Security monitoring and health separation | Independent observations; no self-reported HEALTHY as proof; scoped restrictive-only health interlocks; distinct security incident-response authority | Health / Security | Authority split specified; independent topology unresolved |
| SEC-12 | Vulnerability and incident lifecycle | Asset inventory, advisories/CVEs, triage, severity, containment, eradication, recovery, disclosure/notification assessment, lessons learned and evidence preservation | Security | Lifecycle designed; no external scan or incident exercise |
| SEC-13 | Backup and recovery trust | Encrypted backups; separate keys; restore quarantine; current revocation anchor; no resurrection of old permits/deleted data; independent attestations and owner release | Security / Recovery | Design specified; provider, RPO/RTO and restore tests open |
| SEC-14 | External side-effect fencing | Owner envelope, identity, security, data, health, risk and reservation gates; one-use permit; final version recheck; serialised DISPATCH_STARTED | Action Boundary / Risk / Security | Design specified; no execution adapter or runtime proof |

## 4. Threat-to-control traceability

| Threat ID | Adversarial scenario | Primary controls | Secondary controls | Required test / expected result |
|---|---|---|---|---|
| T-01 | Owner approval replayed against another artefact | SEC-01, SEC-02 | SEC-10 | Digest/nonce/context mismatch is rejected |
| T-02 | Publisher signs unapproved scope expansion | SEC-01, SEC-02, SEC-03 | SEC-10 | Missing owner approval blocks activation |
| T-03 | Compromised workload impersonates another service | SEC-02, SEC-03 | SEC-05 | Invalid/expired identity denied |
| T-04 | Strategy/AI reads venue credentials | SEC-04, SEC-05, SEC-08 | SEC-12 | File/IPC/env/network access denied |
| T-05 | AI/strategy sends direct venue network traffic | SEC-05, SEC-08 | SEC-14 | Egress firewall denies all non-allowlisted destinations |
| T-06 | Prompt injection causes privileged tool use | SEC-02, SEC-08 | SEC-01, SEC-14 | Tool cannot invoke privileged action without external gate |
| T-07 | Action payload altered after approval | SEC-01, SEC-02, SEC-14 | SEC-10 | Digest mismatch denies action |
| T-08 | Revocation races dispatch-start | SEC-03, SEC-14 | SEC-10 | Revocation-first blocks; dispatch-start-first remains in-flight |
| T-09 | Local audit write fails but external action dispatches | SEC-10, SEC-14 | SEC-02 | No network write without durable local transaction |
| T-10 | Lost venue acknowledgement causes duplicate retry | SEC-10, SEC-14 | Risk reservation / reconciliation | UNKNOWN retains reservation; idempotency/reconciliation prevents blind duplicate |
| T-11 | Host root/kernel compromise defeats local isolation | SEC-05, SEC-11, SEC-13 | SEC-03 | Separate trust domain or dormant fail-safe; local process separation not treated as sufficient |
| T-12 | Backup restore resurrects revoked identity/permit | SEC-03, SEC-13 | SEC-10 | Old generation/permit rejected after restore |
| T-13 | Data source is manipulated but digest is valid | SEC-06, SEC-09 | Data Integrity | Plausibility/source/sequence checks quarantine bad evidence |
| T-14 | Late correction contaminates historical backtest | SEC-06, SEC-09 | Data Integrity | As-known-then snapshot remains immutable |
| T-15 | Provider row changes under same ID and double-posts | SEC-06, SEC-09 | Reconciliation | Revision and duplicate tests; one journal posting |
| T-16 | Stale bank balance appears current | SEC-06, SEC-09 | Health | Refresh timestamp visible; stale data not treated as available cash |
| T-17 | Private finance/tax data leaks into model training | SEC-08, SEC-09 | SEC-04 | C2/C3 dataset ingestion and retrieval denied by default |
| T-18 | Offshore processor uses data for its own training | SEC-09 | SEC-12 | Processor-role/contract assessment; own-purpose use blocked absent approval |
| T-19 | Retention deletion leaves copies in backups/indexes | SEC-09, SEC-13 | SEC-10 | End-to-end deletion and restore-after-deletion tests |
| T-20 | Malicious dependency/build artefact enters trusted runtime | SEC-07 | SEC-02, SEC-12 | Provenance/licence/advisory verification; unsigned artefact denied |
| T-21 | CI workflow token abused to alter repository | SEC-07 | SEC-10 | Least-privilege token and workflow policy checks |
| T-22 | Health supervisor falsely asserts HEALTHY or sends financial action | SEC-11 | SEC-02, SEC-14 | No authority-grant/action interface; independent probes |
| T-23 | Security incident controller initiates transfer/flatten/payment | SEC-11, SEC-14 | SEC-01 | No such permission or adapter path exists |
| T-24 | Denial-of-service floods audit/health channels | SEC-06, SEC-10, SEC-11 | SEC-12 | Rate limits, bounded queues, scoped restrictions and alerting |
| T-25 | Malware steals data from lost device/backup | SEC-09, SEC-13 | SEC-03 | Full-disk/backup encryption and key recovery tests |
| T-26 | Remote access tunnel exposes admin/API surface | SEC-05 | SEC-01, SEC-12 | No inbound default; authenticated device/service identity and network policy |
| T-27 | Vulnerability is silently ignored or falsely marked closed | SEC-12 | SEC-07, SEC-10 | Finding requires evidence, owner, severity, remediation and retest |
| T-28 | Incident recovery releases system with incomplete evidence | SEC-11, SEC-13, SEC-14 | SEC-10 | Missing/stale pillar attestation keeps system quarantined |

The threat IDs are traceability identifiers, not a claim that the listed vulnerabilities were found in an operating system.

## 5. Security assurance lifecycle

| Stage | Required record | Exit condition |
|---|---|---|
| Asset and trust inventory | Asset ID, owner, sensitivity, dependencies and trust zone | Critical assets and trust boundaries are known |
| Threat modelling | Threat actor, capability, attack path, impact and assumptions | Material paths mapped to controls |
| Control design | Control owner, enforcement point, failure mode and residual risk | No control relies solely on prompt/UI instructions |
| Verification design | Positive/negative tests, fault injection, replay and recovery | Every material control has an independent oracle |
| Implementation review (future) | Code/config/version, dependency and evidence | Explicit owner approval and phase gate |
| Runtime assurance (future) | Test reports, logs, host evidence and coverage | Results reproduce on pinned target environment |
| Vulnerability operations | Advisory/CVE, severity, exploitability, remediation and retest | Closure evidence accepted; unresolved risks remain visible |
| Incident response | Timeline, containment, affected assets, notification and recovery | Trust re-established and owner release where required |
| Periodic reassessment | New threats, provider changes, dependency drift and topology | Controls remain appropriate; scope changes require approval |

## 6. Residual risks

- Same-host root/kernel compromise can defeat local process and VM isolation.
- Hardware-backed keys and measured boot cannot prove that every application component is benign.
- An external request already transmitted cannot be recalled.
- A single owner does not provide true two-person control.
- A local audit chain cannot independently prove integrity if all storage and checkpoint keys are compromised.
- A provider/processor may change terms, subprocessors, security posture or data use.
- No finite scan/test set discovers every vulnerability.
- Security controls can reduce availability; denial-of-service and false-positive containment remain operational risks.

## 7. Evidence status and next work

- Phase 01 dependency/workflow audits and POC tests remain scoped evidence only; they do not verify the future architecture.
- All SEC-01–SEC-14 controls remain design-level until implemented and tested.
- No external penetration test, host inspection, credential test, account integration or incident exercise was performed.
- Independent security/operations review remains required before Phase 02 acceptance.
- No technology, provider, authenticator, key store, sandbox or hosting option is selected.

## 8. Sources

- NIST SP 800-207 Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- NIST SP 800-57 Part 1 Rev. 5: https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- OWASP Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- OWASP Software Supply Chain Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html
- Firecracker production host setup: https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md
- Microsoft WSL security model: https://github.com/microsoft/WSL/blob/master/doc/docs/technical-documentation/security.md
- New Zealand Privacy Commissioner third-party provider guidance: https://www.privacy.org.nz/resources-and-learning/a-z-topics/working-with-third-party-providers/

## 9. Disposition

This matrix provides design traceability. It is not a security certification, runtime test report or proof that the system is secure. Phase 02 remains active; Phases 03–19 remain locked. No implementation or external security test is authorised.


## Checkpoint 097 — owner authenticator and transaction approval refinement

Owner-authentication controls must distinguish synced/backup-eligible passkeys from device-bound credentials (WebAuthn BE/BS flags), verify actual authenticator properties rather than rely on product labels, and enforce user verification for consequential approval. Android Keystore security level (TEE vs StrongBox) and per-use key authorization are platform facts to be verified, not assumed. A WebAuthn assertion must bind the exact action proposal digest, one-time nonce, origin/RP ID, expiry and policy/authority generation; dispatch rechecks the version vector. Credential loss/compromise requires revocation and fresh enrollment; backup restore cannot resurrect old authority. See [Owner Authenticator and Recovery Options](IDEAL_OWNER_AUTHENTICATOR_AND_RECOVERY_OPTIONS.md). These are design requirements only; no runtime test or device inspection was performed.
