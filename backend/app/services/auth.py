import logging
from typing import Optional
from datetime import timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import TokenPayload
from app.schemas.user import UserCreate, UserLogin, ForgotPassword
from app.repositories.user_repository import user_repository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import SecureVisionException
import uuid

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

logger = logging.getLogger(__name__)

def get_token_from_request(request: Request) -> Optional[str]:
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header
    if not token:
        return None
    return token.replace("Bearer ", "").strip()

def get_current_user(
    request: Request, db: Session = Depends(get_db)
) -> User:
    token = get_token_from_request(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        user_uuid = uuid.UUID(token_data.sub) if isinstance(token_data.sub, str) else token_data.sub
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user

def get_optional_user(
    request: Request, db: Session = Depends(get_db)
) -> Optional[User]:
    try:
        token = get_token_from_request(request)
        if token:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            user_uuid = uuid.UUID(token_data.sub) if isinstance(token_data.sub, str) else token_data.sub
            user = db.query(User).filter(User.id == user_uuid).first()
            if user:
                return user
    except (JWTError, ValueError):
        return None
    return None

class AuthService:
    def create_user_access_token(self, user: User) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(str(user.id), expires_delta=access_token_expires)

    def register(self, db: Session, user_in: UserCreate) -> dict:
        user = user_repository.get_by_email(db, user_in.email)
        if user:
            raise SecureVisionException("The user with this email already exists in the system.", status_code=400)
        
        hashed_password = get_password_hash(user_in.password)
        user_data = {
            "email": user_in.email,
            "full_name": user_in.full_name,
            "organization": user_in.organization,
            "password_hash": hashed_password
        }
        
        user = user_repository.create(db, obj_in=user_data)
        return user

    def login(self, db: Session, user_in: UserLogin) -> str:
        user = user_repository.get_by_email(db, user_in.email)
        if not user or not verify_password(user_in.password, user.password_hash):
            raise SecureVisionException("Incorrect email or password", status_code=400)
        
        return self.create_user_access_token(user)

    def process_forgot_password(self, db: Session, email: str) -> str:
        user = user_repository.get_by_email(db, email)
        if user:
            reset_token = str(uuid.uuid4())
            logger.info(f"[MOCK EMAIL] Password reset requested for {email}. Token: {reset_token}")
            return reset_token
        else:
            logger.info(f"Password reset requested for non-existent email: {email}")
            return None

auth_service = AuthService()
