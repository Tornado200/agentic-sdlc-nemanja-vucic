# 12. Glossary

| Term | Definition |
|------|------------|
| **Rover** | Robotic vehicle navigating Martian grid. Tracks position (x,y) and heading (N,S,E,W). |
| **Heading** | Rover orientation: North (N), South (S), East (E), West (W). |
| **Grid** | Rectangular coordinate system defined by width and height (e.g., 5×5). |
| **Obstacle** | Grid coordinate where rover movement is blocked. Initial requirement. |
| **Command Sequence** | String of L (left), R (right), M (move) operations (e.g., "LMLMLMLMM"). |
| **Bounded Context** | Clear responsibility boundary between modules (parser, navigation, grid, state). |
| **ADR** | Architecture Decision Record. Documents key decisions with rationale and consequences. |
| **arc42** | Template for software architecture documentation (this document). |
| **C4 Model** | Context, Container, Component, Code abstraction levels for architecture diagrams. |
| **Modular Monolith** | Single executable with internal module boundaries. This system's pattern. |
| **CLI** | Command-Line Interface. Primary user interaction via `argparse`. |
| **Mission State** | In-memory tracking of rover position and heading during command execution. |
| **ValidationError** | Error type for invalid inputs (commands, positions, grid dimensions). |
| **BoundaryError** | Error type for movement outside grid bounds. |
| **ObstacleError** | Error type for movement blocked by terrain obstacle. |

---

**Documentation Complete:** All 12 arc42 chapters have been created for the Mars Rover Software Architecture.
