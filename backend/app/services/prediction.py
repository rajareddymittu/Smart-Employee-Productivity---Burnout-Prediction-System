from sqlalchemy.orm import Session
from app.repositories.prediction import PredictionRepository
from app.models import Prediction
from app.schemas import PredictRequest
from app.ml.predict import predict_burnout, predict_productivity
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class PredictionService:
    def __init__(self, session: Session):
        self.repo = PredictionRepository(session)

    def create_prediction(self, employee_id: int, predict_request: PredictRequest) -> Optional[Prediction]:
        """Create a new prediction using ML model."""
        try:
            # Prepare features for ML model
            features = {
                'working_hours_per_day': predict_request.working_hours_per_day,
                'overtime_hours': predict_request.overtime_hours,
                'meeting_hours': predict_request.meeting_hours,
                'leave_count': predict_request.leave_count,
                'late_arrivals': predict_request.late_arrivals,
                'task_count': predict_request.task_count,
                'task_completion_percent': predict_request.task_completion_percent,
                'performance_rating': predict_request.performance_rating,
                'experience_years': predict_request.experience_years,
                'project_count': predict_request.project_count,
            }

            # Get predictions from ML models
            burnout_risk, burnout_score = predict_burnout(features)
            productivity_score = predict_productivity(features)

            # Store prediction in database
            prediction_dict = {
                'employee_id': employee_id,
                'burnout_risk': burnout_risk,
                'burnout_score': burnout_score,
                'productivity_score': productivity_score,
            }
            
            return self.repo.create(prediction_dict)
        except Exception as e:
            logger.error(f"Error creating prediction for employee {employee_id}: {str(e)}")
            return None

    def get_prediction(self, prediction_id: int) -> Optional[Prediction]:
        """Get prediction by ID."""
        return self.repo.get(prediction_id)

    def get_employee_latest_prediction(self, employee_id: int) -> Optional[Prediction]:
        """Get latest prediction for an employee."""
        return self.repo.get_by_employee(employee_id)

    def get_employee_prediction_history(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """Get prediction history for an employee."""
        return self.repo.get_history(employee_id, skip=skip, limit=limit)

    def get_all_predictions(self, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """Get all predictions."""
        return self.repo.get_all(skip=skip, limit=limit)
