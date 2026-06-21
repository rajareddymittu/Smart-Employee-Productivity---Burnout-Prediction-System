AI-Powered Employee Productivity Analytics & Burnout Prediction System

Overview
--------
This repository contains a full-stack prototype for employee productivity analytics and burnout prediction. It includes:
- backend: FastAPI (Python) with SQLAlchemy models, JWT auth, ML prediction service and various API endpoints
- frontend: Angular (standalone components) app used for login, dashboards, employee views, HR views
- scripts: database seeders, model training and utilities

This README documents how to install from scratch, configure a database, seed data, run ML training, start backend and frontend, and common troubleshooting steps.

Table of Contents
-----------------
- Prerequisites
- Quick start (development)
- Backend setup (detailed)
  - virtualenv
  - env vars
  - install deps
  - database connection examples
  - create tables / migrations
  - seeding the DB
  - assign managers
  - run backend server
- Frontend setup
  - install
  - run dev server (HMR)
- ML: training and artifacts
- Important scripts
- API overview (important endpoints)
- Running from scratch examples
- Troubleshooting & tips

Prerequisites
-------------
- macOS / Linux / Windows (WSL)
- Python 3.9+ (project uses 3.9 in venv but newer py3 versions should work)
- Node.js 16+ and npm or yarn for the frontend
- git
- Optional: a SQL server (MySQL, PostgreSQL) if not using the bundled SQLite dev DB

Quick start (development)
-------------------------
1. Backend: create & activate virtualenv and install deps

   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Configure environment (dev uses SQLite by default)
   - Copy `.env` from `.env.example` if needed.
   - By default, `.env` contains `DATABASE_URL=sqlite+pysqlite:///./dev.db`.

3. Create DB tables (if required) and seed data

   # From backend/ directory
   python3 -m scripts.create_tables   # if present
   python3 -m scripts.seed_roles_and_users
   python3 -m scripts.seed_data
   python3 -m scripts.assign_managers

4. Start backend

   # from backend/
   source .venv/bin/activate
   uvicorn app.main:app --reload --port 8000

5. Frontend

   cd frontend/angular-app
   npm install
   npm start   # or `ng serve` if using Angular CLI

6. Open frontend (default) at http://localhost:4200 and backend at http://127.0.0.1:8000

Backend setup — detailed
------------------------
Virtual environment
- Create and activate a venv in `backend/`:

  cd backend
  python3 -m venv .venv
  # macOS / Linux
  source .venv/bin/activate
  # Windows (PowerShell)
  # .\.venv\Scripts\Activate.ps1
  # Windows (cmd.exe)
  # .\.venv\Scripts\activate.bat

Install dependencies

  pip install -r requirements.txt

Environment variables
- The backend reads config from environment variables. See `backend/.env` or create your own `.env` file.
- Key variables (example `.env` shown below):

  # .env.example
  DATABASE_URL=sqlite+pysqlite:///./dev.db
  JWT_SECRET=replace-with-a-strong-secret
  ACCESS_TOKEN_EXPIRE_MINUTES=60
  JWT_ALGORITHM=HS256
  # Optional: comma-separated list of allowed frontend origins for CORS
  CORS_ORIGINS=http://localhost:4200

  Save your values in `backend/.env` or export them in your shell before starting the server.

Database connection examples (SQLAlchemy URL)
- SQLite (dev):
  - sqlite+pysqlite:///./dev.db
- MySQL (pymysql):
  - mysql+pymysql://user:password@localhost:3306/employee_db
- PostgreSQL (psycopg2):
  - postgresql+psycopg2://user:password@localhost:5432/employee_db

To use another DB, update `backend/.env` or export `DATABASE_URL` in your shell, then restart the backend.

Create tables / schema
- The project includes `scripts/create_tables.py` which creates tables using SQLAlchemy metadata. Run from `backend/`:

  source .venv/bin/activate
  python3 -m scripts.create_tables

Seeding the DB
- There are seed scripts under `backend/scripts/`:
  - `seed_roles_and_users.py` — creates roles (Employee, Manager, HR) and demo users
  - `seed_data.py` — creates many sample Employee rows (names, dept, joining, experience)
  - `assign_managers.py` — assigns managers (MGR001/MGR002 or found managers) round-robin to employees

Run them as modules so imports resolve correctly (run from `backend/`):

  source .venv/bin/activate
  python3 -m scripts.seed_roles_and_users
  python3 -m scripts.seed_data
  python3 -m scripts.assign_managers

Notes about running scripts
- If you see `ModuleNotFoundError: No module named 'app'` when running scripts directly, run them as modules with `-m` from the `backend/` folder (so Python adds the package root to sys.path):

  python3 -m scripts.seed_data

Assigning managers
- After seeding, run:

  python3 -m scripts.assign_managers

This will find `MGR%` employees, or create two manager records, and assign all other employees a `manager_id` in round-robin fashion.

Running the backend
-------------------
From `backend/` (with venv activated):

  uvicorn app.main:app --reload --port 8000

The API root is available at `http://127.0.0.1:8000/api`. Open interactive docs at `http://127.0.0.1:8000/docs`.

Frontend setup
--------------
1. Install dependencies and run the dev server

   cd frontend/angular-app
   npm install
   npm start

2. The dev server typically runs at `http://localhost:4200`. HMR / live reload will pick up frontend file edits.

ML: training and artifacts
-------------------------
- Training scripts are under `backend/scripts/` (e.g. `train_and_save.py` or `ml/train_model.py`) — run them inside the `backend/.venv` environment.
- The training process typically creates `models/burnout_model.pkl` and `models/scaler.pkl` in `backend/models/`.
- The API loads model artifacts at startup (see `app/ml/predict.py`). If you retrain, restart the backend to pick up new artifacts.

