from sqlalchemy.orm import Session
from app.repositories.leave import LeaveRepository
from app.models import LeaveRequest
from app.schemas import LeaveRequestCreate, LeaveRequestUpdate
from typing import List, Optional


class LeaveService:
    def __init__(self, session: Session):
        self.repo = LeaveRepository(session)

    def apply_leave(self, leave_data: LeaveRequestCreate) -> LeaveRequest:
        """Apply for leave."""
        leave_dict = leave_data.dict()
        return self.repo.create(leave_dict)

    def get_leave(self, leave_id: int) -> Optional[LeaveRequest]:
        """Get leave request."""
        return self.repo.get(leave_id)

    def get_employee_leaves(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
        """Get all leave requests for an employee."""
        return self.repo.get_by_employee(employee_id, skip=skip, limit=limit)

    def get_pending_leaves(self, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
        """Get all pending leave requests."""
        return self.repo.get_pending_leaves(skip=skip, limit=limit)

    def approve_leave(self, leave_id: int) -> Optional[LeaveRequest]:
        """Approve a leave request."""
        return self.repo.update(leave_id, {"status": "approved"})

    def reject_leave(self, leave_id: int) -> Optional[LeaveRequest]:
        """Reject a leave request."""
        return self.repo.update(leave_id, {"status": "rejected"})

    def get_leaves_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
        """Get leaves by status."""
        return self.repo.get_by_status(status, skip=skip, limit=limit)
