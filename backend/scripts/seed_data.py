from app.database.session import SessionLocal
from app import models
import random
from datetime import date, timedelta

FIRST = ["Alice","Bob","Carol","David","Eve","Frank","Grace","Hector","Ivy","Jack","Karen","Leo","Mona","Nate","Olivia","Paul","Quinn","Rachel","Sam","Tina"]
LAST = ["Johnson","Smith","Lee","Garcia","Khan","Brown","Miller","Davis","Wilson","Moore","Taylor","Anderson","Thomas","Jackson","White","Harris","Martin","Thompson","Martinez","Robinson"]
DEPT_NAMES = ["Engineering", "Sales", "HR", "Support"]

def random_date(start_year=2010, end_year=2023):
    start = date(start_year,1,1)
    end = date(end_year,12,31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def seed():
    db = SessionLocal()
    try:
        # ensure departments exist and collect their ids
        dept_objs = []
        for name in DEPT_NAMES:
            d = db.query(models.Department).filter(models.Department.name == name).first()
            if not d:
                d = models.Department(name=name)
                db.add(d)
                db.flush()
            dept_objs.append(d)
        # commit departments so they get ids
        db.commit()
        dept_ids = [d.id for d in dept_objs if d and d.id]

        created = 0
        for i in range(1, 101):
            code = f"EMP{i:03d}"
            existing = db.query(models.Employee).filter(models.Employee.employee_code == code).first()
            if existing:
                continue
            first = random.choice(FIRST)
            last = random.choice(LAST)
            gender = random.choice(['Male','Female','Other'])
            dob = random_date(1970,1998)
            # ensure joining not in future
            joining = random_date(2015, date.today().year)
            # compute realistic experience as years between dob and joining
            try:
                days = (joining - dob).days
                experience = round(max(0.0, days / 365.0), 2)
                # ensure small values are at least 0.5 years for new hires
                if experience > 0 and experience < 0.5:
                    experience = 0.5
            except Exception:
                experience = None
            salary_grade = random.choice(['A1','A2','B1','B2','C1'])
            # random department (or None)
            dept = random.choice([None] + dept_ids)
            emp = models.Employee(
                employee_code=code,
                first_name=first,
                last_name=last,
                gender=gender,
                dob=dob,
                joining_date=joining,
                experience=experience,
                salary_grade=salary_grade,
                department_id=dept,
                status='active'
            )
            db.add(emp)
            created += 1
        if created:
            db.commit()
        print(f"Seed complete — created {created} employees (skipped existing)")
    finally:
        db.close()


if __name__ == '__main__':
    seed()
