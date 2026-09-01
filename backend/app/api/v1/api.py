from fastapi import APIRouter
from app.api.v1 import auth, dashboard, assessment, reports, health, github, ai_detection, threat_intel

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["assessment"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(github.router, prefix="/github", tags=["github"])
api_router.include_router(ai_detection.router, prefix="/ai-detection", tags=["ai-detection"])
api_router.include_router(threat_intel.router, prefix="/threat-intel", tags=["threat-intel"])

