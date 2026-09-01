from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.database import get_db
from app.core.responses import StandardResponse, success_response, error_response
import time

router = APIRouter()

@router.get("/health", response_model=StandardResponse)
async def check_health(db: Session = Depends(get_db)):
    """
    Enterprise health check endpoint.
    Verifies DB connection and returns service status.
    """
    start_time = time.time()
    try:
        # Simple query to check db connectivity
        db.execute(text("SELECT 1"))
        latency = round((time.time() - start_time) * 1000, 2)
        
        return success_response({
            "status": "healthy",
            "database": "connected",
            "latency_ms": latency
        })
    except Exception as e:
        return error_response({
            "status": "degraded",
            "database": "disconnected",
            "error": str(e)
        })
