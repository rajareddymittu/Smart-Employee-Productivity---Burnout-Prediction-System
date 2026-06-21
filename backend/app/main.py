from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings
from app.database.session import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Employee Productivity API",
    description="Analytics platform for employee productivity and burnout prediction",
    version="1.0.0"
)

# Allow the local dev frontend to access the API
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def on_startup():
    try:
        conn = engine.connect()
        conn.close()
        logger.info("Database connection successful")
    except Exception as e:
        logger.warning(f"Could not connect to DB on startup: {e}")


@app.get("/")
def root():
    return {
        "name": "AI-Powered Employee Productivity API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }
