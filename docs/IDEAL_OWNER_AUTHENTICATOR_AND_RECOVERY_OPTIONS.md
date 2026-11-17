# IDEAL Owner Authenticator and Recovery Options

**Research checkpoint:** 097  
**Date:** 18 November 2026  
**Phase:** 02 — authority, security and host trust research  
**Status:** technology-neutral options analysis; no authenticator, device, vendor or recovery method selected.

## 1. Purpose and boundaries

Define evidence-based requirements for the future owner authentication and approval ceremony, including device-bound versus synced credentials, WebAuthn/passkeys, Android hardware-backed keys, dedicated FIDO2 security keys, root-key separation, device loss and recovery.

This document does not identify the owner, inspect any device, register credentials, select a vendor, create keys, configure accounts or authorize any financial action. NIST SP 800-63B-4 is used as a technical reference model, not as a claim that IDEAL is a regulated federal system or that an AAL certification is being pursued.

## 2. Current standards and platform facts

### WebAuthn Level 3

W3C published WebAuthn Level 3 as a Recommendation on 25 August 2026. A credential is scoped to a Relying Party ID and assertions bind the origin/context into signed authenticator data. This provides strong phishing resistance when the relying-party implementation validates the challenge, origin, RP ID, signature, credential status and ceremony state correctly.

WebAuthn distinguishes:
- **Backup eligibility (BE):** set at credential creation and permanent; identifies a multi-device/backup-eligible credential versus a single-device credential.
- **Backup state (BS):** current state of a backup-eligible credential and may change.
- **User verification (UV):** local authenticator authorization, which may use PIN, password or biometrics. It does not independently prove a particular natural person's civil identity; multiple people may be enrolled or share an authenticator.

The RP must record and assess BE/BS and authenticator properties rather than assume that every passkey is device-bound. Attestation can provide authenticator provenance, but privacy and ecosystem support affect whether it is available and useful.

### NIST SP 800-63B-4

NIST's August 2025 revision defines:
- AAL2: two distinct factors and an available phishing-resistant option.
- AAL3: phishing-resistant public-key authentication using a non-exportable authentication key, plus two distinct factors.

These are useful high-assurance design benchmarks. IDEAL must not claim AAL2/AAL3 compliance without a complete assessment of verifier, authenticator, enrollment, recovery, session and operational requirements.

### Android Keystore and StrongBox

Android Keystore prevents private key material from entering the app process and can bind keys to a TEE or StrongBox secure element. A compromised app process may still be able to invoke operations with a key unless key-use authorization prevents it. A compromised Android OS may be able to use a TEE-backed key, although it cannot extract key material from the secure hardware. StrongBox offers stronger isolation/tamper resistance but is optional, slower, resource constrained and supports fewer algorithms/operations. Availability and supported algorithms vary by device.

A future Android implementation must inspect actual key security level and key-use authorizations; the mere presence of Android Keystore does not prove StrongBox backing. Key attestation, where used, requires server-side challenge and certificate-chain validation; a client-reported boolean is not evidence.

Android Credential Manager supports passkeys on Android 9/API 28 and later, but its normal passkey flow may use a credential provider such as Google Password Manager and support synchronization/restore. It must not be assumed to create a device-bound StrongBox key.

### Dedicated FIDO2 security keys

A dedicated FIDO2 key can provide a device-bound, non-copyable credential under the vendor's stated normal operating model. The PIN/user-verification state, supported algorithms, firmware, attestation, reset semantics, inventory and backup-key process must be reviewed. Loss or reset can make credentials unavailable; a second registered key or controlled replacement ceremony is required. A backup key must be registered and tested before it is needed.

## 3. Options and trade-offs

| Option | Security properties | Recovery/operational cost | IDEAL assessment |
|---|---|---|---|
| Synced passkey | Phishing-resistant RP-bound public-key credential; backup eligible and may be available on multiple devices; security depends partly on platform account and sync/recovery controls | Convenient account recovery; platform-account takeover/recovery becomes part of IDEAL's trust boundary | Potential convenience authenticator, not the sole independent owner root or recovery anchor |
| Device-bound platform passkey | Single-device credential; can be protected by platform secure hardware, but exact backing and attestation vary by device/provider | Lost device requires controlled re-enrollment; hardware and provider specifics matter | Candidate only after actual target-device capabilities and credential BE/BS/attestation are verified |
| Dedicated FIDO2 security key | Purpose-built, device-bound credential; phishing-resistant; hardware and PIN properties can be more predictable | Requires physical possession, spare key, secure storage, registration and replacement ceremony | Strong candidate for high-assurance owner authentication, but not yet selected |
| Android app-generated Keystore/StrongBox key | Non-exportable key with per-use restrictions; StrongBox optional; process/OS compromise assumptions differ by security level | App lifecycle, device replacement, attestation validation and recovery all become IDEAL responsibilities | Useful for a future transaction-approval key if actual device supports required security level; distinct from passkey |
| Offline owner root / recovery key | Can remain offline and authorize policy/owner-key lifecycle changes without routine use | Manual ceremony, secure backup custody, loss and emergency recovery complexity | Separate root/recovery role recommended in architecture; hardware and ceremony remain undecided |

No option should be described as invulnerable. Device-bound credentials reduce copying/sync exposure but increase loss/recovery burden. Synced credentials improve availability but expand trust to the sync account, provider and its recovery process.

## 4. Approval ceremony: authentication is not transaction intent

WebAuthn proves control of a credential and user presence/verification for a challenge. It does not, by itself, prove that the user reviewed or understood the human-readable financial action being approved.

