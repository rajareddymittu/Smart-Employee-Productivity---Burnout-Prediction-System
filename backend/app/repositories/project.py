from sqlalchemy.orm import Session
from app.models import Project
from app.repositories.base import BaseRepository
from typing import List


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: Session):
        super().__init__(session, Project)

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects by status."""
        return self.get_all_by_filter(skip=skip, limit=limit, status=status)

    def get_active_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all active projects."""
        return self.get_by_status('active', skip=skip, limit=limit)
