
# Chapter 10: Application and Results

# 10. Application and Results

## 10.1 Introduction

This chapter presents the developed **Smart Employee Productivity & Burnout Prediction System Using Machine Learning** and demonstrates how the implemented modules work together. The application integrates an Angular frontend, FastAPI backend, PostgreSQL database, and a Machine Learning model to deliver intelligent workforce analytics and burnout prediction.

---

## 10.2 Application Overview

The application provides the following features:

- Secure JWT-based authentication
- Employee management
- Department management
- Attendance management
- Burnout prediction
- Dashboard analytics
- Report generation

The frontend communicates with the backend using REST APIs, while prediction requests are processed by the Machine Learning module.

---

## 10.3 Authentication Module

Users authenticate through a secure login page.

### Workflow

1. User enters credentials.
2. Angular sends a login request.
3. FastAPI validates the credentials.
4. JWT token is generated.
5. User is redirected to the dashboard.

**Insert Login Screenshot**

`images/results/login.png`

---

## 10.4 Dashboard

The dashboard provides an overview of organizational data including employee statistics, department information, productivity indicators, and burnout summaries.

Displayed information may include:

- Total Employees
- Active Employees
- Departments
- Burnout Risk Distribution
- Recent Activities

**Insert Dashboard Screenshot**

`images/results/dashboard.png`

---

## 10.5 Employee Management

The Employee module supports complete lifecycle management.

Functions include:

- Add Employee
- Update Employee
- Delete Employee
- Search Employee
- View Employee Details

**Insert Employee Module Screenshot**

`images/results/employees.png`

---

## 10.6 Burnout Prediction Module

The prediction module analyses employee attributes and estimates burnout risk using the trained Machine Learning model.

### Prediction Workflow

```text
Employee Data
      │
Data Preprocessing
      │
Feature Engineering
      │
Trained ML Model
      │
Prediction Score
      │
Dashboard Display
```

The backend training pipeline includes:

- train_model.py
- train_model_v2.py

**Insert Prediction Screenshot**

`images/results/prediction.png`

---

## 10.7 API Results

Representative API operations include:

| Endpoint | Purpose |
|---|---|
| Login | User authentication |
| Employees | CRUD operations |
| Departments | Department management |
| Attendance | Attendance management |
| Predict | Burnout prediction |
| Reports | Dashboard analytics |

---

## 10.8 Application Results

The developed application successfully:

- Authenticates users securely.
- Maintains employee records.
- Stores attendance information.
- Generates burnout predictions.
- Produces analytical reports.
- Supports data-driven HR decisions.

---

## 10.9 Performance Summary

| Feature | Status |
|---|---|
| Authentication | Successful |
| CRUD Operations | Successful |
| Dashboard | Functional |
| Prediction | Functional |
| Reporting | Functional |

---

## 10.10 Benefits

The system offers:

- Improved workforce monitoring
- Early burnout detection
- Centralized employee management
- Better reporting
- Secure access control
- Scalable architecture

---

## 10.11 Screenshots

Include screenshots for:

- Login
- Dashboard
- Employee Management
- Department Management
- Attendance
- Burnout Prediction
- Reports
- API Testing

---

## 10.12 Chapter Summary

The developed application integrates Angular, FastAPI, PostgreSQL, and Machine Learning into a unified enterprise solution. The implementation successfully automates employee management while providing predictive burnout analysis, secure REST APIs, and interactive dashboards to support organizational decision-making.
