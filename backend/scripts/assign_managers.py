from app.database.session import SessionLocal
from app import models

def assign_managers():
    db = SessionLocal()
    try:
        # find existing managers by convention (employee_code starting with 'MGR')
        managers = db.query(models.Employee).filter(models.Employee.employee_code.ilike('MGR%')).all()

        # if none found, create two manager placeholders
        if not managers:
            m1 = models.Employee(employee_code='MGR001', first_name='Manager', last_name='One', status='active')
            m2 = models.Employee(employee_code='MGR002', first_name='Manager', last_name='Two', status='active')
            db.add_all([m1, m2])
            db.commit()
            db.refresh(m1)
            db.refresh(m2)
            managers = [m1, m2]

        mgr_ids = [m.id for m in managers]
        print(f'Found/created managers: {[(m.id,m.employee_code) for m in managers]}')

        # select employees without manager
        employees = db.query(models.Employee).filter(models.Employee.manager_id == None).all()
        to_assign = [e for e in employees if e.id not in mgr_ids]
        print(f'Employees without manager (excluding managers themselves): {len(to_assign)}')

        updated = 0
        for idx, emp in enumerate(to_assign):
            mgr_id = mgr_ids[idx % len(mgr_ids)]
            emp.manager_id = mgr_id
            db.add(emp)
            updated += 1

        if updated:
            db.commit()

        print(f'Assigned manager_id to {updated} employees (round-robin).')
    finally:
        db.close()


if __name__ == '__main__':
    assign_managers()
