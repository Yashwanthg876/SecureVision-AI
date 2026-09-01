import uuid
from typing import List, Optional, Tuple, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.repositories.base_repository import BaseRepository
from app.models.assessment import Assessment, AssessmentFinding
from app.models.user import User

def _resolve_user_uuid(db: Session, user_id: Any) -> Optional[uuid.UUID]:
    if isinstance(user_id, uuid.UUID):
        return user_id
    if isinstance(user_id, str) and user_id:
        try:
            return uuid.UUID(user_id)
        except Exception:
            pass
    return None

def _resolve_uuid(val: Any) -> Optional[uuid.UUID]:
    if isinstance(val, uuid.UUID):
        return val
    if isinstance(val, str) and val:
        try:
            return uuid.UUID(val)
        except Exception:
            pass
    return None

class AssessmentRepository(BaseRepository[Assessment]):
    """
    Data access layer for Assessment and AssessmentFinding entities.
    """
    def __init__(self):
        super().__init__(Assessment)

    def get_user_assessments(self, db: Session, user_id: Any, domain: str = None, risk_level: str = None, status: str = None) -> List[Assessment]:
        resolved_uuid = _resolve_user_uuid(db, user_id)
        if resolved_uuid is None:
            return []
        query = db.query(self.model).filter(self.model.is_deleted == False)
        query = query.filter(self.model.user_id == resolved_uuid)
        
        if domain:
            query = query.filter(self.model.domain == domain)
        if risk_level:
            query = query.filter(self.model.risk_level == risk_level)
        if status:
            query = query.filter(self.model.status == status)
            
        return query.order_by(desc(self.model.created_at)).all()
        
    def get_timeline(self, db: Session, user_id: Any) -> List[Assessment]:
        resolved_uuid = _resolve_user_uuid(db, user_id)
        if resolved_uuid is None:
            return []
        query = db.query(self.model).filter(self.model.is_deleted == False)
        query = query.filter(self.model.user_id == resolved_uuid)
        return query.order_by(self.model.created_at).all()
        
    def get_latest_two_by_domain(self, db: Session, user_id: Any, domain: str) -> List[Assessment]:
        resolved_uuid = _resolve_user_uuid(db, user_id)
        if resolved_uuid is None:
            return []
        query = db.query(self.model).filter(
            self.model.domain == domain,
            self.model.is_deleted == False
        )
        query = query.filter(self.model.user_id == resolved_uuid)
        return query.order_by(desc(self.model.created_at)).limit(2).all()
        
    def get_findings_by_assessment_id(self, db: Session, assessment_id: Any) -> List[AssessmentFinding]:
        resolved_id = _resolve_uuid(assessment_id) or assessment_id
        return db.query(AssessmentFinding).filter(
            AssessmentFinding.assessment_id == resolved_id
        ).all()
        
    def save_assessment_with_findings(self, db: Session, assessment: Assessment, findings: List[AssessmentFinding]) -> Assessment:
        try:
            db.add(assessment)
            db.flush() # flush to get the ID for relationships
            for f in findings:
                f.assessment_id = assessment.id
                db.add(f)
            db.commit()
            db.refresh(assessment)
            return assessment
        except Exception:
            db.rollback()
            raise

# Singleton instance
assessment_repository = AssessmentRepository()
