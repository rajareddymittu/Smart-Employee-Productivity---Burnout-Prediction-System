from sqlalchemy.orm import Session
from app.models import Task
from app.repositories.base import BaseRepository
from typing import List


class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: Session):
        super().__init__(session, Task)

    def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks in a project."""
        return self.get_all_by_filter(skip=skip, limit=limit, project_id=project_id)

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks by status."""
        return self.get_all_by_filter(skip=skip, limit=limit, status=status)

    def get_pending_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all pending tasks."""
        return self.get_by_status('pending', skip=skip, limit=limit)

    def get_by_priority(self, priority: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks by priority."""
        return self.get_all_by_filter(skip=skip, limit=limit, priority=priority)
