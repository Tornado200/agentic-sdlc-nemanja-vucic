# 8. Cross-cutting Concepts

## 8.1 Error Handling

**Structured error hierarchy** ensures clear diagnostics:
- `ValidationError`: Invalid inputs (commands, positions, grid)
- `BoundaryError`: Movement outside grid bounds
- `ObstacleError`: Movement blocked by terrain obstacle

Errors propagate up through components and are formatted by Command Interface for user presentation. Each failed operation prevents state mutation.

## 8.2 Validation

**Layered validation** occurs at multiple points:
1. **CLI layer**: Argument parsing and format checking
2. **Parser layer**: Command character validation (L/R/M only)
3. **Navigation layer**: Movement validation via Grid Management
4. **Grid layer**: Boundary and obstacle checks

Validation failures stop execution immediately with descriptive messages.

## 8.3 Testing Strategy

**Comprehensive test pyramid** using pytest:
- **Unit tests**: Pure functions (parser, grid logic)
- **Integration tests**: Component interactions
- **Property-based tests**: Random command sequences
- **BDD scenarios**: Given-When-Then specifications

Test isolation via dependency injection enables testing components independently.

## 8.4 State Management

**In-memory state only** with clear lifecycle:
- State initialized per command sequence
- Updated after each valid operation
- Preserved for successful operations when later operations fail
- Lost on program exit (no persistence)

Atomic state updates ensure consistency without rollback mechanisms.

## 8.5 Logging and Observability

**Minimal logging** for development and debugging:
- Error details for diagnostics
- Optional debug output for command execution
- No production telemetry or monitoring
- Console-based logging only

Logging is optional and can be disabled for clean CLI output.

---

*Next: Chapter 9 will document architecture decisions.*
