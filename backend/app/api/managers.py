from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.auth.dependencies import get_current_user, require_roles
from app import models
from app.schemas import EmployeeOut

router = APIRouter(prefix="/managers", tags=["managers"])


@router.get("/{manager_id}/reportees", response_model=List[EmployeeOut], dependencies=[Depends(get_current_user)])
def get_reportees(manager_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Only HR can view any manager's reportees. Managers may view only their own reportees.
    roles = [r.name for r in current_user.roles]
    if 'HR' in roles:
        pass
    elif 'Manager' in roles:
        # manager may only view their own reportees
        if current_user.employee_id != manager_id:
            raise HTTPException(status_code=403, detail='Not authorized to view other manager reportees')
    else:
        raise HTTPException(status_code=403, detail='Not authorized to view reportees')

    employees = db.query(models.Employee).filter(models.Employee.manager_id == manager_id).all()
    return employees
