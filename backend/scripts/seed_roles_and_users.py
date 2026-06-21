#!/usr/bin/env python
from app.database.session import SessionLocal
from app import models
from passlib.context import CryptContext

# use local password hasher to avoid importing app.api.auth (which imports schemas)
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def ensure():
    db = SessionLocal()
    try:
        # ensure roles
        for rname in ('Employee', 'Manager', 'HR'):
            role = db.query(models.Role).filter(models.Role.name == rname).first()
            if not role:
                role = models.Role(name=rname)
                db.add(role)
        db.commit()

        emp_role = db.query(models.Role).filter(models.Role.name == 'Employee').first()
        mgr_role = db.query(models.Role).filter(models.Role.name == 'Manager').first()
        hr_role = db.query(models.Role).filter(models.Role.name == 'HR').first()

        # Create multiple managers
        num_managers = 2
        for i in range(1, num_managers + 1):
            username = f'manager{i}' if i > 1 else 'manager'
            user = db.query(models.User).filter(models.User.username == username).first()
            emp_code = f'MGR{i:03d}'
            if not user:
                mgr_emp = db.query(models.Employee).filter(models.Employee.employee_code == emp_code).first()
                if not mgr_emp:
                    mgr_emp = models.Employee(employee_code=emp_code, first_name=f'Manager{i}', last_name='Auto')
                    db.add(mgr_emp)
                    db.commit()
                    db.refresh(mgr_emp)

                user = models.User(username=username, email=f'{username}@example.com', password_hash=get_password_hash(f'ManagerPass{i}'))
                user.roles.append(mgr_role)
                user.employee_id = mgr_emp.id
                db.add(user)
                db.commit()
                print(f'Created manager user: {username} / ManagerPass{i}')

        # Create multiple HR users
        num_hr = 2
        for i in range(1, num_hr + 1):
            username = f'hr{i}' if i > 1 else 'hr'
            user = db.query(models.User).filter(models.User.username == username).first()
            emp_code = f'HR{i:03d}'
            if not user:
                hr_emp = db.query(models.Employee).filter(models.Employee.employee_code == emp_code).first()
                if not hr_emp:
                    hr_emp = models.Employee(employee_code=emp_code, first_name=f'HR{i}', last_name='Auto')
                    db.add(hr_emp)
                    db.commit()
                    db.refresh(hr_emp)

                user = models.User(username=username, email=f'{username}@example.com', password_hash=get_password_hash(f'HRPass{i}'))
                user.roles.append(hr_role)
                user.employee_id = hr_emp.id
                db.add(user)
                db.commit()
                print(f'Created HR user: {username} / HRPass{i}')

        # Create multiple employees under each manager
        employees_per_manager = 5
        managers = db.query(models.Employee).filter(models.Employee.employee_code.like('MGR%')).all()
        emp_counter = 1
        for mgr_emp in managers:
            for j in range(1, employees_per_manager + 1):
                emp_code = f'EMP_{mgr_emp.employee_code}_{j:03d}'
                e = db.query(models.Employee).filter(models.Employee.employee_code == emp_code).first()
                if not e:
                    e = models.Employee(employee_code=emp_code, first_name=f'Emp{emp_counter}', last_name='Auto', manager_id=mgr_emp.id)
                    db.add(e)
                    db.commit()
                    db.refresh(e)

                # create corresponding user
                uname = f'emp_{mgr_emp.employee_code.lower()}_{j}'
                u = db.query(models.User).filter(models.User.username == uname).first()
                if not u:
                    u = models.User(username=uname, email=f'{uname}@example.com', password_hash=get_password_hash(f'EmpPass{emp_counter}'))
                    u.roles.append(emp_role)
                    u.employee_id = e.id
                    db.add(u)
                    db.commit()
                    print(f'Created employee user: {uname} / EmpPass{emp_counter}')
                emp_counter += 1

        # Create a few standalone demo employees
        for k in range(1, 4):
            emp_code = f'DEMO{k:03d}'
            e = db.query(models.Employee).filter(models.Employee.employee_code == emp_code).first()
            if not e:
                e = models.Employee(employee_code=emp_code, first_name=f'Demo{k}', last_name='User')
                db.add(e)
                db.commit()
                db.refresh(e)
            uname = f'demo{k}'
            u = db.query(models.User).filter(models.User.username == uname).first()
            if not u:
                u = models.User(username=uname, email=f'{uname}@example.com', password_hash=get_password_hash(f'DemoPass{k}'))
                u.roles.append(emp_role)
                u.employee_id = e.id
                db.add(u)
                db.commit()
                print(f'Created demo employee user: {uname} / DemoPass{k}')

        print('Seeding complete.')
    finally:
        db.close()


if __name__ == '__main__':
    ensure()
