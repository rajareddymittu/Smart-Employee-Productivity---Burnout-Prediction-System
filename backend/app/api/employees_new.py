from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.employee import EmployeeService
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut
from app.auth.dependencies import get_current_active_user, require_roles
from app import models as _models
from typing import List

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/", response_model=EmployeeOut, status_code=201)
def create_employee(emp_in: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee."""
    service = EmployeeService(db)
    try:
        employee = service.create_employee(emp_in)
        return employee
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[EmployeeOut])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: _models.User = Depends(require_roles(["HR"]))
):
    """Get all employees (HR-only)."""
    service = EmployeeService(db)
    employees = service.get_all_employees(skip=skip, limit=limit)
    return employees


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get employee by ID."""
    service = EmployeeService(db)
    employee = service.get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(
    employee_id: int,
    emp_in: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    """Update employee."""
    service = EmployeeService(db)
    employee = service.update_employee(employee_id, emp_in)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete employee."""
    service = EmployeeService(db)
    success = service.delete_employee(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None


@router.get("/department/{department_id}", response_model=List[EmployeeOut])
def get_employees_by_department(
    department_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get employees in a department."""
    service = EmployeeService(db)
    employees = service.get_employees_by_department(department_id, skip=skip, limit=limit)
    return employees


@router.get("/status/active", response_model=List[EmployeeOut])
def get_active_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all active employees."""
    service = EmployeeService(db)
    employees = service.get_active_employees(skip=skip, limit=limit)
    return employees
