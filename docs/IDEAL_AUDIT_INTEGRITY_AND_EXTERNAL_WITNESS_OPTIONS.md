# IDEAL Audit Integrity and External Witness Options

**Research checkpoint:** 098  
**Date:** 18 November 2026  
**Phase:** 02 — audit, recovery and infrastructure research  
**Status:** architecture comparison; no audit database, transparency log, witness, service or provider selected.

## 1. Purpose

Evaluate how IDEAL can detect retrospective tampering, truncation, rollback and split-view attacks against its durable audit trail, while preserving privacy and avoiding an unnecessary external dependency.

The central distinction is:
- **Authoritative audit storage:** retains the complete event records and supports retrieval/reconciliation.
- **Tamper evidence:** cryptographically detects changes to records or history.
- **External witnessing:** an independent trust domain stores/checks a commitment to the audit history so a host that controls the local log cannot silently rewrite both the records and every local integrity anchor.

A hash chain or Merkle tree on the same compromised host is not independent evidence. A transparency log is a witness, not a replacement for IDEAL's durable event store.

## 2. Current project and standards findings

### Sigstore Rekor / Rekor v2 (tile-backed)

Sigstore describes Rekor as an append-only transparency log for software-signing metadata. Merkle inclusion proofs show that a record is committed to a signed checkpoint; consistency proofs show that a later tree extends an earlier tree. Sigstore's security model explicitly says logs require independent monitoring/witnessing and that the log must not be trusted as the sole source of truth.

The Rekor v2 specification describes:
- signed checkpoints containing the Merkle root and log state;
- inclusion and consistency proofs that can be verified offline;
- periodically updated checkpoints and batching (the spec describes roughly 2–10 seconds for entry integration, depending on configuration);
- log sharding and TUF-distributed discovery of active shard URLs and trust roots;
- a synchronous witness design in which a log obtains witness co-signatures before returning an inclusion proof.

Important qualification: the Rekor v2 client documentation notes that initial launch checkpoints were not witnessed while the public witness network was being established. Do not assume that a given public endpoint currently returns witness-cosigned checkpoints; inspect its live trust configuration and actual response before relying on that property.

Rekor records are append-only and cannot be deleted. The service is designed for software-signature metadata, not private financial event storage. Do not submit personal finance, account, order, trading, tax or other sensitive IDEAL records to a public transparency log.

### Tessera and Trillian

Google Trillian documentation now states that Trillian is in maintenance mode and recommends Tessera for new transparency-log deployments. Tessera is an implementation of a verifiable, tile-backed transparency log. Rekor v2 uses Tessera as its underlying transparency-log implementation.

A current read of the Tessera repository showed active development and open operational issues, including AWS storage/connection lifecycle, slow object-storage writes, publication polling and fsck error handling. This is not evidence of a vulnerability; it is evidence that a self-hosted witness stack carries real operational and storage-backend complexity. Do not adopt Tessera as a lightweight embedded library or assume a one-click private log.

### immudb

immudb is an immutable database with a cryptographically protected append-only transaction log, Merkle proofs and verified read APIs. It can provide a stronger tamper-evident storage model than an ordinary mutable database. However:
- it is a separate database/service and changes the storage/operations architecture;
- old transactions cannot be modified or deleted, which complicates privacy deletion and retention obligations;
- its index is built asynchronously;
- replicas can be eventually consistent;
- proof verification remains a client/auditor responsibility;
- its own documentation describes optional signing of database state and external auditors.

immudb is a database option, not an independent witness by itself if the same operator/host controls the server, signing key and all replicas.

## 3. Threat model and limits

| Threat | Local hash chain/Merkle root only | Independent witness/checkpoint |
|---|---|---|
| Accidental record corruption | Detectable if recomputed against trusted prior root | Detectable |
| Single event modification/deletion | Detectable if a trusted root exists outside the modified store | Detectable with inclusion/consistency evidence |
| Tail truncation / rollback | Not reliably detectable if attacker can roll back both data and local root | Detectable if an external witness retains a newer checkpoint |
| Rewriting entire history | Not detectable if all keys and anchors are controlled by attacker | Detectable if witness independently retains and checks prior checkpoint |
| Split-view log | Local client may see only one view | Cross-witness gossip/cosignatures can expose inconsistent views |
| False but properly recorded event | Not prevented | Not prevented |
| Compromised signing key before checkpoint | May authenticate attacker-created events | Witness proves the event was committed, not that it was legitimate |
| Witness outage/partition | Local integrity remains available | Fresh external assurance unavailable; must report uncertainty |
| Public metadata leakage | None if local only | Possible through submitted data, timing, digest correlation and proof queries |

Transparency does not prove the truth of an event, prevent an authorized writer from recording a false event, guarantee service availability, or replace access control and incident response.

## 4. Privacy and retention constraints

- Never publish raw audit records, account IDs, instrument names, order details, balances, tax data, bank references, user identifiers or AI traces to a public log.
- Even a hash may leak information if the underlying event has low entropy or can be guessed. Hashing alone is not anonymization.
- A public append-only log cannot honor deletion of a submitted leaf. Therefore do not place personal or regulated content in a public transparency log, even encrypted, unless a separate legal/privacy assessment explicitly approves it.
- Prefer a batch commitment over a set of opaque, randomly salted event digests, with the salt and event mapping held locally. The public witness receives only a commitment to the batch root and minimal protocol metadata. This reduces direct disclosure but does not eliminate timing, frequency or correlation leakage.
- Retain local records according to the source/purpose-specific retention and deletion policy. External witness commitments should be non-identifying, minimally descriptive and separately classified.
- A commitment must be generated only after the local audit batch is durably committed. The witness must never become the primary audit store.

