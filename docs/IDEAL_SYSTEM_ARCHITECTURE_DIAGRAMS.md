# IDEAL System Architecture Diagrams

**Status:** Phase 02 logical diagrams; provisional, technology-neutral  
**Checkpoint:** 082 — 17 November 2026  
**Authority:** D-020, D-021, D-022, D-023  
**Boundary:** Conceptual diagrams only. They do not select deployment, storage, API, network, technology or execution authority.

## 1. Domain and evidence flow

```mermaid
flowchart TD
  subgraph SOURCES["External sources — untrusted until validated"]
    MKT["Public / licensed market feeds"]
    BANK["Bank statements / future provider observations"]
    VENUE["Future venue account/order evidence"]
    TAX["Legislation / IRD guidance / assessments"]
  end

  subgraph DATA["Data Integrity and Evidence Plane"]
    REG["Source and entitlement registry"]
    RAW["Immutable raw observations"]
    VAL["Validation, sequence, quality and provenance"]
    CAN["Canonical versioned records"]
    PIT["Point-in-time dataset manifests"]
  end

  subgraph MARKET["Market Research Domain — active: crypto perpetual research"]
    MI["Market intelligence / regimes / features"]
    SR["Strategy research and registry"]
    BT["Backtest and statistical validation"]
    DR["Derivatives risk research"]
  end

  subgraph PRIVATE["Proposed private domains — not active"]
    PF["Personal Finance journal / reconciliation"]
    TX["Tax Intelligence and workpapers"]
    PV["Read-only Portfolio and Capital View"]
  end

  subgraph CROSS["Shared control foundations"]
    RISK["Independent Risk Authority"]
    HEALTH["System Health — restrictive only"]
    SEC["Security and Identity"]
    AUTH["Owner Authority / Policy Registry"]
    AUDIT["Audit and Evidence Registry"]
  end

  MKT --> REG
  BANK --> REG
  VENUE --> REG
  TAX --> REG
  REG --> RAW --> VAL --> CAN
  CAN --> MI --> SR --> BT
  PIT --> BT
  CAN --> DR
  RAW --> PIT
  BANK --> PF
  PF --> TX
  TAX --> TX
  PF --> PV
  TX --> PV
  DR --> PV
  MI --> PV
  RISK -. independent gate .-> DR
  HEALTH -. restrictive interlock .-> RISK
  SEC -. identity and policy enforcement .-> AUTH
  AUTH -. owner grant .-> RISK
  CAN --> AUDIT
  PF --> AUDIT
  TX --> AUDIT
  DR --> AUDIT
  RISK --> AUDIT
  SEC --> AUDIT
  HEALTH --> AUDIT
```

The proposed private domains are not activated. Portfolio/capital is a read-only projection; the diagram does not imply shared ledgers, cash, collateral, permissions or tax treatment.

## 2. Trust zones and forbidden flows

```mermaid
flowchart LR
  Z0["Z0 — Untrusted workloads
AI / strategy / plugins / generated code"]
  Z1["Z1 — Constrained ingestion
External parsers / adapters"]
  Z2["Z2 — Deterministic domain services
Data / research / risk"]
  Z3["Z3 — Protected action boundary
Future gateway / narrow adapters"]
  Z4["Z4 — Trust anchors and recovery
Owner root / policy signing / revocation"]
  UI["Owner device / mobile UI"]
  VENUE["External venue"]

  Z0 -->|"typed proposals only"| Z2
  Z1 -->|"validated observations"| Z2
  Z2 -->|"exact action request"| Z3
  Z4 -->|"signed policy / current generation"| Z3
  UI -->|"authenticated owner ceremony"| Z4
  Z3 -->|"narrow allowlisted egress
only after all gates"| VENUE

  Z0 -. "FORBIDDEN: credentials / venue egress / policy write" .-> VENUE
  Z0 -. "FORBIDDEN: root keys / audit anchor" .-> Z4
  Z1 -. "FORBIDDEN: action authority" .-> Z3
```

Logical zones are mandatory; physical separation is deployment-dependent. Same-host process/VM separation does not survive host-root/kernel compromise.

## 3. Consequential action admission and dispatch

```mermaid
flowchart TD
  A["PROPOSED"] --> B["VALIDATED
Canonical action + evidence"]
  B --> C{"Owner envelope active
and exact scope?"}
  C -->|No / unknown| X["REJECTED"]
  C -->|Yes| D{"Identity + Security
permit exact action?"}
  D -->|No / unknown| X
  D -->|Yes| E{"Data valid and fresh?
Health interlocks clear?"}
  E -->|No / unknown| H["RESTRICTED / INCIDENT_HOLD"]
  E -->|Yes| F{"Independent Risk
APPROVED?"}
  F -->|No / indeterminate| X
  F -->|Yes| G["RESERVED
Durable risk reservation"]
  G --> I["ADMITTED
One-use permit exists"]
  I --> J{"Final generation + version-vector
recheck; audit commit"}
  J -->|Fail / stale / unknown| X
  J -->|Pass| K["DISPATCH_STARTED
Local linearisation point"]
  K --> L["DISPATCHED
Network write attempted"]
  L --> M{"Definitive response?"}
  M -->|Yes| N["ACKNOWLEDGED"]
  M -->|No / timeout| O["UNKNOWN
Keep reservation"]
  N --> P["RECONCILED"]
  O --> P
  P --> Q["Update position / residual reservation
exactly once"]
```

The external venue is outside IDEAL's local ACID transaction. DISPATCH_STARTED means potentially in-flight; it does not prove venue receipt.

## 4. Incident and recovery lifecycle

```mermaid
flowchart TD
  N["NORMAL"] --> D["DEGRADED"]
  D --> R["RESTRICTED"]
  R --> I["INCIDENT_HOLD"]
  I --> Q["RECOVERY_QUARANTINE"]
  Q --> C["RECONCILIATION_REQUIRED"]
  C --> A["ATTESTATION_REQUIRED"]
  A --> O["OWNER_RELEASE_REQUIRED"]
  O --> N
  I -->|Evidence insufficient| I
  Q -->|Trust cannot be established| I
  C -->|Mismatch / unknown| I
  A -->|Any pillar fails| I
  O -->|Owner does not release| R
```

Recovery requires external-state reconciliation, current revocation/identity state, audit/data integrity and scoped pillar attestations. A process restart or successful backup restore is not a recovery release.

## 5. Evidence and temporal lifecycle

```mermaid
flowchart LR
  S["Source event"] --> R["Raw observation
immutable"]
  R --> V["Validation result
versioned"]
  V --> C["Canonical record
revisioned"]
  C --> D["Derived record
lineage"]
  D --> P["Point-in-time dataset
immutable manifest"]
  P --> E["Decision evidence
exact as-of snapshot"]
  E --> A["Audit / reconciliation
ordered event"]
  COR["Late correction"] --> R2["New raw revision"]
  R2 --> V2["New validation"]
  V2 --> C2["New canonical revision"]
  C2 --> D2["Recompute affected current views"]
```

The original as-known-then decision snapshot remains immutable. A late correction creates a new latest-known view and invalidates only dependent current calculations.

## 6. Diagram governance

These diagrams are conceptual and must be reconciled with final contracts, threat model, owner decisions and deployment topology before any implementation blueprint. The arrows show logical information/authority flow, not network routes or API endpoints. Dashed lines represent constrained authority or forbidden-flow concepts, not actual protocol choices.

No implementation, external integration, deployment, paper/live execution or phase advancement is authorised.
