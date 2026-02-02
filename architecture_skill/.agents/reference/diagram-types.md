# Mermaid Diagram Types Reference

## C4 Context Diagram (Level 1 - System Overview)

Use for showing system boundaries and external actors.

```mermaid
C4Context
    title System Context Diagram
    
    Person(user, "User", "A user of the system")
    System(system, "System Name", "Core system description")
    System_Ext(ext_api, "External API", "Third-party service")
    System_Ext(ext_db, "External Database", "Shared data store")
    
    Rel(user, system, "Uses")
    Rel(system, ext_api, "Calls", "REST/HTTPS")
    Rel(system, ext_db, "Reads/Writes", "SQL")
```

## C4 Container Diagram (Level 2 - Components)

Use for showing major containers/services within the system.

```mermaid
C4Container
    title Container Diagram
    
    Person(user, "User")
    
    Container_Boundary(system, "System") {
        Container(web, "Web App", "React", "User interface")
        Container(api, "API Server", "Node.js", "REST API")
        Container(worker, "Worker", "Node.js", "Background jobs")
        ContainerDb(db, "Database", "PostgreSQL", "Stores data")
        ContainerQueue(queue, "Message Queue", "Redis", "Job queue")
    }
    
    Rel(user, web, "Uses", "HTTPS")
    Rel(web, api, "Calls", "REST")
    Rel(api, db, "Reads/Writes")
    Rel(api, queue, "Publishes")
    Rel(worker, queue, "Consumes")
    Rel(worker, db, "Reads/Writes")
```

## Flowchart (Components & Data Flow)

Use for showing component relationships or process flows.

```mermaid
flowchart TD
    subgraph Frontend
        A[React App] --> B[State Manager]
    end
    
    subgraph Backend
        C[API Gateway] --> D[Auth Service]
        C --> E[Core Service]
        E --> F[(Database)]
    end
    
    A --> C
    D --> F
```

### Horizontal Layout

```mermaid
flowchart LR
    Input --> Process --> Output
    Process --> Cache[(Cache)]
```

## Sequence Diagram (Module Deep Dives)

Use for showing interaction flows between components.

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web App
    participant A as API
    participant D as Database
    
    U->>W: Click login
    W->>A: POST /auth/login
    A->>D: SELECT user
    D-->>A: User data
    A-->>W: JWT token
    W-->>U: Redirect to dashboard
```

### With Loops and Conditionals

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant DB as Database
    
    C->>S: Request data
    
    alt Cache hit
        S-->>C: Cached response
    else Cache miss
        S->>DB: Query
        DB-->>S: Results
        S-->>C: Fresh response
    end
    
    loop Every 5 seconds
        C->>S: Heartbeat
    end
```

## Class Diagram (Module Structure)

Use for showing class relationships and dependencies.

```mermaid
classDiagram
    class Controller {
        +handleRequest()
        -validate()
    }
    
    class Service {
        +execute()
        -processData()
    }
    
    class Repository {
        +find()
        +save()
        +delete()
    }
    
    Controller --> Service
    Service --> Repository
```

## State Diagram (State Management)

Use for showing state transitions.

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Loading: fetch
    Loading --> Success: data received
    Loading --> Error: request failed
    Success --> Idle: reset
    Error --> Loading: retry
    Error --> Idle: dismiss
```

## Entity Relationship Diagram (Data Models)

Use for showing database schema relationships.

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        int id PK
        string email
        string name
    }
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        int id PK
        int user_id FK
        date created_at
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
    }
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"
    PRODUCT {
        int id PK
        string name
        decimal price
    }
```

## Choosing the Right Diagram

| Documentation Level | Primary Diagram | Alternative |
|---------------------|-----------------|-------------|
| System Overview | C4Context | Flowchart (LR) |
| Components | C4Container | Flowchart (TD) |
| Module Deep Dive | Sequence | Class, State |
| Data Flow | Flowchart | Sequence |
| Data Models | ERDiagram | Class |
