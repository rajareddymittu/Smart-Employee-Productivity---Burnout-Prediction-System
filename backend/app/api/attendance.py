from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.attendance import AttendanceService
from app.schemas import AttendanceCreate, AttendanceUpdate, AttendanceOut
from app.auth.dependencies import get_current_active_user
from typing import List
from datetime import datetime, date

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/checkin", response_model=AttendanceOut, status_code=201)
def check_in(employee_id: int, db: Session = Depends(get_db)):
    """Record employee check-in."""
    service = AttendanceService(db)
    try:
        attendance = service.check_in(employee_id, datetime.now())
        return attendance
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/checkout", response_model=AttendanceOut)
def check_out(employee_id: int, db: Session = Depends(get_db)):
    """Record employee check-out."""
    service = AttendanceService(db)
    attendance = service.check_out(employee_id, datetime.now())
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance


@router.get("/{attendance_id}", response_model=AttendanceOut)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    """Get attendance record."""
    service = AttendanceService(db)
    attendance = service.get_attendance(attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance


@router.get("/employee/{employee_id}", response_model=List[AttendanceOut])
def get_employee_attendance(
    employee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get attendance records for an employee."""
    service = AttendanceService(db)
    attendance = service.get_employee_attendance(employee_id, skip=skip, limit=limit)
    return attendance


@router.get("/employee/{employee_id}/range", response_model=List[AttendanceOut])
def get_attendance_range(
    employee_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Get attendance records between dates."""
    service = AttendanceService(db)
    attendance = service.get_attendance_between_dates(employee_id, start_date, end_date)
    return attendance


@router.put("/{attendance_id}", response_model=AttendanceOut)
def update_attendance(
    attendance_id: int,
    att_in: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    """Update attendance record."""
    service = AttendanceService(db)
    attendance = service.update_attendance(attendance_id, att_in)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance
