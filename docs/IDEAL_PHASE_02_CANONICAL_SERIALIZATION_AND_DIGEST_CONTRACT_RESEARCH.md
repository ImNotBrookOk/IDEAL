# IDEAL Phase 02 — Canonical Serialization and Digest Contract Research

**Checkpoint:** 109 — 18 November 2026  
**Status:** Technology-neutral research; no serializer or wire format selected  
**Scope:** Exact digests, signatures, idempotency, replay and schema evolution  
**Boundary:** No implementation, dependency, database, API or runtime selected.

## 1. Executive result

The existing critical contract schemas correctly require exact decimal values and a versioned canonical digest, but the architecture still lacks the normative byte-level rules needed to compute those digests consistently across implementations.

RFC 8785 JSON Canonicalization Scheme (JCS) does not make arbitrary-precision financial numbers safe by itself. JCS constrains JSON numbers to IEEE-754 binary64-compatible values; the RFC recommends representing values needing higher precision or longer integers as JSON strings. IDEAL's authoritative Decimal, Quantity, Price and AssetAmount fields therefore cannot be emitted as unconstrained JSON numeric tokens under a JCS profile without risking precision loss.

JCS is one viable candidate if IDEAL defines strict string encodings for exact decimals and integer-like values. Deterministic CBOR under RFC 8949 is another candidate, but it still requires an application profile defining numeric representation, tags, map-key ordering, optional/absent fields and semantic versioning. Neither standard removes the need for an IDEAL-specific contract profile.

## 2. Source-derived facts

### RFC 8785 — JSON Canonicalization Scheme

RFC 8785 defines deterministic JSON representation for cryptographic hashing/signing. It requires I-JSON-compatible input and prohibits duplicate property names; constrains JSON number values to IEEE-754 binary64; recommends strings for numbers needing higher precision or longer integers; sorts object property names recursively by UTF-16 code units; preserves array order; emits UTF-8 canonical output; and does not perform Unicode normalization.

Implication: JCS cannot be treated as a generic exact-decimal financial serialization scheme. It can only be considered with an explicit application-level representation for Decimal and integer values, strict validation and test vectors.

### RFC 8949 — CBOR

RFC 8949 defines core deterministic encoding requirements, including preferred shortest encodings and deterministic map ordering. It also describes tag-related semantic ambiguity: an application protocol must specify whether a semantic value is represented with a tag or without one, rather than allowing both forms.

Implication: deterministic CBOR is a candidate binary encoding, but IDEAL must define a constrained profile and reject alternate encodings of the same semantic contract.

### PostgreSQL numeric reference (illustrative only)

PostgreSQL documents NUMERIC as arbitrary precision and recommends it for monetary/exact quantities, while noting it is slower than integer and floating-point types. This is evidence about one database's type semantics, not a database selection or a complete financial arithmetic policy.

## 3. Required IDEAL canonical contract profile

Before any digest/signature-bearing runtime contract is implemented, the profile must define:

1. Canonical envelope: contract family, schema version, semantic version, canonicalization profile ID/version, digest algorithm ID, payload and explicit domain separation.
2. Exact decimal encoding: canonical decimal grammar; no exponent notation unless explicitly specified; no leading plus; no leading zeros except zero; defined negative-zero handling; trailing-zero normalization policy; explicit scale where scale is semantically meaningful; no binary floating-point conversion.
3. Integer encoding: bounded signed/unsigned ranges, canonical base-10 or binary form, overflow rejection.
4. Asset and unit identity: canonical AssetId, instrument/contract specification version, unit, multiplier and precision context included in digest-bearing data.
5. Optionality: distinguish absent, explicit null, unknown, not-applicable and zero; no default insertion that changes meaning.
6. Object rules: duplicate keys rejected before canonicalization; deterministic key order; unknown-field policy per contract family.
7. Strings: UTF-8 validity, control-character handling, Unicode normalization policy (preserve-as-is or normalize under a named profile); never normalize implicitly.
8. Collections: arrays ordered unless schema explicitly declares a set; set elements require canonical sort key and duplicate rejection.
9. Time: UTC representation, precision, leap-second policy, offset/original-zone retention where semantically relevant; timestamp unit and rounding rules explicit.
10. Digest/signature domain separation: include contract family/version and canonicalization profile in the preimage; specify hash algorithm and signature algorithm/key ID separately.
11. Schema evolution: immutable published versions; explicit compatibility class; breaking semantic change requires new version; migration must preserve old bytes and historical verification.
12. Validation order: parse → duplicate/encoding checks → schema validation → semantic validation → canonical encode → digest → signature verification. Never canonicalize malformed or ambiguous input into a valid approval.
13. Replay/idempotency: exact canonical action digest and scope included; deduplication keys scoped to principal, operation and validity window; replay after expiry/revocation denied.
14. Test vectors: golden byte strings and digests across at least two independent implementations, including Unicode, decimals, large integers, absent/null, arrays, map ordering and malformed input.

