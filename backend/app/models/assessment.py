import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, func, Text, JSON, Uuid
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    target_url = Column(String, nullable=False)
    domain = Column(String, nullable=False, index=True)
    assessment_type = Column(String, default="Passive", nullable=False)
    
    overall_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False) # e.g., Critical, High, Medium, Low
    
    # Sub-scores for analytics
    ssl_score = Column(Integer, nullable=False, default=100)
    headers_score = Column(Integer, nullable=False, default=100)
    dns_score = Column(Integer, nullable=False, default=100)
    tech_score = Column(Integer, nullable=False, default=100)
    
    # Precomputed analytics
    recommendation_count = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    
    scan_duration = Column(Integer, nullable=False) # milliseconds
    status = Column(String, default="Completed", nullable=False)
    engine_version = Column(String, default="1.0", nullable=False)
    
    # Telemetry JSON
    ssl_details = Column(JSON, nullable=True)
    headers_details = Column(JSON, nullable=True)
    dns_details = Column(JSON, nullable=True)
    whois_details = Column(JSON, nullable=True)
    technology_details = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False, index=True)

    # Relationships
    user = relationship("User", backref="assessments")
    findings = relationship("AssessmentFinding", back_populates="assessment", cascade="all, delete-orphan")

class AssessmentFinding(Base):
    __tablename__ = "assessment_findings"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    assessment_id = Column(Uuid, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    
    category = Column(String, nullable=False) # SSL, Headers, DNS, Tech
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False) # Critical, High, Medium, Low
    recommendation = Column(Text, nullable=False)
    reference = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    assessment = relationship("Assessment", back_populates="findings")
