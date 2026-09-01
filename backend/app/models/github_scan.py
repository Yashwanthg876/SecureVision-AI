import uuid
import json
from sqlalchemy import Column, String, DateTime, Integer, Text, func, Uuid
from app.database.base_class import Base


class GitHubScan(Base):
    __tablename__ = "github_scans"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    repo_url = Column(String(512), nullable=False)
    repo_name = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    risk_level = Column(String(50), nullable=False)
    security_score = Column(Integer, nullable=False)
    total_files_scanned = Column(Integer, default=0)
    secrets_count = Column(Integer, default=0)
    risky_files_count = Column(Integer, default=0)
    dependency_files_count = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    scan_duration_ms = Column(Integer, default=0)
    status = Column(String(50), default="Completed")
    # Store full result JSON for retrieval
    result_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
