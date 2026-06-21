from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.leave import LeaveService
from app.schemas import LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestOut
from app.auth.dependencies import get_current_active_user
from typing import List

router = APIRouter(
    prefix="/leaves",
    tags=["leaves"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/", response_model=LeaveRequestOut, status_code=201)
def apply_leave(leave_in: LeaveRequestCreate, db: Session = Depends(get_db)):
    """Apply for leave."""
    service = LeaveService(db)
    try:
        leave = service.apply_leave(leave_in)
        return leave
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{leave_id}", response_model=LeaveRequestOut)
def get_leave(leave_id: int, db: Session = Depends(get_db)):
    """Get leave request."""
    service = LeaveService(db)
    leave = service.get_leave(leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave


@router.get("/employee/{employee_id}", response_model=List[LeaveRequestOut])
def get_employee_leaves(
    employee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get leave requests for an employee."""
    service = LeaveService(db)
    leaves = service.get_employee_leaves(employee_id, skip=skip, limit=limit)
    return leaves


@router.get("/pending", response_model=List[LeaveRequestOut])
def get_pending_leaves(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all pending leave requests."""
    service = LeaveService(db)
    leaves = service.get_pending_leaves(skip=skip, limit=limit)
    return leaves


@router.put("/{leave_id}/approve", response_model=LeaveRequestOut)
def approve_leave(leave_id: int, db: Session = Depends(get_db)):
    """Approve a leave request."""
    service = LeaveService(db)
    leave = service.approve_leave(leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave


@router.put("/{leave_id}/reject", response_model=LeaveRequestOut)
def reject_leave(leave_id: int, db: Session = Depends(get_db)):
    """Reject a leave request."""
    service = LeaveService(db)
    leave = service.reject_leave(leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave


@router.get("/status/{status}", response_model=List[LeaveRequestOut])
def get_leaves_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get leaves by status."""
    service = LeaveService(db)
    leaves = service.get_leaves_by_status(status, skip=skip, limit=limit)
    return leaves
