from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.auth.dependencies import require_roles, get_current_user
from app import models

router = APIRouter(prefix="/hr", tags=["hr"], dependencies=[Depends(require_roles(['HR']))])


@router.get('/manager-burnout')
def manager_burnout_stats(db: Session = Depends(get_db)):
    """Return burnout statistics grouped by manager."""
    # join predictions -> employees to find employee.manager_id
    q = (
        db.query(models.Employee.manager_id, func.count(models.Prediction.id).label('pred_count'), func.avg(models.Prediction.burnout_score).label('avg_score'))
        .join(models.Prediction, models.Employee.id == models.Prediction.employee_id)
        .group_by(models.Employee.manager_id)
    )
    rows = q.all()
    results = []
    for mgr_id, cnt, avg in rows:
        # fetch manager info
        mgr = None
        if mgr_id:
            mgr = db.query(models.Employee).filter(models.Employee.id == mgr_id).first()
        results.append({'manager_id': mgr_id, 'manager_name': f"{mgr.first_name} {mgr.last_name}" if mgr else None, 'predictions': cnt, 'avg_burnout_score': float(avg) if avg is not None else None})

    # sort by avg_burnout_score desc
    results_sorted = sorted(results, key=lambda r: (r['avg_burnout_score'] is not None, r['avg_burnout_score']), reverse=True)
    return {'by_manager': results_sorted}


@router.get('/recent-hires')
def recent_hires(q: str = None, limit: int = 50, db: Session = Depends(get_db)):
    """Return recent hires (full employee details) with optional search and latest burnout score."""
    # select employees and eager load department and manager info
    query = db.query(models.Employee)
    if q:
        likeq = f"%{q}%"
        query = query.filter((models.Employee.employee_code.ilike(likeq)) | (models.Employee.first_name.ilike(likeq)) | (models.Employee.last_name.ilike(likeq)))
    query = query.order_by(models.Employee.joining_date.desc().nullslast()).limit(limit)
    employees = query.all()
    # build groups by manager
    groups: dict = {}
    for e in employees:
        # latest prediction
        pred = db.query(models.Prediction).filter(models.Prediction.employee_id == e.id).order_by(models.Prediction.predicted_on.desc()).first()
        burnout_score = float(pred.burnout_score) if pred and pred.burnout_score is not None else None
        exp_val = float(e.experience) if e.experience is not None else None
        if exp_val is not None and exp_val <= 0:
            exp_val = None

        # department name lookup
        dept = None
        if e.department_id:
            d = db.query(models.Department).filter(models.Department.id == e.department_id).first()
            dept = d.name if d else None

        emp_obj = {
            'id': e.id,
            'employee_code': e.employee_code,
            'first_name': e.first_name,
            'last_name': e.last_name,
            'gender': e.gender,
            'dob': e.dob.isoformat() if e.dob else None,
            'department_id': e.department_id,
            'department_name': dept,
            'manager_id': e.manager_id,
            'joining_date': e.joining_date.isoformat() if e.joining_date else None,
            'experience': exp_val,
            'salary_grade': e.salary_grade,
            'status': e.status,
            'created_at': e.created_at.isoformat() if e.created_at else None,
            'burnout_score': burnout_score
        }

        key = e.manager_id or 0
        if key not in groups:
            groups[key] = {'manager_id': e.manager_id, 'manager_name': None, 'employees': []}
        groups[key]['employees'].append(emp_obj)

    # fill manager names
    results = []
    for k, g in groups.items():
        mgr_name = None
        if g['manager_id']:
            mgr = db.query(models.Employee).filter(models.Employee.id == g['manager_id']).first()
            if mgr:
                mgr_name = f"{mgr.first_name} {mgr.last_name}".strip()
        else:
            mgr_name = 'Unassigned'
        results.append({'manager_id': g['manager_id'], 'manager_name': mgr_name, 'employees': g['employees']})

    # sort groups by manager_name
    results_sorted = sorted(results, key=lambda r: (r['manager_name'] or '').lower())
    return {'by_manager': results_sorted}
