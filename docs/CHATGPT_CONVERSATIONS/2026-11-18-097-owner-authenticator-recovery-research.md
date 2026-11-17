# IDEAL Work Audit — Checkpoint 097

**Date:** 18 November 2026  
**Workstream:** Phase 02 — owner authenticator, approval and recovery research  
**Status:** Research and documentation only.

## Research performed

Reviewed W3C WebAuthn Level 3 Recommendation (25 August 2026), NIST SP 800-63B-4, Android Keystore and Credential Manager documentation, FIDO Alliance high-assurance guidance and Yubico FIDO2 key/PIN lifecycle documentation.

## Material findings

1. WebAuthn Level 3 distinguishes backup eligibility (BE, permanent property) from backup state (BS, mutable state). A passkey must not be assumed device-bound; relying parties need to record and assess these authenticator flags and provenance.
2. WebAuthn binds credentials to an RP ID and signs origin/context, providing phishing resistance when correctly verified. User verification can be PIN/password/biometric and does not prove a unique natural person's identity in all circumstances.
3. NIST SP 800-63B-4 defines AAL3 as phishing-resistant public-key authentication with a non-exportable key and two distinct factors. This is used only as a design benchmark; no compliance claim is made.
4. Android Keystore prevents app-process extraction of private key material and can bind keys to TEE/StrongBox. A compromised app process may still invoke keys unless key-use authorizations prevent it; a compromised OS may use TEE-backed keys. StrongBox is optional, resource constrained and device-dependent.
5. Android Credential Manager passkeys may be synchronized/restored by a credential provider. The API's availability does not prove the credential is device-bound or StrongBox-backed.
6. Dedicated FIDO2 keys provide a clearer device-bound credential model but create physical-loss, PIN-reset, spare-key and replacement-ceremony requirements.
7. WebAuthn authenticates credential control, not the user's comprehension of a financial transaction. A future approval challenge must bind the exact canonical action digest and authority/policy generation, with explicit display/confirmation, one-time nonce, replay prevention and dispatch-time version recheck.
8. Recovery must revoke lost/compromised credentials, sessions and permits, establish fresh key material, verify independent current revocation state, reconcile outstanding actions and require explicit reactivation. Restoring backups must never resurrect revoked authority.

## Disposition

No device, authenticator, vendor, key type or recovery approach selected. Provisional requirements recorded under ODR-10. Synced passkeys remain a convenience/recovery trust domain, not the sole independent root. Device-bound authentication remains a candidate for high-assurance approval subject to actual platform verification.

## Repository changes

Created docs/IDEAL_OWNER_AUTHENTICATOR_AND_RECOVERY_OPTIONS.md; updated owner decision register, host trust topology, security control traceability, Phase 02 document map, roadmap, README and audit index; created this checkpoint record.

## Boundaries

No device inspection, account, authenticator registration, key generation, hardware purchase, credential, hosting, code, runtime or financial action. No compliance assessment or platform test. No owner decision accepted; Phase 02 active; Phases 03–19 locked.
