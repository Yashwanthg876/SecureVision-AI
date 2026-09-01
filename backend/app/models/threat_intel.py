import uuid
from sqlalchemy import Column, String, DateTime, Float, Text, func, Uuid
from app.database.base_class import Base

class ThreatIOC(Base):
    __tablename__ = "threat_iocs"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    ioc_value = Column(String(255), nullable=False, index=True)
    ioc_type = Column(String(50), nullable=False, index=True) # 'ip', 'domain', 'hash', 'url', 'cve'
    threat_type = Column(String(100), nullable=False, index=True) # e.g., 'Ransomware', 'Phishing', 'Botnet', 'Malware', 'Zero-Day'
    severity = Column(String(50), nullable=False, index=True) # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    confidence_score = Column(Float, nullable=False, default=85.0)
    source = Column(String(150), nullable=False, default="SecureVision AI Feed")
    target_sector = Column(String(150), nullable=False, default="Cross-Sector Infrastructure")
    description = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="ACTIVE") # 'ACTIVE', 'MITIGATED', 'INVESTIGATING'
    country_code = Column(String(10), nullable=True, default="US")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
