import logging
from typing import Any
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.schemas.github_security import GitHubScanRequest, GitHubScanResponse
from app.services.github_security.scanner import github_scanner
from app.repositories.github_scan_repository import github_scan_repository
from app.core.responses import StandardResponse, success_response
from app.core.exceptions import SecureVisionException

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scan", response_model=StandardResponse[GitHubScanResponse])
async def scan_github_repo(
    req: Request,
    body: GitHubScanRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Scan a public GitHub repository for exposed secrets, risky files,
    and dependency manifests. No authentication token needed for public repos.
    """
    user_id = str(current_user.id)
    try:
        result = await github_scanner.scan(body.repo_url, db, user_id)
        logger.info(f"GitHub scan completed for {body.repo_url} by user {user_id}: score={result.security_score}")
        return success_response(result, req.state.request_id)
    except ValueError as ve:
        raise SecureVisionException(str(ve), status_code=400)
    except Exception as e:
        logger.error(f"GitHub scan failed for {body.repo_url}: {e}", exc_info=True)
        raise SecureVisionException("Scan failed due to an unexpected error. Please try again.", status_code=500)


@router.get("/history", response_model=StandardResponse)
async def get_github_scan_history(
    req: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Return the scan history for the current user.
    """
    user_id = str(current_user.id)
    scans = github_scan_repository.get_by_user(db, user_id)
    data = [
        {
            "id": str(s.id),
            "repo_url": s.repo_url,
            "repo_name": s.repo_name,
            "owner": s.owner,
            "risk_level": s.risk_level,
            "security_score": s.security_score,
            "secrets_count": s.secrets_count,
            "critical_count": s.critical_count,
            "high_count": s.high_count,
            "status": s.status,
            "created_at": s.created_at.isoformat() if s.created_at else "",
        }
        for s in scans
    ]
    return success_response({"items": data}, req.state.request_id)
