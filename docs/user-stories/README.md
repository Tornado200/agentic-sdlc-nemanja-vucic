# Mars Rover — User Story Inventory & Pareto Plan

> Derived from the arc42 architecture in [`architecture/`](../../architecture/).
> Method: Domain-Driven Design (bounded contexts → aggregates) + Pareto (80/20) prioritization.

## 1. Source of Truth

| Concern | Architecture source |
|---------|---------------------|
| Requirements overview | [Ch. 1.1 Requirements Overview](../../architecture/01-introduction-and-goals.md) |
| Quality goals | [Ch. 1.2 Quality Goals](../../architecture/01-introduction-and-goals.md) |
| Scope & responsibilities | [Ch. 3.2 Scope](../../architecture/03-context-and-scope.md), [3.5 Responsibilities](../../architecture/03-context-and-scope.md) |
| Solution strategy & data flow | [Ch. 4 Solution Strategy](../../architecture/04-solution-strategy.md) |
| Building blocks (components) | [Ch. 5 Building Block View](../../architecture/05-building-block-view.md) |
| Runtime scenarios | [Ch. 6 Runtime View](../../architecture/06-runtime-view.md) |
| Deployment | [Ch. 7 Deployment View](../../architecture/07-deployment-view.md) |
| Cross-cutting concepts | [Ch. 8 Cross-cutting Concepts](../../architecture/08-cross-cutting-concepts.md) |
| Decisions | [Ch. 9 ADR-001, ADR-002](../../architecture/09-architecture-decisions.md) |
| Quality requirements | [Ch. 10 Quality Requirements](../../architecture/10-quality-requirements.md) |
| Risks / technical debt | [Ch. 11 Risks and Technical Debt](../../architecture/11-risks-and-technical-debts.md) |
| Glossary | [Ch. 12 Glossary](../../architecture/12-glossary.md) |

## 2. Domain Decomposition (DDD)

The system is a **modular monolith** with one executable and five internal components (Ch. 5.3).
The architecture explicitly frames these boundaries as *bounded contexts* (Ch. 12 Glossary:
"Bounded Context — clear responsibility boundary between modules: parser, navigation, grid, state").

| Bounded Context | Component (Ch. 5) | Core responsibility | Story layer |
|-----------------|-------------------|---------------------|-------------|
| **Command Processing** | Command Parser | Validate `L`/`R`/`M`, convert to operations | **BE** |
| **Navigation** | Rover Navigation | Heading state machine + forward-move arithmetic | **BE** |
| **Terrain / Grid** | Grid Management | Grid dimensions, boundary + obstacle invariants | **BE** |
| **Mission State** | Mission State | In-memory position/heading, per-invocation lifecycle | **BE / INFRA (state store)** |
| **Mission Console** | Command Interface | `argparse` CLI input, formatted output | **FE** |
| **Delivery & Observability** | `pyproject.toml`, tooling | Packaging, logging, quality gates | **INFRA** |

**Ubiquitous language:** Rover, Heading (N/S/E/W), Grid, Obstacle, Command Sequence,
Mission State, ValidationError, BoundaryError, ObstacleError (Ch. 12).

**Primary ubiquitous-language aggregate:** the **Rover** (position + heading) validated against the
**Grid** (bounds + obstacles), producing a **Mission State** snapshot per invocation.

The single core domain prefix used for all story IDs is **`ROVER`** (Rover Mission Control).
FE sub-stories represent the Mission Console; BE sub-stories represent the four domain bounded
contexts; INFRA sub-stories cover packaging, the in-memory state store, and observability.

## 3. Pareto Analysis (80/20)

The **Runtime View (Ch. 6)** defines the four scenarios that constitute the system's mission value:
successful execution (6.3), invalid-command handling (6.4), obstacle violation (6.5), and boundary
violation (6.6). These map onto three core stories:

- **ROVER-STORY-001** covers Ch. 6.3 (successful execution).
- **ROVER-STORY-002** covers Ch. 6.4 (invalid commands / `ValidationError`).
- **ROVER-STORY-003** covers Ch. 6.5 + 6.6, because boundary and obstacle enforcement are the two
  invariants of the single **Grid** aggregate (both owned by Grid Management, Ch. 5.3.2.4).

**Core 3 of 15 stories = 20%**, and they deliver the ~80% of value: every core story exercises the
full `CLI → Parser → Navigation → Grid → State → CLI` path and every primary runtime scenario.

