from typing import List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.ai_detection_scan import AIDetectionScan

class AIDetectionRepository(BaseRepository[AIDetectionScan]):
    def __init__(self):
        super().__init__(AIDetectionScan)

    def get_by_user(self, db: Session, user_id: str, limit: int = 20) -> List[AIDetectionScan]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .all()
        )

ai_detection_repository = AIDetectionRepository()
