from sqlalchemy.orm import Session
from app.models import Prediction
from app.repositories.base import BaseRepository
from typing import List, Optional


class PredictionRepository(BaseRepository[Prediction]):
    def __init__(self, session: Session):
        super().__init__(session, Prediction)

    def get_by_employee(self, employee_id: int) -> Optional[Prediction]:
        """Get latest prediction for an employee."""
        return self.session.query(Prediction).filter(
            Prediction.employee_id == employee_id
        ).order_by(Prediction.predicted_on.desc()).first()

    def get_history(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """Get prediction history for an employee."""
        return self.session.query(Prediction).filter(
            Prediction.employee_id == employee_id
        ).order_by(Prediction.predicted_on.desc()).offset(skip).limit(limit).all()
