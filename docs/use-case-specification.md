# Use-Case Flow Specification

**Project:** OpenAPI Mock Server Generator  
**Problem Statement ID:** #41  
**Domain:** Developer Tools & IT Operations  

---

## Use Case Specification: UC-01 Ingest OpenAPI Spec & Generate Dynamic Mock Server

| Field | Description |
| :--- | :--- |
| **Use Case ID** | **UC-01** |
| **Use Case Name** | Ingest OpenAPI Specification and Generate Dynamic Mock Server |
| **Primary Actor** | **API Developer** / **QA Engineer** |
| **Secondary Actor(s)** | CI/CD Automated Test Runner |
| **Scope** | OpenAPI Mock Server Generator System |
| **Level** | User-Goal Level |
| **Trigger** | The actor executes the CLI command or submits an OpenAPI 3.0 specification file via the web/REST interface to start a mock server instance. |

---

### 1. Description
The actor provides an OpenAPI 3.0 YAML or JSON specification file (or remote URL) along with optional configuration parameters (e.g., port number, simulated network latency, response generation strategies). The system validates the specification syntax and semantics, generates dynamic HTTP mock REST routes with schema-compliant payload generators, applies latency simulation rules, and starts a running HTTP mock server ready to serve client requests.

---

### 2. Preconditions
1. The actor has a valid or draft OpenAPI 3.0 specification file (in `.yaml`, `.yml`, or `.json` format) accessible locally or via URL.
2. The required network port (default: `8080` or user-specified) is available on the host machine.
3. System dependencies and runtime environment are initialized.

---

### 3. Postconditions
- **Success End Condition:**
  - The OpenAPI specification is verified and parsed successfully.
  - Dynamic mock HTTP routes for all declared paths and HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`) are registered and listening.
  - The mock server logs endpoint URLs, simulated latency profiles, and ready state to the console.
  - Active endpoints respond to HTTP client requests with schema-validated randomized payloads and simulated latency.
- **Failure End Condition:**
  - The mock server is not started, network ports are freed, and descriptive error messages with line-number diagnostics are returned to the actor.

---

### 4. Main Success Scenario (Basic Flow)

| Step | Actor Action | System Response |
| :---: | :--- | :--- |
| **1** | The Actor initiates the mock server by providing an OpenAPI 3.0 specification file path (e.g., `mock-gen start --spec ./petstore.yaml --port 8080 --latency 200ms`). | The system receives the CLI command, validates input arguments, and loads the specification file from disk/URI. |
| **2** | *(Include: Parse & Validate Specification)* | The system executes **«include» UC-02 (Parse & Validate OpenAPI Spec)**, verifying schema syntax compliance against the OpenAPI 3.0 standard. |
| **3** | | The system parses all paths, HTTP methods, request bodies, query/header parameters, and response definitions into an internal memory route table. |
| **4** | | The system synthesizes dynamic response generators for each endpoint that dynamically produce schema-compliant JSON data matching defined primitive types, enums, regex patterns, and nested data structures. |
| **5** | *(Extend: Configure Latency Simulation)* | If latency flags were provided, the system executes **«extend» UC-04 (Configure Simulated Latency)**, attaching artificial delay timers to each endpoint handler. |
| **6** | | The system binds to the specified network port (e.g., `http://localhost:8080`), starts the HTTP server listener, and outputs an interactive routing table and access URLs to stdout. |
| **7** | The Actor (or client app) sends an HTTP request to a generated mock endpoint (e.g., `GET http://localhost:8080/pets/123`). | The system receives the request, matches the route, validates path/query parameters, applies the 200 ms latency simulation, and returns an HTTP 200 OK response with a schema-compliant JSON payload. |

---

### 5. Alternate Flows

#### Alternate Flow 5a: Remote Specification URL Ingestion
- **5a.1:** In Step 1, the actor specifies a remote HTTP/HTTPS URL instead of a local file path (e.g., `--spec https://api.example.com/openapi.json`).
- **5a.2:** The system fetches the specification over HTTPS with strict timeout (10s) and SSRF safety checks.
- **5a.3:** The flow resumes at Step 2.

#### Alternate Flow 5b: Scenario-Based Error Code Emulation (`«extend» UC-05`)
- **5b.1:** In Step 7, the actor passes a mock override header (e.g., `X-Mock-Status: 404` or `X-Mock-Scenario: PetNotFound`).
- **5b.2:** The system triggers **«extend» UC-05 (Emulate HTTP Error Scenarios)**, bypassing the default 200 OK mock response and returning the designated 404 error schema defined in the OpenAPI spec.
- **5b.3:** The flow terminates with the mock error response sent to the actor.

---

### 6. Exception Flows

#### Exception Flow 6a: Malformed or Invalid OpenAPI Specification
- **6a.1:** At Step 2, the specification parser detects invalid YAML/JSON syntax or violations of the OpenAPI 3.0 specification.
- **6a.2:** The system halts server startup, formats a comprehensive error log displaying exact file line numbers and violated constraints, and outputs it to stderr with exit code `1`.
- **6a.3:** The use case terminates in failure.

#### Exception Flow 6b: Port Conflict / Network Address In Use
- **6b.1:** At Step 6, the system attempts to bind to the requested port, but the OS reports `EADDRINUSE`.
- **6b.2:** The system outputs an error message: `"Error: Port 8080 is already in use. Specify a different port using --port <number>"`.
- **6b.3:** The use case terminates in failure without crashing existing host processes.

---

### 7. Special Requirements & Non-Functional Constraints
- **Performance:** Dynamic schema mock generation overhead must not exceed 5 ms per request.
- **Throughput:** Server must maintain $\ge 1,000$ concurrent requests/sec without memory leaks.
- **Precision:** Configured artificial latency must be accurate within $\pm 10$ ms.
- **Security:** Strict YAML parser sandboxing to prevent unsafe code execution or entity expansion attacks.
