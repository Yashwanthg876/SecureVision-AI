# SecureVision AI Architecture

## Overview
SecureVision AI is an enterprise-grade cybersecurity analysis platform built to assess website vulnerabilities using a combination of traditional heuristic analysis, Machine Learning, and Generative AI.

## High-Level Architecture
The system follows a modernized layered architecture with clear separation of concerns.

```text
[ Frontend (React/Next.js) ]
          │
      (REST API)
          │
[ Backend (FastAPI) ]
          │
    ├── API Layer (Routers)
    ├── Service Layer (Business Logic)
    ├── Repository Layer (Data Access)
    └── ML/AI Layer (Models & Copilot)
          │
[ SQLite / Database ]
```

## Architectural Principles
1. **Repository Pattern:** The API and Service layers never interact directly with the ORM (SQLAlchemy). All data access is mediated through Repositories (`app/repositories`).
2. **Service-Oriented Business Logic:** Business rules are encapsulated in `app/services`, making them reusable across API endpoints or background jobs.
3. **Unified API Responses:** Every API response adheres to a strict schema containing `success`, `data`, and `meta` (request IDs).
4. **Structured Logging:** All backend logs are emitted as JSON with injected request traceability for enterprise log aggregators (ELK/Splunk).

## Subsystems

### 1. Website Assessment Engine
Orchestrates parallel scans of SSL, DNS, HTTP Headers, and Technologies. Uses heuristic scoring to identify immediate vulnerabilities.

### 2. ML Decision Engine
Built with XGBoost and Random Forest. Analyzes heuristic scores alongside engineered features to output a `Unified Risk Level` and confidence score.

### 3. SHAP Explainability Engine
Examines the XGBoost model to provide mathematical feature importance, explaining *why* an AI decision was made.

### 4. Isolation Forest Anomaly Engine
Unsupervised learning subsystem that detects zero-day attacks or strange behavior configurations that don't fit historical global traffic patterns.

### 5. Security Trend Intelligence Engine
Utilizes LSTM (Long Short-Term Memory) neural networks to forecast a website's future risk trajectory over a 30-day horizon.

### 6. Provider-Agnostic AI Copilot
Converts the mathematical, structured outputs of all the above subsystems into human-readable executive summaries, technical reports, and developer remediation guides. Operates strictly on a structured JSON context to prevent hallucination.
