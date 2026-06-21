from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.employees_new import router as employees_router
from app.api.attendance import router as attendance_router
from app.api.leaves import router as leaves_router
from app.api.tasks import router as tasks_router
from app.api.projects import router as projects_router
from app.api.predictions_endpoints import router as predictions_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(employees_router)
router.include_router(attendance_router)
router.include_router(leaves_router)
router.include_router(tasks_router)
router.include_router(projects_router)
router.include_router(predictions_router)


@router.get("/health")
def health():
    return {"status": "ok"}
