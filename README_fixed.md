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
