# ROVER — User Story Bundles (Rover Mission Control)

> Domain: **Rover Mission Control** (prefix `ROVER`).
> Source: [`architecture/`](../../architecture/). Inventory & Pareto plan: [README.md](./README.md).

**Bundle status**

| Story | Priority | State |
|-------|----------|-------|
| ROVER-STORY-001 | Pareto Core 20% | Approved |
| ROVER-STORY-002 | Pareto Core 20% | Approved |
| ROVER-STORY-003 | Pareto Core 20% | Approved |
| ROVER-STORY-004 | Supporting 80% | Approved |
| ROVER-STORY-005 | Supporting 80% | Approved |
| ROVER-STORY-006 | Supporting 80% | Approved |
| ROVER-STORY-007 | Supporting 80% | Approved |
| ROVER-STORY-008 | Supporting 80% | Approved |
| ROVER-STORY-009 | Backlog (optional) | Approved |
| ROVER-STORY-010 | Supporting 80% | Approved |
| ROVER-STORY-011 … 015 | Supporting 80% / Backlog | Backlog |

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

> Telemetry events are covered separately in ROVER-INFRA-001.4; this story only covers optional console logging.

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


#### ROVER-INFRA-001.4 — Emit telemetry events for position updates and mission outcomes

**AS A** Ground Control operator
**I WANT** in-process telemetry events for position updates and mission outcomes
**SO THAT** external monitoring can follow the rover's progress.

**Traceability:** [Ch. 3.4.4 Ground Control & Telemetry](../../architecture/03-context-and-scope.md), [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md), [Ch. 2.4 Zero Infrastructure](../../architecture/02-constraints.md).

> Adapted to the architecture: there is no message broker. Events are in-process notifications written to the console (no external services).

##### SCENARIO 1: Position update event after a successful move

**Scenario ID**: ROVER-INFRA-001.4-S1

**GIVEN**
* Telemetry output is enabled
* The rover is at (1, 2, N)

**WHEN**
* The rover successfully executes the command M

**THEN**
* A "PositionUpdated" event with position (1, 3) and heading N is emitted to the console

##### SCENARIO 2: Mission outcome event on blocked move

**Scenario ID**: ROVER-INFRA-001.4-S2

**GIVEN**
* Telemetry output is enabled
* An obstacle is located directly in front of the rover

**WHEN**
* The rover attempts the command M

**THEN**
* A "MovementBlocked" event with the current position is emitted
* The rover state remains unchanged

##### SCENARIO 3: Events disabled by default

**Scenario ID**: ROVER-INFRA-001.4-S3

**GIVEN**
* Telemetry output is not enabled

**WHEN**
* A command sequence is executed

**THEN**
* No telemetry events are emitted
* Only the final position is printed

---

---

## ROVER-STORY-002

### Architecture Traceability

| Trace | Link |
|-------|------|
| Core functionality | [Ch. 3.2.1 Command Parsing](../../architecture/03-context-and-scope.md), [Ch. 3.5 Command Validation (High)](../../architecture/03-context-and-scope.md) |
| Validation points | [Ch. 4.5.1 Validation Points](../../architecture/04-solution-strategy.md), [Ch. 4.5.2 Error Types](../../architecture/04-solution-strategy.md) |
| Component | [Ch. 5.3.2.2 Command Parser](../../architecture/05-building-block-view.md), [Ch. 5.5.2 `parse_command_string`](../../architecture/05-building-block-view.md) |
| Runtime scenario | [Ch. 6.4 Invalid Command Handling](../../architecture/06-runtime-view.md) |
| Error taxonomy | [Ch. 6.7.1 Error Hierarchy](../../architecture/06-runtime-view.md), [Ch. 8.1 Error Handling](../../architecture/08-cross-cutting-concepts.md) |
| Layered validation | [Ch. 8.2 Validation](../../architecture/08-cross-cutting-concepts.md) |
| Quality requirement | [Ch. 10 Reliability (`LMXRM` reported <10ms, no corruption)](../../architecture/10-quality-requirements.md) |
| Decisions | [ADR-002 argparse](../../architecture/09-architecture-decisions.md) |

### Original Story

**ROVER-STORY-002**

> **AS A** Mission Operator
> **I WANT** the system to reject command sequences containing invalid or empty input with a clear, specific error
> **SO THAT** a malformed mission never executes and I can correct exactly the offending character.

**Priority:** `Pareto Core 20%`

**Acceptance Scenarios**

#### SCENARIO 1: Invalid character aborts before navigation

**Scenario ID**: ROVER-STORY-002-S1

**GIVEN**
* a 5×5 grid with no obstacles
* the rover starts at `(1, 2)` facing `N`
* mission state is initialised to `(1, 2, N)`

**WHEN**
* the Mission Operator submits command sequence `"LMXRM"`

**THEN**
* validation fails at character `X`
* the console reports `"Error: Invalid command 'X' in sequence"`
* no navigation is attempted and mission state remains `(1, 2, N)`
* the process exits with a non-zero code

#### SCENARIO 2: The error names the exact offending character

**Scenario ID**: ROVER-STORY-002-S2

**GIVEN**
* the sequence `"MMZ"` contains a single invalid character `Z`

**WHEN**
* the sequence is validated

**THEN**
* the error message identifies `Z` as the invalid command
* the error message does not misreport any valid `M` as invalid

#### SCENARIO 3: An empty sequence is rejected

**Scenario ID**: ROVER-STORY-002-S3

**GIVEN**
* the command string is `""` (zero length)

**WHEN**
* the sequence is validated

**THEN**
* a `ValidationError` is reported stating the command sequence must not be empty
* no navigation is attempted

#### SCENARIO 4: A valid sequence is accepted unchanged

**Scenario ID**: ROVER-STORY-002-S4

**GIVEN**
* the command string `"LMLMLMLMM"` contains only allowed characters

**WHEN**
* the sequence is validated

**THEN**
* validation succeeds and returns the ordered operation list
* no error is raised and the normal execution path continues (ROVER-STORY-001)

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-002.1 — Present validation errors clearly to the operator

