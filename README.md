# SecureVision AI

SecureVision AI is a full-stack security assessment platform with website security analysis, GitHub repository scanning, AI-content detection, threat intelligence, reporting, dashboards, and experimental machine-learning pipelines.

## Stack

- Frontend: Next.js 16, React 19, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLAlchemy, SQLite/PostgreSQL
- ML: scikit-learn, XGBoost, Isolation Forest, and an experimental LSTM forecasting pipeline

## Local development

### Backend

```powershell
cd backend
.\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. API documentation is available at http://localhost:8000/docs.

The root `start.ps1` script can also launch both services on Windows.

## Configuration

Production deployments must provide a unique `SECRET_KEY`, enable secure cookies, disable demo login, and configure the production database through environment variables. Local databases, virtual environments, build caches, secrets, and generated model binaries are intentionally excluded from version control.

## Documentation

- [Architecture](ARCHITECTURE.md)
- [Backend](BACKEND.md)
- [API](API.md)
- [ML validation summary](reports/ml_validation/ML_VALIDATION_SUMMARY.md)

