from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.prediction import PredictionService
from app.schemas import PredictRequest, PredictionOut
from app.auth.dependencies import get_current_active_user
from typing import List

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/burnout", response_model=PredictionOut, status_code=201)
def predict_burnout(
    employee_id: int,
    predict_req: PredictRequest,
    db: Session = Depends(get_db)
):
    """Generate burnout and productivity predictions for an employee."""
    service = PredictionService(db)
    try:
        prediction = service.create_prediction(employee_id, predict_req)
        if not prediction:
            raise HTTPException(status_code=500, detail="Prediction failed")
        return prediction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{prediction_id}", response_model=PredictionOut)
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Get prediction by ID."""
    service = PredictionService(db)
    prediction = service.get_prediction(prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction


@router.get("/employee/{employee_id}/latest", response_model=PredictionOut)
def get_latest_prediction(employee_id: int, db: Session = Depends(get_db)):
    """Get latest prediction for an employee."""
    service = PredictionService(db)
    prediction = service.get_employee_latest_prediction(employee_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="No predictions found for this employee")
    return prediction


@router.get("/employee/{employee_id}/history", response_model=List[PredictionOut])
def get_prediction_history(
    employee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get prediction history for an employee."""
    service = PredictionService(db)
    predictions = service.get_employee_prediction_history(employee_id, skip=skip, limit=limit)
    return predictions


@router.get("/", response_model=List[PredictionOut])
def list_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all predictions."""
    service = PredictionService(db)
    predictions = service.get_all_predictions(skip=skip, limit=limit)
    return predictions
