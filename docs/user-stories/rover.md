# ROVER — User Story Bundles (Rover Mission Control)

> Domain: **Rover Mission Control** (prefix `ROVER`).
> Source: [`architecture/`](../../architecture/). Inventory & Pareto plan: [README.md](./README.md).

**Bundle status**

| Story | Priority | State |
|-------|----------|-------|
| ROVER-STORY-001 | Pareto Core 20% | Drafted — awaiting approval |
| ROVER-STORY-002 … 015 | Supporting 80% / Backlog | Pending |

---

## ROVER-STORY-001

### Architecture Traceability

| Trace | Link |
|-------|------|
| Requirements | [Ch. 1.1](../../architecture/01-introduction-and-goals.md), [Ch. 3.2.1 Core Functionality](../../architecture/03-context-and-scope.md) |
| Responsibilities | [Ch. 3.5 Position Tracking / Command Validation](../../architecture/03-context-and-scope.md) |
| Data flow | [Ch. 4.3.3 Data Flow](../../architecture/04-solution-strategy.md) |
| Components | Command Interface (5.3.2.1), Command Parser (5.3.2.2), Rover Navigation (5.3.2.3), Grid Management (5.3.2.4), Mission State (5.3.2.5) — [Ch. 5.3](../../architecture/05-building-block-view.md) |
| Interfaces | [Ch. 5.5 Interfaces and Contracts](../../architecture/05-building-block-view.md) |
| Runtime scenario | [Ch. 6.3 Successful Command Execution](../../architecture/06-runtime-view.md) |
| State lifecycle | [Ch. 8.4 State Management](../../architecture/08-cross-cutting-concepts.md) |
| Decisions | [ADR-001](../../architecture/09-architecture-decisions.md), [ADR-002](../../architecture/09-architecture-decisions.md) |

### Original Story

**ROVER-STORY-001**

> **AS A** Mission Operator
> **I WANT** to submit a command sequence together with a starting position and grid size and receive the resulting rover position and heading
> **SO THAT** I can navigate the rover to a target location on the Martian grid and confirm where it ended up.

**Priority:** `Pareto Core 20%`

**Acceptance Scenarios**

#### SCENARIO 1: Canonical valid sequence produces the expected final position

**Scenario ID**: ROVER-STORY-001-S1

**GIVEN**
* a 5×5 grid with no obstacles
* the rover starts at position `(1, 2)` facing North (`N`)

**WHEN**
* the Mission Operator submits command sequence `"LMLMLMLMM"`

**THEN**
* every command is processed in order
* the final position is `(1, 3)` facing `N`
* the console reports `"Final position: 1 3 N"`
* the process exits with code `0`

#### SCENARIO 2: A turn-only sequence rotates without changing position

**Scenario ID**: ROVER-STORY-001-S2

**GIVEN**
* a 5×5 grid with no obstacles
* the rover starts at `(0, 0)` facing `N`

**WHEN**
* the Mission Operator submits command sequence `"RRRR"`

**THEN**
* the rover heading passes through `E → S → W → N`
* the position remains `(0, 0)`
* the final state is `(0, 0)` facing `N`

#### SCENARIO 3: Movement follows the current heading

**Scenario ID**: ROVER-STORY-001-S3

**GIVEN**
* a 5×5 grid with no obstacles
* the rover starts at `(0, 0)` facing East (`E`)

**WHEN**
* the Mission Operator submits command sequence `"MMLMLM"`

**THEN**
* the state evolves `(0,0,E) → (1,0,E) → (2,0,E) → (2,0,N) → (2,1,N) → (2,1,W) → (1,1,W)`
* the final position is `(1, 1)` facing `W`

#### SCENARIO 4: Mission state reflects every successful operation

**Scenario ID**: ROVER-STORY-001-S4

**GIVEN**
* a 5×5 grid with no obstacles
* the rover starts at `(1, 2)` facing `N`
* mission state is initialised to the starting position

**WHEN**
* the sequence `"LMLMLMLMM"` executes and each operation is valid

**THEN**
* mission state is updated after each valid operation
* reading the final state returns `(1, 3, N)` — the cumulative result of the last successful operation

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-001.1 — Accept mission arguments and emit the final position

**AS A** Mission Operator
**I WANT** to pass `--commands`, `--position` and `--grid` on the command line and see the final position
**SO THAT** I can drive the rover from a terminal without any other interface.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 5.5.1 External Interface](../../architecture/05-building-block-view.md), [Ch. 7.4.2 Execution](../../architecture/07-deployment-view.md).

##### SCENARIO 1: Valid invocation prints the final position

