# 2. Architecture Constraints

## 2.1 Technical Constraints

| Constraint | Description | Impact |
|------------|-------------|--------|
| **Python 3.12** | Development must use Python 3.12 as specified in pyproject.toml | Code must be compatible with Python 3.12 syntax and features |
| **In-Memory State** | State persistence is initially in-memory only (per ADR-001) | No database dependencies; state lost on restart unless saved explicitly |
| **Minimal Dependencies** | External packages limited to testing and code quality tools | Core logic must be self-contained with minimal external dependencies |
| **Pytest for Testing** | Unit and integration testing framework is pytest | Test structure and assertions must follow pytest conventions |
| **Code Quality Tools** | Must work with ruff, black, and isort as configured | Code must be formatted to pass linting and formatting checks |

## 2.2 Development Process Constraints

| Constraint | Description | Impact |
|------------|-------------|--------|
| **Agentic SDLC Context** | System serves as demonstration for software factory agents | Architecture must be amenable to automated analysis and generation |
| **Modular Structure** | Must separate parsing, domain logic, and state (per ADR-001) | Clear module boundaries with defined interfaces between components |
| **Test-Driven Development** | Must support TDD/BDD workflows | Domain logic must be isolated and pure for comprehensive testing |
| **Evolutionary Design** | System must evolve through course modules | Architecture must accommodate incremental addition of features |

## 2.3 Interface Constraints

| Constraint | Description | Impact |
|------------|-------------|--------|
| **CLI Interface** | Primary interface is command-line | Input parsing must handle CLI arguments and command sequences |
| **Simple Data Formats** | Input/output uses plain text or JSON | No complex serialization formats required |
| **Stateless Operation** | Each command sequence is independent | System can process commands without maintaining session state between invocations |

## 2.4 Deployment Constraints

| Constraint | Description | Impact |
|------------|-------------|--------|
| **Local Execution Only** | Initial deployment is local Python environment | No cloud or container orchestration requirements |
| **Zero Infrastructure** | No external services (database, message queue, etc.) | All functionality must be self-contained |
| **Development Focus** | System is for educational demonstration | Production scalability and high availability are not required |

## 2.5 Organizational Constraints

| Constraint | Description | Impact |
|------------|-------------|--------|
| **Course Timeline** | Development occurs across multiple modules | Architecture must support incremental implementation |
| **Educational Focus** | Primary goal is teaching agentic SDLC concepts | Implementation must illustrate software factory principles |
| **Individual Kata** | Final project is individual demonstration | Architecture must be comprehensible and maintainable by a single developer |

## 2.6 Quality Attribute Constraints

| Constraint | Description | Impact |
|------------|-------------|--------|
| **Testability** | Domain logic must be isolated for unit testing | Pure functions with minimal side effects required |
| **Simplicity** | Architecture must be minimal and understandable | Avoid over-engineering; prefer simplest solution |
| **Maintainability** | Code must be readable and well-documented | Clear naming, consistent patterns, and comprehensive documentation |
| **Extensibility** | Must support future features (obstacles, multi-rover, etc.) | Design patterns that accommodate new requirements without major refactoring |
