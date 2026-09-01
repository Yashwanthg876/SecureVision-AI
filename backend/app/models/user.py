import uuid
from sqlalchemy import Column, String, DateTime, func, Uuid
from app.database.base_class import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    full_name = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="User", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
