# Documentation Templates

## 00-system-overview.md Template

```markdown
# System Overview

## Purpose

Brief description of what the system does and its primary goals.

## Key Features

- Feature 1
- Feature 2
- Feature 3

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | ... |
| Backend | ... |
| Database | ... |
| Infrastructure | ... |

## External Dependencies

| Dependency | Purpose | Type |
|------------|---------|------|
| Service A | Authentication | API |
| Service B | Payment processing | API |

## System Context

```mermaid
C4Context
    title System Context Diagram
    
    Person(user, "User", "Description")
    System(system, "System Name", "Description")
    System_Ext(ext, "External System", "Description")
    
    Rel(user, system, "Uses")
    Rel(system, ext, "Integrates with")
`` `

## Getting Started

Brief instructions for running the system locally.
```

---

## 01-components.md Template

```markdown
# Component Architecture

## Overview

High-level description of the system's component structure.

## Components

### Component A

**Purpose:** What it does

**Responsibilities:**
- Responsibility 1
- Responsibility 2

**Key Files:**
- `path/to/main/file`
- `path/to/config`

### Component B

**Purpose:** What it does

**Responsibilities:**
- Responsibility 1
- Responsibility 2

## Component Diagram

```mermaid
flowchart TD
    subgraph ComponentA
        A1[Module 1]
        A2[Module 2]
    end
    
    subgraph ComponentB
        B1[Module 1]
    end
    
    A1 --> B1
    A2 --> B1
`` `

## Communication Patterns

How components communicate (REST, events, direct calls, etc.)

## Dependencies

| Component | Depends On | Interface |
|-----------|------------|-----------|
| A | B | REST API |
| B | Database | SQL |
```

---

## 02-data-flow.md Template

```markdown
# Data Flow

## Overview

Description of how data flows through the system.

## Request Flow

### User Request Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Service
    participant Database
    
    User->>Frontend: Action
    Frontend->>API: HTTP Request
    API->>Service: Process
    Service->>Database: Query
    Database-->>Service: Result
    Service-->>API: Response
    API-->>Frontend: JSON
    Frontend-->>User: Updated UI
`` `

## Data Transformations

| Stage | Input | Output | Transformation |
|-------|-------|--------|----------------|
| API | HTTP Request | DTO | Validation, parsing |
| Service | DTO | Entity | Business logic |
| Repository | Entity | DB Record | Serialization |

## State Management

How state is managed across the application.

```mermaid
stateDiagram-v2
    [*] --> Initial
    Initial --> Loading: fetch
    Loading --> Ready: success
    Loading --> Error: failure
    Ready --> Loading: refresh
    Error --> Loading: retry
`` `

## Caching Strategy

Description of caching layers and invalidation.
```

---

## modules/<module-name>.md Template

```markdown
# Module: <Module Name>

## Overview

What this module does and why it exists.

## Location

`path/to/module/`

## Public Interface

### Functions/Methods

| Name | Parameters | Returns | Description |
|------|------------|---------|-------------|
| `function1` | `(arg: Type)` | `Result` | What it does |
| `function2` | `(arg: Type)` | `void` | What it does |

### Types/Interfaces

```typescript
interface ExampleType {
    field: string;
    count: number;
}
`` `

## Internal Structure

```mermaid
flowchart TD
    Entry[Entry Point] --> Handler
    Handler --> Validator
    Validator --> Processor
    Processor --> Output
`` `

## Key Flows

### Flow 1: Description

```mermaid
sequenceDiagram
    participant A
    participant B
    participant C
    
    A->>B: Step 1
    B->>C: Step 2
    C-->>A: Result
`` `

## Dependencies

- `dependency-1`: Used for X
- `dependency-2`: Used for Y

## Configuration

| Config Key | Type | Default | Description |
|------------|------|---------|-------------|
| `option1` | string | `"default"` | Description |

## Testing

How to run tests for this module:

```bash
npm test -- path/to/module
`` `
```
