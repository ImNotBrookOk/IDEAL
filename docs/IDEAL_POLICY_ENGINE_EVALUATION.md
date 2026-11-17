# IDEAL Policy Engine Evaluation — Cedar vs Open Policy Agent

**Research checkpoint:** 096  
**Date:** 18 November 2026  
**Phase:** 02 — architecture and infrastructure research  
**Status:** comparative research; no engine selected, adopted or integrated.

## 1. Decision scope

Evaluate policy-engine candidates for the future IDEAL authorization decision point (PDP), with particular attention to action-admission and dispatch safety, policy integrity, deterministic behaviour, runtime coupling, operational burden and failure semantics.

This document does not select the owner policy language, host, deployment model, or runtime. It does not grant authority to execute trades or any other external action. The policy engine is only one input to IDEAL's conjunctive admission decision; it cannot grant authority, relax risk limits, override health/security restrictions, or create an action permit by itself.

## 2. Current upstream state (checked 18 November 2026)

| Candidate | Current release observed | Licence | Relevant recent security state |
|---|---|---|---|
| Cedar Rust policy engine | 4.15.0, released 16 Nov 2026 | Apache-2.0 | Parser memory-exhaustion advisory GHSA-m84h-6f26-p3p7 affects >=4.3 and <4.13; fixed in 4.13.0. Release 4.15.0 adds depth-limited parsing APIs. |
| Open Policy Agent | 1.22.4, released 12 Nov 2026 | Apache-2.0 | High-severity bundle signature verification bypass GHSA-g2pf-6v5v-qcc8 affects <=1.21.2; fixed in 1.21.3. 1.22.4 also updates published binaries for Go HTTP/1 server CVE-2026-97054. |

CedarJava is a separate binding, not the Cedar Rust engine. Its 2026 advisories include policy-expression injection (CVE-2026-55773 / GHSA-qmch-v2q9-wg4p), fixed in 2.3.6, 3.4.1 and 4.9.0; and other high-severity advisories. Do not transfer the Rust engine's security posture to a language binding. Any binding must receive its own version-specific advisory, maintenance, licence and integration review.

## 3. Authorization semantics and critical failure modes

### 3.1 Cedar

Cedar's authorization algorithm provides default deny and forbid-overrides-permit. However, it deliberately uses skip-on-error: if an individual policy evaluation errors, that policy is omitted from the combined decision. A separate matching permit can therefore still result in Allow while another policy errored.

Cedar validation is a separate operation performed when policies are created or loaded; authorization does not automatically validate every policy at decision time. The Cedar documentation also notes that schema changes can make previously validated policies invalid, and that evaluation errors may then cause policies to be skipped.

**IDEAL wrapper requirement:** never treat the engine's Allow field alone as sufficient. Require a complete successful evaluation with zero policy diagnostics/errors, current schema and policy digests, a known policy-set revision, complete request/entity data, and an exact allow decision. Any diagnostic error, missing entity, stale schema/policy, parse/validation failure or incomplete response must produce DENY / POLICY_UNAVAILABLE and prevent dispatch. Policy validation must be mandatory before publication and activation.

### 3.2 Open Policy Agent

OPA is a general-purpose policy engine using Rego. It supports in-process Go APIs/SDK, standalone REST service and other integration approaches. Its policy decision is application-defined: a Rego policy can provide default allow false, but this is not automatic for every query. An undefined decision can be returned as HTTP 200 without a result field. Some runtime input/builtin type errors become undefined by default rather than halting evaluation; explicit strict builtin error behaviour is available for evaluation tools, but must be verified for the exact embedded integration path.

OPA bundles support policy/data distribution and can be activated while the service continues running. Updates are eventually consistent across OPA instances. Health APIs can report initial bundle activation, and status APIs provide more detailed status. Persisted bundles may be loaded best-effort at startup if the bundle server is unavailable.

