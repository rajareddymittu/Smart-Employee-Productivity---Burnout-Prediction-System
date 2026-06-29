
# Chapter 6: System Design (Updated)

# Part 2 – UML and Deployment Design

## 6.7 Login Sequence Diagram

The Login Sequence Diagram illustrates the interaction between the user, Angular frontend, FastAPI backend, authentication service, and PostgreSQL database during the authentication process.

**Workflow**

1. User enters credentials.
2. Angular sends a login request to the FastAPI backend.
3. Backend validates the credentials.
4. User information is retrieved from PostgreSQL.
5. JWT access token is generated.
6. Token is returned to the Angular application.
7. User is redirected to the dashboard.

**Diagram**

Insert the rendered image generated from:

```text
login_sequence_diagram.puml
```

---

## 6.8 Burnout Prediction Sequence Diagram

The prediction sequence represents the interaction between the frontend, backend, machine learning service, and database during burnout prediction.

**Workflow**

1. HR Manager selects an employee.
2. Angular requests prediction.
3. FastAPI collects employee features.
4. ML model loads trained weights.
5. Burnout score is calculated.
6. Prediction is stored in PostgreSQL.
7. Result is returned to the dashboard.

**Diagram**

Insert the rendered image generated from:

```text
burnout_prediction_sequence.puml
```

---

## 6.9 Class Diagram

The Class Diagram represents the static structure of the application and the relationships among major entities.

Important entities include:

- User
- Role
- Employee
- Department
- Attendance
- Prediction
- Report

The diagram demonstrates associations, inheritance (where applicable), and dependencies between classes.

**Diagram**

Insert the rendered image generated from:

```text
class_diagram.puml
```

---

## 6.10 Data Flow Diagram (DFD)

The Data Flow Diagram illustrates how information flows through the application.

Major processes include:

- User Authentication
- Employee Management
- Attendance Processing
- Burnout Prediction
- Report Generation

Primary external entities:

- Administrator
- HR Manager
- Employee

Data stores:

- PostgreSQL Database
- Prediction History

**Diagram**

Insert the rendered image generated from:

```text
dfd_level_0.puml
```

---

## 6.11 Deployment Diagram

The deployment architecture illustrates how the application components are deployed across the execution environment.

Deployment nodes include:

- Client Browser
- Angular Application
- FastAPI Server
- Machine Learning Service
- PostgreSQL Database

Communication is performed over HTTPS using REST APIs secured by JWT authentication.

**Diagram**

Insert the rendered image generated from:

```text
deployment_diagram.puml
```

---

## 6.12 Component Interaction

The overall interaction among system components follows this sequence:

```text
Angular UI
      │
 REST API
      │
 FastAPI Backend
      │
 ├── Authentication
 ├── Business Logic
 ├── ML Prediction
 └── PostgreSQL Database
```

The modular architecture enables independent development, testing, and maintenance of each subsystem while ensuring secure communication through RESTful services.

---

## Chapter Summary

This part of the System Design chapter explains the behavioral and structural UML models of the application, including sequence diagrams, class relationships, data flow, deployment architecture, and component interactions. Together with Part 1 and the upcoming Part 3, these sections provide a complete architectural description of the proposed system.
