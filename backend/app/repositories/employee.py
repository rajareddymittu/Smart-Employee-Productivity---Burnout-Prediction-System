from sqlalchemy.orm import Session
from app.models import Employee
from app.repositories.base import BaseRepository
from datetime import date
from typing import List, Optional


class EmployeeRepository(BaseRepository[Employee]):
    def __init__(self, session: Session):
        super().__init__(session, Employee)

    def get_by_employee_code(self, employee_code: str) -> Optional[Employee]:
        """Get employee by employee code."""
        return self.get_by_filter(employee_code=employee_code)

    def get_by_department(self, department_id: int, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all employees in a department."""
        return self.get_all_by_filter(skip=skip, limit=limit, department_id=department_id)

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get employees by status."""
        return self.get_all_by_filter(skip=skip, limit=limit, status=status)

    def get_active_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all active employees."""
        return self.get_by_status('active', skip=skip, limit=limit)
