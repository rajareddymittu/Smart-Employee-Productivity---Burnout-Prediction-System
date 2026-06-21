# Backend (FastAPI)

Quick start:

1. Copy `.env.example` to `.env` and update values.
2. Create a Python virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app:

```bash
uvicorn app.main:app --reload --port 8000
```

Notes:
- Database is configured for MySQL via `DATABASE_URL` using `pymysql`.
- Use Alembic for migrations (not scaffolded here yet).
