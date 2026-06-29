# Chapter 7: Database Design

# 7. Database Design

## 7.1 Introduction

The Database Design defines how data is organized, stored, retrieved, and maintained within the **Smart Employee Productivity & Burnout Prediction System Using Machine Learning**. A well-designed relational database ensures data integrity, consistency, scalability, and efficient query execution.

The project uses **PostgreSQL** as the relational database management system (RDBMS). The database stores employee information, authentication details, departments, attendance records, productivity metrics, burnout predictions, and system logs.

---

# 7.2 Database Objectives

The objectives of the database design are:

- Store employee information securely.
- Maintain data integrity.
- Reduce redundancy through normalization.
- Support efficient querying.
- Maintain relationships among entities.
- Enable secure data access.

---

# 7.3 Database Architecture

The application follows a layered architecture where:

- Frontend communicates with Backend APIs.
- Backend interacts with PostgreSQL using ORM.
- Machine Learning module reads processed employee data.
- Prediction results are stored back into the database.

## Figure 7.1 Database Architecture

> **Placeholder**

Insert Database Architecture Diagram.

```text
diagrams/database_architecture.svg
```

---

# 7.4 Entity Relationship (ER) Diagram

The ER Diagram illustrates relationships between all entities in the system.

## Figure 7.2 ER Diagram

> **Placeholder**

```text
diagrams/er_diagram.svg
```

**Description**

Explain relationships among:

- User
- Employee
- Department
- Attendance
- Performance
- Burnout Prediction
- Reports

---

# 7.5 Database Tables

## Users

| Column | Data Type | Description |
|--------|-----------|-------------|
| id | UUID / INT | Primary Key |
| username | VARCHAR | Login Username |
| password_hash | TEXT | Encrypted Password |
| role | VARCHAR | User Role |
| created_at | TIMESTAMP | Creation Date |

---

## Employees

| Column | Data Type | Description |
|--------|-----------|-------------|
| employee_id | UUID / INT | Primary Key |
| employee_name | VARCHAR | Employee Name |
| email | VARCHAR | Email |
| department_id | FK | Department |
| designation | VARCHAR | Job Title |
| joining_date | DATE | Joining Date |

---

## Departments

| Column | Data Type | Description |
|--------|-----------|-------------|
| department_id | INT | Primary Key |
| department_name | VARCHAR | Department Name |

---

## Attendance

| Column | Data Type | Description |
|--------|-----------|-------------|
| attendance_id | INT | Primary Key |
| employee_id | FK | Employee |
| attendance_date | DATE | Attendance Date |
| status | VARCHAR | Present/Absent |

---

## Performance

| Column | Data Type | Description |
|--------|-----------|-------------|
| performance_id | INT | Primary Key |
| employee_id | FK | Employee |
| productivity_score | FLOAT | Productivity |
| rating | FLOAT | Performance Rating |

---

## Burnout Predictions

| Column | Data Type | Description |
|--------|-----------|-------------|
| prediction_id | INT | Primary Key |
| employee_id | FK | Employee |
| burnout_score | FLOAT | Prediction Score |
| prediction_date | DATE | Generated On |

> **Placeholder:** Replace the above schemas with your actual database structure.

---

# 7.6 Relationships

| Parent | Child | Relationship |
|---------|-------|--------------|
| Department | Employee | One-to-Many |
| Employee | Attendance | One-to-Many |
| Employee | Performance | One-to-Many |
| Employee | Burnout Prediction | One-to-Many |
| User | Employee | One-to-One (if applicable) |

---

# 7.7 Database Constraints

The following constraints are used:

- Primary Keys
- Foreign Keys
- Unique Constraints
- NOT NULL Constraints
- Check Constraints (where applicable)

---

# 7.8 Indexes

Recommended indexes:

| Table | Indexed Column |
|--------|----------------|
| Users | username |
| Employees | email |
| Attendance | employee_id |
| Performance | employee_id |
| Burnout Predictions | employee_id |

---

# 7.9 Database Normalization

The database is normalized up to **Third Normal Form (3NF)**.

### First Normal Form (1NF)

- Eliminate repeating groups.
- Atomic values only.

### Second Normal Form (2NF)

- Remove partial dependencies.

### Third Normal Form (3NF)

- Remove transitive dependencies.

This normalization minimizes redundancy while maintaining efficient data retrieval.

---

# 7.10 Data Dictionary

> **Placeholder**

Add a detailed data dictionary containing:

- Table Name
- Column Name
- Data Type
- Length
- Nullable
- Default Value
- Description

---

# 7.11 Sample SQL Queries

> **Placeholder**

Insert important SQL queries.

```sql
-- Example:
SELECT * FROM employees;
```

---

# 7.12 Backup and Recovery

Database maintenance includes:

- Regular backups
- Transaction logging
- Recovery procedures
- Integrity verification

---

# 7.13 Security Considerations

- Password hashing
- Role-based permissions
- SQL injection prevention
- Parameterized queries
- Database access restrictions

---

## Placeholder Checklist

### Diagrams

- Database Architecture
- ER Diagram

### SQL

- CREATE TABLE scripts
- ALTER TABLE scripts
- Sample Queries
- Stored Procedures (if any)

### Screenshots

- Database tables
- pgAdmin / Database Browser

### Code

No application code is required in this chapter.

---

# Chapter Summary

This chapter described the database design for the proposed system, including the relational schema, entity relationships, normalization, constraints, indexing strategy, and security considerations. The database provides a reliable and scalable foundation for storing employee information and supporting burnout prediction functionality.
