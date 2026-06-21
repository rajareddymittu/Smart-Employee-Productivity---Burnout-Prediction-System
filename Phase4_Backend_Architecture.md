# Phase 4 - Backend Architecture & FastAPI Design

# 1. Backend Technology

-   Python 3.12
-   FastAPI
-   SQLAlchemy ORM
-   Alembic
-   PostgreSQL
-   JWT Authentication
-   Pydantic
-   APScheduler
-   Scikit-Learn
-   Uvicorn

------------------------------------------------------------------------

# 2. Clean Architecture

    Client
       |
    API Routers
       |
    Controllers
       |
    Services
       |
    Repositories
       |
    Database
       |
    PostgreSQL

    ML Service accessed from Service Layer

------------------------------------------------------------------------

# 3. Project Structure

    backend/

    app/
        api/
        core/
        auth/
        models/
        schemas/
        repositories/
        services/
        ml/
        middleware/
        database/
        utils/

    tests/

    alembic/

    main.py
    requirements.txt

------------------------------------------------------------------------

# 4. Authentication

-   JWT Access Token
-   Refresh Token
-   Password Hashing (bcrypt)
-   Role Based Access Control
-   Token Expiry
-   Logout

Roles: - Admin - HR - Manager - Employee

------------------------------------------------------------------------

# 5. Repository Layer

Responsible for: - CRUD Operations - Query Optimization - Pagination -
Filtering

Each module has its own repository.

------------------------------------------------------------------------

# 6. Service Layer

Contains business logic.

Example Services:

-   EmployeeService
-   AttendanceService
-   LeaveService
-   TaskService
-   ProjectService
-   PredictionService
-   ReportService

------------------------------------------------------------------------

# 7. ML Integration

PredictionService

↓

Loads burnout_model.pkl

↓

Preprocesses employee features

↓

Returns: - Burnout Risk - Productivity Score

No external AI APIs used.

------------------------------------------------------------------------

# 8. Middleware

-   JWT Validation
-   CORS
-   Request Logging
-   Exception Handling
-   Rate Limiting

------------------------------------------------------------------------

# 9. Logging

Application logs: - Login - CRUD - Prediction Requests - Errors -
Security Events

------------------------------------------------------------------------

# 10. Configuration

Use environment variables:

DATABASE_URL

JWT_SECRET

JWT_EXPIRY

REFRESH_SECRET

MODEL_PATH

LOG_LEVEL

------------------------------------------------------------------------

# 11. Background Jobs

-   Monthly Prediction Generation
-   Attendance Summary
-   Email Reports
-   Cleanup Expired Tokens

Using APScheduler.

------------------------------------------------------------------------

# 12. Security

-   Password Hashing
-   SQL Injection Protection
-   Input Validation
-   JWT Verification
-   HTTPS Ready
-   Audit Logging

------------------------------------------------------------------------

# 13. Testing

-   Unit Tests
-   API Tests
-   Repository Tests
-   Service Tests
-   Authentication Tests

------------------------------------------------------------------------

# 14. Deployment

Docker

↓

Nginx

↓

FastAPI

↓

MySQL
PyMySQL (MySQL Driver)

Single VM or Cloud Deployment supported.