**IDEAL wrapper requirement:** only accept an explicit, correctly typed Boolean true result from the exact expected decision path. Missing result, undefined, malformed output, evaluation error, missing policy revision, stale bundle, signature/verification failure, inactive bundle or health failure must be deny/unavailable. Pin and bind the active bundle digest/revision to the authority version vector and action intent. A persisted older bundle must not silently satisfy a current policy-generation requirement.

## 4. Security and supply-chain findings

### Cedar

- The Cedar Rust project describes a formal model in Lean, a Rust production engine using the safe subset of Rust, property-based testing and differential testing between the model and implementation.
- GHSA-m84h-6f26-p3p7 disclosed a parser memory-exhaustion issue: a crafted policy of roughly 258 bytes could cause an allocation attempt of about 29 GB in affected versions. Fixed in 4.13.0 by changing the AST representation. Cedar 4.15.0 also exposes depth-limited parsing functions; future integrations should set explicit parse depth and input-size limits, not rely on the default parser alone for untrusted policy text.
- A separate JSON-template issue GHSA-c33x-vcv4-vg3g affected specific malformed JSON templates and was fixed in 4.11.1 / 3.4.3. Avoid JSON-form policy templates unless required and separately validated.
- CedarJava has distinct security advisories. If selected, require patched release, safe value construction (never build policy source from user-controlled values), exact binding/version audit and negative tests.

### OPA

- GHSA-g2pf-6v5v-qcc8 disclosed that unsigned bundles could be accepted despite a signing configuration that omitted keyid, and unsigned delta bundles could replace signed snapshot bundles. Patched in 1.21.3. Any future deployment must use a patched release, explicit signing configuration and keys, signed immutable snapshot bundles, and tests for missing/invalid signatures, empty key IDs, unsigned deltas, rollback and persistence tampering.
- OPA's own documentation describes bundle updates as eventually consistent. This is unsuitable for immediate revocation unless IDEAL independently fences dispatch on a current authority generation and enforces a strict policy-revision freshness rule.
- OPA's server API must not be exposed to untrusted networks. A local embedded API or tightly restricted loopback/private endpoint is preferable to a publicly reachable PDP.

## 5. Comparison for IDEAL

| Criterion | Cedar | OPA |
|---|---|---|
| Primary purpose | Authorization-specific policy language and engine | General-purpose policy engine (authorization and other policy domains) |
| Policy model | Principal/action/resource/context; permit/forbid | Rego rules and arbitrary application-defined decision document |
| Default behaviour | Built-in default deny | Must explicitly define a safe decision; undefined is not a Boolean deny response by itself |
| Explicit deny guardrails | forbid overrides any permit | Must be authored into decision logic and tested |
| Error semantics | Per-policy evaluation errors are skipped; wrapper must reject any error | Some runtime errors become undefined; wrapper must reject errors, undefined and missing result |
| Static validation | Schema-based Cedar validation; separate from evaluation | Compiler/type checks, schemas and strict checks; exact compile/eval configuration must be controlled |
| Embedding | Native Rust library; other language bindings have separate maturity/security posture | Native Go library/SDK; REST service; Wasm options for other runtimes |
| Policy distribution | IDEAL would own signed publication/distribution and activation protocol unless a selected integration supplies it | Bundles, signatures, status and decision logs are built in; eventual consistency and rollout semantics must be controlled |
| Audit | Authorizer diagnostics can identify determining/error policies; IDEAL must persist a canonical decision record | Decision logs/status/metrics available; IDEAL must persist an independently durable canonical decision record |
| Complexity risk | Narrow authorization model; schema/entity modeling is explicit | More expressive/general, therefore more room for policy complexity and unintended rule semantics |
| Key risk for this use | Skip-on-error must be overridden at wrapper boundary; binding selection matters | Undefined/error and bundle rollout semantics must be overridden at wrapper boundary |

## 6. Provisional disposition

