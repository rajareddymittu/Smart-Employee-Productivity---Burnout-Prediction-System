from sqlalchemy.orm import Session
from app.repositories.project import ProjectRepository
from app.models import Project
from app.schemas import ProjectCreate, ProjectUpdate
from typing import List, Optional


class ProjectService:
    def __init__(self, session: Session):
        self.repo = ProjectRepository(session)

    def create_project(self, project_data: ProjectCreate) -> Project:
        """Create a new project."""
        project_dict = project_data.dict()
        return self.repo.create(project_dict)

    def get_project(self, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        return self.repo.get(project_id)

    def get_all_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all projects."""
        return self.repo.get_all(skip=skip, limit=limit)

    def update_project(self, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """Update project."""
        update_dict = project_data.dict(exclude_unset=True)
        return self.repo.update(project_id, update_dict)

    def delete_project(self, project_id: int) -> bool:
        """Delete project."""
        return self.repo.delete(project_id)

    def get_active_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all active projects."""
        return self.repo.get_active_projects(skip=skip, limit=limit)
