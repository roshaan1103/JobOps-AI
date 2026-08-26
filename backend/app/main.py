from fastapi import FastAPI

from app.core.config import get_settings
from app.db.health import check_database_connection


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="AI-powered job search and application automation platform.",
)


@app.get("/")
def root():
    return {
        "application": settings.app_name,
        "version": "0.1.0",
        "environment": settings.app_env,
        "message": "JobOps AI backend is running.",
    }


@app.get("/health")
def health():
    database_ok = check_database_connection()

    return {
        "status": "ok" if database_ok else "degraded",
        "database": "connected" if database_ok else "unavailable",
    }