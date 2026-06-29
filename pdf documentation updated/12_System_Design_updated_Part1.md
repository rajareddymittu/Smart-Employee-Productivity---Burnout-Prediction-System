
# Chapter 6: System Design (Updated)

# 6. System Design

## 6.1 Introduction

System Design translates the functional and non-functional requirements into a comprehensive software architecture that defines the interaction between various software components. The Smart Employee Productivity & Burnout Prediction System follows a modular, layered architecture that separates presentation, business logic, machine learning, and persistence concerns. This separation improves maintainability, scalability, security, and ease of future enhancement.

The application is designed using Angular for the frontend, FastAPI for the backend, PostgreSQL for persistent storage, and Scikit-learn for burnout prediction. Communication between layers is achieved using secure REST APIs with JSON and JWT authentication.

---

## 6.2 Design Objectives

The primary design objectives are:

- Modular software architecture
- High scalability
- Secure authentication
- Easy maintainability
- Separation of concerns
- Reusable components
- Efficient database interaction
- Machine Learning integration
- REST-based communication

---

## 6.3 Overall System Architecture

The system follows a four-layer enterprise architecture.

```text
                Angular Frontend
                        │
              REST API (HTTPS + JWT)
                        │
                 FastAPI Backend
      ┌───────────────┬───────────────┐
      │               │               │
 Authentication   Business Logic   ML Service
      │               │               │
      └───────────────┴───────────────┘
                PostgreSQL Database
```

### Presentation Layer

Implemented using Angular.

Responsibilities include:

- Login
- Employee Management
- Dashboard
- Reports
- Burnout Prediction
- API Communication

### Business Layer

Implemented using FastAPI.

Responsibilities include:

- Authentication
- Request validation
- CRUD operations
- Authorization
- Report generation
- ML invocation

### Machine Learning Layer

The backend contains training scripts including:

- `train_model.py`
- `train_model_v2.py`

Responsibilities include:

- Dataset preprocessing
- Feature engineering
- Model training
- Prediction generation

### Database Layer

Implemented using PostgreSQL.

Database management is supported through:

- `schema.sql`
- `create_tables.py`
- Seed scripts

The database stores:

- Users
- Roles
- Employees
- Departments
- Attendance
- Performance
- Prediction History

---

## 6.4 Major Software Modules

### Authentication Module

- Secure Login
- JWT Token Generation
- Token Validation
- Role-Based Authorization

### Employee Module

- Add Employee
- Update Employee
- Delete Employee
- Search Employee
- View Employee Profile

### Department Module

- Department CRUD
- Employee Assignment

### Attendance Module

- Attendance Recording
- Attendance Reports
- Attendance History

### Burnout Prediction Module

Workflow:

Employee Data → Feature Engineering → Model Prediction → Burnout Score → Dashboard Visualization

### Reporting Module

- Productivity Reports
- Employee Reports
- Department Reports
- Prediction Reports

---

## 6.5 Use Case Diagram

Insert the rendered **Use Case Diagram** generated from `use_case_diagram.puml`.

Describe the interactions between:

- Administrator
- HR Manager
- Employee

---

## 6.6 Activity Diagram

Insert the rendered **Activity Diagram** generated from `activity_diagram.puml`.

The diagram illustrates:

- User authentication
- Request processing
- Database interaction
- Burnout prediction workflow
- Result visualization

---

## Chapter Summary

This section presents the architectural foundation of the application, introducing the layered design, major software modules, and high-level workflows. The remaining sections of the System Design chapter will describe sequence diagrams, class diagram, DFD, deployment architecture, API design, and navigation flow.
