from sqlalchemy.orm import Session
from app.models import LeaveRequest
from app.repositories.base import BaseRepository
from typing import List


class LeaveRepository(BaseRepository[LeaveRequest]):
    def __init__(self, session: Session):
        super().__init__(session, LeaveRequest)

    def get_by_employee(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
        """Get all leave requests for an employee."""
        return self.get_all_by_filter(skip=skip, limit=limit, employee_id=employee_id)

    def get_pending_leaves(self, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
        """Get all pending leave requests."""
        return self.get_all_by_filter(skip=skip, limit=limit, status='pending')

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
        """Get leave requests by status."""
        return self.get_all_by_filter(skip=skip, limit=limit, status=status)

    def get_by_employee_and_status(self, employee_id: int, status: str, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
        """Get leave requests for an employee with specific status."""
        return self.session.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status == status
        ).offset(skip).limit(limit).all()
