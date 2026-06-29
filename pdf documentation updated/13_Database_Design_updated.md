
# Chapter 7: Database Design

# 7. Database Design

## 7.1 Introduction

The Smart Employee Productivity & Burnout Prediction System uses **PostgreSQL** as its relational database management system. The database is designed to store employee information, authentication data, departments, attendance records, productivity metrics, and burnout prediction history while maintaining data integrity and supporting efficient query execution.

The backend project contains a database schema (`schema.sql`) and supporting scripts for table creation and data initialization, ensuring a consistent database setup.

---

## 7.2 Database Objectives

The database is designed to:

- Store employee and organizational data securely.
- Maintain referential integrity.
- Reduce redundancy through normalization.
- Support efficient CRUD operations.
- Preserve prediction history for analytics.
- Enable future scalability.

---

## 7.3 Database Architecture

```text
Angular Frontend
        │
   REST APIs
        │
 FastAPI Backend
        │
 PostgreSQL Database
```

The backend communicates with PostgreSQL using a layered architecture, isolating business logic from persistence.

---

## 7.4 Major Database Entities

The database contains entities similar to the following:

- Users
- Roles
- Employees
- Departments
- Attendance
- Burnout Predictions
- Reports

> Update this list if additional tables exist in the final schema.

---

## 7.5 Entity Relationship Diagram

Insert the rendered **ER Diagram** generated from your PlantUML source.

**Figure 7.1 Entity Relationship Diagram**

Explain the major relationships:

- One Department → Many Employees
- One Employee → Many Attendance Records
- One Employee → Many Prediction Records
- One Role → Many Users

---

## 7.6 Normalization

The schema follows normalization principles to reduce redundancy.

- First Normal Form (1NF)
- Second Normal Form (2NF)
- Third Normal Form (3NF)

Normalization improves consistency and minimizes duplicate data.

---

## 7.7 Data Dictionary

| Entity | Purpose |
|---|---|
| Users | Authentication and authorization |
| Roles | Role-based access control |
| Employees | Employee profile information |
| Departments | Department details |
| Attendance | Attendance records |
| Predictions | Burnout prediction results |

Replace or extend this table to match the final schema.

---

## 7.8 Keys and Relationships

The design uses:

- Primary Keys
- Foreign Keys
- Unique Constraints
- Indexes

These constraints enforce referential integrity and improve query performance.

---

## 7.9 Sample SQL Operations

Typical database operations include:

- Employee insertion
- Employee update
- Attendance recording
- Prediction storage
- Report generation

The implementation is based on the SQL schema and backend data-access layer.

---

## 7.10 Backup and Recovery

Recommended practices:

- Periodic database backups
- Transaction logging
- Role-based database access
- Secure credential management

---

## 7.11 Database Advantages

- Structured relational storage
- High data integrity
- Efficient joins
- ACID compliance
- Scalability
- Reliable analytics support

---

## 7.12 Chapter Summary

This chapter described the database architecture of the proposed system, including the major entities, relationships, normalization strategy, keys, and database management practices. The PostgreSQL schema provides a robust foundation for securely storing operational and analytical data used throughout the application.
