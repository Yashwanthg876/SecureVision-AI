# Backend Developer Guide

## Core Technologies
- **Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **Configuration:** Pydantic Settings
- **Machine Learning:** scikit-learn, XGBoost, PyTorch (LSTM)
- **Generative AI:** Provider-Agnostic LLM Interface (Gemini Default)

## Directory Structure
- `app/api/v1/`: FastAPI routers. Should contain no business logic.
- `app/core/`: Application-wide configurations, structured logging, middleware, and exception handlers.
- `app/database/`: Database connection and Base models.
- `app/models/`: SQLAlchemy ORM definitions.
- `app/repositories/`: Data Access Layer implementing the Repository Pattern.
- `app/schemas/`: Pydantic validation models.
- `app/services/`: Core business logic and orchestration.
- `app/ml/`: Machine Learning models, pipelines, and training scripts.
- `app/ai/`: Generative AI Copilot framework and prompts.

## Adding a New Endpoint
1. Define the input/output schemas in `app/schemas/`.
2. If new tables are needed, create the ORM in `app/models/` and a corresponding Repository in `app/repositories/`.
3. Create the business logic in `app/services/`.
4. Expose the route in `app/api/v1/` and inject the necessary Service/Repository.
5. Ensure the route returns a `StandardResponse` wrapped via `success_response` or `error_response`.

## Error Handling
Do not raise raw `HTTPException`. Define domain-specific exceptions in `app/core/exceptions.py` (inheriting from `SecureVisionException`). The global exception handler will automatically catch these and format them into the standard JSON response structure.
