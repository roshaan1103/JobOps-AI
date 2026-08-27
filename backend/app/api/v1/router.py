from fastapi import APIRouter

from app.api.v1.candidate import router as candidate_router
from app.api.v1 import experience
from app.api.v1 import project

api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(candidate_router)
api_router.include_router(experience.router)
api_router.include_router(project.router)