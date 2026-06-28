# Phase 1: Foundation & Blueprint Architecture

## Multi-Agent Compliance & Transaction Analytics Platform (GuardShield AI)

Welcome to the production-ready architecture blueprint for GuardShield AI — an enterprise-grade, multi-agent financial risk management and compliance auditing platform tailored to the exact specifications of your high-level AI/LLM stack.

## 1. Project Story & Business Blueprint

### Business Problem
Modern global financial institutions (like UBS, JP Morgan, or HSBC) process millions of cross-border transactions and unstructured client communications daily. Compliance teams struggle to detect real-time regulatory violations, insider trading patterns, fraud, and data leaks (PII) using traditional static rulesets. The explosion of Large Language Models (LLMs) within corporate workflows adds a massive attack surface, including prompt injection vulnerabilities, unauthorized tool execution, and compliance drift.

### Business Goals
- **Automate Auditing:** Orchestrate a multi-agent system to parse, verify, and cross-reference structured transactions against unstructured regulatory frameworks (e.g., FINRA, SEC, GDPR).
- **Mitigate AI Risk:** Enforce a hard-line operational guardrail layer preventing PII leaks, toxic generations, and malicious prompt injections before they reach upstream models.
- **Auditability & Observability:** Provide a clear line of sight into agent decisions, execution cost (tokens), latency, and accuracy metrics for institutional compliance reporting.

### Functional Requirements
- **Multi-Agent Coordination:** Separate autonomous agents for intake analysis, regulatory cross-referencing, and final risk scoring.
- **Adaptive Memory Management:** Contextual long-term and short-term memory persistence across user interactions and transaction workflows.
- **Deterministic Evaluation Gates:** Every agent payload must pass through automated evaluation criteria (eval scores) acting as production quality gates.

### Non-Functional Requirements
- **Latency:** Critical path guardrail checks must execute in < 200 ms.
- **Security:** Full zero-trust data handling with PII masking, automated OAuth2/OIDC validation, and tool invocation safety boundaries.
- **Scalability:** Horizontal scaling via decoupled async task workers handling high-throughput chunking, indexing, and vector processing.

## 2. System Architecture & Component Mapping
The system utilizes Clean Architecture principles to cleanly separate technical frameworks (FastAPI, AutoGen, Pydantic AI) from the underlying core financial compliance business rules.

## System Sequence Flow
```text
[Client / API Gateway]       [FastAPI Security Layer]       [Guardrail Engine]       [Multi-Agent Router]       [Vector DB / Mem0]
          |                             |                           |                         |                         |
          |---- 1. Submit Request ----->|                           |                         |                         |
          |      (OIDC / JWT Token)     |---- 2. Inspect Policy --->|                         |                         |
          |                             |        & Check Injection  |                         |                         |
          |                             |<--- 3. Clean Payload -----|                         |                         |
          |                             |                                                     |                         |
          |                             |---------------- 4. Route to Orchestrator ---------->|                         |
          |                             |                                                     |--- 5. Fetch Memory ---->|
          |                             |                                                     |<-- 6. Context & Rules --|
          |                             |                                                     |                         |
          |                             |                                                     |--- 7. Execute Tools --->|
          |                             |<--------------- 8. Return Validated Audit ----------|                         |
```
3. Enterprise Repository Workspace
Below is the complete corporate directory structure designed for modular development, isolated container targets, and scalable deployment orchestrations.

guardshield-ai/
│
├── .github/
│   └── workflows/
│       ├── build-test.yml
│       └── cd-deploy.yml
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agents.py
│   │   │   │   ├── compliance.py
│   │   │   │   └── auth.py
│   │   │   └── middleware/
│   │   │       ├── telemetry.py
│   │   │       └── guardrails.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── exceptions.py
│   │   │   └── logging.py
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py
│   │   │   ├── compliance_agent.py
│   │   │   └── risk_agent.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── rag_engine.py
│   │   │   ├── memory_manager.py
│   │   │   └── evaluation.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── audit_repo.py
│   │   │   └── mock_repo.py
│   │   │
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── domain.py
│   │       └── schemas.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── migrations/
│
├── docker/
│   ├── docker-compose.yml
│   └── redis.conf
│
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   └── ingress.yaml
│
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_guardrails.py
│   └── test_api.py
│
└── README.md

### Repository Directory Breakdown
- backend/app/api/: Holds all controller routers, HTTP endpoints, and foundational API request-response patterns.

- backend/app/api/middleware/: Intercepts raw incoming payloads for immediate OpenTelemetry tracking, performance profile compilation, and prompt injection analysis.

- backend/app/agents/: Encapsulates the execution configurations, system persona prompts, and tools bound to Pydantic AI and AutoGen.

- backend/app/services/: Core logic engines for running RAG operations, fetching short-to-long term memories via Mem0/Redis, and evaluating processing criteria.

- backend/app/repositories/: Isolates data store queries behind the Repository Pattern, letting engineers instantly toggle mock memory structures when primary databases are offline.


### 4. Foundational Orchestration Environment
To initialize the platform baseline, we establish our dependency maps and configure the core configuration loader utilizing validation typing rules.

backend/requirements.txt

fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.6.0
pydantic-ai>=0.0.18
autogen-agentchat>=0.2.0
langfuse>=2.20.0
mem0ai>=0.1.5
redis>=5.0.0
chromadb>=0.4.24
opentelemetry-api>=1.23.0
opentelemetry-sdk>=1.23.0
opentelemetry-instrumentation-fastapi>=0.44b0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.9
asyncpg>=0.29.0
sqlalchemy[asyncio]>=2.0.28