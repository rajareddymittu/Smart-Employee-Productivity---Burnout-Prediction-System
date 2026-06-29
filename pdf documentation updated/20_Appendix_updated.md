
# Chapter 14: Appendix

# 14. Appendix

## 14.1 Introduction

This appendix provides supporting technical information for the **Smart Employee Productivity & Burnout Prediction System Using Machine Learning**. It contains supplementary material including project structure, installation steps, configuration details, API summary, database information, user guidance, and other reference material used during development.

---

## Appendix A – Project Structure

### Backend

```text
backend/
├── ml/
│   ├── train_model.py
│   ├── train_model_v2.py
│   └── train_and_save.py
├── sql/
│   └── schema.sql
├── scripts/
│   ├── create_tables.py
│   ├── seed_data.py
│   ├── seed_roles_and_users.py
│   └── assign_managers.py
├── requirements.txt
└── README.md
```

### Frontend

```text
frontend/
├── angular.json
├── src/
├── assets/
├── environments/
├── package.json
└── dist/
```

---

## Appendix B – Installation Guide

### Prerequisites

- Python 3.x
- Node.js
- PostgreSQL
- Git
- Visual Studio Code

### Backend

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
npm install

ng serve
```

---

## Appendix C – Environment Variables

```env
DATABASE_URL=<database_connection_string>
JWT_SECRET=<secret_key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Appendix D – API Summary

| Method | Purpose |
|---|---|
| POST | Login |
| GET | Employees |
| POST | Create Employee |
| PUT | Update Employee |
| DELETE | Delete Employee |
| POST | Burnout Prediction |

---

## Appendix E – Database

The PostgreSQL database is initialized using the provided SQL schema and database setup scripts.

Key entities include:

- Users
- Roles
- Employees
- Departments
- Attendance
- Predictions

---

## Appendix F – Configuration Files

Major configuration files include:

- requirements.txt
- angular.json
- package.json
- schema.sql

---

## Appendix G – User Manual

### Administrator

- Login
- Manage Employees
- Manage Departments
- View Reports
- Access Dashboard

### HR Manager

- Employee Management
- Attendance
- Burnout Prediction
- Reports

---

## Appendix H – Additional Screenshots

Include screenshots of:

- Login
- Dashboard
- Employee Module
- Department Module
- Attendance Module
- Burnout Prediction
- Reports
- API Testing

---

## Appendix I – Glossary

| Term | Description |
|---|---|
| AI | Artificial Intelligence |
| ML | Machine Learning |
| JWT | JSON Web Token |
| API | Application Programming Interface |
| REST | Representational State Transfer |
| HR | Human Resources |

---

## Appendix J – Acronyms

| Acronym | Full Form |
|---|---|
| SDLC | System Development Life Cycle |
| SRS | Software Requirement Specification |
| DBMS | Database Management System |
| UAT | User Acceptance Testing |
| RBAC | Role-Based Access Control |

---

## Appendix K – Final Submission Checklist

- Project report completed
- UML diagrams inserted
- Screenshots inserted
- Bibliography verified
- Page numbers updated
- Table of Contents updated
- PDF generated
- Source code archived

---

## Chapter Summary

The appendix provides supplementary technical information supporting the implementation and evaluation of the proposed system. It serves as a reference for installation, configuration, deployment, maintenance, and future enhancement of the application.
