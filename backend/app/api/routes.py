from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.employees_new import router as employees_router
from app.api.attendance import router as attendance_router
from app.api.leaves import router as leaves_router
from app.api.tasks import router as tasks_router
from app.api.projects import router as projects_router
from app.api.predictions_endpoints import router as predictions_router
from app.api.predictions import router as predict_router
from app.api.worklogs import router as worklogs_router
from app.api.hr import router as hr_router
from app.api.managers import router as managers_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(employees_router)
router.include_router(attendance_router)
router.include_router(leaves_router)
router.include_router(tasks_router)
router.include_router(projects_router)
router.include_router(predictions_router)
router.include_router(predict_router)
router.include_router(worklogs_router)
router.include_router(hr_router)
router.include_router(managers_router)


@router.get("/health")
def health():
    return {"status": "ok"}
