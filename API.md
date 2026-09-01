# API Documentation

## Base URL
`http://localhost:8000/api/v1`

## Standard Response Format
All API responses follow a unified JSON schema, regardless of success or failure.

### Success Response
```json
{
  "success": true,
  "data": {
    "key": "value"
  },
  "error": null,
  "meta": {
    "timestamp": "2026-08-11T12:00:00Z",
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "version": "1.0.0"
  }
}
```

### Error Response
```json
{
  "success": false,
  "data": null,
  "error": "Assessment with ID 123 not found.",
  "meta": {
    "timestamp": "2026-08-11T12:01:00Z",
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "version": "1.0.0"
  }
}
```

## Core Endpoints Overview

### Health & Auth
- `GET /health` : System health & status check
- `POST /auth/register` : User registration
- `POST /auth/login` : Authenticate user & set secure HTTP-only access token cookie
- `POST /auth/logout` : Clear access token cookie
- `GET /auth/me` : Read current authenticated user profile

### Dashboard Aggregation
- `GET /dashboard/summary` : High-level security KPIs (Score, Websites, GitHub Repos, AI Threats)
- `GET /dashboard/threat-trend` : Daily threat trend data for line charts
- `GET /dashboard/risk-distribution` : Risk breakdown data for donut charts
- `GET /dashboard/recent-activity` : Chronological activity log stream
- `GET /dashboard/critical-findings` : Top priority findings requiring attention

### Website Security Engine
- `POST /assessment/scan` : Run full passive security scan on target domain
- `GET /assessment/history` : Get user assessment scan history
- `GET /assessment/{id}` : Get assessment details with SHAP feature explainability

### GitHub Security Scanner
- `POST /github/scan` : Scan public/private GitHub repository for secrets, SAST, and dependencies
- `GET /github/history` : Get user repository scan history

### AI Detection Engine
- `POST /ai-detection/scan` : Analyze text or code for AI signatures, perplexity, and burstiness
- `GET /ai-detection/history` : Get user AI content scan history

### Threat Intelligence Subsystem
- `GET /threat-intel/feed` : Paginated & filterable active Indicators of Compromise (IOCs)
- `POST /threat-intel/lookup` : Instant reputation lookup for IP, Domain, Hash, URL, or CVE ID
- `GET /threat-intel/stats` : Threat category metrics and top threat vectors

### Reports & Compliance Subsystem
- `GET /reports` : List user security assessment reports available for export
- `POST /reports/generate` : Trigger custom report export
- `GET /reports/{id}/pdf` : Stream formatted PDF Security Assessment Report
- `GET /reports/{id}/csv` : Stream CSV findings spreadsheet
- `GET /reports/{id}/json` : Stream raw JSON assessment payload
