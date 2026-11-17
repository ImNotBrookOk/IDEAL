# IDEAL Work Audit — Checkpoint 098

**Date:** 18 November 2026  
**Workstream:** Phase 02 — audit integrity, external checkpoint and witness options  
**Status:** Research and documentation only.

## Research performed

Reviewed official Sigstore security model and Rekor documentation/specification, Rekor v2 implementation repository, Tessera repository/releases, Trillian documentation, immudb database/verified-read/replication/audit documentation and RFC 9162. Queried current GitHub repository activity and open issues for Tessera.

## Material findings

1. A local hash chain/Merkle tree detects changes only relative to a trusted checkpoint. If the attacker controls the host, data and all local integrity keys, the attacker can rewrite the entire history and local anchor.
2. Sigstore's transparency model uses signed Merkle checkpoints, inclusion proofs and consistency proofs. Its security model says logs need independent monitoring/witnesses and should not be trusted as the source of truth.
3. Rekor v2 uses a tile-backed Tessera implementation, batches entries and periodically updates checkpoints. Its specification describes synchronous witness co-signing, but the implementation documentation says initial launch checkpoints were not witnessed while the public witness network was being established. A live deployment's witness properties must be verified rather than assumed.
4. Trillian documentation states it is in maintenance mode and recommends Tessera for new transparency logs.
5. Tessera has active development but current open issues include backend connection lifecycle, slow object-storage writes, polling and fsck behaviour. Self-hosting is an operational project, not a lightweight dependency.
6. immudb provides an append-only cryptographic transaction log and verified read APIs, but adds a database/service; records cannot be deleted; indexing and replication have asynchronous/eventual-consistency aspects; independent auditors remain relevant. It is not an external witness when the same operator controls it and all keys.
7. Public transparency logs are append-only and expose submitted metadata. Do not publish personal/financial records or low-entropy hashes. A public log is not an authoritative audit database and does not prove event truth.
8. Provisional direction: local authoritative audit + local hash/Merkle chain + periodic minimal signed batch checkpoint retained by an independent trust domain. Keep raw records local. On stale/missing/inconsistent checkpoint during recovery, report uncertainty and require RECOVERY_HOLD.

## Repository changes

Created docs/IDEAL_AUDIT_INTEGRITY_AND_EXTERNAL_WITNESS_OPTIONS.md; updated ODR-11 evidence in the owner decision register, host trust topology, data retention/audit policy, Phase 02 document map, roadmap, README and audit index; created this audit.

## Boundaries

No database, transparency log, witness, provider, account, key, credential, external service, deployment, code or benchmark. No financial or personal data transmitted. No owner decision accepted; Phase 02 active; Phases 03–19 locked.
