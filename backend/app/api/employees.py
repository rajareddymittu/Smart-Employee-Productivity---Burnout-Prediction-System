from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app import models
from app.schemas import EmployeeCreate, EmployeeOut
from app.auth.dependencies import get_current_user, require_roles
from app import models as _models

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=EmployeeOut)
def create_employee(emp_in: EmployeeCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Employee).filter(models.Employee.employee_code == emp_in.employee_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee code already exists")
    emp = models.Employee(employee_code=emp_in.employee_code, first_name=emp_in.first_name, last_name=emp_in.last_name)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


@router.get("/", response_model=list[EmployeeOut])
def list_employees(db: Session = Depends(get_db), current_user: _models.User = Depends(require_roles(["HR"]))):
    items = db.query(models.Employee).limit(100).all()
    return items


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp
