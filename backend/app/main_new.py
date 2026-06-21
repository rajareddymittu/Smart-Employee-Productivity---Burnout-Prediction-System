from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_new import router as api_router
from app.core.config import settings
from app.database.session import engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Employee Productivity API",
    description="Analytics platform for managing employee productivity and burnout prediction",
    version="1.0.0"
)

# Allow CORS for frontend
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

# Include API routes
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def on_startup():
    """Startup event - check database connection."""
    try:
        conn = engine.connect()
        conn.close()
        logger.info("Database connection successful")
    except Exception as e:
        logger.warning(f"Could not connect to DB on startup: {e}")


@app.on_event("shutdown")
def on_shutdown():
    """Shutdown event."""
    logger.info("Application shutting down")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "AI-Powered Employee Productivity API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }
