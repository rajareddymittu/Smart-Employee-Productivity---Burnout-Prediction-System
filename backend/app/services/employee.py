from sqlalchemy.orm import Session
from app.repositories.employee import EmployeeRepository
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate
from typing import List, Optional


class EmployeeService:
    def __init__(self, session: Session):
        self.repo = EmployeeRepository(session)

    def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        """Create a new employee."""
        employee_dict = employee_data.dict()
        return self.repo.create(employee_dict)

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        """Get employee by ID."""
        return self.repo.get(employee_id)

    def get_all_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all employees."""
        return self.repo.get_all(skip=skip, limit=limit)

    def update_employee(self, employee_id: int, employee_data: EmployeeUpdate) -> Optional[Employee]:
        """Update employee."""
        update_dict = employee_data.dict(exclude_unset=True)
        return self.repo.update(employee_id, update_dict)

    def delete_employee(self, employee_id: int) -> bool:
        """Delete employee."""
        return self.repo.delete(employee_id)

    def get_employees_by_department(self, department_id: int, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get employees in a department."""
        return self.repo.get_by_department(department_id, skip=skip, limit=limit)

    def get_active_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all active employees."""
        return self.repo.get_active_employees(skip=skip, limit=limit)
