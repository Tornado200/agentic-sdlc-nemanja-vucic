# 3. System Scope and Context

## 3.1 Business Context

The Mars Rover system serves as the demonstration kata for an **Agentic Software Development Lifecycle (SDLC)** course. It provides a concrete implementation target for software factory agents that automate various development disciplines:

- **Git workflow agent** - Manages version control and branching strategies
- **arc42 architecture design agent** - Designs and documents system architecture
- **User story requirements agent** - Derives requirements from business needs
- **CI/CD deployment pipeline agent** - Automates testing and deployment
- **TDD/BDD multi-agent test system** - Generates and executes comprehensive tests

## 3.2 System Scope

### 3.2.1 Core Functionality
- **Command Parsing**: Accept and validate command sequences (L, R, M)
- **Rover Navigation**: Update position and heading based on commands
- **Grid Management**: Enforce boundaries of rectangular Martian grid
- **Obstacle Handling**: Detect obstacles and prevent movement into blocked cells
- **Status Reporting**: Return current position, heading, and mission status

### 3.2.2 External Interfaces
- **CLI Interface**: Accept commands via command-line arguments
- **API Interface** (future): REST/HTTP endpoint for remote control
- **Telemetry Output**: Position updates and mission logs
- **File I/O**: Load/save mission configurations and snapshots

### 3.2.3 Excluded Functionality
- Physical rover hardware control systems
- Real-time sensor data processing
- Multi-rover coordination (initial version)
- Advanced path planning algorithms
- Production-grade persistence layers
- Graphical user interfaces

## 3.3 System Context Diagram

The system interacts with several external actors and systems:

```plantuml
@startuml c4-context
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

title Mars Rover - System Context Diagram

Person(operator, "Mission Operator", "Sends command sequences (e.g., L, R, M) and monitors rover position and mission status.")
Person(student, "Course Student", "Implements and extends the system as part of agentic SDLC coursework.")
System(mars_rover, "Mars Rover System", "Parses movement commands, manages orientation and grid coordinates, and tracks terrain/mission state.")
System_Ext(telemetry_sim, "Ground Control & Telemetry", "External mission control interface or terrain simulation environment receiving status reports.")
System_Ext(software_factory, "Software Factory Agents", "Automated agents that analyze, test, and evolve the rover system.")

Rel(operator, mars_rover, "Sends command sequences and queries status", "CLI / API")
Rel(mars_rover, telemetry_sim, "Publishes position updates and mission logs", "Telemetry / Events")
Rel(student, mars_rover, "Develops, tests, and extends", "Development Environment")
Rel(software_factory, mars_rover, "Analyzes, generates tests, and validates", "Automated SDLC Tools")

@enduml
```

*Diagram file: [./diagrams/c4-context.puml](./diagrams/c4-context.puml)*

## 3.4 Key External Entities

### 3.4.1 Mission Operator
- **Role**: Controls the rover during mission execution
- **Interactions**:
  - Sends command sequences (e.g., "LMLMLMLMM")
  - Queries current position and heading
  - Receives obstacle detection reports
- **Interface**: CLI commands or API calls

### 3.4.2 Course Student
- **Role**: Implements and learns from the system
- **Interactions**:
  - Writes and modifies rover code
  - Runs tests and validates behavior
  - Extends functionality through course modules
- **Interface**: Development environment (IDE, terminal)

### 3.4.3 Software Factory Agents
- **Role**: Automated SDLC tools that work with the system
- **Interactions**:
  - Architecture agent analyzes and documents design
  - Test agent generates and executes BDD scenarios
  - CI/CD agent builds and validates deployments
  - Requirements agent derives user stories
- **Interface**: Code analysis, test execution, build pipelines

### 3.4.4 Ground Control & Telemetry
- **Role**: External monitoring and simulation systems
- **Interactions**:
  - Receives position updates and mission status
  - Simulates Martian terrain conditions
  - Provides mission planning context
- **Interface**: Telemetry data streams, event publishing

## 3.5 System Responsibilities

| Responsibility | Description | Criticality |
|----------------|-------------|-------------|
| **Command Validation** | Ensure command sequences contain only valid characters (L, R, M) | High |
| **Position Tracking** | Maintain accurate x, y coordinates and heading (N, S, E, W) | High |
| **Boundary Enforcement** | Prevent movement beyond grid boundaries (0,0) to (width,height) | High |
| **Obstacle Detection** | Stop and report when movement blocked by obstacle | Medium |
| **Error Reporting** | Provide clear error messages for invalid operations | Medium |
| **State Persistence** | Support saving/loading mission state (optional) | Low |

## 3.6 Technology Context

### 3.6.1 Development Stack
- **Language**: Python 3.12
- **Testing**: pytest for unit and integration tests
- **Quality**: ruff (linting), black (formatting), isort (import sorting)
- **Build**: Standard Python packaging (pyproject.toml)

### 3.6.2 Runtime Environment
- **Execution**: Local Python interpreter
- **State Storage**: In-memory with optional JSON file persistence
- **Dependencies**: Minimal external libraries
- **Deployment**: Local development environment

### 3.6.3 Integration Points
- **CLI Interface**: Command-line argument parsing
- **File I/O**: JSON configuration and state files
- **Testing Framework**: pytest integration hooks
- **Code Analysis**: AST parsing for software factory agents
