from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.auth.dependencies import get_current_user, require_roles
from app import models
from app.schemas import WorkLogCreate, WorkLogOut

router = APIRouter(prefix="/worklogs", tags=["worklogs"])


@router.post("/", response_model=WorkLogOut)
def create_worklog(payload: WorkLogCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Employees can log their own worklogs; managers/HR can create for others
    user_roles = [r.name for r in current_user.roles]
    if 'Employee' in user_roles and current_user.employee_id != payload.employee_id and 'Manager' not in user_roles and 'HR' not in user_roles:
        raise HTTPException(status_code=403, detail='Employees can only create their own worklogs')

    work = models.WorkLog(
        employee_id=payload.employee_id,
        date=payload.date,
        working_hours=payload.working_hours or 0,
        meeting_hours=payload.meeting_hours or 0,
        task_count=payload.task_count or 0,
        task_completion_percent=payload.task_completion_percent or 0
    )
    db.add(work)
    db.commit()
    db.refresh(work)
    return work


@router.get("/employee/{employee_id}", response_model=List[WorkLogOut])
def get_employee_worklogs(employee_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user_roles = [r.name for r in current_user.roles]
    # allow if requesting own logs
    if 'HR' in user_roles:
        pass
    elif 'Manager' in user_roles:
        # check manager relationship
        emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
        if not emp or emp.manager_id != current_user.employee_id:
            raise HTTPException(status_code=403, detail='Manager can only view their reportees')
    else:
        # employee
        if current_user.employee_id != employee_id:
            raise HTTPException(status_code=403, detail='Can only view own worklogs')

    logs = db.query(models.WorkLog).filter(models.WorkLog.employee_id == employee_id).order_by(models.WorkLog.date.desc()).all()
    return logs
