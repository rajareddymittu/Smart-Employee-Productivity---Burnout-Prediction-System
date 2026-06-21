# Phase 3 - Database Design & API Specification

# 1. Database Overview

Database: MySQL

Schema follows normalization up to 3NF with foreign keys and indexing.

# 2. Core Tables

## users

-   id (PK)
-   username
-   email
-   password_hash
-   employee_id
-   created_at
-   updated_at

## roles

-   id
-   name

## user_roles

-   user_id
-   role_id

## departments

-   id
-   name
-   manager_id

## employees

-   id
-   employee_code
-   first_name
-   last_name
-   gender
-   dob
-   department_id
-   joining_date
-   experience
-   salary_grade
-   status

## attendance

-   id
-   employee_id
-   date
-   check_in
-   check_out
-   overtime_hours

## leave_types

-   id
-   name

## leave_requests

-   id
-   employee_id
-   leave_type_id
-   start_date
-   end_date
-   status

## projects

-   id
-   name
-   description
-   start_date
-   end_date

## employee_projects

-   employee_id
-   project_id

## tasks

-   id
-   title
-   description
-   priority
-   due_date
-   status

## task_assignments

-   employee_id
-   task_id

## meetings

-   id
-   title
-   duration

## performance_reviews

-   id
-   employee_id
-   rating
-   comments

## predictions

-   id
-   employee_id
-   burnout_risk
-   productivity_score
-   predicted_on

# 3. Foreign Keys

employees.department_id -\> departments.id

attendance.employee_id -\> employees.id

leave_requests.employee_id -\> employees.id

employee_projects.employee_id -\> employees.id

employee_projects.project_id -\> projects.id

task_assignments.employee_id -\> employees.id

task_assignments.task_id -\> tasks.id

predictions.employee_id -\> employees.id

# 4. Suggested Indexes

-   employee_code
-   email
-   attendance(date)
-   task(status)
-   predictions(employee_id)

# 5. REST API Specification

## Authentication

POST /api/auth/login

POST /api/auth/refresh

POST /api/auth/logout

GET /api/auth/profile

## Employees

GET /api/employees

GET /api/employees/{id}

POST /api/employees

PUT /api/employees/{id}

DELETE /api/employees/{id}

## Departments

GET /api/departments

POST /api/departments

PUT /api/departments/{id}

DELETE /api/departments/{id}

## Attendance

GET /api/attendance

POST /api/attendance/checkin

POST /api/attendance/checkout

## Leave

POST /api/leaves

GET /api/leaves

PUT /api/leaves/{id}/approve

PUT /api/leaves/{id}/reject

## Projects

GET /api/projects

POST /api/projects

PUT /api/projects/{id}

## Tasks

GET /api/tasks

POST /api/tasks

PUT /api/tasks/{id}

## Reviews

GET /api/reviews

POST /api/reviews

## AI Prediction

POST /api/predict/burnout

POST /api/predict/productivity

GET /api/predictions/history

## Reports

GET /api/reports/attendance

GET /api/reports/performance

GET /api/reports/burnout

GET /api/reports/productivity

# 6. JWT Flow

Client Login -\> JWT Access Token -\> Refresh Token -\> Protected API
-\> Validation Middleware -\> Controller

# 7. HTTP Status Codes

200 OK

201 Created

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

500 Internal Server Error

# 8. Error Response

{ "success": false, "message": "Validation Failed", "errors": \[\] }
