from sqlalchemy.orm import Session
from app.repositories.attendance import AttendanceRepository
from app.models import Attendance
from app.schemas import AttendanceCreate, AttendanceUpdate
from datetime import date
from typing import List, Optional


class AttendanceService:
    def __init__(self, session: Session):
        self.repo = AttendanceRepository(session)

    def check_in(self, employee_id: int, check_in_time) -> Attendance:
        """Record employee check-in."""
        attendance_dict = {
            "employee_id": employee_id,
            "date": date.today(),
            "check_in": check_in_time
        }
        return self.repo.create(attendance_dict)

    def check_out(self, employee_id: int, check_out_time) -> Optional[Attendance]:
        """Record employee check-out."""
        attendance = self.repo.get_by_employee_and_date(employee_id, date.today())
        if attendance:
            return self.repo.update(attendance.id, {"check_out": check_out_time})
        return None

    def get_attendance(self, attendance_id: int) -> Optional[Attendance]:
        """Get attendance record."""
        return self.repo.get(attendance_id)

    def get_employee_attendance(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[Attendance]:
        """Get all attendance records for an employee."""
        return self.repo.get_by_employee(employee_id, skip=skip, limit=limit)

    def get_attendance_between_dates(self, employee_id: int, start_date: date, end_date: date) -> List[Attendance]:
        """Get attendance records between dates."""
        return self.repo.get_between_dates(employee_id, start_date, end_date)

    def update_attendance(self, attendance_id: int, attendance_data: AttendanceUpdate) -> Optional[Attendance]:
        """Update attendance record."""
        update_dict = attendance_data.dict(exclude_unset=True)
        return self.repo.update(attendance_id, update_dict)