## 4. Candidate comparison — no selection

| Candidate | Strength | Material limitation for IDEAL | Current disposition |
|---|---|---|---|
| RFC 8785 JCS + IDEAL exact-decimal string profile | Human-inspectable JSON; mature documented deterministic rules; interoperable signing preimage | IEEE-754 number restriction; Unicode preservation rules; custom decimal grammar and application profile still required | Candidate only |
| RFC 8949 deterministic CBOR + IDEAL profile | Compact binary; deterministic encoding rules; native byte representation | Tags and numeric representation still require strict application profile; less human-readable; cross-language implementation/test vectors required | Candidate only |
| Bespoke canonical JSON/CBOR | Can exactly match IDEAL semantics | Highest risk of subtle cross-language divergence, maintenance burden and undocumented edge cases | Do not prefer without compelling evidence |

No performance or security benchmark was performed. No library was evaluated for maintenance, licence, CVEs or cross-language conformance; that belongs in a later implementation dependency review after the owner approves a stack.

## 5. Mandatory negative and conformance test catalogue

Future tests must include:
- same semantic object with different input key order produces identical canonical bytes/digest;
- duplicate object keys are rejected, not silently overwritten;
- decimal values beyond binary64 precision round-trip exactly;
- 1, 1.0, 1.00, negative zero, exponent forms and trailing zeros follow one explicit semantic/scale policy;
- values beyond signed/unsigned integer limits reject;
- Unicode composed/decomposed strings follow the declared policy and never vary silently;
- unknown fields reject or are ignored only where the contract compatibility rule explicitly permits;
- absent, null, unknown, not-applicable and zero remain distinct;
- reordered set values canonicalize identically only for schema-declared sets; array reordering changes digest;
- timestamps with different offsets but same instant follow the declared normalization and source-time preservation rules;
- schema-version change cannot verify under an incompatible old profile;
- same digest with different contract family/profile cannot be replayed across domains;
- expired/revoked approval and idempotency token cannot authorize a new dispatch;
- two independent implementations produce byte-identical golden vectors.

## 6. Required owner/architecture disposition

This research does not choose JCS, CBOR, a database, a language, a serializer or a cryptographic suite. It narrows the design requirement: choose a published deterministic encoding only with a versioned IDEAL profile, exact decimal representation, domain separation and cross-implementation golden vectors.

ODR-12 remains the Phase 02 acceptance gate. ODR-02/03 remain open for financial semantics. Before Phase 03 contract implementation, the architecture baseline must approve the canonical profile and a test plan. No action digest or owner signature should be implemented against an underspecified serialization.

## 7. Sources

- RFC 8785 — JSON Canonicalization Scheme: https://www.rfc-editor.org/rfc/rfc8785.html
- RFC 8949 — Concise Binary Object Representation (CBOR): https://www.rfc-editor.org/rfc/rfc8949.html
- PostgreSQL 17 Numeric Types: https://www.postgresql.org/docs/17/datatype-numeric.html

## 8. Disposition

The canonical serialization gap is now precisely specified as a Phase 02 contract requirement. The architecture remains technology-neutral. The high-severity TST-105-01 finding remains open until a profile is selected and approved; this research does not close it. Phase 02 ACTIVE; Phases 03–19 LOCKED.
