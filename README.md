# OpenAPI Mock Server Generator

[![Domain: Developer Tools & IT Operations](https://img.shields.io/badge/Domain-Developer%20Tools%20%26%20IT%20Operations-blue.svg)](#)
[![PES University - Dept. of CSE](https://img.shields.io/badge/PES%20University-Lab%201%3A%20Requirements%20%26%20UML-orange.svg)](#)
[![OpenAPI 3.0 Supported](https://img.shields.io/badge/OpenAPI-3.0-green.svg)](#)

> **Problem Statement #41 | Developer Tools & IT Operations**  
> **Course:** Software Engineering Lab 1 - Requirements Engineering & UML Use-Case Modelling  
> **Target Stakeholders / Actors:** `API Developer`, `QA Engineer`  

---

## 1. Problem Context & Overview

Modern software development requires frontend developers, backend developers, and QA engineers to work concurrently. However, client-side engineering and test automation are frequently blocked when backend APIs are still under development or unstable. 

The **OpenAPI Mock Server Generator** is a high-performance developer productivity tool that:
1. **Ingests OpenAPI 3.0 specifications** (in YAML and JSON formats).
2. **Generates dynamic, schema-compliant mock REST endpoints** with realistic randomized data payloads.
3. **Validates incoming client requests** against defined parameter and payload schemas.
4. **Simulates configurable response latency and network jitter** to test client resilience and timeout handling.
5. **Emulates edge-case error scenarios and status code overrides** (e.g., 400, 404, 500) for robust automated QA testing.

---

## 2. Complete Requirements Table

### 2.1 Functional Requirements (FR-001 to FR-005)

| Requirement ID | Requirement Type | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-001** | Functional (Specification Ingestion) | The system shall parse and validate OpenAPI 3.0 (YAML and JSON) specification files, extracting paths, HTTP methods, request parameters, request bodies, and response schemas to dynamically construct mock routing endpoints. | **High** | **Pass:** Valid OpenAPI 3.0 YAML/JSON file is successfully parsed and all defined routes are registered into the mock server routing table.<br>**Fail:** Malformed file or unsupported specification versions are rejected with explicit line-number validation error messages. | Ingestion and validation of OpenAPI specifications form the fundamental core of the tool, allowing automatic route generation without manual coding. |
| **FR-002** | Functional (Dynamic Mocking) | The system shall generate dynamic, randomized, schema-compliant JSON payloads for mock endpoints corresponding to response schemas, enums, data types, formats (e.g., `uuid`, `date-time`, `email`), and nested object hierarchies. | **High** | **Pass:** Mock endpoint returns HTTP 200/201 responses matching the expected response schema structure and realistic randomized field values.<br>**Fail:** Response payload violates defined schema types, misses required fields, or returns empty/null unformatted bodies. | Enables frontend and API developers to develop and test against realistic backend API responses before backend service implementation is complete. |
| **FR-003** | Functional (Request Validation) | The system shall validate incoming HTTP request payloads, path variables, query parameters, and headers against the OpenAPI 3.0 specification rules (e.g., required fields, type constraints, pattern regex). | **High** | **Pass:** Requests failing schema constraints are rejected with HTTP 400 Bad Request and detailed schema validation errors; valid requests proceed to mock response generation.<br>**Fail:** Request containing invalid data types or missing required fields is processed without validation. | Empowers QA engineers and developers to test client-side error handling and verify that client requests strictly adhere to API contracts. |
| **FR-004** | Functional (Latency Simulation) | The system shall allow users to configure simulated response latency per endpoint, globally, or with jitter (e.g., fixed delay of 250 ms, or normal distribution between 100 ms and 500 ms) to emulate real-world network and backend performance conditions. | **Medium** | **Pass:** Mock endpoint response delivery time matches the configured latency parameter within a tolerance of ±10 ms.<br>**Fail:** Mock response returns immediately ignoring configured delay rules, or introduces uncontrollable overhead (>50 ms deviation). | Crucial for QA engineers and developers to test client-side timeout handling, loading indicators, race conditions, and degraded network resilience. |
| **FR-005** | Functional (Scenario & State Management) | The system shall support stateful mock scenarios and dynamic response switching based on custom request headers (e.g., `X-Mock-Status: 404`, `X-Mock-Scenario: payment_failed`) or query parameters to return predefined edge-case responses. | **Medium** | **Pass:** Request specifying `X-Mock-Status: 500` returns the defined 500 error schema and status code.<br>**Fail:** Header-based scenario trigger is ignored and default 200 OK mock response is returned instead. | Allows QA engineers to automate edge-case test suites, simulate backend server failures, and test recovery workflows without altering mock server code. |

---

### 2.2 Non-Functional Requirements (NFR-001 & NFR-002)

| Requirement ID | Requirement Type | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NFR-001** | Performance & Scalability | The mock server engine must sustain a minimum throughput of 1,000 mock API requests per second with simulated latency accuracy within ±10 ms under concurrent multi-client load. | **High** | **Pass:** Automated load benchmarking (e.g., via k6 or wrk) verifies ≥1,000 req/sec sustained throughput with <5 ms internal processing overhead at 99th percentile.<br>**Fail:** Throughput drops below 1,000 req/sec or engine processing latency exceeds 25 ms under peak load. | Ensures the mock server can be utilized effectively in CI/CD automated test pipelines and performance regression environments without becoming a bottleneck. |
| **NFR-002** | Security & Reliability | The system must sanitize all ingested OpenAPI specification files to prevent XML External Entity (XXE), YAML deserialization, and Server-Side Request Forgery (SSRF) vulnerabilities, maintaining 99.9% uptime during active test sessions. | **High** | **Pass:** Security audit scans confirm zero arbitrary code execution or unsafe deserialization vulnerabilities when parsing untrusted external spec files.<br>**Fail:** System executes malicious embedded YAML anchors, crashes, or leaks local file system paths upon parsing hostile input. | Mock servers frequently ingest external and third-party specifications, requiring strict security boundaries to protect local developer workstations and shared test servers. |

---

## 3. UML Use-Case Diagram

### 3.1 Visual Diagram
![UML Use-Case Diagram](docs/assets/use-case-diagram.svg)

### 3.2 Diagram Structure & Stereotype Relationships
The UML diagram models interactions between the primary human actors (**API Developer**, **QA Engineer**) and the secondary system actor (**CI/CD Test Runner**) within the **OpenAPI Mock Server Generator System** boundary:

- **`«include»` Relationships:**
  - `UC-01 (Ingest OpenAPI Spec)` and `UC-03 (Generate Dynamic Mock Endpoints)` **«include»** `UC-02 (Parse & Validate OpenAPI Schema)`.
  - `UC-04 (Process Mock API Request)` **«include»** `UC-05 (Validate Request Schema)`.
- **`«extend»` Relationships:**
  - `UC-06 (Simulate Configurable Latency)` **«extend»** `UC-04 (Process Mock API Request)` at extension point *Latency Injection*.
  - `UC-07 (Emulate HTTP Error Scenarios)` **«extend»** `UC-04 (Process Mock API Request)` at extension point *Fault Injection / Header Overrides*.

---

## 4. Use-Case Flow Specification (UC-01)

### Summary Table for Core Use Case: UC-01
- **Use Case Name:** Ingest OpenAPI Specification and Generate Dynamic Mock Server
- **Primary Actors:** API Developer, QA Engineer
- **Preconditions:** Valid or draft OpenAPI 3.0 specification file (`.yaml` / `.json`) available; target port is free.
- **Postconditions:** Mock HTTP server running and listening on target port; dynamic schema-compliant routes registered.
- **Main Success Scenario:**
  1. Actor supplies OpenAPI specification file and configuration parameters (port, latency).
  2. System parses and validates the specification syntax and structure (**«include» UC-02**).
  3. System dynamically constructs HTTP endpoints with randomized data synthesizers.
  4. System registers latency simulation middlewares (**«extend» UC-04**).
  5. System opens network port and outputs live route URLs to terminal.
  6. Client sends request to mock endpoint and receives validated schema-compliant JSON response with configured delay.
- **Alternate Flows:**
  - **AF-1 (Remote URL Ingestion):** Specification ingested from remote HTTPS URL with safety sanitization.
  - **AF-2 (Scenario-Based Fault Injection):** Client provides `X-Mock-Status: 500` header triggering **«extend» UC-05** to return mock error payload.
- **Exception Flows:**
  - **EF-1 (Invalid Spec):** Syntax/schema errors displayed with line numbers; server stops cleanly.
  - **EF-2 (Port Conflict):** Port in use error returned; instructs user to pick alternate port.

*(For the complete 1-page use-case flow document, see [`docs/use-case-specification.md`](docs/use-case-specification.md).)*

---

## 5. Repository Structure

```
.
├── README.md                          # Master project and Lab 1 submission document
├── docs/
│   ├── requirements-table.md          # Complete 5 FRs and 2 NFRs specification
│   ├── use-case-diagram.md            # Detailed UML diagram notes, Mermaid, & PlantUML
│   ├── use-case-specification.md      # Formal 1-page core use case flow specification
│   └── assets/
│       └── use-case-diagram.svg       # High-resolution vector UML diagram graphic
├── examples/
│   └── petstore-openapi.yaml          # Sample OpenAPI 3.0 spec for testing & demonstration
└── .gitignore
```

---

## 6. Author & Course Info
- **Student Name / GitHub:** [@Akshayarcot](https://github.com/Akshayarcot)
- **Repository:** [`Akshayarcot/openapi-mock-server-generator`](https://github.com/Akshayarcot/openapi-mock-server-generator)
- **Institution:** PES University - Department of Computer Science & Engineering
- **Course Lab:** Lab 1: Requirements Engineering & UML Use-Case Modelling
