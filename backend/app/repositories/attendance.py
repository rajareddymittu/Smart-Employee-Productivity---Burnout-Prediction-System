from sqlalchemy.orm import Session
from app.models import Attendance
from app.repositories.base import BaseRepository
from datetime import date
from typing import List


class AttendanceRepository(BaseRepository[Attendance]):
    def __init__(self, session: Session):
        super().__init__(session, Attendance)

    def get_by_employee_and_date(self, employee_id: int, date_: date) -> Attendance:
        """Get attendance record by employee and date."""
        return self.get_by_filter(employee_id=employee_id, date=date_)

    def get_by_employee(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[Attendance]:
        """Get all attendance records for an employee."""
        return self.get_all_by_filter(skip=skip, limit=limit, employee_id=employee_id)

    def get_between_dates(self, employee_id: int, start_date: date, end_date: date) -> List[Attendance]:
        """Get attendance records between dates."""
        return self.session.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).all()