**Scenario ID**: ROVER-FE-001.1-S1

**GIVEN**
* the application is installed and runnable
* arguments `--commands "LMLMLMLMM" --position "1 2 N" --grid "5 5"`

**WHEN**
* the operator runs the CLI

**THEN**
* the three arguments are parsed and forwarded to the Command Parser unchanged
* stdout contains `"Final position: 1 3 N"`
* the process exits with code `0`

##### SCENARIO 2: Output format is exactly `Final position: <x> <y> <heading>`

**Scenario ID**: ROVER-FE-001.1-S2

**GIVEN**
* a successful execution ending at `(1, 3, N)`

**WHEN**
* the CLI formats its result

**THEN**
* the output is the single line `"Final position: 1 3 N"`
* no debug or trace output pollutes stdout by default

##### SCENARIO 3: Argument values are passed through verbatim

**Scenario ID**: ROVER-FE-001.1-S3

**GIVEN**
* the operator quotes the command string and the position string as shell arguments

**WHEN**
* the CLI parses `--commands "LMLMLMLMM"` and `--position "1 2 N"`

**THEN**
* internal spaces in the position are preserved and split into `x y heading`
* the command string is not reordered or altered

---

#### ROVER-FE-001.2 — Provide usage/help and stable exit codes

**AS A** Mission Operator
**I WANT** discoverable usage information and predictable exit codes
**SO THAT** I can learn the interface and script rover runs reliably.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [ADR-002 argparse](../../architecture/09-architecture-decisions.md), [Ch. 8.2 Layered Validation](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: `--help` documents the three mission arguments

**Scenario ID**: ROVER-FE-001.2-S1

**GIVEN**
* the application is installed

**WHEN**
* the operator runs the CLI with `--help`

**THEN**
* usage text lists `--commands`, `--position` and `--grid`
* the process exits with code `0`

##### SCENARIO 2: Success and usage-error exit codes are distinct

**Scenario ID**: ROVER-FE-001.2-S2

**GIVEN**
* one successful invocation and one invocation missing a required argument

**WHEN**
* both are executed

**THEN**
* the successful run exits `0`
* the missing-argument run prints an `argparse` usage error to stderr and exits non-zero

---

### BE Sub-Stories — Domain Bounded Contexts (Ch. 5.3.2.2–5.3.2.5)

#### ROVER-BE-001.1 — Parse a valid command string into an ordered operation list

**AS A** Command Parser
**I WANT** to convert a valid `L`/`R`/`M` string into an ordered list of operations
**SO THAT** Rover Navigation can execute the sequence deterministically.

**Traceability:** [Ch. 5.3.2.2 Command Parser](../../architecture/05-building-block-view.md), [Ch. 5.5.2 `parse_command_string`](../../architecture/05-building-block-view.md), [Ch. 6.3 Phase 1](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Mixed valid sequence maps to operations in order

**Scenario ID**: ROVER-BE-001.1-S1

**GIVEN**
* the command string `"LMLMLMLMM"`

**WHEN**
* `parse_command_string("LMLMLMLMM")` is called

**THEN**
* it returns `[TurnLeft, MoveForward, TurnLeft, MoveForward, TurnLeft, MoveForward, TurnLeft, MoveForward, MoveForward]`
* the order and duplicates are preserved

##### SCENARIO 2: Single-character sequences map correctly

**Scenario ID**: ROVER-BE-001.1-S2

**GIVEN**
* the inputs `"L"`, `"R"` and `"M"`

**WHEN**
* each is parsed

**THEN**
* `"L"` → `[TurnLeft]`, `"R"` → `[TurnRight]`, `"M"` → `[MoveForward]`

##### SCENARIO 3: Parsing is pure and side-effect free

**Scenario ID**: ROVER-BE-001.1-S3

**GIVEN**
* the same valid command string

**WHEN**
* it is parsed multiple times

**THEN**
* every call returns an equal operation list
* no mission state or external resource is modified

---

#### ROVER-BE-001.2 — Update heading via a 90° rotation state machine

**AS A** Rover Navigation
**I WANT** `L` and `R` to rotate the heading by 90° without moving the rover
**SO THAT** the rover can be re-oriented before moving.

**Traceability:** [Ch. 4.4.2 Rotation logic](../../architecture/04-solution-strategy.md), [Ch. 5.3.2.3 Rover Navigation](../../architecture/05-building-block-view.md), [Ch. 6.3.4 State Transitions](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Four left turns cycle back to North

**Scenario ID**: ROVER-BE-001.2-S1

**GIVEN**
* the rover is at `(2, 2)` facing `N`

**WHEN**
* `TurnLeft` is applied four times

**THEN**
* the heading cycles `N → W → S → E → N`
* the position remains `(2, 2)` throughout

##### SCENARIO 2: Four right turns cycle back to North

**Scenario ID**: ROVER-BE-001.2-S2

**GIVEN**
* the rover is at `(2, 2)` facing `N`

**WHEN**
* `TurnRight` is applied four times

**THEN**
* the heading cycles `N → E → S → W → N`
* the position remains `(2, 2)` throughout

##### SCENARIO 3: Rotation never changes coordinates

**Scenario ID**: ROVER-BE-001.2-S3

**GIVEN**
* any position and heading on the grid

**WHEN**
* any `L` or `R` operation is applied

**THEN**
* `(x, y)` is unchanged
* only the heading is updated

---

#### ROVER-BE-001.3 — Compute and validate forward movement per heading

**AS A** Rover Navigation
**I WANT** `M` to advance one grid unit in the current heading, validated against the Grid
**SO THAT** the rover moves correctly and only into legal cells.

**Traceability:** [Ch. 4.4.2 Movement calculation](../../architecture/04-solution-strategy.md), [Ch. 5.3.2.3](../../architecture/05-building-block-view.md), [Ch. 5.5.2 `can_move_to`](../../architecture/05-building-block-view.md), [Ch. 6.3 Phase 2](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Forward movement follows heading arithmetic

**Scenario ID**: ROVER-BE-001.3-S1

**GIVEN**
* a rover at `(1, 2)` and a 5×5 grid

**WHEN**
* `MoveForward` is applied facing each heading

**THEN**
* facing `N` → `(1, 3)`, facing `S` → `(1, 1)`, facing `E` → `(2, 2)`, facing `W` → `(0, 2)`

##### SCENARIO 2: Grid validation precedes the state commit

**Scenario ID**: ROVER-BE-001.3-S2

**GIVEN**
* a proposed move to position `p` in the current heading

**WHEN**
* `M` is processed

**THEN**
* `can_move_to(p, heading)` is consulted before any state change
* on `(True, None)` the new position is committed
* on `(False, reason)` no state mutation occurs (detailed in ROVER-STORY-003)

##### SCENARIO 3: Interior moves are always legal on an obstacle-free grid

**Scenario ID**: ROVER-BE-001.3-S3

**GIVEN**
* a 5×5 grid with no obstacles and a rover at `(2, 2)`

**WHEN**
* `M` is applied in any heading

**THEN**
* the move is accepted and the coordinates update by exactly one unit on the correct axis

---

#### ROVER-BE-001.4 — Maintain and expose in-memory mission state

**AS A** Mission State
**I WANT** to hold the current position and heading and expose it to the console
**SO THAT** the final position can be reported and state is consistent during execution.

**Traceability:** [Ch. 5.3.2.5 Mission State](../../architecture/05-building-block-view.md), [Ch. 5.5.2 `set_current_position` / `get_current_position`](../../architecture/05-building-block-view.md), [Ch. 6.8 State Management](../../architecture/06-runtime-view.md), [Ch. 8.4](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: State is initialised from the starting position

**Scenario ID**: ROVER-BE-001.4-S1

**GIVEN**
* a starting position `(1, 2, N)`

**WHEN**
* a mission begins

**THEN**
* `get_current_position()` returns `(1, 2, N)` before any command executes

##### SCENARIO 2: State is updated after each valid operation

**Scenario ID**: ROVER-BE-001.4-S2

**GIVEN**
* a running sequence where operations succeed

**WHEN**
* each valid operation completes

**THEN**
* `set_current_position(position, heading)` is called
* `get_current_position()` returns the latest committed position and heading

##### SCENARIO 3: State does not carry over between invocations

**Scenario ID**: ROVER-BE-001.4-S3

**GIVEN**
* a completed mission ending at `(1, 3, N)`

**WHEN**
* a new invocation starts with `--position "0 0 E"`

**THEN**
* the new mission state begins at `(0, 0, E)`
* the previous run's position is not visible

---

### INFRA Sub-Stories — Deployment, State Store, Observability

#### ROVER-INFRA-001.1 — Package for local deployment with a console entry point

**AS A** Course Student
**I WANT** to install the project into a Python 3.12 virtual environment and run a `mars_rover` command
**SO THAT** the CLI is reproducible and easy to launch.

**Traceability:** [Ch. 7.4 Deployment Process](../../architecture/07-deployment-view.md), [Ch. 4.2.3 Build and Packaging](../../architecture/04-solution-strategy.md), [Ch. 2.1 Python 3.12 / Minimal Dependencies](../../architecture/02-constraints.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: Editable install exposes the console command

**Scenario ID**: ROVER-INFRA-001.1-S1

**GIVEN**
* a Python 3.12 virtual environment
* the repository checked out locally

**WHEN**
* `pip install -e ".[dev]"` is run

**THEN**
* installation succeeds with only standard-library runtime dependencies
* a `mars_rover` console entry point is available

##### SCENARIO 2: Installed command runs a mission from any directory

**Scenario ID**: ROVER-INFRA-001.1-S2

**GIVEN**
* the package is installed in the active environment

**WHEN**
* the operator runs `mars_rover --commands "LMLMLMLMM" --position "1 2 N" --grid "5 5"`

**THEN**
* the command resolves without referencing a source path
* it prints `"Final position: 1 3 N"`

##### SCENARIO 3: Module entry point also works

**Scenario ID**: ROVER-INFRA-001.1-S3

**GIVEN**
* the project workspace

**WHEN**
* the operator runs `python mars_rover/cli/main.py --commands "LMLMLMLMM" --position "1 2 N" --grid "5 5"`

**THEN**
* the run produces the same `"Final position: 1 3 N"` result (Ch. 7.4.2)

---

#### ROVER-INFRA-001.2 — Manage the in-memory state store lifecycle (no persistence)

**AS A** System
**I WANT** mission state held purely in memory and discarded on exit
**SO THAT** the architecture honours the in-memory-state constraint (ADR-001).

**Traceability:** [ADR-001 In-Memory State](../../architecture/09-architecture-decisions.md), [Ch. 2.1 In-Memory State](../../architecture/02-constraints.md), [Ch. 5.6.3 State Lifecycle](../../architecture/05-building-block-view.md), [Ch. 6.9.3 Resource Management](../../architecture/06-runtime-view.md).

##### SCENARIO 1: A run writes no files to disk

**Scenario ID**: ROVER-INFRA-001.2-S1

**GIVEN**
* a clean working directory
* no persistence option requested

**WHEN**
* a mission executes to completion

**THEN**
* no state, snapshot or log file is created
* all state lived in process memory

##### SCENARIO 2: Runs are independent and deterministic

**Scenario ID**: ROVER-INFRA-001.2-S2

**GIVEN**
* the same command arguments `--commands "LMLMLMLMM" --position "1 2 N" --grid "5 5"`

**WHEN**
* two separate invocations are executed

**THEN**
* both produce `"Final position: 1 3 N"`
* the second run inherits no state from the first

##### SCENARIO 3: Exit discards state

**Scenario ID**: ROVER-INFRA-001.2-S3

**GIVEN**
* a completed invocation ended at `(1, 3, N)`

**WHEN**
* the process exits and a new invocation starts with `--position "0 0 E"`

**THEN**
* the new state begins at `(0, 0, E)`
* the prior position is gone

---

#### ROVER-INFRA-001.3 — Provide optional console logging/observability

**AS A** Course Student
**I WANT** optional debug output for command execution while keeping default output clean
**SO THAT** I can diagnose rover behaviour without polluting operator-facing results.

**Traceability:** [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md), [Ch. 4.5.3 Basic logging](../../architecture/04-solution-strategy.md), [Ch. 2.4 Zero Infrastructure](../../architecture/02-constraints.md).

> **Events/notifications are not applicable** in the initial scope (Ch. 4.8.2 / Ch. 8.5 defer
> telemetry publishing to a future extension). No event bus is introduced.

##### SCENARIO 1: Default output stays clean

**Scenario ID**: ROVER-INFRA-001.3-S1

**GIVEN**
* logging is not enabled

**WHEN**
* a mission executes successfully

**THEN**
* stdout contains only the `Final position:` line
* no per-operation trace is emitted

##### SCENARIO 2: Debug logging emits a per-operation trace

**Scenario ID**: ROVER-INFRA-001.3-S2

**GIVEN**
* debug logging is enabled via an opt-in switch (environment variable or flag)

**WHEN**
* a mission executes

**THEN**
* a trace of each operation and resulting position is written to stderr
* the final `Final position:` line on stdout is unchanged

##### SCENARIO 3: Logging never changes the domain result

**Scenario ID**: ROVER-INFRA-001.3-S3

**GIVEN**
* the same mission run with logging disabled and with logging enabled

**WHEN**
* both runs complete

**THEN**
* the reported final position and exit code are identical

---

*Next bundle: ROVER-STORY-002 — Validate command sequences and reject invalid input (pending approval).*