A future IDEAL approval ceremony must therefore:
1. Construct an immutable action proposal and human-readable summary from canonical server-side data.
2. Bind the WebAuthn challenge to a cryptographic digest of the exact proposal, including action type, instrument/account scope, size/limits, expiry, policy generation, risk decision and unique nonce.
3. Display the same canonical summary to the owner before invoking the authenticator; never trust client-supplied text as the authoritative action description.
4. Require explicit user verification for consequential approval and validate the assertion's challenge, origin, RP ID, credential ID, signature, UV flag and ceremony expiry.
5. Consume the nonce exactly once and reject replay, duplicate approval, altered proposal, expired challenge or changed policy/authority generation.
6. Persist the approval assertion reference, proposal digest, credential identity, verification flags, timestamps and policy/authority version vector in the durable audit record.
7. Recheck the complete version vector at dispatch. An authenticated owner approval is not a standing permission and cannot override risk, health, security or revocation gates.

A compromised endpoint can still misrepresent the action before the user authenticates. High-assurance designs need a trustworthy display/confirmation path and must state the residual endpoint-compromise risk; WebAuthn origin binding alone is not transaction-content integrity.

## 5. Key-role separation

Keep cryptographic purposes distinct:
- offline owner root / owner-authority key;
- day-to-day owner authentication and approval credential;
- policy signing key;
- workload identity keys;
- audit checkpoint/witness key;
- encryption-at-rest and backup-encryption keys;
- recovery authority key.

Do not reuse one private key across these purposes. Root keys should not be exposed to strategy agents, ordinary application processes, policy evaluation or action workers. Policy signing must be distinct from owner login; a compromised workload identity must not mint owner approval. Recovery authority must not silently restore a revoked key or policy generation.

## 6. Recovery lifecycle requirements

Recovery is a security ceremony, not password reset:
- declare the incident type: lost device, damaged authenticator, forgotten PIN, suspected compromise, account recovery or owner-key compromise;
- immediately restrict new consequential actions when owner-authentication integrity is uncertain;
- revoke the lost/compromised credential and all associated sessions, permits and pending approvals;
- verify the independent recovery authority and its current revocation generation;
- establish a new authenticator with fresh key material and fresh credential registration;
- re-approve owner authority and policy state through a separately controlled ceremony;
- reconcile outstanding actions and external state;
- preserve evidence and record who/what authorized the recovery;
- only then permit owner-authorized reactivation.

Restoring an old backup, browser profile, cloud account or passkey-sync state must not automatically restore revoked permissions. Recovery keys and backup authenticators must be tested periodically, with no shared single point of compromise.

## 7. Provisional disposition

No authenticator or vendor selected. Architecture-level direction:
- use phishing-resistant public-key authentication for owner access;
- prefer a device-bound credential for the highest-assurance approval/root-adjacent role where operationally feasible;
- treat synced passkeys as a separate convenience/recovery trust domain, not as the sole independent root;
- separate offline owner root, day-to-day approval, policy signing and recovery roles;
- bind every approval to an exact action digest and current authority/policy generation;
- make recovery revoke-and-re-enrol, never restore old authority from backup.

The eventual choice depends on the actual Android/PC/browser support, the selected host and trust topology, whether a hardware security key is acceptable, and the owner's recovery model. These owner choices remain deferred under ODR-10.

## 8. Mandatory future verification (not executed)

1. Verify target platform's actual authenticator attachment, BE/BS flags, user verification, attestation availability and credential exportability.
2. Verify StrongBox/TEE level, algorithm support, per-use authentication, key invalidation and attestation chain if Android Keystore is used.
3. Test WebAuthn RP ID/origin binding, challenge freshness, signature validation, UV enforcement, BE/BS recording, replay rejection and credential revocation.
4. Test proposal-digest binding against altered amount, instrument, scope, policy generation, expiry and action type.
5. Test duplicate submissions, race conditions, stale session, concurrent revocation and policy-generation changes.
6. Exercise lost device, forgotten PIN, damaged key, suspected compromise, cloud-account recovery and owner-root recovery.
7. Confirm a backup authenticator works without weakening the primary assurance policy.
8. Prove restored credentials and backups cannot resurrect revoked authority or sessions.
9. Test recovery under offline/partition conditions and require explicit RECOVERY_HOLD when current revocation state cannot be verified.
10. Document user-visible ceremony, accessibility, privacy, attestation retention and data minimization.

No device was inspected and no tests were executed in this checkpoint.

## 9. Sources

- W3C WebAuthn Level 3 Recommendation (25 Aug 2026): https://www.w3.org/TR/webauthn-3/
- NIST SP 800-63B-4 (26 Aug 2025): https://pages.nist.gov/800-63-4/sp800-63b.html
- Android Keystore security model: https://developer.android.com/privacy-and-security/keystore
- Android passkeys / Credential Manager: https://developer.android.com/identity/passkeys
- FIDO Alliance high-assurance enterprise authentication: https://fidoalliance.org/white-paper-high-assurance-enterprise-fido-authentication/
- Yubico FIDO2 credential and PIN management: https://docs.yubico.com/software/yubikey/tools/authenticator/auth-guide/fido2.html
- Yubico lost-key FAQ: https://developers.yubico.com/WebAuthn/WebAuthn_Developer_Guide/FAQ.html

## 10. Authority boundary

Research and documentation only. No authenticator, device, hardware, vendor, account, key, credential, recovery mechanism or runtime selected or provisioned. No owner approval or financial action authorized. Phase 02 remains active; Phases 03–19 remain locked.
