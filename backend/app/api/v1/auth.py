import logging
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, ForgotPassword
from app.services.auth import get_current_user, auth_service
from app.core.responses import StandardResponse, success_response, error_response
from app.core.exceptions import SecureVisionException
from app.core.security import get_password_hash
import uuid
import secrets

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=StandardResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def register(request: Request, user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    """
    Create new user.
    """
    user = auth_service.register(db, user_in)
    logger.info(f"New user registered: {user.email}")
    return success_response(user, request.state.request_id)

@router.post("/login", response_model=StandardResponse)
def login(
    request: Request,
    response: Response,
    user_in: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    and set it as an HTTP-only secure cookie.
    """
    access_token = auth_service.login(db, user_in)
    
    # We fallback to basic cookie settings from config if available, otherwise defaults
    secure_cookie = getattr(settings, "COOKIE_SECURE", False)
    samesite_cookie = getattr(settings, "COOKIE_SAMESITE", "lax")
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=secure_cookie,
        samesite=samesite_cookie,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    logger.info("User logged in successfully")
    return success_response({"message": "Login successful"}, request.state.request_id)

@router.post("/demo-login", response_model=StandardResponse)
def demo_login(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> Any:
    """Create a real session for the local demo account in development only."""
    if not settings.ENABLE_DEMO_LOGIN or settings.ENVIRONMENT.lower() == "production":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    demo_user = db.query(User).filter(User.email == settings.DEMO_USER_EMAIL).first()
    if not demo_user:
        demo_user = User(
            email=settings.DEMO_USER_EMAIL,
            full_name="SecureVision Demo",
            organization="Demo Workspace",
            role="Demo User",
            password_hash=get_password_hash(secrets.token_urlsafe(32)),
        )
        db.add(demo_user)
        try:
            db.commit()
            db.refresh(demo_user)
        except Exception:
            db.rollback()
            demo_user = db.query(User).filter(User.email == settings.DEMO_USER_EMAIL).first()
            if not demo_user:
                raise SecureVisionException("Demo account could not be initialized.", status_code=500)

    access_token = auth_service.create_user_access_token(demo_user)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return success_response({"message": "Demo login successful"}, request.state.request_id)

@router.post("/logout", response_model=StandardResponse)
def logout(request: Request, response: Response) -> Any:
    """
    Logout user by clearing the access token cookie.
    """
    secure_cookie = getattr(settings, "COOKIE_SECURE", False)
    samesite_cookie = getattr(settings, "COOKIE_SAMESITE", "lax")
    
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=secure_cookie,
        samesite=samesite_cookie
    )
    return success_response({"message": "Logout successful"}, request.state.request_id)

@router.post("/forgot-password", response_model=StandardResponse)
def forgot_password(
    request: Request,
    data: ForgotPassword,
    db: Session = Depends(get_db)
) -> Any:
    """
    Password Recovery. Mocks sending an email.
    """
    auth_service.process_forgot_password(db, data.email)
    
    return success_response({"message": "If that email exists in our system, we have sent a password reset link."}, request.state.request_id)

from app.schemas.user import UserCreate, UserLogin, UserResponse, ForgotPassword, UserUpdate

@router.get("/me", response_model=StandardResponse[UserResponse])
def read_current_user(
    request: Request,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return success_response(current_user, request.state.request_id)

@router.put("/me", response_model=StandardResponse[UserResponse])
def update_current_user(
    request: Request,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update profile details for current user.
    """
    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name
    if user_in.organization is not None:
        current_user.organization = user_in.organization
    if user_in.email is not None and user_in.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_in.email).first()
        if existing_user:
            raise SecureVisionException("The user with this email already exists in the system.", status_code=400)
        current_user.email = user_in.email
    db.commit()
    db.refresh(current_user)
    return success_response(current_user, request.state.request_id)
