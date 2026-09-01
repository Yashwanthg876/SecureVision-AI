from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.github_scan import GitHubScan


class GitHubScanRepository(BaseRepository[GitHubScan]):
    def __init__(self):
        super().__init__(GitHubScan)

    def get_by_user(self, db: Session, user_id: str, limit: int = 20) -> List[GitHubScan]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_repo(self, db: Session, user_id: str, repo_name: str) -> List[GitHubScan]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.repo_name == repo_name)
            .order_by(self.model.created_at.desc())
            .all()
        )


github_scan_repository = GitHubScanRepository()
