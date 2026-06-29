
# Chapter 2: Requirement Analysis

# 2. Requirement Analysis

## 2.1 Introduction

Requirement Analysis identifies, validates, and documents the functional and non-functional requirements of the Smart Employee Productivity & Burnout Prediction System. It establishes the foundation for system design, implementation, testing, and deployment. The analysis was carried out considering the needs of administrators, HR personnel, and employees.

---

## 2.2 Requirement Gathering

Requirements were gathered through:
- Study of existing HRMS applications.
- Analysis of employee burnout prediction research.
- Review of organizational HR workflows.
- Examination of the proposed software architecture.

---

## 2.3 Stakeholders

| Stakeholder | Responsibility |
|---|---|
| Administrator | Manage users, configuration and reports |
| HR Manager | Employee management, monitoring, analytics |
| Employee | Access personal information and reports |
| System Administrator | Maintain infrastructure and database |

---

## 2.4 Functional Requirements

### Authentication
- Secure login
- JWT authentication
- Role-based authorization
- Session management

### Employee Management
- Create employee records
- Update employee information
- Delete employees
- Search and filter employees

### Department Management
- Department CRUD operations
- Employee assignment

### Attendance
- Record attendance
- Attendance history
- Attendance reports

### Performance & Burnout
- Store productivity metrics
- Execute burnout prediction
- Display prediction history
- Generate analytical reports

---

## 2.5 Non-Functional Requirements

### Performance
- Fast API response time
- Efficient database queries

### Security
- JWT authentication
- Password hashing
- Input validation
- Role-based access

### Reliability
- Error handling
- Backup strategy
- Logging

### Scalability
- Modular Angular frontend
- FastAPI service architecture
- PostgreSQL database

### Maintainability
- Layered architecture
- Modular source code
- RESTful API design

---

## 2.6 User Roles

| Role | Permissions |
|---|---|
| Administrator | Complete system access |
| HR Manager | Employee management and analytics |
| Employee | View profile and prediction results |

---

## 2.7 Hardware Requirements

| Component | Specification |
|---|---|
| Processor | Intel Core i5 / Apple Silicon |
| RAM | 8 GB or above |
| Storage | 20 GB Free |
| Network | Internet Connection |

---

## 2.8 Software Requirements

| Component | Technology |
|---|---|
| Frontend | Angular |
| Backend | FastAPI |
| Database | PostgreSQL |
| ML | Scikit-learn |
| Language | Python, TypeScript |
| IDE | Visual Studio Code |
| Version Control | Git |

---

## 2.9 System Constraints

- Valid employee data is required.
- Prediction accuracy depends on training data.
- Authenticated access is mandatory.
- Database availability is essential.

---

## 2.10 Assumptions

- Users provide correct information.
- Database server remains available.
- ML model is periodically retrained.
- Authorized users follow security policies.

---

## 2.11 Requirement Traceability Matrix

| ID | Requirement | Module |
|---|---|---|
| FR-01 | Authentication | Auth |
| FR-02 | Employee CRUD | Employee |
| FR-03 | Attendance | Attendance |
| FR-04 | Dashboard | Dashboard |
| FR-05 | Burnout Prediction | ML |
| FR-06 | Reports | Reporting |

---

## 2.12 Risks

- Poor quality datasets
- Unauthorized access
- Infrastructure failure
- Incorrect data entry

Mitigation includes validation, authentication, backups, monitoring, and periodic model evaluation.

---

## 2.13 Chapter Summary

This chapter defines the complete functional and non-functional requirements of the application and establishes the baseline for system design, implementation, and testing. These requirements ensure that the developed solution satisfies both organizational and technical objectives while supporting secure and intelligent employee productivity analysis.
