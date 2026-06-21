from app.database.session import SessionLocal
from app import models
from app.api.auth import get_password_hash

def seed(username: str = 'demo', email: str = 'demo@example.com', password: str = 'DemoPass123!'):
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter((models.User.username == username) | (models.User.email == email)).first()
        if existing:
            print(f"User already exists: {existing.username} <{existing.email}>")
            return existing.username, existing.email, None
        user = models.User(username=username, email=email, password_hash=get_password_hash(password))
        # ensure basic roles exist
        for rname in ('Employee','Manager','HR'):
            role = db.query(models.Role).filter(models.Role.name == rname).first()
            if not role:
                role = models.Role(name=rname)
                db.add(role)
        db.commit()
        # attach Employee role to demo
        emp_role = db.query(models.Role).filter(models.Role.name == 'Employee').first()
        user.roles.append(emp_role)
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Created user:")
        print("  username:", username)
        print("  email:   ", email)
        print("  password:", password)
        # Also create a manager and HR user with linked employee records
        # create manager employee
        mgr_emp = models.Employee(employee_code='MGR001', first_name='Alice', last_name='Manager')
        db.add(mgr_emp)
        db.commit()
        db.refresh(mgr_emp)
        mgr_user = models.User(username='manager', email='manager@example.com', password_hash=get_password_hash('ManagerPass1'))
        mgr_role = db.query(models.Role).filter(models.Role.name == 'Manager').first()
        mgr_user.roles.append(mgr_role)
        mgr_user.employee_id = mgr_emp.id
        db.add(mgr_user)

        # create HR user
        hr_emp = models.Employee(employee_code='HR001', first_name='Helen', last_name='HR')
        db.add(hr_emp)
        db.commit()
        db.refresh(hr_emp)
        hr_user = models.User(username='hr', email='hr@example.com', password_hash=get_password_hash('HRPass1'))
        hr_role = db.query(models.Role).filter(models.Role.name == 'HR').first()
        hr_user.roles.append(hr_role)
        hr_user.employee_id = hr_emp.id
        db.add(hr_user)

        # create two employees reporting to manager
        e1 = models.Employee(employee_code='EMP_M1_001', first_name='Bob', last_name='Report', manager_id=mgr_emp.id)
        e2 = models.Employee(employee_code='EMP_M1_002', first_name='Carol', last_name='Report', manager_id=mgr_emp.id)
        db.add_all([e1,e2])
        db.commit()

        # create user accounts for those employees
        u1 = models.User(username='bob', email='bob@example.com', password_hash=get_password_hash('BobPass1'))
        u1.roles.append(emp_role)
        u1.employee_id = e1.id
        u2 = models.User(username='carol', email='carol@example.com', password_hash=get_password_hash('CarolPass1'))
        u2.roles.append(emp_role)
        u2.employee_id = e2.id
        db.add_all([u1,u2])
        db.commit()
        print('Seeded demo, manager, hr, and two sample employees with users')
        return username, email, password
    finally:
        db.close()


if __name__ == '__main__':
    seed()