Important scripts (summary)
--------------------------
- `scripts/create_tables.py` — create DB schema
- `scripts/seed_roles_and_users.py` — create roles and demo users
- `scripts/seed_data.py` — seed employees (names, dept, joining_date, experience)
- `scripts/assign_managers.py` — assign `manager_id` for employees missing it
- `scripts/train_and_save.py` — generate synthetic training data and save model/scaler
- `scripts/diagnostics.py` — run simple ML diagnostics

API overview (key endpoints)
----------------------------
- `POST /api/auth/register` — create user
- `POST /api/auth/login` — login (use username + password), returns `access_token`
- `GET /api/auth/me` — get current user (requires Bearer token)

- Employees:
  - `GET /api/employees/` — HR-only list of employees
  - `GET /api/employees/{id}` — get employee detail (protected)

- Managers:
  - `GET /api/managers/{manager_id}/reportees` — manager's reportees (or HR can view)

- HR:
  - `GET /api/hr/recent-hires` — returns employees grouped by manager (includes department_name, joining_date, experience)
  - `GET /api/hr/manager-burnout` — burnout stats grouped by manager

- Worklogs:
  - `POST /api/worklogs/` — create worklog (requires auth). Employee role may only create for themselves; Managers/HR can create for others.
  - `GET /api/worklogs/employee/{employee_id}` — list worklogs for an employee (role-protected)

- Predictions:
  - `POST /api/predict/burnout` — send features to get burnout prediction (model-dependent)

API examples
------------
Login and use the token in subsequent requests (replace values as needed):

```bash
# Login (returns access_token)
curl -s -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"hr","password":"password"}' | jq

# Use the token from the login response with subsequent requests
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:8000/api/auth/me
```

Frontend notes
--------------
- The frontend stores authentication data in `sessionStorage` keys: `access_token`, `username`, `user_id`, `employee_id`, and `roles` (JSON array of role names).
- The Angular `ApiService` attaches the `Authorization: Bearer <token>` header when available.
- Login-first UI: the root page is the login component until authenticated.

How to connect to a new DB (example)
------------------------------------
1. Choose your DB (MySQL, PostgreSQL).
2. Install DB driver in backend venv (example for Postgres):

   pip install psycopg2-binary

3. Update `backend/.env` (or export env var) `DATABASE_URL` with a SQLAlchemy connection string, e.g.: 

   # PostgreSQL
   DATABASE_URL=postgresql+psycopg2://dbuser:dbpass@dbhost:5432/employee_db

   # MySQL
   DATABASE_URL=mysql+pymysql://dbuser:dbpass@dbhost:3306/employee_db

4. Ensure the database exists and user has privileges. Then run:

   source .venv/bin/activate
   python3 -m scripts.create_tables
   python3 -m scripts.seed_roles_and_users
   python3 -m scripts.seed_data
   python3 -m scripts.assign_managers

5. Start backend.

Notes about migrations and production
- This project uses SQLAlchemy metadata to create tables via a script; for production, integrate Alembic for migrations.
- Use strong `JWT_SECRET` in production and serve backend over TLS.
- Configure a production ASGI server (e.g. uvicorn + process manager or Gunicorn with uvicorn workers).

Security best practices (short)
-----------------------------
- Use a strong, unpredictable `JWT_SECRET` and keep it out of source control (use a secrets manager in production).
- Prefer storing tokens in HttpOnly, Secure cookies rather than `sessionStorage` to reduce XSS risk.
- Set reasonable `ACCESS_TOKEN_EXPIRE_MINUTES` and consider implementing a refresh-token flow.
- Enable CORS only for trusted origins (for dev: `http://localhost:4200`) and validate inputs server-side.
- Consider adding rate-limiting and basic monitoring for authentication and prediction endpoints.

Running the seeders & scripts from scratch (full example)
--------------------------------------------------------
# from project root
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# ensure .env contains a DATABASE_URL (sqlite default is fine)
python3 -m scripts.create_tables
python3 -m scripts.seed_roles_and_users
python3 -m scripts.seed_data
python3 -m scripts.assign_managers

Start backend:
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

Open frontend:
cd frontend/angular-app
npm install
npm start

Troubleshooting & common errors
------------------------------
- ModuleNotFoundError: No module named 'app' when running a script:
  - Run scripts as modules from the `backend/` directory: `python3 -m scripts.seed_data`.
  - Or set `PYTHONPATH=.` before invoking python so the `app` package is importable.

- Auth / hashing errors
  - The backend uses `passlib` CryptContext; if you see UnknownHashError, ensure the seeders / runtime use the same hashing schemes configured in `app/api/auth.py`.

- Port in use when restarting uvicorn
  - Kill existing process: `lsof -tiTCP:8000 -sTCP:LISTEN | xargs -r kill -9` or `pkill -f uvicorn` then start again.

- Frontend HMR not picking changes
  - Ensure the frontend dev server is running. If HMR doesn't reload, restart `npm start`.

Where things live (important files)
----------------------------------
- Backend: `backend/app/` — FastAPI app, models, schemas, API routes
- Backend scripts: `backend/scripts/` — seeders, training, helpers
- Frontend: `frontend/angular-app/` — Angular app, `src/app` contains components and services
- ML artifacts: `backend/models/` — model & scaler pickles used by the prediction API

If you want
-----------
- I can add an `INSTALL.md` condensed into quick commands for Unix and macOS.
- I can add a small `docker-compose.yml` for a containerized dev setup (Postgres + backend + frontend).
- I can add Alembic config and a basic migration to replace `create_tables.py` for safer schema evolution.


---
Generated by the project assistant. If you want this content split into `README.md` + `INSTALL.md` + `DEVELOPMENT.md`, tell me which split you prefer and I'll create them.