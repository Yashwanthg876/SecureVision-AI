import uuid
from sqlalchemy import Column, String, DateTime, Integer, Text, func, Uuid
from app.database.base_class import Base

class AIDetectionScan(Base):
    __tablename__ = "ai_detection_scans"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    content_snippet = Column(String(512), nullable=False)
    content_type = Column(String(50), nullable=False) # 'text' or 'code'
    ai_probability = Column(Integer, nullable=False)
    risk_level = Column(String(50), nullable=False)
    status = Column(String(50), default="Completed")
    result_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