Prioritization follows the required order **`INFRA → BE → FE`**: within each bundle, INFRA
sub-stories are sequenced first, then BE, then FE, so each layer unblocks the next.

| Tier | Stories | Share | Rationale |
|------|---------|-------|-----------|
| **Core 20%** | ROVER-STORY-001, 002, 003 | 3 / 15 = 20% | MVP; maps 1:1 to the four Runtime View scenarios; exercises all five components |
| **Supporting 80%** | ROVER-STORY-004 … 015 | 12 / 15 = 80% | Configuration, diagnostics, state guarantees, persistence, observability, delivery, test scaffolding, evolution |

## 4. Story Inventory

Legend — Priority: `CORE` = Pareto Core 20%, `SUP` = Supporting 80%, `BACKLOG` = future/optional
extension explicitly deferred by the architecture.

| ID | Title | Bounded context / component | Priority | Status |
|----|-------|-----------------------------|----------|--------|
| **ROVER-STORY-001** | Execute a valid command sequence and report the final position | All five components | **CORE** | Bundle drafted — awaiting approval |
| **ROVER-STORY-002** | Validate command sequences and reject invalid input | Command Processing + Mission Console | **CORE** | Pending |
| **ROVER-STORY-003** | Enforce grid spatial constraints (bounds + obstacles) and halt safely | Terrain/Grid + Navigation + State | **CORE** | Pending |
| ROVER-STORY-004 | Configure mission parameters (grid size, start position, heading) with validation | Mission Console + Grid | SUP | Pending |
| ROVER-STORY-005 | Provide a discoverable CLI with help, usage and exit codes | Mission Console (`argparse`) | SUP | Pending |
| ROVER-STORY-006 | Report consistent, actionable error diagnostics with current-position context | Mission Console + error taxonomy | SUP | Pending |
| ROVER-STORY-007 | Guarantee atomic per-operation state updates and last-valid-state preservation | Mission State + Navigation | SUP | Pending |
| ROVER-STORY-008 | Handle empty and whitespace-only command sequences deterministically | Command Processing + Mission Console | SUP | Pending |
| ROVER-STORY-009 | Persist and reload mission snapshots as JSON (optional) | Mission State (persistence) | BACKLOG | Pending |
| ROVER-STORY-010 | Provide optional structured logging for execution tracing | Cross-cutting (Ch. 8.5) | SUP | Pending |
| ROVER-STORY-011 | Package the application for local deployment | Delivery (`pyproject`, entry point) | SUP | Pending |
| ROVER-STORY-012 | Enforce automated quality gates (pytest, ruff, black, isort, ≥80% coverage) | Delivery / QA | SUP | Pending |
| ROVER-STORY-013 | Provide BDD / property-based test scaffolding for runtime scenarios | QA / Software Factory Agents | SUP | Pending |
| ROVER-STORY-014 | Support evolutionary terrain configuration without touching parser/navigation | Terrain/Grid | BACKLOG | Pending |
| ROVER-STORY-015 | Support future multi-rover coordination on a shared grid | Navigation + State | BACKLOG | Pending |

## 5. Pareto Completion Metrics

Updated as bundles are approved. A story counts as **Approved** only after explicit user sign-off.

| Metric | Count | Percentage |
|--------|-------|------------|
| **Core stories approved** | 0 / 3 | 0% |
| **Supporting stories approved** | 0 / 12 | 0% |
| **Total stories approved** | 0 / 15 | 0% |
| Core bundles drafted | 1 / 3 | 33% |
| Core value unlocked (by approval) | 0% | — |

## 6. Bundle Index

All bundles for the `ROVER` domain are maintained in [`rover.md`](./rover.md).

| Story | Bundle section | Layers present |
|-------|----------------|----------------|
| ROVER-STORY-001 | [rover.md § ROVER-STORY-001](./rover.md#rover-story-001) | Original + FE + BE + INFRA |

## 7. Conventions

- **Original:** `ROVER-STORY-{N}` — `AS A … I WANT … SO THAT …`.
- **Frontend (Mission Console / CLI):** `ROVER-FE-{N}.{X}`.
- **Backend (domain/parsing/state/navigation):** `ROVER-BE-{N}.{X}`.
- **Infrastructure:** `ROVER-INFRA-{N}.{X}`.
- **Scenario:** `{STORY-ID}-S{N}` — every scenario is `GIVEN-WHEN-THEN`.
- Every story and sub-story cites the `architecture/` chapter/component it traces to.
