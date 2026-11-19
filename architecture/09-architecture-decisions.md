# Architecture Decision Records (ADRs)

## ADR-001: Modular Python 3.12 Architecture with In-Memory State

**Status:** Accepted

**Context:**
The Mars Rover kata requires parsing command sequences (turn left, turn
right, move forward), updating rover position and heading on a bounded
grid, and handling boundary or obstacle conditions. The solution must be
easy to test and to evolve across the later course modules (requirements,
CI/CD, TDD/BDD).

**Decision:**
Implement the system in Python 3.12 with a modular structure that
separates command parsing, rover navigation logic, and grid/terrain
state. State is kept in memory, with optional JSON persistence for
mission snapshots.

**Rationale:**
- Python 3.12 fits the course tooling (pytest, ruff, black, isort)
- Separating parser, navigation and grid keeps domain logic isolated
- Isolated domain logic is easy to unit test and cover with BDD scenarios
- In-memory state is the simplest option for a kata, with no infrastructure

**Consequences:**
- State is lost on restart unless a snapshot is saved
- Module boundaries must be maintained as the code grows
- A real database can be added later behind the grid/state module
