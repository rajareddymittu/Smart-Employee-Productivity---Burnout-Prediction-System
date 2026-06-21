from sqlalchemy.orm import Session
from app.repositories.task import TaskRepository
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from typing import List, Optional


class TaskService:
    def __init__(self, session: Session):
        self.repo = TaskRepository(session)

    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task."""
        task_dict = task_data.dict()
        return self.repo.create(task_dict)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return self.repo.get(task_id)

    def get_all_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks."""
        return self.repo.get_all(skip=skip, limit=limit)

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update task."""
        update_dict = task_data.dict(exclude_unset=True)
        return self.repo.update(task_id, update_dict)

    def delete_task(self, task_id: int) -> bool:
        """Delete task."""
        return self.repo.delete(task_id)

    def get_tasks_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks in a project."""
        return self.repo.get_by_project(project_id, skip=skip, limit=limit)

    def get_tasks_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks by status."""
        return self.repo.get_by_status(status, skip=skip, limit=limit)

    def get_pending_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all pending tasks."""
        return self.repo.get_pending_tasks(skip=skip, limit=limit)