**AS A** Mission Operator
**I WANT** a concise, specific error message on stderr when my command sequence is invalid
**SO THAT** I can see exactly what to fix and never mistake a failure for a successful run.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 6.4.2 Sequence Diagram](../../architecture/06-runtime-view.md), [Ch. 6.7.3 User Experience](../../architecture/06-runtime-view.md), [Ch. 8.1](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Invalid sequence prints an error and no final position

**Scenario ID**: ROVER-FE-002.1-S1

**GIVEN**
* arguments `--commands "LMXRM" --position "1 2 N" --grid "5 5"`

**WHEN**
* the operator runs the CLI

**THEN**
* stderr contains `"Error: Invalid command 'X' in sequence"`
* stdout does not contain any `Final position:` line
* the process exits with a non-zero code

##### SCENARIO 2: The message contains the offending character and context

**Scenario ID**: ROVER-FE-002.1-S2

**GIVEN**
* any validation failure caused by an invalid character

**WHEN**
* the CLI formats the error

**THEN**
* the message includes the offending character in single quotes
* the message includes the phrase `in sequence`

##### SCENARIO 3: Successful runs are unaffected

**Scenario ID**: ROVER-FE-002.1-S3

**GIVEN**
* a valid sequence `"LMLMLMLMM"`

**WHEN**
* the CLI runs

**THEN**
* it prints `"Final position: 1 3 N"` to stdout
* no error appears on stderr
* the process exits `0`

---

#### ROVER-FE-002.2 — Distinguish usage errors from domain validation errors

**AS A** Mission Operator
**I WANT** malformed command-line usage and invalid domain input to be reported distinctly
**SO THAT** I can tell whether I mistyped the invocation or supplied a bad command sequence.

**Traceability:** [ADR-002 argparse](../../architecture/09-architecture-decisions.md), [Ch. 8.2 Layered Validation](../../architecture/08-cross-cutting-concepts.md), [Ch. 6.7.2 Error Propagation](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Missing required argument is a usage error

**Scenario ID**: ROVER-FE-002.2-S1

**GIVEN**
* an invocation that omits `--commands`

**WHEN**
* the CLI parses arguments

**THEN**
* `argparse` prints a usage error to stderr
* the process exits with the usage error code `2` (argparse convention)

##### SCENARIO 2: Invalid command character is a domain error

**Scenario ID**: ROVER-FE-002.2-S2

**GIVEN**
* a well-formed invocation whose `--commands` value contains an invalid character

**WHEN**
* the sequence fails validation

**THEN**
* the domain error is reported with exit code `1`
* the code differs from the usage error code `2`

##### SCENARIO 3: Both error classes write only to stderr

**Scenario ID**: ROVER-FE-002.2-S3

**GIVEN**
* one usage error and one domain validation error

**WHEN**
* both are reported

**THEN**
* neither writes an error to stdout
* stdout remains reserved for successful `Final position:` output

---

### BE Sub-Stories — Domain Bounded Contexts (Ch. 5.3.2.2)

#### ROVER-BE-002.1 — Validate characters against the allowed set

**AS A** Command Parser
**I WANT** to accept only uppercase `L`, `R`, `M` and reject everything else
**SO THAT** only well-formed operations reach navigation.

**Traceability:** [Ch. 5.3.2.2](../../architecture/05-building-block-view.md), [Ch. 6.4.3 Validation Rules](../../architecture/06-runtime-view.md), [Ch. 8.2 Parser-layer validation](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Only allowed characters pass

**Scenario ID**: ROVER-BE-002.1-S1

**GIVEN**
* the sequences `"L"`, `"R"`, `"M"`, `"LMR"` and `"LMLMLMLMM"`

**WHEN**
* each is validated

**THEN**
* every sequence is accepted

##### SCENARIO 2: An unsupported alphabetic character is rejected

**Scenario ID**: ROVER-BE-002.1-S2

**GIVEN**
* the sequence `"LMXRM"`

**WHEN**
* validated

**THEN**
* validation fails and identifies `X` as the first invalid character

##### SCENARIO 3: Lowercase characters are rejected

**Scenario ID**: ROVER-BE-002.1-S3

**GIVEN**
* the sequence `"lmlm"`

**WHEN**
* validated

**THEN**
* validation fails and identifies `l` as invalid (only uppercase `L`, `R`, `M` are allowed by Ch. 6.4.3)

##### SCENARIO 4: Digits and whitespace inside the sequence are rejected

**Scenario ID**: ROVER-BE-002.1-S4

**GIVEN**
* the sequences `"M2M"` and `"LM M"`

**WHEN**
* each is validated

**THEN**
* `"M2M"` fails on `2` and `"LM M"` fails on the space character
* internal whitespace is not treated as a command separator

---

#### ROVER-BE-002.2 — Raise a specific ValidationError and abort execution

**AS A** Command Parser
**I WANT** to raise a typed, descriptive error at the first invalid character
**SO THAT** the CLI can report it and navigation never starts on bad input.

**Traceability:** [Ch. 6.4.2 Raise `ValidationError`](../../architecture/06-runtime-view.md), [Ch. 6.7.1 Error Hierarchy](../../architecture/06-runtime-view.md), [Ch. 5.5.2 `parse_command_string`](../../architecture/05-building-block-view.md).

##### SCENARIO 1: Invalid input raises `InvalidCommandError`

**Scenario ID**: ROVER-BE-002.2-S1

**GIVEN**
* the sequence `"LMXRM"`

**WHEN**
* `parse_command_string("LMXRM")` is called

**THEN**
* it raises `InvalidCommandError` (a subclass of `ValidationError`, itself a subclass of `MarsRoverError`)
* the message is `"Invalid command 'X'"`
* no operation list is returned

##### SCENARIO 2: Validation stops at the first invalid character

**Scenario ID**: ROVER-BE-002.2-S2

**GIVEN**
* the sequence `"MXMR"` with multiple invalid characters

**WHEN**
* validated

**THEN**
* the error identifies the first invalid character `X`
* later invalid characters are not used to construct a misleading message

##### SCENARIO 3: Navigation is never invoked on failure

**Scenario ID**: ROVER-BE-002.2-S3

**GIVEN**
* a sequence that fails parsing

**WHEN**
* the CLI orchestrates the run

**THEN**
* `execute_operations` is never called
* `set_current_position` is never called

---

#### ROVER-BE-002.3 — Reject empty and whitespace-only sequences

**AS A** Command Parser
**I WANT** empty or blank sequences to fail validation
**SO THAT** a no-operation invocation is explicitly reported rather than silently accepted.

**Traceability:** [Ch. 6.4.3 Error Types — Empty Sequence / Whitespace](../../architecture/06-runtime-view.md), [Ch. 4.6.3 Edge Cases](../../architecture/04-solution-strategy.md).

##### SCENARIO 1: Zero-length sequence is rejected

**Scenario ID**: ROVER-BE-002.3-S1

**GIVEN**
* the command string `""`

**WHEN**
* validated

**THEN**
* a `ValidationError` is raised stating the command sequence must not be empty
* no operations are produced

##### SCENARIO 2: Whitespace-only sequence is rejected

**Scenario ID**: ROVER-BE-002.3-S2

**GIVEN**
* the command string `"   "` (after CLI boundary trimming leaves an empty value)

**WHEN**
* validated

**THEN**
* the same empty-sequence `ValidationError` is raised
* no operations are produced

---

#### ROVER-BE-002.4 — Preserve mission-state integrity on validation failure

**AS A** Mission State
**I WANT** failed validation to leave the rover state untouched
**SO THAT** a corrected re-run starts from the intended initial position.

**Traceability:** [Ch. 6.4.3 No State Mutation](../../architecture/06-runtime-view.md), [Ch. 6.8.2 State Consistency Guarantees](../../architecture/06-runtime-view.md), [Ch. 8.4](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: State remains at the initial position after a failure

**Scenario ID**: ROVER-BE-002.4-S1

**GIVEN**
* starting state `(1, 2, N)` and the invalid sequence `"LMXRM"`

**WHEN**
* the run aborts on validation

**THEN**
* `get_current_position()` returns `(1, 2, N)`
* no partial movement from the leading `LM` is applied

##### SCENARIO 2: A corrected re-run starts from the initial state

**Scenario ID**: ROVER-BE-002.4-S2

**GIVEN**
* a failed invocation using `--position "1 2 N"`
* the operator re-runs with the corrected sequence `"LMLMLMLMM"`

**WHEN**
* the corrected run executes

**THEN**
* it starts at `(1, 2, N)` and ends at `(1, 3, N)`

---

### INFRA Sub-Stories — Error Contract, State Store, Observability

#### ROVER-INFRA-002.1 — Centralise the error hierarchy and CLI exit-code contract

**AS A** System
**I WANT** one error-hierarchy module and a documented exit-code mapping
**SO THAT** every layer reports failures consistently and scripts can react reliably.

**Traceability:** [Ch. 6.7.1 Error Hierarchy](../../architecture/06-runtime-view.md), [Ch. 8.1 Error Handling](../../architecture/08-cross-cutting-concepts.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: The full error hierarchy is importable

**Scenario ID**: ROVER-INFRA-002.1-S1

**GIVEN**
* the installed package

**WHEN**
* the error module is imported

**THEN**
* it exposes `MarsRoverError`, `ValidationError`, `InvalidCommandError`, `InvalidPositionError`, `InvalidGridError`, `BoundaryError` and `ObstacleError`
* each subclass inherits from the correct parent per Ch. 6.7.1

##### SCENARIO 2: Exit codes follow the documented contract

**Scenario ID**: ROVER-INFRA-002.1-S2

**GIVEN**
* a successful run, a domain validation failure, and a usage failure

**WHEN**
* each process exits

**THEN**
* success exits `0`
* domain errors (`ValidationError`/`BoundaryError`/`ObstacleError`) exit `1`
* `argparse` usage errors exit `2`

##### SCENARIO 3: Errors are defined in a single source of truth

**Scenario ID**: ROVER-INFRA-002.1-S3

**GIVEN**
* the parser, navigation, grid and CLI modules

**WHEN**
* any module raises a domain error

**THEN**
* it imports the error type from the shared module rather than redefining it
* no duplicate, incompatible error classes exist

---

#### ROVER-INFRA-002.2 — Log validation failures for diagnostics

**AS A** Course Student
**I WANT** validation failures to be logged to stderr, with optional verbose detail
**SO THAT** I can debug bad inputs without changing the operator-facing result.

**Traceability:** [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md), [Ch. 4.5.3 Basic logging](../../architecture/04-solution-strategy.md).

> **Events/notifications are not applicable** to this story; no telemetry or event bus is in scope
> (Ch. 4.8.2 / Ch. 8.5).

##### SCENARIO 1: Default logging emits the error once

**Scenario ID**: ROVER-INFRA-002.2-S1

**GIVEN**
* default logging settings

**WHEN**
* a validation failure occurs

**THEN**
* the error message appears once on stderr
* stdout is unaffected

##### SCENARIO 2: Verbose mode adds diagnostic detail

**Scenario ID**: ROVER-INFRA-002.2-S2

**GIVEN**
* verbose/debug logging enabled via an opt-in switch

**WHEN**
* a validation failure occurs

**THEN**
* the log includes the offending character/index and the raw input
* the error is still reported to stderr

##### SCENARIO 3: Logging never changes the outcome

**Scenario ID**: ROVER-INFRA-002.2-S3

**GIVEN**
* the same invalid input run with logging off and with logging on

**WHEN**
* both finish

**THEN**
* the exit code and stderr error message are identical

---

#### ROVER-INFRA-002.3 — Ensure no state-store writes on validation failure

**AS A** System
**I WANT** failed validation to leave no persisted artifacts
**SO THAT** mission state remains purely in-memory and consistent (ADR-001).

**Traceability:** [ADR-001 In-Memory State](../../architecture/09-architecture-decisions.md), [Ch. 2.1 In-Memory State](../../architecture/02-constraints.md), [Ch. 5.6.3 State Lifecycle](../../architecture/05-building-block-view.md), [Ch. 6.9.3 Resource Management](../../architecture/06-runtime-view.md).

##### SCENARIO 1: A validation failure writes no files

**Scenario ID**: ROVER-INFRA-002.3-S1

**GIVEN**
* a clean working directory and an invalid command sequence

**WHEN**
* the run aborts on validation

**THEN**
* no snapshot, state, or default log file is written
* no temporary artifacts remain

##### SCENARIO 2: The state store is not mutated

**Scenario ID**: ROVER-INFRA-002.3-S2

**GIVEN**
* an initialised in-memory state at `(1, 2, N)`

**WHEN**
* validation fails

**THEN**
* the state object reflects the untouched initial values
* no `set_current_position` write occurred

##### SCENARIO 3: The process exits cleanly without partial state

**Scenario ID**: ROVER-INFRA-002.3-S3

**GIVEN**
* a failed validation run

**WHEN**
* the process exits

**THEN**
* it exits with the domain error code `1`
* all in-memory state is discarded and nothing is persisted

---

---

## ROVER-STORY-003

### Architecture Traceability

| Trace | Link |
|-------|------|
| Responsibilities | [Ch. 3.5 Boundary Enforcement (High) / Obstacle Detection (Medium)](../../architecture/03-context-and-scope.md) |
| Validation points | [Ch. 4.5.1 Movement Validation / Obstacle Detection](../../architecture/04-solution-strategy.md), [Ch. 4.5.2 Error Types](../../architecture/04-solution-strategy.md) |
| Component | [Ch. 5.3.2.4 Grid Management](../../architecture/05-building-block-view.md), [Ch. 5.5.2 `can_move_to`](../../architecture/05-building-block-view.md) |
| Runtime scenarios | [Ch. 6.5 Obstacle Violation](../../architecture/06-runtime-view.md), [Ch. 6.6 Boundary Violation](../../architecture/06-runtime-view.md) |
| Error taxonomy | [Ch. 6.7.1 `BoundaryError` / `ObstacleError`](../../architecture/06-runtime-view.md) |
| State consistency | [Ch. 6.5.3 Partial Execution](../../architecture/06-runtime-view.md), [Ch. 6.8.2](../../architecture/06-runtime-view.md) |
| Constraint / debt | [Ch. 11.2 Hardcoded obstacle configuration](../../architecture/11-risks-and-technical-debts.md), [ADR-001](../../architecture/09-architecture-decisions.md) |

### Original Story

**ROVER-STORY-003**

> **AS A** Mission Operator
> **I WANT** the rover to stop and report when a move would leave the grid or enter an obstacle
> **SO THAT** the rover never goes out of bounds or collides, and I always know its last safe position.

**Priority:** `Pareto Core 20%`

**Acceptance Scenarios**

#### SCENARIO 1: A boundary violation stops execution with no state change

**Scenario ID**: ROVER-STORY-003-S1

**GIVEN**
* a 3×3 grid (valid coordinates `0..2`)
* the rover starts at `(0, 2)` facing West (`W`)

**WHEN**
* the Mission Operator submits command sequence `"M"` (which would move to `(-1, 2)`)

**THEN**
* the move is rejected as a `BoundaryError`
* the console reports `"Error: Position (-1, 2) outside grid bounds (3x3)"` and `"Current position: 0 2 W"`
* mission state remains `(0, 2, W)`
* the process exits non-zero

#### SCENARIO 2: An obstacle stops the rover after prior successful moves

**Scenario ID**: ROVER-STORY-003-S2

**GIVEN**
* a 3×3 grid with obstacles at `(0, 2)` and `(1, 2)`
* the rover starts at `(0, 0)` facing `N`

**WHEN**
* the Mission Operator submits command sequence `"MMMM"`

**THEN**
* the first move to `(0, 1)` succeeds and state becomes `(0, 1, N)`
* the second move to `(0, 2)` is rejected as an `ObstacleError`
* the console reports `"Error: Movement blocked by obstacle at (0, 2)"` and `"Current position: 0 1 N"`
* execution stops and the final state is `(0, 1, N)`

#### SCENARIO 3: Boundary is validated before obstacle

**Scenario ID**: ROVER-STORY-003-S3

**GIVEN**
* a 3×3 grid where the target cell is both off-grid and configured as an obstacle
* the rover is at the grid edge facing outward

**WHEN**
* a forward move is attempted

**THEN**
* the result is classified as a `BoundaryError`, not an `ObstacleError`
* the boundary message is reported with grid dimensions
* no state mutation occurs

#### SCENARIO 4: A blocked first command leaves the starting position intact

**Scenario ID**: ROVER-STORY-003-S4

**GIVEN**
* a 3×3 grid with an obstacle directly in front of the rover
* the rover starts at `(1, 1)` facing `N` and `(1, 2)` is an obstacle

**WHEN**
* the sequence `"M"` is executed

**THEN**
* the move is rejected as an `ObstacleError`
* `get_current_position()` returns `(1, 1, N)`
* the error message includes both the obstacle location and `"Current position: 1 1 N"`

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-003.1 — Report boundary and obstacle errors with current position

**AS A** Mission Operator
**I WANT** blocked-movement errors to state the cause and the rover's last safe position
**SO THAT** I can decide whether to adjust the commands or the mission configuration.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 6.5.2](../../architecture/06-runtime-view.md), [Ch. 6.6.2](../../architecture/06-runtime-view.md), [Ch. 6.7.3 User Experience](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Obstacle error includes the obstacle cell and current position

**Scenario ID**: ROVER-FE-003.1-S1

**GIVEN**
* an execution that stops because `(0, 2)` is an obstacle, with the rover at `(0, 1, N)`

**WHEN**
* the CLI reports the failure

**THEN**
* stderr contains `"Error: Movement blocked by obstacle at (0, 2)"`
* stderr contains `"Current position: 0 1 N"`
* stdout contains no `Final position:` line
* the process exits with code `1`

##### SCENARIO 2: Boundary error includes the rejected coordinate and grid dimensions

**Scenario ID**: ROVER-FE-003.1-S2

**GIVEN**
* an execution that stops because `(-1, 2)` is outside a 3×3 grid, with the rover at `(0, 2, W)`

**WHEN**
* the CLI reports the failure

**THEN**
* stderr contains `"Error: Position (-1, 2) outside grid bounds (3x3)"`
* stderr contains `"Current position: 0 2 W"`
* the process exits with code `1`

##### SCENARIO 3: Error messages are consistent in structure

**Scenario ID**: ROVER-FE-003.1-S3

**GIVEN**
* one obstacle failure and one boundary failure

**WHEN**
* both are reported

**THEN**
* both use the `"Error: <reason>"` first line followed by `"Current position: <x> <y> <heading>"`

---

#### ROVER-FE-003.2 — Never mask a blocked run as a success

**AS A** Mission Operator
**I WANT** blocked runs to exit non-zero and omit the success line
**SO THAT** scripts and I can reliably distinguish a complete mission from a halted one.

**Traceability:** [Ch. 6.5.2](../../architecture/06-runtime-view.md), [Ch. 6.7.2 Error Propagation](../../architecture/06-runtime-view.md), [Ch. 8.1](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Blocked run prints no success line

**Scenario ID**: ROVER-FE-003.2-S1

**GIVEN**
* any run halted by an obstacle or boundary

**WHEN**
* the process ends

**THEN**
* stdout has no `Final position:` line
* the halt reason and current position appear on stderr
* the exit code is `1`

##### SCENARIO 2: Fully successful run is unchanged

**Scenario ID**: ROVER-FE-003.2-S2

**GIVEN**
* the canonical valid run `"LMLMLMLMM"` on a 5×5 grid

**WHEN**
* no move is blocked

**THEN**
* stdout prints `"Final position: 1 3 N"`
* stderr is empty and the exit code is `0`

---

### BE Sub-Stories — Terrain/Grid and Navigation (Ch. 5.3.2.3–5.3.2.4)

#### ROVER-BE-003.1 — Enforce the grid boundary invariant

**AS A** Grid Management
**I WANT** to accept only coordinates with `0 ≤ x < width` and `0 ≤ y < height`
**SO THAT** the rover can never leave the grid.

**Traceability:** [Ch. 5.3.2.4](../../architecture/05-building-block-view.md), [Ch. 6.6.3 Grid Coordinate System / Exclusive Upper Bound](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Negative coordinates are rejected

**Scenario ID**: ROVER-BE-003.1-S1

**GIVEN**
* a 3×3 grid

**WHEN**
* `can_move_to((-1, 2), W)` is checked

**THEN**
* it returns `(False, "Boundary violation")`
* the user-facing reason is `"Position (-1, 2) outside grid bounds (3x3)"`

##### SCENARIO 2: The upper bound is exclusive

**Scenario ID**: ROVER-BE-003.1-S2

**GIVEN**
* a 3×3 grid (valid `0..2`)

**WHEN**
* `can_move_to((3, 2), E)` and `can_move_to((2, 3), N)` are checked

**THEN**
* both return `(False, "Boundary violation")`
* `can_move_to((2, 2), E)` is within bounds

##### SCENARIO 3: In-bounds coordinates pass the boundary check

**Scenario ID**: ROVER-BE-003.1-S3

**GIVEN**
* a 5×5 grid with no obstacles

**WHEN**
* `can_move_to((0, 0), N)` and `can_move_to((4, 4), N)` are checked

**THEN**
* both return `(True, None)` (boundary invariant satisfied)

---

#### ROVER-BE-003.2 — Enforce the obstacle invariant

**AS A** Grid Management
**I WANT** to reject moves into any configured obstacle cell
**SO THAT** the rover never occupies a blocked coordinate.

**Traceability:** [Ch. 5.3.2.4](../../architecture/05-building-block-view.md), [Ch. 6.5.4 Obstacle Detection Rules](../../architecture/06-runtime-view.md), [Ch. 6.5.2](../../architecture/06-runtime-view.md).

##### SCENARIO 1: A configured obstacle blocks the move

**Scenario ID**: ROVER-BE-003.2-S1

**GIVEN**
* a 3×3 grid with obstacles at `(0, 2)` and `(1, 2)`

**WHEN**
* `can_move_to((0, 2), N)` is checked

**THEN**
* it returns `(False, "Obstacle blocked")`
* the user-facing reason is `"Movement blocked by obstacle at (0, 2)"`

##### SCENARIO 2: A free in-bounds cell is allowed

**Scenario ID**: ROVER-BE-003.2-S2

**GIVEN**
* the same grid with obstacles at `(0, 2)` and `(1, 2)`

**WHEN**
* `can_move_to((0, 1), N)` is checked

**THEN**
* it returns `(True, None)`

##### SCENARIO 3: Every configured obstacle is honoured

**Scenario ID**: ROVER-BE-003.2-S3

**GIVEN**
* an obstacle set `{(0,2), (1,2)}` on a 3×3 grid

**WHEN**
* each obstacle coordinate is checked as a target

**THEN**
* every configured coordinate returns `(False, "Obstacle blocked")`
* non-obstacle in-bounds coordinates return `(True, None)`

---

#### ROVER-BE-003.3 — Apply validation order: boundary before obstacle

**AS A** Grid Management
**I WANT** boundary checks to run before obstacle checks
**SO THAT** off-grid moves are classified consistently as `BoundaryError`.

**Traceability:** [Ch. 6.6.3 Validation Order](../../architecture/06-runtime-view.md), [Ch. 6.6.4 Boundary vs Obstacle Errors](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Off-grid and obstacle overlap yields a boundary result

**Scenario ID**: ROVER-BE-003.3-S1

**GIVEN**
* a target cell outside the grid that also appears in the obstacle configuration

**WHEN**
* `can_move_to` evaluates it

**THEN**
* the boundary check fails first
* the returned reason is a boundary violation, not an obstacle block

##### SCENARIO 2: In-bounds obstacle yields an obstacle result

**Scenario ID**: ROVER-BE-003.3-S2

**GIVEN**
* an in-bounds target that is a configured obstacle

**WHEN**
* `can_move_to` evaluates it

**THEN**
* the boundary check passes
* the obstacle check fails and the reason is `"Obstacle blocked"`

---

#### ROVER-BE-003.4 — Halt atomically and preserve last valid state

**AS A** Rover Navigation
**I WANT** a blocked operation to stop the sequence without mutating state
**SO THAT** the final state equals the last successful operation.

**Traceability:** [Ch. 6.5.3 State Consistency in Partial Execution](../../architecture/06-runtime-view.md), [Ch. 6.8.2](../../architecture/06-runtime-view.md), [Ch. 5.3.2.3](../../architecture/05-building-block-view.md).

##### SCENARIO 1: Successful operations before the block persist

**Scenario ID**: ROVER-BE-003.4-S1

**GIVEN**
* start `(0, 0, N)`, obstacles `(0,2)`/`(1,2)`, sequence `"MMMM"`

**WHEN**
* execution proceeds

**THEN**
* `(0,0) → (0,1)` commits and updates mission state
* the move to `(0,2)` raises `ObstacleError`
* the final state is `(0, 1, N)` and no rollback occurs

##### SCENARIO 2: A blocked first move leaves state at the start

**Scenario ID**: ROVER-BE-003.4-S2

**GIVEN**
* start `(1, 1, N)` with `(1, 2)` as an obstacle and sequence `"M"`

**WHEN**
* the move is evaluated

**THEN**
* `set_current_position` is never called
* `get_current_position()` returns `(1, 1, N)`

##### SCENARIO 3: Execution stops at the first block

**Scenario ID**: ROVER-BE-003.4-S3

**GIVEN**
* a sequence whose third operation is blocked

**WHEN**
* the block occurs

**THEN**
* no later operation is executed
* the navigation layer raises a typed `BoundaryError` or `ObstacleError`

##### SCENARIO 4: The typed error carries the blocking detail

**Scenario ID**: ROVER-BE-003.4-S4

**GIVEN**
* a blocked move

**WHEN**
* the error is raised

**THEN**
* the exception is `BoundaryError` for out-of-bounds or `ObstacleError` for an obstacle
* messages match `"Position (x, y) outside grid bounds (WxH)"` or `"Movement blocked by obstacle at (x, y)"`

---

### INFRA Sub-Stories — Configuration, State Store, Observability

#### ROVER-INFRA-003.1 — Own grid and obstacle configuration in Grid Management

**AS A** System
**I WANT** grid dimensions and obstacle coordinates owned by a single in-memory configuration
**SO THAT** spatial rules have one source of truth and introduce no new dependencies.

**Traceability:** [Ch. 5.3.2.4](../../architecture/05-building-block-view.md), [Ch. 5.4.2 No Grid-State Dependency](../../architecture/05-building-block-view.md), [Ch. 11.2 Hardcoded obstacle configuration](../../architecture/11-risks-and-technical-debts.md), [Ch. 2.1 Minimal Dependencies](../../architecture/02-constraints.md).

##### SCENARIO 1: Default configuration is in-memory only

**Scenario ID**: ROVER-INFRA-003.1-S1

**GIVEN**
* a mission run with `--grid "3 3"` and internal obstacles `(0,2)`, `(1,2)`

**WHEN**
* the grid component initialises

**THEN**
* dimensions and obstacle set are held in memory
* no external configuration file is required

##### SCENARIO 2: No new runtime dependencies

**Scenario ID**: ROVER-INFRA-003.1-S2

**GIVEN**
* the installed package

**WHEN**
* boundary and obstacle checks run

**THEN**
* they use only the Python standard library
* packaging adds no runtime dependency (ADR-002)

##### SCENARIO 3: Configuration is not duplicated across modules

**Scenario ID**: ROVER-INFRA-003.1-S3

**GIVEN**
* navigation and CLI modules that need grid facts

**WHEN**
* a boundary or obstacle question is asked

**THEN**
* the answer comes from the Grid Management configuration
* navigation and the CLI do not keep their own boundary/obstacle copies

---

#### ROVER-INFRA-003.2 — Log blocked-movement diagnostics by classification

**AS A** Course Student
**I WANT** blocked movements logged with their classification (boundary vs obstacle)
**SO THAT** I can diagnose halts without confusing the two error classes.

**Traceability:** [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md), [Ch. 6.6.4 Error Distinction](../../architecture/06-runtime-view.md), [Ch. 4.5.3](../../architecture/04-solution-strategy.md).

> **Events/notifications are not applicable** to this story; no telemetry stream is in scope
> (Ch. 4.8.2 / Ch. 8.5).

##### SCENARIO 1: Default logging reports the halt once

**Scenario ID**: ROVER-INFRA-003.2-S1

**GIVEN**
* default logging settings and a blocked run

**WHEN**
* the halt occurs

**THEN**
* one error line is written to stderr
* stdout remains free of `Final position:` output

##### SCENARIO 2: Verbose mode adds classification detail

**Scenario ID**: ROVER-INFRA-003.2-S2

**GIVEN**
* verbose/debug logging enabled

**WHEN**
* a boundary or obstacle halt occurs

**THEN**
* the log states `boundary` or `obstacle` and the offending coordinate
* the exit code is unchanged

##### SCENARIO 3: Classification matches the raised error type

**Scenario ID**: ROVER-INFRA-003.2-S3

**GIVEN**
* `BoundaryError` and `ObstacleError` runs

**WHEN**
* each is logged

**THEN**
* the logged classification is consistent with the exception type

---

#### ROVER-INFRA-003.3 — Persist nothing on a blocked run and keep no partial artifacts

**AS A** System
**I WANT** blocked runs to leave no persisted state or partial files
**SO THAT** the in-memory-state constraint holds even on failure paths (ADR-001).

**Traceability:** [ADR-001 In-Memory State](../../architecture/09-architecture-decisions.md), [Ch. 2.1](../../architecture/02-constraints.md), [Ch. 5.6.3 State Lifecycle](../../architecture/05-building-block-view.md), [Ch. 6.9.3 Resource Management](../../architecture/06-runtime-view.md).

##### SCENARIO 1: A blocked run writes no files

**Scenario ID**: ROVER-INFRA-003.3-S1

**GIVEN**
* a clean working directory and a run that halts on an obstacle

**WHEN**
* the process exits

**THEN**
* no snapshot, state, or default log file is created
* no temporary artifacts remain

##### SCENARIO 2: Last valid state is retained only in memory

**Scenario ID**: ROVER-INFRA-003.3-S2

**GIVEN**
* a blocked run ending at `(0, 1, N)`

**WHEN**
* the CLI reports the error

**THEN**
* the last valid position is read from in-memory mission state
* nothing about that state is written to disk

##### SCENARIO 3: A later invocation starts fresh

**Scenario ID**: ROVER-INFRA-003.3-S3

**GIVEN**
* a blocked invocation followed by a new invocation with `--position "0 0 N"`

**WHEN**
* the new run starts

**THEN**
* the grid and obstacles are reconfigured in memory
* the new state begins at `(0, 0, N)` with no carry-over

---

---

## ROVER-STORY-004

### Architecture Traceability

| Trace | Link |
|-------|------|
| Scope | [Ch. 3.2.1 Grid Management / Status Reporting](../../architecture/03-context-and-scope.md), [Ch. 3.2.2 CLI Interface](../../architecture/03-context-and-scope.md) |
| Validation points | [Ch. 4.5.1 Initial Position / Movement Validation](../../architecture/04-solution-strategy.md), [Ch. 4.5.2 Error Types](../../architecture/04-solution-strategy.md) |
| Components | [Ch. 5.3.2.1 Command Interface](../../architecture/05-building-block-view.md), [Ch. 5.3.2.4 Grid Management](../../architecture/05-building-block-view.md) |
| Interfaces | [Ch. 5.5.1 External CLI Interface (`--commands`, `--position`, `--grid`)](../../architecture/05-building-block-view.md) |
| Error taxonomy | [Ch. 6.7.1 `InvalidPositionError`, `InvalidGridError`](../../architecture/06-runtime-view.md) |
| Layered validation | [Ch. 8.2 CLI layer](../../architecture/08-cross-cutting-concepts.md) |
| Deployment | [Ch. 7.4.2 Execution](../../architecture/07-deployment-view.md), [ADR-002 argparse](../../architecture/09-architecture-decisions.md) |

### Original Story

**ROVER-STORY-004**

> **AS A** Mission Operator
> **I WANT** to specify the grid dimensions, starting position and heading, and have them validated before the rover runs
> **SO THAT** a malformed mission configuration is rejected with a clear message and the rover only ever starts from a legal cell.

**Priority:** `Supporting 80%`

**Acceptance Scenarios**

#### SCENARIO 1: A valid configuration is accepted and drives the mission

**Scenario ID**: ROVER-STORY-004-S1

**GIVEN**
* arguments `--grid "5 5" --position "1 2 N" --commands "M"`

**WHEN**
* the CLI validates the configuration

**THEN**
* the grid is configured as width `5`, height `5`
* the rover starts at `(1, 2)` facing `N`
* the mission executes and reports `"Final position: 1 3 N"` with exit code `0`

#### SCENARIO 2: A starting position outside the grid is rejected

**Scenario ID**: ROVER-STORY-004-S2

**GIVEN**
* a 5×5 grid whose valid coordinates are `0..4`
* the starting position `"5 2 N"` (x = 5 is outside the exclusive upper bound)

**WHEN**
* the configuration is validated

**THEN**
* an `InvalidPositionError` is reported: `"Invalid starting position (5, 2) outside grid bounds (5x5)"`
* navigation never starts
* the process exits with code `1`

#### SCENARIO 3: Invalid grid dimensions are rejected

**Scenario ID**: ROVER-STORY-004-S3

**GIVEN**
* the grid argument `"0 5"` (zero width)

**WHEN**
* the configuration is validated

**THEN**
* an `InvalidGridError` is reported stating width and height must each be at least 1
* no mission executes
* the process exits with code `1`

#### SCENARIO 4: An unsupported heading is rejected

**Scenario ID**: ROVER-STORY-004-S4

**GIVEN**
* the position argument `"1 2 X"`

**WHEN**
* the configuration is validated

**THEN**
* a `ValidationError` is reported: `"Invalid heading 'X': expected one of N, S, E, W"`
* no mission executes
* the process exits non-zero

#### SCENARIO 5: A starting cell occupied by an obstacle is rejected

**Scenario ID**: ROVER-STORY-004-S5

**GIVEN**
* a 3×3 grid with obstacles at `(0, 2)` and `(1, 2)`
* the starting position `"0 2 N"` (an obstacle cell)
* *(derived from the Grid obstacle invariant, Ch. 5.3.2.4)*

**WHEN**
* the configuration is validated

**THEN**
* an `InvalidPositionError` is reported: `"Invalid starting position (0, 2): cell occupied by obstacle"`
* no mission executes and the process exits with code `1`

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-004.1 — Parse grid and position arguments with format validation

**AS A** Mission Operator
**I WANT** `--grid` and `--position` to be parsed into structured values with format errors caught early
**SO THAT** I get immediate feedback on malformed input before any domain logic runs.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 5.5.1](../../architecture/05-building-block-view.md), [Ch. 8.2 CLI layer validation](../../architecture/08-cross-cutting-concepts.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: Well-formed arguments are parsed

**Scenario ID**: ROVER-FE-004.1-S1

**GIVEN**
* `--grid "5 5"` and `--position "1 2 N"`

**WHEN**
* the CLI parses the arguments

**THEN**
* `--grid` yields `(width=5, height=5)`
* `--position` yields `(x=1, y=2, heading=N)`

##### SCENARIO 2: A position without a heading is a usage error

**Scenario ID**: ROVER-FE-004.1-S2

**GIVEN**
* `--position "1 2"` (two tokens only)

**WHEN**
* the CLI parses the arguments

**THEN**
* an `argparse` usage error is printed to stderr
* the process exits with code `2`

##### SCENARIO 3: A non-numeric grid is a usage error

**Scenario ID**: ROVER-FE-004.1-S3

**GIVEN**
* `--grid "five five"`

**WHEN**
* the CLI parses the arguments

**THEN**
* an `argparse` usage error is printed to stderr
* the process exits with code `2`

##### SCENARIO 4: A malformed position ordering is a usage error

**Scenario ID**: ROVER-FE-004.1-S4

**GIVEN**
* `--position "1 N 2"` (wrong token order)

**WHEN**
* the CLI parses the arguments

**THEN**
* a usage error identifies the expected `x y heading` format
* the process exits with code `2`

---

#### ROVER-FE-004.2 — Report configuration errors distinctly

**AS A** Mission Operator
**I WANT** format problems and semantic configuration problems to be reported differently
**SO THAT** I know whether I mistyped the arguments or chose an impossible configuration.

**Traceability:** [Ch. 8.2 Layered Validation](../../architecture/08-cross-cutting-concepts.md), [Ch. 6.7.2 Error Propagation](../../architecture/06-runtime-view.md), [Ch. 6.7.3](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Semantic configuration errors exit with the domain code

**Scenario ID**: ROVER-FE-004.2-S1

**GIVEN**
* well-formed arguments describing an out-of-bounds start or an invalid grid size

**WHEN**
* the configuration is rejected

**THEN**
* the error is printed to stderr
* no `Final position:` line appears on stdout
* the process exits with code `1`

##### SCENARIO 2: Format/usage errors exit with the usage code

**Scenario ID**: ROVER-FE-004.2-S2

**GIVEN**
* malformed `--grid` or `--position` values

**WHEN**
* the CLI rejects them

**THEN**
* the process exits with code `2`
* the domain error code `1` is reserved for semantically invalid but well-formed configuration

##### SCENARIO 3: Successful configuration remains silent

**Scenario ID**: ROVER-FE-004.2-S3

**GIVEN**
* a valid configuration

**WHEN**
* the mission runs successfully

**THEN**
* stderr is empty
* stdout contains only the final `Final position:` line

---

### BE Sub-Stories — Mission Configuration (Ch. 5.3.2.4)

#### ROVER-BE-004.1 — Parse a position string into coordinates and heading

**AS A** Mission Configuration
**I WANT** `"x y H"` to become a validated position and heading
**SO THAT** navigation receives a well-typed initial state.

**Traceability:** [Ch. 5.6.2 Key Data Structures](../../architecture/05-building-block-view.md), [Ch. 4.4.2 Heading orientation](../../architecture/04-solution-strategy.md), [Ch. 6.7.1](../../architecture/06-runtime-view.md).

##### SCENARIO 1: A valid position parses correctly

**Scenario ID**: ROVER-BE-004.1-S1

**GIVEN**
* the position string `"1 2 N"`

**WHEN**
* it is parsed

**THEN**
* it yields coordinates `(1, 2)` and heading `N`

##### SCENARIO 2: All four headings are accepted

**Scenario ID**: ROVER-BE-004.1-S2

**GIVEN**
* the position strings `"1 2 N"`, `"1 2 S"`, `"1 2 E"`, `"1 2 W"`

**WHEN**
* each is parsed

**THEN**
* each yields the corresponding `Heading` value (`NORTH`, `SOUTH`, `EAST`, `WEST`)

##### SCENARIO 3: A lowercase heading is rejected

**Scenario ID**: ROVER-BE-004.1-S3

**GIVEN**
* the position string `"1 2 n"`

**WHEN**
* it is parsed

**THEN**
* a `ValidationError` is raised identifying `n` as an unsupported heading

##### SCENARIO 4: Non-integer coordinates are rejected

**Scenario ID**: ROVER-BE-004.1-S4

**GIVEN**
* the position strings `"a 2 N"` and `"1 b N"`

**WHEN**
* each is parsed

**THEN**
* a `ValidationError` is raised stating coordinates must be integers

---

#### ROVER-BE-004.2 — Validate grid dimensions

**AS A** Mission Configuration
**I WANT** width and height to be positive integers
**SO THAT** the grid is always well-defined.

**Traceability:** [Ch. 5.3.2.4 Grid Management](../../architecture/05-building-block-view.md), [Ch. 6.6.3 Grid Coordinate System](../../architecture/06-runtime-view.md), [Ch. 6.7.1 `InvalidGridError`](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Positive dimensions are accepted

**Scenario ID**: ROVER-BE-004.2-S1

**GIVEN**
* the grid `"5 5"`

**WHEN**
* it is validated

**THEN**
* it yields `(width=5, height=5)` with no error

##### SCENARIO 2: Zero dimensions are rejected

**Scenario ID**: ROVER-BE-004.2-S2

**GIVEN**
* the grids `"0 5"` and `"5 0"`

**WHEN**
* each is validated

**THEN**
* an `InvalidGridError` is raised stating width and height must be at least 1

##### SCENARIO 3: Negative and non-integer dimensions are rejected

**Scenario ID**: ROVER-BE-004.2-S3

**GIVEN**
* the grids `"-3 5"` and `"5 x"`

**WHEN**
* each is validated

**THEN**
* an `InvalidGridError` is raised
* no grid is constructed

---

#### ROVER-BE-004.3 — Validate the starting position within grid bounds

**AS A** Mission Configuration
**I WANT** to reject start positions outside `0 ≤ x < width`, `0 ≤ y < height`
**SO THAT** the rover never begins in an illegal cell.

**Traceability:** [Ch. 4.5.1 Initial Position Validation](../../architecture/04-solution-strategy.md), [Ch. 6.6.3 Exclusive Upper Bound](../../architecture/06-runtime-view.md), [Ch. 6.7.1 `InvalidPositionError`](../../architecture/06-runtime-view.md).

##### SCENARIO 1: An in-bounds start is accepted

**Scenario ID**: ROVER-BE-004.3-S1

**GIVEN**
* a 5×5 grid and starting position `(1, 2)`

**WHEN**
* the start position is validated

**THEN**
* validation succeeds

##### SCENARIO 2: The exclusive upper bound is enforced

**Scenario ID**: ROVER-BE-004.3-S2

**GIVEN**
* a 5×5 grid (valid `0..4`)

**WHEN**
* start positions `(5, 2)` and `(2, 5)` are validated

**THEN**
* both raise `InvalidPositionError` reporting the coordinate and `grid bounds (5x5)`

##### SCENARIO 3: Negative starts are rejected before execution

**Scenario ID**: ROVER-BE-004.3-S3

**GIVEN**
* a 5×5 grid and starting position `(-1, 0)`

**WHEN**
* the configuration is validated

**THEN**
* `InvalidPositionError` is raised
* navigation and mission-state updates are never invoked

---

#### ROVER-BE-004.4 — Reject a starting position occupied by an obstacle

**AS A** Mission Configuration
**I WANT** the start cell checked against the obstacle set
**SO THAT** the rover can never be placed on a blocked cell.
*(Derived from the Grid obstacle invariant, Ch. 5.3.2.4 and Ch. 6.5.4.)*

**Traceability:** [Ch. 5.3.2.4](../../architecture/05-building-block-view.md), [Ch. 6.5.4 Obstacle Detection Rules](../../architecture/06-runtime-view.md), [Ch. 6.7.1 `InvalidPositionError`](../../architecture/06-runtime-view.md).

##### SCENARIO 1: A start on an obstacle is rejected

**Scenario ID**: ROVER-BE-004.4-S1

**GIVEN**
* a 3×3 grid with obstacles `{(0,2), (1,2)}` and start `(0, 2)`

**WHEN**
* the configuration is validated

**THEN**
* `InvalidPositionError` is raised stating the cell is occupied by an obstacle
* no mission executes

##### SCENARIO 2: A start on a free in-bounds cell is accepted

**Scenario ID**: ROVER-BE-004.4-S2

**GIVEN**
* a 3×3 grid with obstacles `{(0,2), (1,2)}` and start `(0, 1)`

**WHEN**
* the configuration is validated

**THEN**
* validation succeeds and the mission may proceed

---

#### ROVER-BE-004.5 — Enforce configure-before-run ordering

**AS A** Mission Configuration
**I WANT** all configuration validation to complete before parsing or executing commands
**SO THAT** an invalid configuration cannot cause partial execution or state changes.

**Traceability:** [Ch. 4.5.1 Validation Points](../../architecture/04-solution-strategy.md), [Ch. 6.8.2 Validation Before Mutation](../../architecture/06-runtime-view.md), [Ch. 8.2 Layered Validation](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Invalid configuration aborts before parsing

**Scenario ID**: ROVER-BE-004.5-S1

**GIVEN**
* an invalid grid or start position
* a syntactically valid command sequence

**WHEN**
* the run is orchestrated

**THEN**
* `parse_command_string` is never called for execution
* `execute_operations` is never called

##### SCENARIO 2: Valid configuration unlocks execution

**Scenario ID**: ROVER-BE-004.5-S2

**GIVEN**
* a valid grid, valid start and valid command sequence

**WHEN**
* configuration validation passes

**THEN**
* command parsing and execution proceed normally

##### SCENARIO 3: No state mutation on invalid configuration

**Scenario ID**: ROVER-BE-004.5-S3

**GIVEN**
* an invalid configuration

**WHEN**
* validation fails

**THEN**
* no mission-state position is committed
* `set_current_position` is never called

---

### INFRA Sub-Stories — Argument Converters, State Store, Observability

#### ROVER-INFRA-004.1 — Provide reusable argument converters and a config-error exit contract

**AS A** System
**I WANT** `--grid` and `--position` conversion to live in reusable, stdlib-only helpers with a documented exit-code mapping
**SO THAT** configuration rules have one source of truth and consistent failure semantics.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [ADR-002 argparse / standard library](../../architecture/09-architecture-decisions.md), [Ch. 6.7.1](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Converters are stdlib-only and reusable

**Scenario ID**: ROVER-INFRA-004.1-S1

**GIVEN**
* the installed package

**WHEN**
* the CLI registers `--grid` and `--position` converters

**THEN**
* conversion relies only on the Python standard library
* the converters can be unit-tested independently of the CLI entry point

##### SCENARIO 2: Configuration errors map to the documented exit codes

**Scenario ID**: ROVER-INFRA-004.1-S2

**GIVEN**
* an `InvalidGridError`/`InvalidPositionError` and a format/usage error

**WHEN**
* each exits

**THEN**
* semantic configuration errors exit `1`
* format/usage errors exit `2`

##### SCENARIO 3: Error types come from the shared hierarchy

**Scenario ID**: ROVER-INFRA-004.1-S3

**GIVEN**
* the configuration validation code

**WHEN**
* it raises `InvalidGridError` or `InvalidPositionError`

**THEN**
* both are imported from the shared error module (ROVER-INFRA-002.1)
* no duplicate configuration error classes exist

---

#### ROVER-INFRA-004.2 — Log configuration validation failures

**AS A** Course Student
**I WANT** configuration failures logged to stderr with optional raw-value detail
**SO THAT** I can debug bad `--grid`/`--position` inputs without changing the operator output.

**Traceability:** [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md), [Ch. 4.5.3 Basic logging](../../architecture/04-solution-strategy.md).

> **Events/notifications are not applicable** to this story; no telemetry stream is in scope
> (Ch. 4.8.2 / Ch. 8.5).

##### SCENARIO 1: Default logging reports the failure once

**Scenario ID**: ROVER-INFRA-004.2-S1

**GIVEN**
* default logging and an invalid configuration

**WHEN**
* validation fails

**THEN**
* one error line is written to stderr
* stdout stays clean

##### SCENARIO 2: Verbose mode adds the raw values

**Scenario ID**: ROVER-INFRA-004.2-S2

**GIVEN**
* verbose/debug logging enabled

**WHEN**
* a configuration failure occurs

**THEN**
* the log includes the raw `--grid`/`--position` values and the validation reason

##### SCENARIO 3: Logging does not change the outcome

**Scenario ID**: ROVER-INFRA-004.2-S3

**GIVEN**
* the same invalid configuration run with logging off and on

**WHEN**
* both finish

**THEN**
* the exit code and error message are identical

---

#### ROVER-INFRA-004.3 — Leave no state or artifacts on invalid configuration

**AS A** System
**I WANT** rejected configurations to avoid initialising or persisting mission state
**SO THAT** the in-memory-state discipline holds on the configuration path (ADR-001).

**Traceability:** [ADR-001 In-Memory State](../../architecture/09-architecture-decisions.md), [Ch. 2.1](../../architecture/02-constraints.md), [Ch. 5.6.3 State Lifecycle](../../architecture/05-building-block-view.md).

##### SCENARIO 1: No files are written

**Scenario ID**: ROVER-INFRA-004.3-S1

**GIVEN**
* a clean working directory and an invalid configuration

**WHEN**
* the process exits

**THEN**
* no snapshot, state, or default log file is created

##### SCENARIO 2: Mission state is not committed

**Scenario ID**: ROVER-INFRA-004.3-S2

**GIVEN**
* an invalid start position

**WHEN**
* validation fails

**THEN**
* no initial position is committed to mission state
* the state store holds no mission for that run

##### SCENARIO 3: A corrected re-run starts from validated values

**Scenario ID**: ROVER-INFRA-004.3-S3

**GIVEN**
* a rejected configuration followed by a corrected invocation

**WHEN**
* the corrected run starts

**THEN**
* the grid and start are re-validated in memory
* the mission begins from the newly validated position

---

---

## ROVER-STORY-005

### Architecture Traceability

| Trace | Link |
|-------|------|
| CLI interface | [Ch. 3.2.2 External Interfaces](../../architecture/03-context-and-scope.md), [Ch. 2.3 Interface Constraints](../../architecture/02-constraints.md) |
| Component | [Ch. 5.3.2.1 Command Interface (`argparse`)](../../architecture/05-building-block-view.md) |
| External interface | [Ch. 5.5.1 External Interface](../../architecture/05-building-block-view.md) |
| Deployment | [Ch. 7.4.1 Setup — verify with `mars_rover --help`](../../architecture/07-deployment-view.md), [Ch. 7.4.2 Execution](../../architecture/07-deployment-view.md) |
| Layered validation | [Ch. 8.2 CLI layer](../../architecture/08-cross-cutting-concepts.md) |
| Decision | [ADR-002 CLI with argparse](../../architecture/09-architecture-decisions.md) |

### Original Story

**ROVER-STORY-005**

> **AS A** Mission Operator
> **I WANT** discoverable help, clear usage errors and stable exit codes
> **SO THAT** I can learn the interface without documentation and script rover runs reliably.

**Priority:** `Supporting 80%`

**Acceptance Scenarios**

#### SCENARIO 1: Help lists all mission arguments and exits successfully

**Scenario ID**: ROVER-STORY-005-S1

**GIVEN**
* the application is installed

**WHEN**
* the operator runs `mars_rover --help`

**THEN**
* usage text lists `--commands`, `--position` and `--grid` with descriptions
* the process exits with code `0`
* no mission executes

#### SCENARIO 2: A missing required argument produces a usage error

**Scenario ID**: ROVER-STORY-005-S2

**GIVEN**
* an invocation that omits `--commands`

**WHEN**
* the CLI parses arguments

**THEN**
* a usage error naming the missing argument is written to stderr
* no mission executes
* the process exits with code `2`

#### SCENARIO 3: An unknown option produces a usage error

**Scenario ID**: ROVER-STORY-005-S3

**GIVEN**
* an invocation containing `--foo bar` in addition to the three valid arguments

**WHEN**
* the CLI parses arguments

**THEN**
* a usage error reports the unrecognized argument on stderr
* no mission executes
* the process exits with code `2`

#### SCENARIO 4: Help shows a runnable example

**Scenario ID**: ROVER-STORY-005-S4

**GIVEN**
* the help output

**WHEN**
* the operator reads it

**THEN**
* it contains an example invocation matching Ch. 5.5.1:
  `mars_rover --commands "LMLMLMLMM" --position "1 2 N" --grid "5 5"`
* it describes the expected value formats for each argument

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-005.1 — Render help/usage text

**AS A** Mission Operator
**I WANT** `--help`/`-h` to show usage, argument descriptions and an example
**SO THAT** I can use the CLI without external documentation.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 7.4.1](../../architecture/07-deployment-view.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: `--help` documents the three arguments

**Scenario ID**: ROVER-FE-005.1-S1

**GIVEN**
* the CLI is invoked with `--help`

**WHEN**
* help is rendered

**THEN**
* it lists `--commands <sequence>`, `--position "<x> <y> <heading>"` and `--grid "<width> <height>"`
* each has a short description
* it exits with code `0`

##### SCENARIO 2: The `-h` short form is equivalent

**Scenario ID**: ROVER-FE-005.1-S2

**GIVEN**
* the CLI is invoked with `-h`

**WHEN**
* help is rendered

**THEN**
* the output is equivalent to `--help`
* it exits with code `0`

##### SCENARIO 3: Help includes a complete example

**Scenario ID**: ROVER-FE-005.1-S3

**GIVEN**
* the help output

**WHEN**
* the operator inspects it

**THEN**
* it contains the canonical example `--commands "LMLMLMLMM" --position "1 2 N" --grid "5 5"`

---

#### ROVER-FE-005.2 — Render usage errors with a corrective hint

**AS A** Mission Operator
**I WANT** usage errors on stderr that explain what is wrong and how to see help
**SO THAT** I can fix the invocation quickly.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 8.2 CLI layer validation](../../architecture/08-cross-cutting-concepts.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: Missing required argument names the argument

**Scenario ID**: ROVER-FE-005.2-S1

**GIVEN**
* an invocation omitting `--grid`

**WHEN**
* parsing fails

**THEN**
* stderr shows a usage line plus an error identifying `--grid` as required
* stdout is empty
* the process exits with code `2`

##### SCENARIO 2: Unknown option is reported

**Scenario ID**: ROVER-FE-005.2-S2

**GIVEN**
* an invocation with an unrecognized option

**WHEN**
* parsing fails

**THEN**
* stderr reports the unrecognized argument
* stdout is empty
* the process exits with code `2`

##### SCENARIO 3: Usage errors never start a mission

**Scenario ID**: ROVER-FE-005.2-S3

**GIVEN**
* any usage error

**WHEN**
* the CLI terminates

**THEN**
* no `Final position:` line is printed
* no domain error is raised

---

### BE Sub-Stories — CLI Application Service (argument schema & dispatch)

#### ROVER-BE-005.1 — Define one canonical argument schema

**AS A** System
**I WANT** a single definition of the CLI arguments (names, required-ness, formats)
**SO THAT** help rendering and argument parsing never drift apart.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 5.5.1](../../architecture/05-building-block-view.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: The schema declares all three arguments as required

**Scenario ID**: ROVER-BE-005.1-S1

**GIVEN**
* the argument schema

**WHEN**
* it is inspected

**THEN**
* it defines `--commands`, `--position` and `--grid` as required
* it records the expected value format for each

##### SCENARIO 2: Help and parsing derive from the same schema

**Scenario ID**: ROVER-BE-005.1-S2

**GIVEN**
* the wire CLI and its help output

**WHEN**
* an argument is renamed or added in the schema

**THEN**
* both parsing and help reflect the change
* no separately maintained argument list exists

##### SCENARIO 3: One source of truth is testable

**Scenario ID**: ROVER-BE-005.1-S3

**GIVEN**
* the schema definition

**WHEN**
* covered by a unit test

**THEN**
* the test asserts the required arguments and their formats without invoking a subprocess

---

#### ROVER-BE-005.2 — Enforce required arguments and dispatch semantics

**AS A** System
**I WANT** a valid invocation to dispatch to the domain and an invalid one to stop at the CLI
**SO THAT** the domain only ever receives well-formed mission requests.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 5.4.1 Interaction Flow](../../architecture/05-building-block-view.md), [Ch. 8.2](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: All three arguments present dispatches to the parser

**Scenario ID**: ROVER-BE-005.2-S1

**GIVEN**
* `--commands`, `--position` and `--grid` are all supplied and well-formed

**WHEN**
* the CLI dispatches

**THEN**
* it calls the Command Parser and then Rover Navigation (Ch. 5.4.1)
* it prints the final position

##### SCENARIO 2: Any missing argument stops before the domain

**Scenario ID**: ROVER-BE-005.2-S2

**GIVEN**
* an invocation missing one of the three arguments

**WHEN**
* parsing completes with an error

**THEN**
* `parse_command_string` is never called
* no domain state changes

##### SCENARIO 3: Unknown arguments are rejected before dispatch

**Scenario ID**: ROVER-BE-005.2-S3

**GIVEN**
* an invocation with an unrecognized option

**WHEN**
* parsing fails

**THEN**
* dispatch never happens
* the process exits with the usage code

##### SCENARIO 4: Help short-circuits dispatch

**Scenario ID**: ROVER-BE-005.2-S4

**GIVEN**
* `--help` or `-h`

**WHEN**
* the CLI handles the flag

**THEN**
* it renders help and exits `0`
* neither the parser nor navigation is invoked

---

### INFRA Sub-Stories — Entry Point, Exit Contract, Side-effect Freedom

#### ROVER-INFRA-005.1 — Expose help from the installed entry point

**AS A** Course Student
**I WANT** `mars_rover --help` to work right after installation
**SO THAT** I can verify the environment per the deployment guide.

**Traceability:** [Ch. 7.4.1 Setup / verify installation](../../architecture/07-deployment-view.md), [Ch. 7.4.2 Execution](../../architecture/07-deployment-view.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: Console script shows help after install

**Scenario ID**: ROVER-INFRA-005.1-S1

**GIVEN**
* a successful `pip install -e ".[dev]"` in a Python 3.12 environment

**WHEN**
* `mars_rover --help` is run

**THEN**
* usage is printed and the process exits `0`

##### SCENARIO 2: Module invocation shows the same help

**Scenario ID**: ROVER-INFRA-005.1-S2

**GIVEN**
* the project workspace

**WHEN**
* `python mars_rover/cli/main.py --help` is run

**THEN**
* help output is equivalent to the console script
* the process exits `0`

##### SCENARIO 3: Help needs no extra dependencies

**Scenario ID**: ROVER-INFRA-005.1-S3

**GIVEN**
* only runtime dependencies installed

**WHEN**
* help is rendered

**THEN**
* it uses the standard library only (ADR-002)
* no import error occurs

---

#### ROVER-INFRA-005.2 — Publish a stable exit-code contract

**AS A** System
**I WANT** a documented, stable mapping from outcome to exit code
**SO THAT** operators and scripts can branch on results deterministically.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 6.7.2 Error Propagation](../../architecture/06-runtime-view.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: The contract is exactly 0/1/2

**Scenario ID**: ROVER-INFRA-005.2-S1

**GIVEN**
* a success, a domain error and a usage error

**WHEN**
* each process exits

**THEN**
* success → `0`, domain errors → `1`, usage errors → `2`

##### SCENARIO 2: The contract is documented

**Scenario ID**: ROVER-INFRA-005.2-S2

**GIVEN**
* the help output and project documentation

**WHEN**
* a reader looks for exit codes

**THEN**
* the `0`/`1`/`2` meanings are stated

##### SCENARIO 3: The contract is identical across entry points

**Scenario ID**: ROVER-INFRA-005.2-S3

**GIVEN**
* the console script and the module invocation

**WHEN**
* each is run with the same success, domain-error and usage-error inputs

**THEN**
* both produce the same exit codes

---

#### ROVER-INFRA-005.3 — Keep help and usage paths free of side effects

**AS A** System
**I WANT** help and usage handling to avoid initialising mission state or writing files
**SO THAT** read-only interactions never create artifacts (ADR-001).

**Traceability:** [ADR-001 In-Memory State](../../architecture/09-architecture-decisions.md), [Ch. 2.1](../../architecture/02-constraints.md), [Ch. 8.5 Logging](../../architecture/08-cross-cutting-concepts.md).

> **Events/notifications are not applicable** to this story; no telemetry stream is in scope
> (Ch. 4.8.2 / Ch. 8.5).

##### SCENARIO 1: `--help` writes nothing

**Scenario ID**: ROVER-INFRA-005.3-S1

**GIVEN**
* a clean working directory

**WHEN**
* `--help` is run

**THEN**
* no files are created
* no mission state is initialised

##### SCENARIO 2: Usage errors write no mission state

**Scenario ID**: ROVER-INFRA-005.3-S2

**GIVEN**
* an invocation with a missing or unknown argument

**WHEN**
* the CLI rejects the invocation and exits with code `2`

**THEN**
* no state or snapshot is written
* only the usage error appears on stderr

##### SCENARIO 3: Optional debug logging stays on stderr

**Scenario ID**: ROVER-INFRA-005.3-S3

**GIVEN**
* verbose/debug logging enabled

**WHEN**
* help or a usage error is handled

**THEN**
* any diagnostic output goes to stderr
* stdout remains reserved for mission results

---

---

## ROVER-STORY-006

### Architecture Traceability

| Trace | Link |
|-------|------|
| Error strategy | [Ch. 4.5 Error Handling Strategy](../../architecture/04-solution-strategy.md) |
| Component | [Ch. 5.3.2.1 Command Interface (error presentation)](../../architecture/05-building-block-view.md) |
| Error hierarchy | [Ch. 6.7.1 Error Hierarchy](../../architecture/06-runtime-view.md) |
| Propagation | [Ch. 6.7.2 Error Propagation](../../architecture/06-runtime-view.md) |
| User experience | [Ch. 6.7.3 User Experience](../../architecture/06-runtime-view.md) |
| Error reporting | [Ch. 4.5.3 Error Reporting](../../architecture/04-solution-strategy.md), [Ch. 8.1 Error Handling](../../architecture/08-cross-cutting-concepts.md) |
| Diagnostics in scenarios | [Ch. 6.4.2](../../architecture/06-runtime-view.md), [Ch. 6.5.2](../../architecture/06-runtime-view.md), [Ch. 6.6.2](../../architecture/06-runtime-view.md) |
| Glossary | [Ch. 12 Error Types](../../architecture/12-glossary.md) |

### Original Story

**ROVER-STORY-006**

> **AS A** Mission Operator
> **I WANT** every failure to be reported in one consistent, actionable format that includes the cause and — when a mission is underway — the rover's current position
> **SO THAT** I can diagnose and correct a mission quickly without guessing.

**Priority:** `Supporting 80%`

**Acceptance Scenarios**

#### SCENARIO 1: A movement failure reports cause and current position

**Scenario ID**: ROVER-STORY-006-S1

**GIVEN**
* a mission halted by an obstacle at `(0, 2)` with the rover at `(0, 1, N)`

**WHEN**
* the failure is reported

**THEN**
* stderr shows `"Error: Movement blocked by obstacle at (0, 2)"`
* stderr shows `"Current position: 0 1 N"`
* no `Final position:` line appears on stdout

#### SCENARIO 2: An input-validation failure omits current position

**Scenario ID**: ROVER-STORY-006-S2

**GIVEN**
* the invalid command sequence `"LMXRM"` rejected before navigation

**WHEN**
* the failure is reported

**THEN**
* stderr shows `"Error: Invalid command 'X' in sequence"`
* no `"Current position:"` line is printed (validation failed before movement)
* no state mutation occurred

#### SCENARIO 3: A configuration failure omits current position

**Scenario ID**: ROVER-STORY-006-S3

**GIVEN**
* a rejected starting position `"5 2 N"` on a 5×5 grid

**WHEN**
* the failure is reported

**THEN**
* stderr shows `"Error: Invalid starting position (5, 2) outside grid bounds (5x5)"`
* no `"Current position:"` line is printed (no mission started)

#### SCENARIO 4: All errors share one structural convention

**Scenario ID**: ROVER-STORY-006-S4

**GIVEN**
* one error of each class: validation, config, boundary, obstacle

**WHEN**
* each is reported

**THEN**
* every message begins with `"Error: <reason>"`
* movement failures append `"Current position: <x> <y> <heading>"`
* all errors go to stderr, and stdout is reserved for `Final position:`

#### SCENARIO 5: Messages contain actionable detail

**Scenario ID**: ROVER-STORY-006-S5

**GIVEN**
* any failure

**WHEN**
* the operator reads the message

**THEN**
* it identifies the offending value or location (character, coordinate, or grid dimensions)
* it states the relevant expectation or boundary

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-006.1 — Render every error with one uniform layout

**AS A** Mission Operator
**I WANT** one recognisable error layout across all failure classes
**SO THAT** I can scan output consistently and know how serious a failure is.

**Traceability:** [Ch. 6.7.3 Consistent Formatting](../../architecture/06-runtime-view.md), [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 8.1](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Movement errors include the position line

**Scenario ID**: ROVER-FE-006.1-S1

**GIVEN**
* an obstacle or boundary failure during a mission

**WHEN**
* the CLI renders the error

**THEN**
* line 1 is `"Error: <reason>"`
* line 2 is `"Current position: <x> <y> <heading>"`

##### SCENARIO 2: Validation and config errors omit the position line

**Scenario ID**: ROVER-FE-006.1-S2

**GIVEN**
* a `ValidationError` from command parsing or mission configuration

**WHEN**
* the CLI renders the error

**THEN**
* only the `"Error: <reason>"` line is printed
* no `"Current position:"` line is added

##### SCENARIO 3: Errors never pollute stdout

**Scenario ID**: ROVER-FE-006.1-S3

**GIVEN**
* any failure

**WHEN**
* the CLI reports it

**THEN**
* all error text goes to stderr
* stdout contains no `Final position:` line

---

#### ROVER-FE-006.2 — Make each message actionable

**AS A** Mission Operator
**I WANT** each error to name the offending value and the expectation
**SO THAT** I know exactly what to change.

**Traceability:** [Ch. 6.7.3 Actionable Messages / Context Preservation](../../architecture/06-runtime-view.md), [Ch. 4.5.3](../../architecture/04-solution-strategy.md).

##### SCENARIO 1: Invalid command names the character

**Scenario ID**: ROVER-FE-006.2-S1

**GIVEN**
* the invalid sequence `"LMXRM"`

**WHEN**
* reported

**THEN**
* the message is `"Error: Invalid command 'X' in sequence"`

##### SCENARIO 2: Invalid heading names the value and expected set

**Scenario ID**: ROVER-FE-006.2-S2

**GIVEN**
* the starting position `"1 2 X"`

**WHEN**
* reported

**THEN**
* the message names `X` and the allowed set `N, S, E, W`

##### SCENARIO 3: Out-of-bounds start names the coordinate and grid

**Scenario ID**: ROVER-FE-006.2-S3

**GIVEN**
* a start `(5, 2)` on a 5×5 grid

**WHEN**
* reported

**THEN**
* the message includes `(5, 2)` and `grid bounds (5x5)`

##### SCENARIO 4: Blocked moves name the obstacle cell or rejected coordinate

**Scenario ID**: ROVER-FE-006.2-S4

**GIVEN**
* an obstacle block at `(0, 2)` and a boundary attempt to `(-1, 2)`

**WHEN**
* each is reported

**THEN**
* the obstacle message includes `(0, 2)`
* the boundary message includes `(-1, 2)` and `(3x3)`

---

#### ROVER-FE-006.3 — Align error streams and exit codes

**AS A** Mission Operator
**I WANT** errors on stderr with predictable exit codes and successes on stdout
**SO THAT** I can compose rover runs in scripts confidently.

**Traceability:** [Ch. 6.7.2](../../architecture/06-runtime-view.md), [Ch. 8.1](../../architecture/08-cross-cutting-concepts.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: Domain errors exit `1`

**Scenario ID**: ROVER-FE-006.3-S1

**GIVEN**
* any `ValidationError`, `BoundaryError` or `ObstacleError`

**WHEN**
* the process exits

**THEN**
* the exit code is `1`
* the error text is on stderr

##### SCENARIO 2: Usage errors exit `2`

**Scenario ID**: ROVER-FE-006.3-S2

**GIVEN**
* an `argparse` usage failure

**WHEN**
* the process exits

**THEN**
* the exit code is `2`
* the error text is on stderr

##### SCENARIO 3: Success uses stdout and exit `0` only

**Scenario ID**: ROVER-FE-006.3-S3

**GIVEN**
* a fully successful mission

**WHEN**
* the process exits

**THEN**
* stdout carries `"Final position: 1 3 N"`
* stderr is empty and the exit code is `0`

---

### BE Sub-Stories — Error Taxonomy and Propagation

#### ROVER-BE-006.1 — Model a rich, typed error taxonomy

**AS A** System
**I WANT** each error to be a typed object carrying actionable context
**SO THAT** the console can render consistent messages without re-deriving details.

**Traceability:** [Ch. 6.7.1 Error Hierarchy](../../architecture/06-runtime-view.md), [Ch. 4.5.2 Error Types](../../architecture/04-solution-strategy.md), [Ch. 12](../../architecture/12-glossary.md).

##### SCENARIO 1: All errors share the base type

**Scenario ID**: ROVER-BE-006.1-S1

**GIVEN**
* `ValidationError`, `BoundaryError` and `ObstacleError`

**WHEN**
* their inheritance is inspected

**THEN**
* each ultimately subclasses `MarsRoverError`
* `InvalidCommandError`, `InvalidPositionError` and `InvalidGridError` subclass `ValidationError`

##### SCENARIO 2: Errors carry structured context

**Scenario ID**: ROVER-BE-006.1-S2

**GIVEN**
* an `InvalidCommandError`, an `InvalidPositionError`, a `BoundaryError` and an `ObstacleError`

**WHEN**
* each is constructed

**THEN**
* it exposes the offending value/location and expected constraint
* no detail needed for the message is lost

##### SCENARIO 3: Messages are deterministic

**Scenario ID**: ROVER-BE-006.1-S3

**GIVEN**
* the same failure input twice

**WHEN**
* both errors are constructed

**THEN**
* their rendered messages are identical

---

#### ROVER-BE-006.2 — Propagate errors without swallowing them

**AS A** System
**I WANT** errors detected in any component to bubble to the console with their type intact
**SO THAT** classification and state context are preserved end to end.

**Traceability:** [Ch. 6.7.2 Error Propagation](../../architecture/06-runtime-view.md), [Ch. 5.4.1 Interaction Flow](../../architecture/05-building-block-view.md), [Ch. 8.1](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Parser errors bubble from the parser

**Scenario ID**: ROVER-BE-006.2-S1

**GIVEN**
* an invalid command sequence

**WHEN**
* `parse_command_string` raises

**THEN**
* the exception reaches the CLI handler unchanged
* no domain layer catches and discards it

##### SCENARIO 2: Navigation errors bubble from navigation

**Scenario ID**: ROVER-BE-006.2-S2

**GIVEN**
* a blocked move detected via Grid Management

**WHEN**
* Rover Navigation raises

**THEN**
* the `BoundaryError`/`ObstacleError` reaches the CLI as the same type
* the last valid mission state remains accessible

##### SCENARIO 3: Errors are not re-wrapped into a generic type

**Scenario ID**: ROVER-BE-006.2-S3

**GIVEN**
* any domain error

**WHEN**
* it crosses component boundaries

**THEN**
* its specific type is preserved
* no catch-all `SystemError` replaces it

##### SCENARIO 4: The CLI is the single handling point

**Scenario ID**: ROVER-BE-006.2-S4

**GIVEN**
* errors from parser, navigation or configuration

**WHEN**
* they are handled

**THEN**
* all are handled in the Command Interface (Ch. 6.7.2)

---

#### ROVER-BE-006.3 — Decide when current-position context applies

**AS A** System
**I WANT** current position attached only to movement failures
**SO THAT** output matches the architecture's documented scenarios.

**Traceability:** [Ch. 6.4.2](../../architecture/06-runtime-view.md), [Ch. 6.5.2](../../architecture/06-runtime-view.md), [Ch. 6.6.2](../../architecture/06-runtime-view.md), [Ch. 6.8.3 State Visibility](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Movement failures attach the last valid position

**Scenario ID**: ROVER-BE-006.3-S1

**GIVEN**
* a boundary or obstacle failure after at least one successful operation

**WHEN**
* the error context is assembled

**THEN**
* the current position is read from mission state
* it is the last successfully committed position, not the rejected target

##### SCENARIO 2: Input-validation failures omit position

**Scenario ID**: ROVER-BE-006.3-S2

**GIVEN**
* an `InvalidCommandError`

**WHEN**
* the error context is assembled

**THEN**
* no current-position context is attached

##### SCENARIO 3: Config failures before mission start omit position

**Scenario ID**: ROVER-BE-006.3-S3

**GIVEN**
* an `InvalidGridError` or `InvalidPositionError`

**WHEN**
* the error context is assembled

**THEN**
* no current-position context is attached
* no mission state was committed

##### SCENARIO 4: Rejected target is never reported as current position

**Scenario ID**: ROVER-BE-006.3-S4

**GIVEN**
* a move from `(0, 1)` to a blocked `(0, 2)`

**WHEN**
* the position context is assembled

**THEN**
* it reports `(0, 1)`, the last valid cell

---

### INFRA Sub-Stories — Shared Renderer, Observability, State Safety

#### ROVER-INFRA-006.1 — Centralise error rendering in one module

**AS A** System
**I WANT** a single renderer that owns the `Error:` prefix, the position line and stream routing
**SO THAT** every error path produces identical formatting.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 6.7.3](../../architecture/06-runtime-view.md), [Ch. 8.1](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: All error paths use the shared renderer

**Scenario ID**: ROVER-INFRA-006.1-S1

**GIVEN**
* validation, config, boundary and obstacle failures

**WHEN**
* each is presented

**THEN**
* all pass through one rendering helper
* no module formats its own error text independently

##### SCENARIO 2: Prefix and position line are owned in one place

**Scenario ID**: ROVER-INFRA-006.1-S2

**GIVEN**
* a movement failure and a validation failure

**WHEN**
* rendered

**THEN**
* the `"Error: "` prefix is applied consistently
* the `"Current position: "` line is added only per ROVER-BE-006.3

##### SCENARIO 3: Stream routing is centralised

**Scenario ID**: ROVER-INFRA-006.1-S3

**GIVEN**
* any error and any success

**WHEN**
* output is written

**THEN**
* errors are routed to stderr and results to stdout by the shared helper

---

#### ROVER-INFRA-006.2 — Log diagnostics with classification

**AS A** Course Student
**I WANT** each error logged with its class and context
**SO THAT** I can trace failures without altering operator output.

**Traceability:** [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md), [Ch. 4.5.3 Basic logging](../../architecture/04-solution-strategy.md).

> **Events/notifications are not applicable** to this story; no telemetry stream is in scope
> (Ch. 4.8.2 / Ch. 8.5).

##### SCENARIO 1: Default logging emits the error once

**Scenario ID**: ROVER-INFRA-006.2-S1

**GIVEN**
* default logging and any failure

**WHEN**
* the process exits

**THEN**
* exactly one error message appears on stderr
* stdout is untouched

##### SCENARIO 2: Verbose mode adds classification and context

**Scenario ID**: ROVER-INFRA-006.2-S2

**GIVEN**
* verbose/debug logging enabled

**WHEN**
* an error occurs

**THEN**
* the log includes the error class (validation/config/boundary/obstacle) and its context fields

##### SCENARIO 3: Logging never changes the operator-facing outcome

**Scenario ID**: ROVER-INFRA-006.2-S3

**GIVEN**
* the same failure run with logging off and on

**WHEN**
* both finish

**THEN**
* the rendered message and exit code are identical

---

#### ROVER-INFRA-006.3 — Keep error paths side-effect free

**AS A** System
**I WANT** error reporting to write no files or persisted state
**SO THAT** diagnostics rely solely on in-memory state (ADR-001).

**Traceability:** [ADR-001 In-Memory State](../../architecture/09-architecture-decisions.md), [Ch. 2.1](../../architecture/02-constraints.md), [Ch. 6.9.3 Resource Management](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Error paths create no files

**Scenario ID**: ROVER-INFRA-006.3-S1

**GIVEN**
* a clean working directory and any failing run

**WHEN**
* the process exits

**THEN**
* no snapshot, state, or default log file is created

##### SCENARIO 2: Diagnostics read only in-memory state

**Scenario ID**: ROVER-INFRA-006.3-S2

**GIVEN**
* a movement failure

**WHEN**
* the current position is included

**THEN**
* it comes from in-memory mission state
* no disk read/write is involved

##### SCENARIO 3: Clean exit with no persisted residue

**Scenario ID**: ROVER-INFRA-006.3-S3

**GIVEN**
* any error exit

**WHEN**
* the process terminates

**THEN**
* it exits with the correct code
* no partial artifacts remain and all state is discarded

---

---

## ROVER-STORY-007

### Architecture Traceability

| Trace | Link |
|-------|------|
| Component | [Ch. 5.3.2.5 Mission State](../../architecture/05-building-block-view.md), [Ch. 5.3.2.3 Rover Navigation](../../architecture/05-building-block-view.md) |
| State lifecycle | [Ch. 5.6.3 State Lifecycle](../../architecture/05-building-block-view.md) |
| Partial execution | [Ch. 6.5.3 State Consistency in Partial Execution](../../architecture/06-runtime-view.md) |
| Guarantees | [Ch. 6.8.2 State Consistency Guarantees](../../architecture/06-runtime-view.md), [Ch. 6.8.3 State Visibility and Access](../../architecture/06-runtime-view.md) |
| Cross-cutting | [Ch. 8.4 State Management](../../architecture/08-cross-cutting-concepts.md) |
| Decision | [ADR-001 In-Memory State](../../architecture/09-architecture-decisions.md) |

### Original Story

**ROVER-STORY-007**

> **AS A** Mission Operator
> **I WANT** each operation to either fully commit or leave the rover state untouched, with the last valid state preserved on failure
> **SO THAT** partial missions never corrupt the position and the reported state can always be trusted.

**Priority:** `Supporting 80%`

**Acceptance Scenarios**

#### SCENARIO 1: A valid operation commits atomically

**Scenario ID**: ROVER-STORY-007-S1

**GIVEN**
* a rover at `(1, 2, N)` on a 5×5 grid
* the operation `M` is valid

**WHEN**
* the operation is processed

**THEN**
* the candidate `(1, 3, N)` is validated first
* position and heading are committed together
* `get_current_position()` returns `(1, 3, N)`

#### SCENARIO 2: A failed operation leaves state unchanged

**Scenario ID**: ROVER-STORY-007-S2

**GIVEN**
* a rover at `(0, 1, N)` with an obstacle at `(0, 2)`
* the operation `M` would move to the blocked cell

**WHEN**
* the operation is processed

**THEN**
* no state mutation occurs
* `get_current_position()` still returns `(0, 1, N)`
* the rejected target `(0, 2)` is never stored as the position

#### SCENARIO 3: Prior successes persist (no rollback)

**Scenario ID**: ROVER-STORY-007-S3

**GIVEN**
* a rover at `(0, 0, N)` with obstacles `(0, 2)` and `(1, 2)`
* the sequence `"MMMM"`

**WHEN**
* the first move succeeds and the second is blocked

**THEN**
* the first successful move is not rolled back
* the final state is `(0, 1, N)`
* no later operation executes

#### SCENARIO 4: All validation completes before any mutation

**Scenario ID**: ROVER-STORY-007-S4

**GIVEN**
* any move operation

**WHEN**
* it is processed

**THEN**
* `can_move_to` is evaluated before `set_current_position`
* if validation fails, no write is attempted

#### SCENARIO 5: The final state is deterministic

**Scenario ID**: ROVER-STORY-007-S5

**GIVEN**
* identical grid, start position and command sequence

**WHEN**
* the mission runs twice

**THEN**
* both runs end in the same position and heading

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-007.1 — Report the committed state after success or failure

**AS A** Mission Operator
**I WANT** the console to show the committed final state on success and the last valid state on failure
**SO THAT** what I see always matches what the rover actually committed.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 6.8.3](../../architecture/06-runtime-view.md), [Ch. 6.5.2](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Success reports the final committed position

**Scenario ID**: ROVER-FE-007.1-S1

**GIVEN**
* a fully successful sequence ending at `(1, 3, N)`

**WHEN**
* the CLI reports the result

**THEN**
* stdout shows `"Final position: 1 3 N"`

##### SCENARIO 2: Failure reports the last valid position

**Scenario ID**: ROVER-FE-007.1-S2

**GIVEN**
* a run halted at `(0, 1, N)` by an obstacle

**WHEN**
* the CLI reports the failure

**THEN**
* stderr shows `"Current position: 0 1 N"`
* the committed state is unchanged

##### SCENARIO 3: The rejected target is never displayed

**Scenario ID**: ROVER-FE-007.1-S3

**GIVEN**
* a blocked move toward `(0, 2)` from `(0, 1)`

**WHEN**
* the error is displayed

**THEN**
* the reported position is `(0, 1)`, never `(0, 2)`

---

#### ROVER-FE-007.2 — Read state once after execution completes

**AS A** Mission Operator
**I WANT** the console to query the committed state once after execution
**SO THAT** output reflects a consistent snapshot rather than an intermediate value.

**Traceability:** [Ch. 6.8.3 State Visibility](../../architecture/06-runtime-view.md), [Ch. 5.5.2 `get_current_position`](../../architecture/05-building-block-view.md).

##### SCENARIO 1: State is queried after navigation finishes

**Scenario ID**: ROVER-FE-007.2-S1

**GIVEN**
* a mission run (successful or halted)

**WHEN**
* navigation returns or raises

**THEN**
* the CLI calls `get_current_position()` once
* the displayed state equals that snapshot

##### SCENARIO 2: No intermediate state is printed by default

**Scenario ID**: ROVER-FE-007.2-S2

**GIVEN**
* a multi-step sequence

**WHEN**
* the CLI produces default output

**THEN**
* it prints only the final result or the error
* no per-operation state lines appear

##### SCENARIO 3: Output matches the state at read time

**Scenario ID**: ROVER-FE-007.2-S3

**GIVEN**
* a halted run

**WHEN**
* the state is read for the error message

**THEN**
* the position shown is exactly the last committed snapshot

---

### BE Sub-Stories — Mission State and Navigation (Ch. 5.3.2.3–5.3.2.5)

#### ROVER-BE-007.1 — Commit only after successful validation

**AS A** Rover Navigation
**I WANT** to validate a candidate move fully before writing state
**SO THAT** no operation can leave the rover half-updated.

**Traceability:** [Ch. 6.8.2 Validation Before Mutation](../../architecture/06-runtime-view.md), [Ch. 5.3.2.3](../../architecture/05-building-block-view.md), [Ch. 5.5.2 `set_current_position`](../../architecture/05-building-block-view.md).

##### SCENARIO 1: A valid move commits position and heading together

**Scenario ID**: ROVER-BE-007.1-S1

**GIVEN**
* a candidate move that passes `can_move_to`

**WHEN**
* the operation completes

**THEN**
* `set_current_position(new_position, new_heading)` commits both at once
* state reads return a consistent `(x, y, heading)`

##### SCENARIO 2: Validation precedes the write

**Scenario ID**: ROVER-BE-007.1-S2

**GIVEN**
* a candidate move

**WHEN**
* it is processed

**THEN**
* `can_move_to` returns `(True, None)` before `set_current_position` is called
* a failed check prevents the write

##### SCENARIO 3: No partial coordinate update

**Scenario ID**: ROVER-BE-007.1-S3

**GIVEN**
* a move that changes only one axis (e.g. `N` increments `y`)

**WHEN**
* committed

**THEN**
* the unchanged axis retains its value
* state is never observed with a stale `x` and new `y` (or vice versa)

---

#### ROVER-BE-007.2 — Leave state untouched on failure

**AS A** Mission State
**I WANT** a rejected operation to produce zero side effects
**SO THAT** failures are atomic without needing rollback.

**Traceability:** [Ch. 6.5.3 Individual Operation Atomicity](../../architecture/06-runtime-view.md), [Ch. 6.8.2](../../architecture/06-runtime-view.md), [Ch. 8.4](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: A blocked move produces no mutation

**Scenario ID**: ROVER-BE-007.2-S1

**GIVEN**
* state `(0, 1, N)` and a blocked move to `(0, 2)`

**WHEN**
* the block is detected

**THEN**
* `get_current_position()` returns `(0, 1, N)` before and after

##### SCENARIO 2: The rejected target is not stored

**Scenario ID**: ROVER-BE-007.2-S2

**GIVEN**
* a rejected candidate position

**WHEN**
* the error is raised

**THEN**
* the candidate is never written to mission state

##### SCENARIO 3: The error is raised after no mutation

**Scenario ID**: ROVER-BE-007.2-S3

**GIVEN**
* a blocked operation

**WHEN**
* navigation raises `BoundaryError`/`ObstacleError`

**THEN**
* state is already unchanged at the moment of raising

---

#### ROVER-BE-007.3 — Preserve prior successes without rollback

**AS A** Mission State
**I WANT** successful operations to remain committed when a later one fails
**SO THAT** the final state equals the last successful operation.

**Traceability:** [Ch. 6.5.3 No Transaction Rollback / Progressive State Updates](../../architecture/06-runtime-view.md), [Ch. 6.8.2](../../architecture/06-runtime-view.md).

##### SCENARIO 1: The obstacle example ends at the last success

**Scenario ID**: ROVER-BE-007.3-S1

**GIVEN**
* start `(0, 0, N)`, obstacles `(0,2)`/`(1,2)`, sequence `"MMMM"`

**WHEN**
* the second move is blocked

**THEN**
* the final state is `(0, 1, N)`

##### SCENARIO 2: Earlier commits survive the failure

**Scenario ID**: ROVER-BE-007.3-S2

**GIVEN**
* three successful operations followed by a blocked fourth

**WHEN**
* the fourth fails

**THEN**
* the state reflects the result of the third operation
* nothing is rolled back

##### SCENARIO 3: No later operation runs after the block

**Scenario ID**: ROVER-BE-007.3-S3

**GIVEN**
* a sequence with operations after the blocked one

**WHEN**
* the block occurs

**THEN**
* subsequent operations are not executed
* state stays at the last success

---

#### ROVER-BE-007.4 — Enforce determinism and single-writer visibility

**AS A** Mission State
**I WANT** only navigation to write state and reads to return the last committed snapshot
**SO THAT** state cannot be corrupted by other components or nondeterminism.

**Traceability:** [Ch. 6.8.3 State Visibility and Access](../../architecture/06-runtime-view.md), [Ch. 5.4.2 Relationship Rules](../../architecture/05-building-block-view.md), [Ch. 6.8.2 Deterministic Final State](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Same inputs yield the same final state

**Scenario ID**: ROVER-BE-007.4-S1

**GIVEN**
* identical configuration and commands

**WHEN**
* the mission runs repeatedly

**THEN**
* the final state is identical every time

##### SCENARIO 2: Only navigation writes state

**Scenario ID**: ROVER-BE-007.4-S2

**GIVEN**
* parser, grid and CLI modules

**WHEN**
* they interact with mission state

**THEN**
* they read it at most; only Rover Navigation calls `set_current_position`

##### SCENARIO 3: Reads return the last committed snapshot

**Scenario ID**: ROVER-BE-007.4-S3

**GIVEN**
* a sequence of committed operations

**WHEN**
* `get_current_position()` is called

**THEN**
* it returns the most recently committed position and heading
* never a candidate or intermediate value

##### SCENARIO 4: Failure states are deterministic too

**Scenario ID**: ROVER-BE-007.4-S4

**GIVEN**
* identical configuration and a sequence that blocks

**WHEN**
* the mission runs repeatedly

**THEN**
* the last valid state and the error are identical every time

---

### INFRA Sub-Stories — In-Memory Store, Lifecycle, Observability

#### ROVER-INFRA-007.1 — Make the in-memory update atomic

**AS A** System
**I WANT** state updates to replace position and heading as a single unit
**SO THAT** no observer can see a half-applied update.

**Traceability:** [Ch. 5.6.2 RoverState](../../architecture/05-building-block-view.md), [Ch. 6.8.2 Atomic Operation Updates](../../architecture/06-runtime-view.md), [ADR-001](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: Update is one atomic replacement

**Scenario ID**: ROVER-INFRA-007.1-S1

**GIVEN**
* a current `(x, y, heading)` state

**WHEN**
* a valid operation commits

**THEN**
* position and heading are replaced together
* no intermediate object state is observable

##### SCENARIO 2: No torn reads in sequential execution

**Scenario ID**: ROVER-INFRA-007.1-S2

**GIVEN**
* single-threaded sequential processing (Ch. 6.9.3)

**WHEN**
* state is read between operations

**THEN**
* it always returns a complete `(x, y, heading)` triple

##### SCENARIO 3: No concurrency is introduced

**Scenario ID**: ROVER-INFRA-007.1-S3

**GIVEN**
* the runtime

**WHEN**
* commands execute

**THEN**
* processing remains single-threaded with no locks required

---

#### ROVER-INFRA-007.2 — Keep state per-invocation and discard on exit

**AS A** System
**I WANT** each invocation to own a fresh in-memory state that is never persisted
**SO THAT** failures and prior runs cannot leak into a new mission (ADR-001).

**Traceability:** [ADR-001](../../architecture/09-architecture-decisions.md), [Ch. 5.6.3 State Lifecycle](../../architecture/05-building-block-view.md), [Ch. 6.9.3](../../architecture/06-runtime-view.md).

##### SCENARIO 1: A new invocation starts fresh

**Scenario ID**: ROVER-INFRA-007.2-S1

**GIVEN**
* a completed prior run

**WHEN**
* a new invocation starts with `--position "0 0 E"`

**THEN**
* mission state begins at `(0, 0, E)`

##### SCENARIO 2: A failed run persists nothing

**Scenario ID**: ROVER-INFRA-007.2-S2

**GIVEN**
* a run that halts on an obstacle

**WHEN**
* the process exits

**THEN**
* no state or snapshot file is written
* the last valid state exists only in memory

##### SCENARIO 3: Exit discards all state

**Scenario ID**: ROVER-INFRA-007.2-S3

**GIVEN**
* any run (successful or failed)

**WHEN**
* the process terminates

**THEN**
* all mission state is released
* nothing is persisted between invocations

---

#### ROVER-INFRA-007.3 — Expose optional state-transition tracing

**AS A** Course Student
**I WANT** an opt-in trace of each state commit
**SO THAT** I can verify atomicity during development without noisy default output.

**Traceability:** [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md), [Ch. 4.5.3 Basic logging](../../architecture/04-solution-strategy.md).

> **Events/notifications are not applicable** to this story; state changes are not published to
> any event bus (Ch. 4.8.2 / Ch. 8.5).

##### SCENARIO 1: Default output shows no state trace

**Scenario ID**: ROVER-INFRA-007.3-S1

**GIVEN**
* default logging

**WHEN**
* a mission runs

**THEN**
* only the final result or error is printed

##### SCENARIO 2: Verbose mode traces each commit

**Scenario ID**: ROVER-INFRA-007.3-S2

**GIVEN**
* verbose/debug logging enabled

**WHEN**
* each valid operation commits

**THEN**
* a trace line shows the operation and the resulting `(x, y, heading)` on stderr

##### SCENARIO 3: Tracing does not affect state or outcome

**Scenario ID**: ROVER-INFRA-007.3-S3

**GIVEN**
* the same mission with tracing off and on

**WHEN**
* both finish

**THEN**
* the final state, message and exit code are identical

---

---

## ROVER-STORY-008

### Architecture Traceability

| Trace | Link |
|-------|------|
| Component | [Ch. 5.3.2.1 Command Interface](../../architecture/05-building-block-view.md) |
| Whitespace handling | [Ch. 6.4.3 Error Types — Whitespace Issues (trimmed by CLI)](../../architecture/06-runtime-view.md) |
| Validation layers | [Ch. 8.2 CLI layer / Parser layer](../../architecture/08-cross-cutting-concepts.md) |
| Validation points | [Ch. 4.5.1 Command Input](../../architecture/04-solution-strategy.md) |
| Edge cases | [Ch. 4.6.3 Test Data — empty command sequences](../../architecture/04-solution-strategy.md) |
| CLI interface | [Ch. 5.5.1 External Interface](../../architecture/05-building-block-view.md), [ADR-002](../../architecture/09-architecture-decisions.md) |

### Original Story

**ROVER-STORY-008**

> **AS A** Mission Operator
> **I WANT** incidental leading/trailing whitespace in my command, position and grid inputs to be normalized before validation
> **SO THAT** harmless spacing does not cause false errors, while genuine internal mistakes are still rejected.

**Priority:** `Supporting 80%`

**Acceptance Scenarios**

#### SCENARIO 1: Surrounding whitespace in the command string is trimmed

**Scenario ID**: ROVER-STORY-008-S1

**GIVEN**
* a 5×5 grid and start `(1, 2, N)`
* `--commands " LMLMLMLMM "` (leading and trailing spaces)

**WHEN**
* the mission runs

**THEN**
* the command string is normalized to `"LMLMLMLMM"`
* the mission completes at `"Final position: 1 3 N"`

#### SCENARIO 2: A whitespace-only command string becomes empty and is rejected

**Scenario ID**: ROVER-STORY-008-S2

**GIVEN**
* `--commands "   "`

**WHEN**
* the input is normalized and validated

**THEN**
* normalization yields an empty string
* the empty-sequence `ValidationError` from ROVER-STORY-002 is raised
* no mission executes

#### SCENARIO 3: Extra whitespace in the position is tolerated

**Scenario ID**: ROVER-STORY-008-S3

**GIVEN**
* `--position " 1  2   N "`

**WHEN**
* the position is normalized and parsed

**THEN**
* the tokens are `1`, `2`, `N`
* the rover starts at `(1, 2)` facing `N`

#### SCENARIO 4: Extra whitespace in the grid is tolerated

**Scenario ID**: ROVER-STORY-008-S4

**GIVEN**
* `--grid " 5   5 "`

**WHEN**
* the grid is normalized and parsed

**THEN**
* the tokens are `5`, `5`
* the grid is configured as 5×5

#### SCENARIO 5: Internal whitespace in the command is not repaired

**Scenario ID**: ROVER-STORY-008-S5

**GIVEN**
* `--commands "LM M"` (internal space)

**WHEN**
* outer whitespace is trimmed and the string is validated

**THEN**
* the string remains `"LM M"`
* the parser rejects the internal space as an invalid command (ROVER-STORY-002)
* the system does not silently remove internal spaces

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-008.1 — Trim outer whitespace from CLI argument values

**AS A** Mission Operator
**I WANT** the CLI to strip leading and trailing whitespace from each argument
**SO THAT** copy-pasted values with padding still work.

**Traceability:** [Ch. 6.4.3](../../architecture/06-runtime-view.md), [Ch. 8.2 CLI layer](../../architecture/08-cross-cutting-concepts.md), [Ch. 5.3.2.1](../../architecture/05-building-block-view.md).

##### SCENARIO 1: Command string is trimmed

**Scenario ID**: ROVER-FE-008.1-S1

**GIVEN**
* `--commands "  LMLMLMLMM  "`

**WHEN**
* the CLI processes the argument

**THEN**
* the value passed downstream is `"LMLMLMLMM"`

##### SCENARIO 2: Position and grid values are trimmed

**Scenario ID**: ROVER-FE-008.1-S2

**GIVEN**
* `--position " 1 2 N "` and `--grid " 5 5 "`

**WHEN**
* the CLI processes the arguments

**THEN**
* downstream values are `"1 2 N"` and `"5 5"`

##### SCENARIO 3: Already-clean input is unchanged

**Scenario ID**: ROVER-FE-008.1-S3

**GIVEN**
* `--commands "LMLMLMLMM"` with no surrounding whitespace

**WHEN**
* the CLI processes the argument

**THEN**
* the value is unchanged

---

#### ROVER-FE-008.2 — Split position and grid on runs of whitespace

**AS A** Mission Operator
**I WANT** multiple spaces or tabs between tokens to be treated as a single separator
**SO THAT** aligned or tab-separated input is accepted.

**Traceability:** [Ch. 5.5.1 Value formats](../../architecture/05-building-block-view.md), [Ch. 8.2](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Multiple spaces collapse for the position

**Scenario ID**: ROVER-FE-008.2-S1

**GIVEN**
* the position value `"1    2    N"`

**WHEN**
* it is tokenized

**THEN**
* tokens are `["1", "2", "N"]`

##### SCENARIO 2: Tabs are treated as separators

**Scenario ID**: ROVER-FE-008.2-S2

**GIVEN**
* the grid value `"5\t5"`

**WHEN**
* it is tokenized

**THEN**
* tokens are `["5", "5"]`

##### SCENARIO 3: Missing tokens still fail validation

**Scenario ID**: ROVER-FE-008.2-S3

**GIVEN**
* the position value `"1   N"` (two tokens only)

**WHEN**
* it is tokenized

**THEN**
* it yields fewer than three tokens
* the position format error from ROVER-STORY-004 applies

---

#### ROVER-FE-008.3 — Do not rewrite the internal command content

**AS A** Mission Operator
**I WANT** the CLI to leave the inside of the command string untouched
**SO THAT** real errors are never masked by over-eager cleanup.

**Traceability:** [Ch. 6.4.3](../../architecture/06-runtime-view.md), [Ch. 8.2 Parser-layer validation](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Internal spaces are preserved for validation

**Scenario ID**: ROVER-FE-008.3-S1

**GIVEN**
* `--commands "LM M"`

**WHEN**
* the CLI normalizes only the outer whitespace

**THEN**
* the value passed to the parser is `"LM M"`

##### SCENARIO 2: Internal tabs are preserved for validation

**Scenario ID**: ROVER-FE-008.3-S2

**GIVEN**
* `--commands "LM\tM"`

**WHEN**
* outer whitespace is trimmed

**THEN**
* the internal tab remains and is rejected by the parser as an invalid command

---

### BE Sub-Stories — Input Normalization (Command Processing)

#### ROVER-BE-008.1 — Define trim-only normalization rules

**AS A** Command Processing
**I WANT** normalization to strip only leading/trailing whitespace
**SO THAT** internal characters remain subject to strict validation.

**Traceability:** [Ch. 6.4.3 Whitespace Issues](../../architecture/06-runtime-view.md), [Ch. 8.2](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Outer whitespace is removed

**Scenario ID**: ROVER-BE-008.1-S1

**GIVEN**
* the raw input `"  LMLMLMLMM\n"`

**WHEN**
* normalized

**THEN**
* the result is `"LMLMLMLMM"`

##### SCENARIO 2: Internal whitespace is preserved

**Scenario ID**: ROVER-BE-008.1-S2

**GIVEN**
* the raw input `"LM M"`

**WHEN**
* normalized

**THEN**
* the result is `"LM M"` (internal space kept)

##### SCENARIO 3: Tabs and newlines count as outer whitespace

**Scenario ID**: ROVER-BE-008.1-S3

**GIVEN**
* the raw input `"\tLMLMLMLMM\n"`

**WHEN**
* normalized

**THEN**
* the result is `"LMLMLMLMM"`

---

#### ROVER-BE-008.2 — Route empty-after-trim input to empty-sequence validation

**AS A** Command Processing
**I WANT** a blank input to become an explicit empty-sequence error
**SO THAT** whitespace-only missions are never silently accepted.

**Traceability:** [Ch. 6.4.3 Empty Sequence](../../architecture/06-runtime-view.md), [Ch. 4.6.3 Edge Cases](../../architecture/04-solution-strategy.md), ROVER-BE-002.3.

##### SCENARIO 1: Spaces-only input is rejected

**Scenario ID**: ROVER-BE-008.2-S1

**GIVEN**
* the raw command input `"   "`

**WHEN**
* normalized and validated

**THEN**
* normalization yields `""`
* the empty-sequence `ValidationError` is raised

##### SCENARIO 2: Tabs/newlines-only input is rejected

**Scenario ID**: ROVER-BE-008.2-S2

**GIVEN**
* the raw command input `"\t\n "`

**WHEN**
* normalized and validated

**THEN**
* normalization yields `""`
* the empty-sequence `ValidationError` is raised

---

#### ROVER-BE-008.3 — Tokenize position and grid on whitespace runs

**AS A** Command Processing
**I WANT** position and grid inputs split on one-or-more whitespace characters
**SO THAT** extra spacing does not change the parsed values.

**Traceability:** [Ch. 5.5.1 Value formats](../../architecture/05-building-block-view.md), [Ch. 8.2](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Multiple spaces tokenize correctly

**Scenario ID**: ROVER-BE-008.3-S1

**GIVEN**
* the position input `"1   2   N"`

**WHEN**
* tokenized

**THEN**
* tokens are `["1", "2", "N"]`

##### SCENARIO 2: Mixed whitespace tokenizes correctly

**Scenario ID**: ROVER-BE-008.3-S2

**GIVEN**
* the grid input `"5 \t 5"`

**WHEN**
* tokenized

**THEN**
* tokens are `["5", "5"]`

##### SCENARIO 3: Token count is validated after normalization

**Scenario ID**: ROVER-BE-008.3-S3

**GIVEN**
* a position input with two tokens after normalization

**WHEN**
* parsed

**THEN**
* the position format validation (ROVER-STORY-004) rejects it

---

#### ROVER-BE-008.4 — Make normalization idempotent and deterministic

**AS A** Command Processing
**I WANT** normalization to be a pure, repeatable function
**SO THAT** re-processing input never changes the result.

**Traceability:** [Ch. 8.2](../../architecture/08-cross-cutting-concepts.md), [Ch. 5.7.1 Testability (pure functions)](../../architecture/05-building-block-view.md).

##### SCENARIO 1: Applying normalization twice equals once

**Scenario ID**: ROVER-BE-008.4-S1

**GIVEN**
* any raw input

**WHEN**
* normalization is applied twice

**THEN**
* the result equals a single application

##### SCENARIO 2: Same input yields the same output

**Scenario ID**: ROVER-BE-008.4-S2

**GIVEN**
* identical raw input

**WHEN**
* normalized repeatedly

**THEN**
* the output is identical every time

##### SCENARIO 3: Normalization has no side effects

**Scenario ID**: ROVER-BE-008.4-S3

**GIVEN**
* a raw input

**WHEN**
* normalized

**THEN**
* no mission state, file or external resource is touched

---

### INFRA Sub-Stories — Shared Helper, Observability, Side-effect Freedom

#### ROVER-INFRA-008.1 — Centralise normalization in one stdlib-only helper

**AS A** System
**I WANT** one normalization helper used before every validation layer
**SO THAT** whitespace rules cannot drift between inputs.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 8.2](../../architecture/08-cross-cutting-concepts.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: One helper handles all three inputs

**Scenario ID**: ROVER-INFRA-008.1-S1

**GIVEN**
* command, position and grid inputs

**WHEN**
* the CLI normalizes them

**THEN**
* all three use the same normalization helper

##### SCENARIO 2: No duplicated trimming logic

**Scenario ID**: ROVER-INFRA-008.1-S2

**GIVEN**
* the CLI and configuration modules

**WHEN**
* inspected

**THEN**
* neither re-implements whitespace trimming locally

##### SCENARIO 3: Standard library only

**Scenario ID**: ROVER-INFRA-008.1-S3

**GIVEN**
* the installed package

**WHEN**
* normalization runs

**THEN**
* it uses only the Python standard library (ADR-002)

---

#### ROVER-INFRA-008.2 — Log normalization at debug level

**AS A** Course Student
**I WANT** an opt-in log of raw vs normalized input
**SO THAT** I can diagnose surprising input handling.

**Traceability:** [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md), [Ch. 4.5.3](../../architecture/04-solution-strategy.md).

> **Events/notifications are not applicable** to this story; no telemetry stream is in scope
> (Ch. 4.8.2 / Ch. 8.5).

##### SCENARIO 1: Default logging is silent about normalization

**Scenario ID**: ROVER-INFRA-008.2-S1

**GIVEN**
* default logging

**WHEN**
* inputs are normalized

**THEN**
* no normalization message is printed

##### SCENARIO 2: Verbose mode shows raw and normalized values

**Scenario ID**: ROVER-INFRA-008.2-S2

**GIVEN**
* verbose/debug logging enabled

**WHEN**
* normalization changes an input

**THEN**
* a stderr trace shows the raw and normalized values

##### SCENARIO 3: Logging does not change the parsed result

**Scenario ID**: ROVER-INFRA-008.2-S3

**GIVEN**
* the same input with logging off and on

**WHEN**
* both are parsed

**THEN**
* the resulting values and exit code are identical

---

#### ROVER-INFRA-008.3 — Keep normalization side-effect free

**AS A** System
**I WANT** normalization to touch no files or state
**SO THAT** input hygiene never mutates mission data (ADR-001).

**Traceability:** [ADR-001](../../architecture/09-architecture-decisions.md), [Ch. 2.1](../../architecture/02-constraints.md), [Ch. 6.9.3](../../architecture/06-runtime-view.md).

##### SCENARIO 1: No files are written

**Scenario ID**: ROVER-INFRA-008.3-S1

**GIVEN**
* a clean working directory

**WHEN**
* inputs are normalized

**THEN**
* no files are created

##### SCENARIO 2: Mission state is untouched

**Scenario ID**: ROVER-INFRA-008.3-S2

**GIVEN**
* an existing in-memory mission state

**WHEN**
* normalization runs

**THEN**
* the state is unchanged

##### SCENARIO 3: A rejected blank input leaves no residue

**Scenario ID**: ROVER-INFRA-008.3-S3

**GIVEN**
* a whitespace-only command input

**WHEN**
* it is normalized to empty and rejected

**THEN**
* no state, snapshot or artifact is produced
* the process exits with the domain error code

---

---

## ROVER-STORY-009

> **Status note (backlog):** This is the *optional* JSON persistence extension explicitly allowed
> by ADR-001 and deferred by the initial scope (Ch. 4.8.2, Ch. 5.8.2, Ch. 11.2). It is **opt-in**:
> without the new flags the system remains strictly in-memory and all earlier "no files written"
> guarantees continue to hold.

### Architecture Traceability

| Trace | Link |
|-------|------|
| Decision | [ADR-001 — optional JSON persistence for mission snapshots](../../architecture/09-architecture-decisions.md) |
| File I/O interface | [Ch. 3.2.2 External Interfaces — Load/save snapshots](../../architecture/03-context-and-scope.md) |
| Persistence criticality | [Ch. 3.5 State Persistence (optional, Low)](../../architecture/03-context-and-scope.md) |
| Extension points | [Ch. 4.8.2 / 4.8.3 Future Extensions — JSON persistence](../../architecture/04-solution-strategy.md) |
| Initial scope exclusion | [Ch. 5.8.2 No persistence between invocations](../../architecture/05-building-block-view.md) |
| Data format constraint | [Ch. 2.3 Simple Data Formats (text/JSON)](../../architecture/02-constraints.md) |
| Technical debt | [Ch. 11.2 Hardcoded obstacle configuration](../../architecture/11-risks-and-technical-debts.md) |
| Component | [Ch. 5.3.2.5 Mission State](../../architecture/05-building-block-view.md), [Ch. 5.3.2.4 Grid Management](../../architecture/05-building-block-view.md) |

### Original Story

**ROVER-STORY-009**

> **AS A** Mission Operator
> **I WANT** to optionally save the mission's grid and last valid state to a JSON snapshot and reload it in a later invocation
> **SO THAT** I can resume or audit a mission across runs — without changing the default in-memory behaviour.

**Priority:** `Backlog (optional extension)`

**Acceptance Scenarios**

#### SCENARIO 1: An opt-in save writes a snapshot after a successful mission

**Scenario ID**: ROVER-STORY-009-S1

**GIVEN**
* a 5×5 grid, start `(1, 2, N)`, sequence `"LMLMLMLMM"`
* the opt-in flag `--save-snapshot mission.json`

**WHEN**
* the mission completes

**THEN**
* stdout shows `"Final position: 1 3 N"` and the exit code is `0`
* `mission.json` is written as valid JSON containing the grid (5×5, obstacles) and state `(1, 3, N)`
* the snapshot records a `schema_version` and a `success` status

#### SCENARIO 2: Without the opt-in flag, no snapshot is written

**Scenario ID**: ROVER-STORY-009-S2

**GIVEN**
* the same mission run without `--save-snapshot`

**WHEN**
* the mission completes

**THEN**
* no snapshot or other file is created
* behaviour is identical to the in-memory baseline (ADR-001)

#### SCENARIO 3: A snapshot can be loaded to resume a mission

**Scenario ID**: ROVER-STORY-009-S3

**GIVEN**
* a valid snapshot for a 5×5 grid with state `(1, 3, N)`
* the opt-in flag `--load-snapshot mission.json` and sequence `"M"`

**WHEN**
* the mission runs

**THEN**
* the rover starts at `(1, 3, N)` from the snapshot
* it ends at `"Final position: 1 4 N"`

#### SCENARIO 4: A corrupt or invalid snapshot is rejected

**Scenario ID**: ROVER-STORY-009-S4

**GIVEN**
* a snapshot file that is malformed JSON, missing required fields, or has an unsupported version

**WHEN**
* it is loaded

**THEN**
* a `ValidationError` is reported with a clear reason
* no mission executes and no state is restored
* the process exits with code `1`

#### SCENARIO 5: Save/load round-trips exactly

**Scenario ID**: ROVER-STORY-009-S5

**GIVEN**
* a completed mission saved to a snapshot

**WHEN**
* that snapshot is loaded

**THEN**
* grid dimensions, obstacles, position and heading match the saved values exactly

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-009.1 — Add opt-in snapshot flags

**AS A** Mission Operator
**I WANT** `--save-snapshot <path>` and `--load-snapshot <path>` flags that are off by default
**SO THAT** persistence is available on demand without affecting normal runs.

**Traceability:** [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [Ch. 5.5.1](../../architecture/05-building-block-view.md), [ADR-002](../../architecture/09-architecture-decisions.md), [ADR-001](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: Both flags are parsed as file paths

**Scenario ID**: ROVER-FE-009.1-S1

**GIVEN**
* `--save-snapshot mission.json` and `--load-snapshot prior.json`

**WHEN**
* the CLI parses arguments

**THEN**
* both values are accepted as paths
* neither is required

##### SCENARIO 2: Absence of the flags disables persistence

**Scenario ID**: ROVER-FE-009.1-S2

**GIVEN**
* an invocation without either snapshot flag

**WHEN**
* the mission runs

**THEN**
* no snapshot read or write occurs

##### SCENARIO 3: Help documents the new flags and their opt-in nature

**Scenario ID**: ROVER-FE-009.1-S3

**GIVEN**
* `--help`

**WHEN**
* help is rendered

**THEN**
* it lists `--save-snapshot` and `--load-snapshot`
* it states persistence is off by default

---

#### ROVER-FE-009.2 — Report snapshot outcomes

**AS A** Mission Operator
**I WANT** clear feedback when a snapshot is saved, loaded, or fails
**SO THAT** I know whether persistence succeeded.

**Traceability:** [Ch. 6.7.3 User Experience](../../architecture/06-runtime-view.md), [Ch. 8.1 Error Handling](../../architecture/08-cross-cutting-concepts.md), [Ch. 5.3.2.1](../../architecture/05-building-block-view.md).

##### SCENARIO 1: A successful save is confirmed

**Scenario ID**: ROVER-FE-009.2-S1

**GIVEN**
* a successful mission with `--save-snapshot mission.json`

**WHEN**
* the snapshot is written

**THEN**
* a confirmation such as `"Snapshot saved: mission.json"` appears on stderr
* stdout still carries only `"Final position: 1 3 N"` and the exit code is `0`

##### SCENARIO 2: A load failure is an error exit

**Scenario ID**: ROVER-FE-009.2-S2

**GIVEN**
* `--load-snapshot` pointing at a corrupt snapshot

**WHEN**
* the snapshot is rejected

**THEN**
* an `"Error: ..."` message appears on stderr
* stdout has no `Final position:` line and the exit code is `1`

##### SCENARIO 3: A save failure is an error exit

**Scenario ID**: ROVER-FE-009.2-S3

**GIVEN**
* a mission with `--save-snapshot` pointing at an unwritable location

**WHEN**
* the write fails

**THEN**
* a snapshot error appears on stderr
* no success `Final position:` line is emitted and the exit code is `1`

---

#### ROVER-FE-009.3 — Define snapshot vs explicit-argument precedence

**AS A** Mission Operator
**I WANT** explicit `--grid`/`--position` to override snapshot values
**SO THAT** I can resume from a snapshot yet still adjust the mission.

**Traceability:** [Ch. 5.5.1](../../architecture/05-building-block-view.md), [Ch. 8.2 Layered Validation](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Load-only uses the snapshot values

**Scenario ID**: ROVER-FE-009.3-S1

**GIVEN**
* `--load-snapshot mission.json` with no `--grid`/`--position`

**WHEN**
* the mission starts

**THEN**
* grid, obstacles, position and heading come from the snapshot

##### SCENARIO 2: Explicit values override the snapshot

**Scenario ID**: ROVER-FE-009.3-S2

**GIVEN**
* a snapshot with state `(1, 3, N)` and explicit `--position "0 0 E"`

**WHEN**
* the mission starts

**THEN**
* the rover starts at `(0, 0, E)`
* the override is noted only in debug logging

##### SCENARIO 3: Overridden grid revalidates the restored position

**Scenario ID**: ROVER-FE-009.3-S3

**GIVEN**
* a snapshot whose position is outside an explicitly supplied smaller grid

**WHEN**
* the configuration is validated

**THEN**
* `InvalidPositionError` is raised against the effective grid
* no mission executes

---

### BE Sub-Stories — Snapshot Schema, (De)serialization, Restore

#### ROVER-BE-009.1 — Define a versioned snapshot schema

**AS A** Mission State
**I WANT** a documented, versioned JSON schema for snapshots
**SO THAT** future changes remain backward-detectable.

**Traceability:** [ADR-001](../../architecture/09-architecture-decisions.md), [Ch. 2.3 Simple Data Formats](../../architecture/02-constraints.md), [Ch. 3.2.2 File I/O](../../architecture/03-context-and-scope.md).

##### SCENARIO 1: The schema carries version, grid, state and status

**Scenario ID**: ROVER-BE-009.1-S1

**GIVEN**
* a generated snapshot

**WHEN**
* its keys are inspected

**THEN**
* it contains `schema_version`, `grid` (`width`, `height`, `obstacles`), `state` (`x`, `y`, `heading`) and `status`

##### SCENARIO 2: The version is present and stable

**Scenario ID**: ROVER-BE-009.1-S2

**GIVEN**
* any generated snapshot

**WHEN**
* read

**THEN**
* `schema_version` is present with the current version value

##### SCENARIO 3: Serialization is deterministic

**Scenario ID**: ROVER-BE-009.1-S3

**GIVEN**
* the same mission state saved twice

**WHEN**
* the JSON is compared

**THEN**
* the serialized content is identical (stable key ordering / values)

---

#### ROVER-BE-009.2 — Serialize the mission to a snapshot object

**AS A** Mission State
**I WANT** to capture the grid and last valid state into a snapshot
**SO THAT** the persisted data is complete and trustworthy.

**Traceability:** [Ch. 5.3.2.5](../../architecture/05-building-block-view.md), [Ch. 5.3.2.4](../../architecture/05-building-block-view.md), [Ch. 6.8.3 State Visibility](../../architecture/06-runtime-view.md).

##### SCENARIO 1: A successful mission captures its final state

**Scenario ID**: ROVER-BE-009.2-S1

**GIVEN**
* a mission ending at `(1, 3, N)` on a 5×5 grid with no obstacles

**WHEN**
* the snapshot is produced

**THEN**
* it stores `(1, 3, N)`, grid `5×5`, empty obstacles and `status: "success"`

##### SCENARIO 2: A blocked mission captures the last valid state

**Scenario ID**: ROVER-BE-009.2-S2

**GIVEN**
* a mission halted at `(0, 1, N)` by an obstacle, with opt-in save

**WHEN**
* the snapshot is produced

**THEN**
* it stores `(0, 1, N)` and `status: "blocked"` with the blocking reason
* it never stores the rejected target

##### SCENARIO 3: Obstacles are preserved in the snapshot

**Scenario ID**: ROVER-BE-009.2-S3

**GIVEN**
* a grid with obstacles `{(0,2), (1,2)}`

**WHEN**
* the snapshot is produced

**THEN**
* the obstacle set is serialized in a stable, order-independent form

---

#### ROVER-BE-009.3 — Deserialize and validate a snapshot

**AS A** Mission State
**I WANT** to validate every loaded snapshot before using it
**SO THAT** corrupt or hostile files cannot corrupt a mission.

**Traceability:** [Ch. 6.7.1 ValidationError hierarchy](../../architecture/06-runtime-view.md), [Ch. 8.2](../../architecture/08-cross-cutting-concepts.md), [Ch. 4.5.1](../../architecture/04-solution-strategy.md).

##### SCENARIO 1: A valid snapshot yields grid and state

**Scenario ID**: ROVER-BE-009.3-S1

**GIVEN**
* a well-formed snapshot

**WHEN**
* it is loaded

**THEN**
* it yields a grid configuration and a `(position, heading)` state

##### SCENARIO 2: Missing required fields are rejected

**Scenario ID**: ROVER-BE-009.3-S2

**GIVEN**
* a snapshot missing `grid` or `state`

**WHEN**
* it is loaded

**THEN**
* a `ValidationError` names the missing field
* no state is restored

##### SCENARIO 3: Bad types or heading are rejected

**Scenario ID**: ROVER-BE-009.3-S3

**GIVEN**
* a snapshot with non-integer coordinates or heading `"Q"`

**WHEN**
* it is loaded

**THEN**
* a `ValidationError` is raised describing the invalid value

##### SCENARIO 4: Out-of-bounds state is rejected

**Scenario ID**: ROVER-BE-009.3-S4

**GIVEN**
* a snapshot whose position lies outside its own grid bounds

**WHEN**
* it is loaded

**THEN**
* an `InvalidPositionError` is raised

##### SCENARIO 5: Unsupported schema versions are rejected

**Scenario ID**: ROVER-BE-009.3-S5

**GIVEN**
* a snapshot with an unknown `schema_version`

**WHEN**
* it is loaded

**THEN**
* a `ValidationError` states the version is unsupported

---

#### ROVER-BE-009.4 — Restore mission state atomically

**AS A** Mission State
**I WANT** a valid snapshot to initialise state in one step, and an invalid one to change nothing
**SO THAT** restore is all-or-nothing.

**Traceability:** [Ch. 6.8.2 Validation Before Mutation](../../architecture/06-runtime-view.md), [Ch. 5.3.2.5](../../architecture/05-building-block-view.md), [ADR-001](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: A valid snapshot initialises the mission

**Scenario ID**: ROVER-BE-009.4-S1

**GIVEN**
* a valid snapshot with state `(1, 3, N)`

**WHEN**
* it is restored

**THEN**
* `get_current_position()` returns `(1, 3, N)` before any command runs

##### SCENARIO 2: An invalid snapshot leaves state untouched

**Scenario ID**: ROVER-BE-009.4-S2

**GIVEN**
* an invalid snapshot

**WHEN**
* restore fails

**THEN**
* no mission state is committed
* `set_current_position` is never called

##### SCENARIO 3: Grid and obstacles are restored with the state

**Scenario ID**: ROVER-BE-009.4-S3

**GIVEN**
* a snapshot containing grid dimensions and obstacles

**WHEN**
* restored

**THEN**
* subsequent boundary and obstacle checks use the restored configuration

##### SCENARIO 4: Restored values equal the snapshot

**Scenario ID**: ROVER-BE-009.4-S4

**GIVEN**
* a valid snapshot

**WHEN**
* restored

**THEN**
* the restored position and heading exactly equal the snapshot values

---

#### ROVER-BE-009.5 — Guarantee round-trip fidelity

**AS A** Mission State
**I WANT** save→load to reproduce the exact state
**SO THAT** snapshots can be trusted for resume and audit.

**Traceability:** [Ch. 3.2.2 File I/O](../../architecture/03-context-and-scope.md), [Ch. 2.3](../../architecture/02-constraints.md).

##### SCENARIO 1: Save then load reproduces the state

**Scenario ID**: ROVER-BE-009.5-S1

**GIVEN**
* a mission state and grid configuration

**WHEN**
* it is saved and then loaded

**THEN**
* the loaded grid, obstacles, position and heading equal the originals

##### SCENARIO 2: Repeated round-trips are stable

**Scenario ID**: ROVER-BE-009.5-S2

**GIVEN**
* a snapshot loaded and re-saved multiple times

**WHEN**
* compared

**THEN**
* the content remains equivalent (idempotent round-trip)

##### SCENARIO 3: Obstacle ordering does not affect equality

**Scenario ID**: ROVER-BE-009.5-S3

**GIVEN**
* an obstacle set serialized in different orders

**WHEN**
* loaded

**THEN**
* the restored obstacle set is equal regardless of order

---

### INFRA Sub-Stories — JSON Adapter, Opt-in Guarantee, Observability

#### ROVER-INFRA-009.1 — Provide a stdlib JSON file adapter with atomic writes

**AS A** System
**I WANT** snapshot I/O isolated behind a small adapter that writes atomically
**SO THAT** a crash cannot leave a half-written snapshot.

**Traceability:** [ADR-001](../../architecture/09-architecture-decisions.md), [ADR-002 standard library only](../../architecture/09-architecture-decisions.md), [Ch. 2.1 Minimal Dependencies](../../architecture/02-constraints.md).

##### SCENARIO 1: JSON I/O uses only the standard library

**Scenario ID**: ROVER-INFRA-009.1-S1

**GIVEN**
* the installed package

**WHEN**
* a snapshot is saved or loaded

**THEN**
* only the standard-library `json` module is used
* no third-party dependency is required

##### SCENARIO 2: Writes are atomic

**Scenario ID**: ROVER-INFRA-009.1-S2

**GIVEN**
* a snapshot save in progress

**WHEN**
* the write fails part-way

**THEN**
* no partially written snapshot file remains at the target path
* a temporary file is cleaned up

##### SCENARIO 3: A missing file is reported clearly

**Scenario ID**: ROVER-INFRA-009.1-S3

**GIVEN**
* `--load-snapshot` pointing at a non-existent path

**WHEN**
* loading is attempted

**THEN**
* a clear error is reported (not an unhandled traceback)
* the process exits with code `1`

---

#### ROVER-INFRA-009.2 — Keep persistence strictly opt-in

**AS A** System
**I WANT** no snapshot I/O unless explicitly requested
**SO THAT** the ADR-001 in-memory guarantee remains the default.

**Traceability:** [ADR-001](../../architecture/09-architecture-decisions.md), [Ch. 5.8.2 No persistence between invocations](../../architecture/05-building-block-view.md), [Ch. 7.5.2 Transient state](../../architecture/07-deployment-view.md).

##### SCENARIO 1: Default runs write no files

**Scenario ID**: ROVER-INFRA-009.2-S1

**GIVEN**
* an invocation without snapshot flags

**WHEN**
* the mission completes (success or failure)

**THEN**
* no snapshot or state file is written
* earlier no-persistence guarantees still hold

##### SCENARIO 2: Only the explicit flags trigger I/O

**Scenario ID**: ROVER-INFRA-009.2-S2

**GIVEN**
* only `--save-snapshot` or only `--load-snapshot`

**WHEN**
* the mission runs

**THEN**
* only the requested operation occurs
* no implicit read or write happens

##### SCENARIO 3: Persistence sits behind the state module boundary

**Scenario ID**: ROVER-INFRA-009.2-S3

**GIVEN**
* the persistence adapter

**WHEN**
* its dependencies are inspected

**THEN**
* it is used only via the state/grid modules (ADR-001 extension point)
* parser and navigation do not perform file I/O

---

#### ROVER-INFRA-009.3 — Observe snapshot operations

**AS A** Course Student
**I WANT** snapshot operations logged at an appropriate level
**SO THAT** I can audit persistence without noisy default output.

**Traceability:** [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md), [Ch. 4.5.3](../../architecture/04-solution-strategy.md).

> **Events/notifications are not applicable** to this story; snapshots are file-based, not event-driven
> (Ch. 4.8.2 / Ch. 8.5).

##### SCENARIO 1: Default logging is minimal

**Scenario ID**: ROVER-INFRA-009.3-S1

**GIVEN**
* default logging and a snapshot save

**WHEN**
* the save completes

**THEN**
* at most one confirmation line appears on stderr
* stdout is unaffected

##### SCENARIO 2: Verbose mode records path and size

**Scenario ID**: ROVER-INFRA-009.3-S2

**GIVEN**
* verbose/debug logging enabled

**WHEN**
* a snapshot is saved or loaded

**THEN**
* the log records the path and (for saves) the byte size

##### SCENARIO 3: Logging does not change persistence outcomes

**Scenario ID**: ROVER-INFRA-009.3-S3

**GIVEN**
* the same snapshot operation with logging off and on

**WHEN**
* both finish

**THEN**
* the file content and exit code are identical

---

---

## ROVER-STORY-010

> **Consolidation note:** the earlier bundles introduced small logging hooks (e.g. ROVER-INFRA-001.3,
> 002.2, 003.2, 004.2, 006.2, 007.3, 008.2, 009.3). This story defines the single logging facility
> those hooks plug into, so behaviour is consistent and configured in one place.

### Architecture Traceability

| Trace | Link |
|-------|------|
| Logging concept | [Ch. 8.5 Logging and Observability](../../architecture/08-cross-cutting-concepts.md) |
| Error reporting / basic logging | [Ch. 4.5.3 Error Reporting](../../architecture/04-solution-strategy.md) |
| Zero infrastructure | [Ch. 2.4 Zero Infrastructure](../../architecture/02-constraints.md), [Ch. 7.5 No Operational Infrastructure](../../architecture/07-deployment-view.md) |
| No network / no persistence | [Ch. 6.9.3 Resource Management](../../architecture/06-runtime-view.md) |
| Runtime flow to trace | [Ch. 6.3.3 Step-by-Step Analysis](../../architecture/06-runtime-view.md) |
| Decisions | [ADR-001](../../architecture/09-architecture-decisions.md), [ADR-002 standard library only](../../architecture/09-architecture-decisions.md) |

### Original Story

**ROVER-STORY-010**

> **AS A** Course Student
> **I WANT** an opt-in, structured logging facility that traces command execution and errors to the console
> **SO THAT** I can diagnose rover behaviour without polluting operator-facing output or changing mission results.

**Priority:** `Supporting 80%`

**Acceptance Scenarios**

#### SCENARIO 1: Logging is silent by default

**Scenario ID**: ROVER-STORY-010-S1

**GIVEN**
* default configuration (no logging flag, no log-level env var)
* a valid mission `"LMLMLMLMM"` from `(1, 2, N)` on 5×5

**WHEN**
* the mission runs

**THEN**
* stdout contains only `"Final position: 1 3 N"`
* stderr contains no trace output
* the exit code is `0`

#### SCENARIO 2: Debug mode traces each operation to stderr

**Scenario ID**: ROVER-STORY-010-S2

**GIVEN**
* debug logging enabled
* the same mission

**WHEN**
* the sequence executes

**THEN**
* stderr contains a trace entry for each of the nine operations
* each entry includes the operation and the resulting position/heading
* stdout still contains only the final position

#### SCENARIO 3: Log records are structured and consistent

**Scenario ID**: ROVER-STORY-010-S3

**GIVEN**
* any emitted log record

**WHEN**
* it is inspected

**THEN**
* it carries a level, an event name, and context fields (e.g. operation, position, heading)
* the format is stable and machine-parseable

#### SCENARIO 4: Log level filters output

**Scenario ID**: ROVER-STORY-010-S4

**GIVEN**
* the levels `ERROR`, `INFO` and `DEBUG`
* a run that both succeeds and emits lifecycle events

**WHEN**
* each level is selected

**THEN**
* `ERROR` shows only errors
* `INFO` shows mission start/end summaries but not per-operation detail
* `DEBUG` shows per-operation detail

#### SCENARIO 5: Logging never changes the mission outcome

**Scenario ID**: ROVER-STORY-010-S5

**GIVEN**
* the same inputs run with logging disabled, at `INFO`, and at `DEBUG`

**WHEN**
* each run completes

**THEN**
* the reported final position and exit code are identical across all three

---

### FE Sub-Stories — Mission Console (Command Interface, Ch. 5.3.2.1)

#### ROVER-FE-010.1 — Provide opt-in logging controls

**AS A** Course Student
**I WANT** a `--debug`/`--log-level` flag and an environment variable, with flags taking precedence
**SO THAT** I can enable diagnostics per run or per shell.

**Traceability:** [Ch. 8.5](../../architecture/08-cross-cutting-concepts.md), [Ch. 5.3.2.1](../../architecture/05-building-block-view.md), [ADR-002](../../architecture/09-architecture-decisions.md).

##### SCENARIO 1: Defaults keep logging off

**Scenario ID**: ROVER-FE-010.1-S1

**GIVEN**
* no `--debug`/`--log-level` flag and no log-level env var

**WHEN**
* the CLI runs

**THEN**
* the effective level suppresses all non-error logs

##### SCENARIO 2: The flag enables logging

**Scenario ID**: ROVER-FE-010.1-S2

**GIVEN**
* `--debug` (or `--log-level DEBUG`)

**WHEN**
* the CLI runs

**THEN**
* debug logging is enabled for the run

##### SCENARIO 3: The environment variable enables logging

**Scenario ID**: ROVER-FE-010.1-S3

**GIVEN**
* `MARS_ROVER_LOG_LEVEL=DEBUG` in the environment, no flag

**WHEN**
* the CLI runs

**THEN**
* debug logging is enabled

##### SCENARIO 4: The flag overrides the environment

**Scenario ID**: ROVER-FE-010.1-S4

**GIVEN**
* `MARS_ROVER_LOG_LEVEL=DEBUG` and `--log-level ERROR`

**WHEN**
* the CLI runs

**THEN**
* the effective level is `ERROR` (flag wins)

---

#### ROVER-FE-010.2 — Route logs to stderr and results to stdout

**AS A** Mission Operator
**I WANT** logs and results kept on separate streams
**SO THAT** piping `Final position:` output stays clean.

**Traceability:** [Ch. 8.5](../../architecture/08-cross-cutting-concepts.md), [Ch. 6.7.3](../../architecture/06-runtime-view.md).

##### SCENARIO 1: Debug trace goes to stderr

**Scenario ID**: ROVER-FE-010.2-S1

**GIVEN**
* debug logging enabled

**WHEN**
* a mission runs

**THEN**
* all log records are written to stderr
* stdout contains only the final position or nothing on failure

##### SCENARIO 2: Results stay on stdout

**Scenario ID**: ROVER-FE-010.2-S2

**GIVEN**
* any log level

**WHEN**
* a mission succeeds

**THEN**
* `"Final position: 1 3 N"` is on stdout

##### SCENARIO 3: Errors and logs both go to stderr

**Scenario ID**: ROVER-FE-010.2-S3

**GIVEN**
* a failing run with logging enabled

**WHEN**
* the failure is reported

**THEN**
* both the error message and any trace records are on stderr
* stdout stays empty

---

#### ROVER-FE-010.3 — Render log records readably

**AS A** Course Student
**I WANT** each log line to be both human-readable and machine-parseable
**SO THAT** I can skim it or grep it.

**Traceability:** [Ch. 8.5](../../architecture/08-cross-cutting-concepts.md), [Ch. 10 Simplicity](../../architecture/10-quality-requirements.md).

##### SCENARIO 1: Records show level, event and context

**Scenario ID**: ROVER-FE-010.3-S1

**GIVEN**
* an operation-applied debug record

**WHEN**
* it is rendered

**THEN**
* the line includes the level, the event name, and the operation/position context

##### SCENARIO 2: The format is stable

**Scenario ID**: ROVER-FE-010.3-S2

**GIVEN**
* two records of the same event type

**WHEN**
* compared

**THEN**
* they use the same field order and separators

##### SCENARIO 3: No multi-line records

**Scenario ID**: ROVER-FE-010.3-S3

**GIVEN**
* any log record

**WHEN**
* rendered

**THEN**
* it occupies a single line (one record per line)

---

### BE Sub-Stories — Execution Instrumentation

#### ROVER-BE-010.1 — Instrument the execution pipeline

**AS A** System
**I WANT** lifecycle and per-operation events emitted at defined points
**SO THAT** the trace reflects the real execution order.

**Traceability:** [Ch. 6.3.3 Step-by-Step Analysis](../../architecture/06-runtime-view.md), [Ch. 5.4.1 Interaction Flow](../../architecture/05-building-block-view.md), [Ch. 8.5](../../architecture/08-cross-cutting-concepts.md).

##### SCENARIO 1: Mission start is logged with configuration

**Scenario ID**: ROVER-BE-010.1-S1

**GIVEN**
* logging at `INFO` or `DEBUG`

**WHEN**
* a mission starts

**THEN**
* a `mission_start` record includes grid dimensions and starting position/heading

##### SCENARIO 2: Each applied operation is logged

**Scenario ID**: ROVER-BE-010.1-S2

**GIVEN**
* `DEBUG` level and a multi-operation sequence

**WHEN**
* each valid operation is applied

**THEN**
* an `operation_applied` record shows the operation and the resulting position/heading
* records appear in execution order

##### SCENARIO 3: Mission end or block is logged

**Scenario ID**: ROVER-BE-010.1-S3

**GIVEN**
* a mission that completes or halts

**WHEN**
* it ends

**THEN**
* a `mission_end` record states success or the blocking reason and the final/last-valid state

---

#### ROVER-BE-010.2 — Emit a stable structured event schema

**AS A** System
**I WANT** every event to use a consistent field schema
**SO THAT** logs can be parsed and reasoned about reliably.

**Traceability:** [Ch. 8.5](../../architecture/08-cross-cutting-concepts.md), [Ch. 5.7.1 Testability](../../architecture/05-building-block-view.md).

##### SCENARIO 1: Required fields are always present

**Scenario ID**: ROVER-BE-010.2-S1

**GIVEN**
* any emitted event

**WHEN**
* inspected

**THEN**
* it has `level`, `event`, and the event-specific context fields

##### SCENARIO 2: Field names are consistent across events

**Scenario ID**: ROVER-BE-010.2-S2

**GIVEN**
* `mission_start`, `operation_applied` and `mission_end` events

**WHEN**
* compared

**THEN**
* shared concepts (position, heading, status) use the same field names

##### SCENARIO 3: Events carry no extraneous or sensitive data

**Scenario ID**: ROVER-BE-010.2-S3

**GIVEN**
* any event

**WHEN**
* inspected

**THEN**
* it contains only mission-relevant fields
* no file contents or environment secrets are logged

---

#### ROVER-BE-010.3 — Keep instrumentation side-effect free

**AS A** System
**I WANT** logging to never alter domain behaviour or propagate its own failures
**SO THAT** diagnostics are always safe to enable.

**Traceability:** [Ch. 8.5 (logging optional/disable-able)](../../architecture/08-cross-cutting-concepts.md), [Ch. 6.8.2](../../architecture/06-runtime-view.md), [Ch. 10 Reliability](../../architecture/10-quality-requirements.md).

##### SCENARIO 1: Logging does not mutate state

**Scenario ID**: ROVER-BE-010.3-S1

**GIVEN**
* a mission with logging enabled

**WHEN**
* events are emitted

**THEN**
* mission state and grid configuration are unchanged by logging

##### SCENARIO 2: A logging failure does not break the mission

**Scenario ID**: ROVER-BE-010.3-S2

**GIVEN**
* a failure inside the logging sink

**WHEN**
* the mission runs

**THEN**
* the mission still completes with the correct result
* no logging exception escapes

##### SCENARIO 3: Results are identical with logging on or off

**Scenario ID**: ROVER-BE-010.3-S3

**GIVEN**
* the same inputs at each log level

**WHEN**
* compared

**THEN**
* final position, last valid state and exit code are identical

---

### INFRA Sub-Stories — Logging Facade, Console Handler, Zero-Infra Guarantees

#### ROVER-INFRA-010.1 — Provide one stdlib logging facade

**AS A** System
**I WANT** a single logging setup point built on the standard library
**SO THAT** every module logs consistently with no external dependency.

**Traceability:** [Ch. 8.5](../../architecture/08-cross-cutting-concepts.md), [ADR-002](../../architecture/09-architecture-decisions.md), [Ch. 2.1 Minimal Dependencies](../../architecture/02-constraints.md).

##### SCENARIO 1: Standard library only

**Scenario ID**: ROVER-INFRA-010.1-S1

**GIVEN**
* the installed package

**WHEN**
* logging is configured

**THEN**
* it uses only the Python standard library (`logging`)
* no third-party logging package is required

##### SCENARIO 2: A single configuration point

**Scenario ID**: ROVER-INFRA-010.1-S2

**GIVEN**
* CLI, parser, navigation, grid and state modules

**WHEN**
* they log

**THEN**
* all use the shared logger/facade
* no module configures its own handlers

##### SCENARIO 3: Levels are validated

**Scenario ID**: ROVER-INFRA-010.1-S3

**GIVEN**
* an invalid `--log-level` or env value

**WHEN**
* logging is configured

**THEN**
* a clear usage error is raised (or the documented fallback is applied)
* the process does not crash with an unhandled exception

---

#### ROVER-INFRA-010.2 — Use a console handler on stderr with structured formatting

**AS A** System
**I WANT** a stderr console handler with a stable formatter
**SO THAT** logging stays local and pipeline-friendly (zero infrastructure).

**Traceability:** [Ch. 8.5 (console-based only)](../../architecture/08-cross-cutting-concepts.md), [Ch. 7.5.1 No operational infrastructure](../../architecture/07-deployment-view.md), [Ch. 2.4 Zero Infrastructure](../../architecture/02-constraints.md).

##### SCENARIO 1: Logs are written to stderr only

**Scenario ID**: ROVER-INFRA-010.2-S1

**GIVEN**
* logging enabled

**WHEN**
* events are emitted

**THEN**
* all records go to the stderr console handler
* stdout is untouched

##### SCENARIO 2: No file or network handlers

**Scenario ID**: ROVER-INFRA-010.2-S2

**GIVEN**
* the logging configuration

**WHEN**
* inspected

**THEN**
* there are no file handlers, sockets, or remote sinks
* no log files are created

##### SCENARIO 3: The formatter is deterministic

**Scenario ID**: ROVER-INFRA-010.2-S3

**GIVEN**
* the same event emitted twice

**WHEN**
* formatted

**THEN**
* the structure and field order are identical (timestamps, if any, are the only varying field)

---

#### ROVER-INFRA-010.3 — Guarantee zero-infra and disable-ability

**AS A** System
**I WANT** logging to be fully disable-able with negligible cost and no persistence
**SO THAT** clean CLI output and the zero-infrastructure constraint are preserved.

**Traceability:** [Ch. 8.5 (can be disabled for clean output)](../../architecture/08-cross-cutting-concepts.md), [Ch. 2.4](../../architecture/02-constraints.md), [Ch. 6.9.3](../../architecture/06-runtime-view.md).

> **Events/notifications are not applicable** to this story; logging is local console output, not an
> event stream (Ch. 4.8.2 / Ch. 8.5).

##### SCENARIO 1: Logging can be fully disabled

**Scenario ID**: ROVER-INFRA-010.3-S1

**GIVEN**
* logging disabled

**WHEN**
* a mission runs

**THEN**
* no log records are produced
* output is identical to the pre-logging baseline

##### SCENARIO 2: Disabled logging is cheap

**Scenario ID**: ROVER-INFRA-010.3-S2

**GIVEN**
* logging disabled and a long valid sequence

**WHEN**
* executed

**THEN**
* there is no measurable formatting/serialization work
* runtime stays within the Ch. 10 performance targets

##### SCENARIO 3: Logging persists nothing

**Scenario ID**: ROVER-INFRA-010.3-S3

**GIVEN**
* any log level and any run

**WHEN**
* the process exits

**THEN**
* no log file or other artifact is written
* all logging state is discarded

---

*Status: 10 core and supporting stories approved. ROVER-STORY-011 to 015 remain in the backlog (outside the scope of this exercise).*