## 5. Candidate models

| Model | Benefits | Limitations | IDEAL disposition |
|---|---|---|---|
| Local append-only hash chain / Merkle checkpoints | Lowest cost and fewest external dependencies; supports deterministic local verification | Host/root compromise can rewrite both data and local anchor; no independent rollback detection | Mandatory baseline, but not sufficient against full host compromise |
| Periodic independent signed checkpoint | Small external data footprint; can detect local history rollback/truncation if the witness retains checkpoints independently | Requires independent key custody and durable remote state; availability/partition affects freshness | Strong candidate for a future low-cost single-owner system |
| Self-hosted Tessera/Rekor-style log with independent witnesses | Standard inclusion/consistency proofs, offline verification and witness cosignatures | Operationally substantial: log service, storage, key rotation, sharding, monitoring, witness quorum, upgrades and backup | Research reference only; likely disproportionate unless audit requirements expand |
| Public Sigstore Rekor | Mature public transparency ecosystem and externally operated service | Public/append-only; designed for software signatures; privacy leakage and external availability; witness support must be verified | Do not use for private financial events; possible only for non-sensitive software supply-chain attestations |
| immudb as authoritative audit store | Immutable transaction log, verified reads, history and audit APIs | Adds a separate database; immutable deletion conflict; async index/replica behaviour; server still needs independent auditor/key separation | Candidate only if ordinary DB durability/audit requirements cannot be met; not a default choice |

## 6. Provisional architecture direction

Do not introduce a second database or public log by default. Preserve the current logical design:
1. IDEAL-owned authoritative journal records immutable event envelopes and causal references.
2. Local integrity layer links committed audit batches with a cryptographic hash/Merkle structure.
3. A separately controlled checkpoint signer periodically signs the current batch root, tree size, monotonic sequence, timestamp interval, schema/algorithm identifiers and prior-checkpoint reference.
4. An independent witness stores the signed checkpoint and refuses rollback or non-monotonic generations.
5. IDEAL retains the latest acknowledged checkpoint and proof material locally; verification can be performed offline.
6. Recovery compares restored journal state with the newest independently witnessed checkpoint. If the restored state is older, inconsistent or cannot be checked, enter RECOVERY_HOLD.
7. The witness stores no event payloads and cannot authorize actions, publish policies, release risk reservations or restore credentials.

For a single-owner, low-cost architecture, first evaluate a minimal remote checkpoint service with an independently held signing/witness key rather than deploying a full general-purpose transparency-log cluster. The exact independent trust boundary matters more than the product name: a second process or database under the same host root and credentials is not independent.

No external checkpoint is currently mandatory for action dispatch; the owner decision remains open. Local durable audit-before-action remains mandatory. If the chosen topology cannot guarantee a current external witness during a partition, it must accurately report checkpoint age/uncertainty and apply the approved restricted mode rather than claim fresh independent assurance.

## 7. Mandatory future verification (not executed)

1. Tamper with, delete, reorder and truncate historical records; verify detection from a checkpoint held outside the primary host.
2. Restore an older database and older local checkpoint while the independent witness retains a newer one; require RECOVERY_HOLD.
3. Present two different histories to two clients; verify witness gossip/cosignatures detect split views.
4. Rotate checkpoint keys and witness keys; test revocation, overlap, rollback and lost-key recovery.
5. Verify inclusion and consistency proofs offline with independently provisioned trust roots.
6. Simulate witness outage, network partition, stale checkpoint, clock rollback and delayed publication.
7. Ensure a failed checkpoint upload does not corrupt or block local durable audit, while status explicitly reports no fresh witness.
8. Verify no event payload, identity, account, instrument, order or low-entropy digest is sent to a public service.
9. Test deletion/retention propagation and confirm public immutable logs are not used for personal or financial event records.
10. Verify witness and log operator credentials cannot sign owner approvals, policies or action permits.
11. Benchmark local hash/checkpoint overhead and remote batching without using real financial data.
12. Confirm audit retention, export and recovery remain possible if the witness provider disappears.

No implementation, test, benchmark, deployment or external service call was performed.

## 8. Sources

- Sigstore security model: https://docs.sigstore.dev/about/security/
- Rekor overview: https://docs.sigstore.dev/logging/overview/
- Rekor v2 specification: https://github.com/sigstore/architecture-docs/blob/main/rekor-v2-spec.md
- Rekor v2 implementation: https://github.com/sigstore/rekor-tiles
- Tessera repository: https://github.com/transparency-dev/tessera
- Tessera releases: https://github.com/transparency-dev/tessera/releases
- Trillian maintenance notice: https://google.github.io/trillian/
- Trillian transparent logging guide: https://google.github.io/trillian/docs/TransparentLogging.html
- immudb overview: https://immudb.io/docs/immudb/
- immudb verified reads: https://immudb.io/docs/develop/reading/
- immudb performance and replication: https://immudb.io/docs/production/performance-guide/
- immudb audit logging: https://immudb.io/docs/develop/sql/auditlog/
- RFC 9162 Certificate Transparency Version 2.0: https://www.rfc-editor.org/rfc/rfc9162

## 9. Authority boundary

Research only. No database, transparency log, witness, provider, account, key, credential, external service or deployment selected or provisioned. No event or financial data transmitted. Existing owner decisions remain unchanged. Phase 02 remains active; Phases 03–19 remain locked.
