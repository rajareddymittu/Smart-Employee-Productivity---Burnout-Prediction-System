# Phase 2 - System Design

# AI-Powered Employee Productivity Analytics and Burnout Prediction System

# 1. High Level Architecture

    Angular Frontend
          |
     REST API (FastAPI)
          |
    Business Services
          |
    ML Prediction Engine
          |
      MySQL Database

# 2. Use Cases

## Admin

-   Manage Users
-   Manage Roles
-   View Reports
-   Configure Departments

## HR

-   Manage Employees
-   Manage Leave
-   View Analytics
-   Trigger Predictions

## Manager

-   Assign Tasks
-   Review Performance
-   View Team Dashboard

## Employee

-   Login
-   Mark Attendance
-   Apply Leave
-   Update Tasks
-   View Dashboard

# 3. ER Model

Entities:

-   Users
-   Roles
-   Employees
-   Departments
-   Attendance
-   LeaveRequests
-   Projects
-   Tasks
-   PerformanceReviews
-   Meetings
-   Predictions

Relationships: - Department 1:N Employees - Employee 1:N Attendance -
Employee 1:N LeaveRequests - Employee N:N Projects - Employee 1:N
Tasks - Employee 1:N Reviews

# 4. Database Tables

1.  users
2.  roles
3.  user_roles
4.  employees
5.  departments
6.  attendance
7.  leave_requests
8.  leave_types
9.  projects
10. employee_projects
11. tasks
12. task_assignments
13. meetings
14. meeting_attendance
15. performance_reviews
16. notifications
17. work_logs
18. predictions
19. skills
20. employee_skills
21. audit_logs
22. activity_logs
23. holiday_calendar
24. refresh_tokens
25. sessions

# 5. DFD Level 0

Employee/HR/Admin \| HR Analytics System \| PostgreSQL

# 6. DFD Level 1

Users \| Authentication \| Employee Module Attendance Module Leave
Module Task Module Project Module ML Module Reports

# 7. Component Diagram

Frontend \| API Controllers \| Services \| Repositories \| Database

ML Service attached to Services layer.

# 8. Deployment Diagram

Browser \| Angular App \| Nginx \| FastAPI Server \| PostgreSQL

Separate ML service on same server.

# 9. Sequence (Login)

User -\> UI UI -\> API API -\> Auth Service Auth -\> DB DB -\> Auth Auth
-\> JWT API -\> UI

# 10. Activity Flow

Login -\> Dashboard -\> Attendance -\> Tasks -\> Performance -\>
Prediction -\> Reports -\> Logout
