from fastapi import APIRouter
from app.schemas import PredictRequest
from app.ml.predict import load_burnout_model, predict_burnout

router = APIRouter(prefix="/predict", tags=["predict"])


@router.on_event("startup")
def _load_ml_models():
    # load models into cache (ml.predict module handles caching)
    load_burnout_model()


@router.post("/burnout")
def predict_endpoint(req: PredictRequest):
    features = {
        "working_hours_per_day": req.working_hours_per_day,
        "overtime_hours": req.overtime_hours,
        "meeting_hours": req.meeting_hours,
        "leave_count": req.leave_count,
        "late_arrivals": req.late_arrivals,
        "task_completion_percent": req.task_completion_percent,
        "performance_rating": req.performance_rating,
    }
    risk, score = predict_burnout(features)
    return {"employee_id": req.employee_id, "burnout_risk": risk, "burnout_score": score}
