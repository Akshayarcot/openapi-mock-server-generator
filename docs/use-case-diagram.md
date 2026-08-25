# UML Use-Case Diagram Specification

**Project Title:** OpenAPI Mock Server Generator  
**Problem Statement ID:** #41  
**Domain:** Developer Tools & IT Operations  
**Target Stakeholders / Actors:** API Developer, QA Engineer  

---

## 1. Actors Description

| Actor | Type | Description |
| :--- | :--- | :--- |
| **API Developer** | Primary Human Actor | Builds frontend or client services and relies on mock REST endpoints to develop against unreleased or work-in-progress backend APIs without blocking development. |
| **QA Engineer** | Primary Human Actor | Designs automated API test suites, validates boundary conditions, configures latency, tests error resilience (4xx/5xx responses), and verifies contract compliance. |
| **CI/CD Test Runner** | Secondary System Actor | Automated pipeline that spins up ephemeral mock server instances during automated unit, integration, and end-to-end regression test runs. |

---

## 2. UML Use-Case Diagram (Visual Representation)

Below is the rendered UML Use Case Diagram illustrating all actors, primary use cases, system boundaries, and mandatory **«include»** and **«extend»** relationships.

![UML Use Case Diagram](assets/use-case-diagram.svg)

---

## 3. Mermaid UML Use-Case Diagram

```mermaid
flowchart LR
    %% Actors
    subgraph Actors [Actors]
        direction TB
        Dev["fa:fa-user-code API Developer"]
        QA["fa:fa-user-check QA Engineer"]
        CICD["fa:fa-robot CI/CD Test Runner"]
    end

    %% System Boundary
    subgraph SystemBoundary ["OpenAPI Mock Server Generator System"]
        direction TB

        UC1(["UC-01: Ingest OpenAPI Specification"])
        UC2(["UC-02: Parse & Validate OpenAPI Schema"])
        UC3(["UC-03: Generate Dynamic Mock Endpoints"])
        UC4(["UC-04: Process Mock API Request"])
        UC5(["UC-05: Validate Request Schema"])
        UC6(["UC-06: Simulate Configurable Latency"])
        UC7(["UC-07: Emulate HTTP Error Scenarios"])
        UC8(["UC-08: Inspect Server Logs & Metrics"])

        %% Relationships
        UC1 -.->|"«include»"| UC2
        UC3 -.->|"«include»"| UC2
        UC4 -.->|"«include»"| UC5
        
        UC6 -.->|"«extend»"| UC4
        UC7 -.->|"«extend»"| UC4
    end

    %% Actor Associations
    Dev --- UC1
    Dev --- UC3
    Dev --- UC4
    Dev --- UC8

    QA --- UC1
    QA --- UC4
    QA --- UC6
    QA --- UC7
    QA --- UC8

    CICD --- UC1
    CICD --- UC4

    %% Styling
    classDef actorStyle fill:#2d3748,stroke:#4a5568,stroke-width:2px,color:#fff;
    classDef usecaseStyle fill:#ebf8ff,stroke:#3182ce,stroke-width:2px,color:#2b6cb0;
    classDef includeStyle fill:#e6fffa,stroke:#319795,stroke-width:1.5px,color:#234e52;
    classDef extendStyle fill:#fffaf0,stroke:#dd6b20,stroke-width:1.5px,color:#7b341e;

    class Dev,QA,CICD actorStyle;
    class UC1,UC3,UC4,UC8 usecaseStyle;
    class UC2,UC5 includeStyle;
    class UC6,UC7 extendStyle;
```

---

## 4. Stereotype Relationships Explanation

### 1. «include» Relationships (Mandatory Sub-flows)
1. **`UC-01 / UC-03` «include» `UC-02: Parse & Validate OpenAPI Schema`**:
   - **Rationale:** The system cannot generate mock endpoints or register routes without first parsing the OpenAPI YAML/JSON document and validating its syntax and schema rules. Parsing and validation is an unconditional, mandatory sub-flow.
2. **`UC-04: Process Mock API Request` «include» `UC-05: Validate Request Schema`**:
   - **Rationale:** Whenever a client sends an HTTP request to a dynamic mock endpoint, the system unconditionally validates incoming query params, path variables, and body payloads against the defined schema constraints.

### 2. «extend» Relationships (Optional / Conditional Extensions)
1. **`UC-06: Simulate Configurable Latency` «extend» `UC-04: Process Mock API Request`**:
   - **Extension Point:** `Response Latency Injection`
   - **Condition:** Executed only when artificial delay/latency rules (e.g., fixed delay, jitter, rate-throttling) are explicitly configured for the endpoint or mock server instance.
2. **`UC-07: Emulate HTTP Error Scenarios` «extend» `UC-04: Process Mock API Request`**:
   - **Extension Point:** `Fault Injection & Status Overrides`
   - **Condition:** Executed only when the incoming request specifies scenario triggers (e.g., `X-Mock-Status: 500` or `X-Mock-Scenario: ServiceUnavailable`) or when failure probability rules are activated by the QA engineer.

---

## 5. PlantUML Source Code

For reference or generation via PlantUML tools:

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam monochrome false
skinparam actorStyle awesome

actor "API Developer" as dev
actor "QA Engineer" as qa
actor "CI/CD Test Runner" as cicd

rectangle "OpenAPI Mock Server Generator" {
  usecase "UC-01: Ingest OpenAPI Specification" as UC1
  usecase "UC-02: Parse & Validate OpenAPI Schema" as UC2
  usecase "UC-03: Generate Dynamic Mock Endpoints" as UC3
  usecase "UC-04: Process Mock API Request" as UC4
  usecase "UC-05: Validate Request Schema" as UC5
  usecase "UC-06: Simulate Configurable Latency" as UC6
  usecase "UC-07: Emulate HTTP Error Scenarios" as UC7
  usecase "UC-08: Inspect Server Logs & Metrics" as UC8

  ' Include dependencies
  UC1 .> UC2 : <<include>>
  UC3 .> UC2 : <<include>>
  UC4 .> UC5 : <<include>>

  ' Extend dependencies
  UC6 .> UC4 : <<extend>>
  UC7 .> UC4 : <<extend>>
}

dev --> UC1
dev --> UC3
dev --> UC4
dev --> UC8

qa --> UC1
qa --> UC4
qa --> UC6
qa --> UC7
qa --> UC8

cicd --> UC1
cicd --> UC4
@enduml
```
