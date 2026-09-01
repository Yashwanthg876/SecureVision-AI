import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.database.database import engine
from app.database.base import Base
from app.core.middleware import EnterpriseMiddleware
from app.core.exceptions import global_exception_handler
from app.core.logger import setup_logger

logger = setup_logger("main")

# Note: In a real production app, we use Alembic for migrations instead of create_all
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)

# Middleware
app.add_middleware(EnterpriseMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API v{settings.VERSION}"}
