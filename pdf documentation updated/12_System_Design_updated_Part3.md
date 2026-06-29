
# Chapter 6: System Design (Updated)

# Part 3 – API, User Interface and Security Design

## 6.13 API Design

The backend exposes RESTful APIs implemented using **FastAPI**. The APIs exchange JSON data between the Angular frontend and the backend while protecting secured endpoints using JWT authentication.

### Major API Modules

| Module | Purpose |
|---|---|
| Authentication | User login and token generation |
| Employees | Employee CRUD operations |
| Departments | Department management |
| Attendance | Attendance management |
| Predictions | Burnout prediction |
| Reports | Dashboard and analytics |

### Typical API Flow

```text
Angular Client
      │
 HTTPS + JSON
      │
 FastAPI Router
      │
 Service Layer
      │
 Repository Layer
      │
 PostgreSQL Database
```

---

## 6.14 Navigation Flow

The user navigation follows a role-based workflow.

```text
Login
  │
Dashboard
  ├── Employee Management
  ├── Department Management
  ├── Attendance
  ├── Burnout Prediction
  ├── Reports
  └── Logout
```

Administrators and HR Managers are presented with different navigation options based on their assigned roles.

---

## 6.15 User Interface Design

The frontend is implemented using **Angular** and provides a responsive interface suitable for desktop environments.

Major screens include:

- Login Screen
- Dashboard
- Employee List
- Employee Details
- Department Management
- Attendance Management
- Burnout Prediction
- Reports

Insert screenshots from your project in the corresponding sections of the final report.

---

## 6.16 Security Design

The system incorporates multiple security mechanisms.

- JWT Authentication
- Role-Based Access Control (RBAC)
- Password hashing
- Request validation
- Secure REST APIs
- Input sanitization
- Exception handling

These measures protect sensitive employee information and restrict unauthorized access.

---

## 6.17 Design Principles

The application follows established software engineering principles:

- Layered Architecture
- Separation of Concerns
- High Cohesion
- Low Coupling
- Modular Development
- Reusable Components
- RESTful Design
- Database Normalization

These principles improve maintainability, scalability, and long-term extensibility.

---

## 6.18 Advantages of the Architecture

The proposed architecture provides several benefits:

- Scalable Angular frontend
- Lightweight FastAPI backend
- Secure JWT authentication
- Efficient PostgreSQL database
- Machine Learning integration
- Modular deployment
- Simplified maintenance
- Improved performance

---

## 6.19 Complete Chapter Summary

This chapter presented the complete design of the Smart Employee Productivity & Burnout Prediction System. It described the layered architecture, software modules, UML diagrams, API design, deployment strategy, navigation flow, user interface, and security architecture. Together, these design artifacts provide a comprehensive blueprint for implementing the application and establish the foundation for the database design and implementation chapters that follow.