**No selection.** Cedar is the narrower semantic fit for a dedicated authorization decision point, particularly if the future trusted core is Rust. Its schema validation and permit/forbid model are attractive, but its skip-on-error semantics are not safe to consume directly for IDEAL's action boundary. The wrapper must turn every diagnostic into a denial, and schema/policy publication must be independently validated and versioned.

OPA is a credible alternative if the eventual core is Go or if IDEAL requires one general policy plane for multiple infrastructure controls. It brings more complete distribution, status and decision-log facilities, but the policy language is more expressive and bundle rollout is eventually consistent. The action boundary must pin the exact active bundle revision and fail closed on undefined/error/stale policy.

Do not choose based on feature lists or current release number alone. The final decision depends on the actual core language/runtime, policy ownership model, single-host versus multi-host topology, operator burden and testability. Do not introduce both engines by default; dual engines create policy drift and split-brain authorization unless there is a narrowly justified, independently tested use case.

## 7. Mandatory future acceptance tests (not executed)

1. Default-deny: no policy, unknown action, unknown principal/resource, unknown field and unknown policy revision.
2. Cedar: one permit succeeds while another policy errors; wrapper must deny. Forbid overrides permit. Schema drift invalidates publication. Missing entity, overflow, malformed extension value and invalid context deny.
3. OPA: undefined decision, missing result, non-Boolean result, builtin type error, conflicting rule values, unknown route/team and evaluation timeout deny.
4. Policy supply chain: invalid signature, unsigned bundle, empty/missing key ID, unsigned delta downgrade, stale bundle, rollback, tampered persisted bundle and signer rotation.
5. Publication lifecycle: parse, schema/type validation, static analysis, test suite, human-readable diff, exact digest approval, signature, monotonic generation, staged activation, health confirmation and rollback only to an explicitly approved still-valid generation.
6. Concurrency: policy generation changes between admission and dispatch; dispatch must reject if the authority/policy version vector no longer matches.
7. Audit: record request digest, policy digest, schema digest, engine/build version, decision, diagnostics, decision time, authority generation and correlation ID before any consequential external action.
8. Resource limits: parse depth, input size, memory, CPU, evaluation deadline and cancellation; untrusted policy compilation must not share an unbounded critical process.
9. Determinism: repeat identical inputs against the same policy/schema/entity snapshot and verify stable decisions and diagnostics.
10. Revocation: policy update or revocation must fence stale workers independently of eventual bundle propagation.

No security or performance tests were run in this research checkpoint.

## 8. Sources

- Cedar authorization algorithm: https://docs.cedarpolicy.com/auth/authorization.html
- Cedar validation and schema semantics: https://docs.cedarpolicy.com/policies/validation.html
- Cedar security engineering: https://docs.cedarpolicy.com/other/security.html
- Cedar releases: https://github.com/cedar-policy/cedar/releases
- Cedar parser OOM advisory: https://github.com/cedar-policy/cedar/security/advisories/GHSA-m84h-6f26-p3p7
- Cedar JSON-template advisory: https://github.com/cedar-policy/cedar/security/advisories/GHSA-c33x-vcv4-vg3g
- CedarJava policy injection advisory: https://github.com/cedar-policy/cedar-java/security/advisories/GHSA-qmch-v2q9-wg4p
- OPA integration documentation: https://www.openpolicyagent.org/docs/integration
- OPA bundle management: https://www.openpolicyagent.org/docs/management-bundles
- OPA errors guide: https://www.openpolicyagent.org/docs/errors
- OPA releases: https://github.com/open-policy-agent/opa/releases
- OPA bundle-signature advisory: https://github.com/open-policy-agent/opa/security/advisories/GHSA-g2pf-6v5v-qcc8

## 9. Scope and authority boundary

This is research and documentation only. No engine, binding, dependency, policy, host, account, credential, exchange integration or runtime was installed, selected or tested. No execution authority or policy permission was created. Existing accepted decisions remain unchanged. Phase 02 remains active; Phases 03–19 remain locked.
