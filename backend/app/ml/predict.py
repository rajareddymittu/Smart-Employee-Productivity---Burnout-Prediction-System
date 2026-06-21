import joblib
import os
import numpy as np
from typing import Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)

BURNOUT_MODEL_PATH = os.getenv("BURNOUT_MODEL_PATH", "./models/burnout_model.pkl")
PRODUCTIVITY_MODEL_PATH = os.getenv("PRODUCTIVITY_MODEL_PATH", "./models/productivity_model.pkl")
SCALER_PATH = os.getenv("SCALER_PATH", "./models/scaler.pkl")

# Global model cache
_burnout_model = None
_productivity_model = None
_scaler = None


def load_burnout_model():
    """Load burnout prediction model."""
    global _burnout_model
    if _burnout_model is None:
        try:
            if os.path.exists(BURNOUT_MODEL_PATH):
                _burnout_model = joblib.load(BURNOUT_MODEL_PATH)
                logger.info("Burnout model loaded successfully")
            else:
                logger.warning(f"Burnout model not found at {BURNOUT_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Error loading burnout model: {str(e)}")
    return _burnout_model


def load_productivity_model():
    """Load productivity prediction model."""
    global _productivity_model
    if _productivity_model is None:
        try:
            if os.path.exists(PRODUCTIVITY_MODEL_PATH):
                _productivity_model = joblib.load(PRODUCTIVITY_MODEL_PATH)
                logger.info("Productivity model loaded successfully")
            else:
                logger.warning(f"Productivity model not found at {PRODUCTIVITY_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Error loading productivity model: {str(e)}")
    return _productivity_model


def load_scaler():
    """Load feature scaler."""
    global _scaler
    if _scaler is None:
        try:
            if os.path.exists(SCALER_PATH):
                _scaler = joblib.load(SCALER_PATH)
                logger.info("Scaler loaded successfully")
            else:
                logger.warning(f"Scaler not found at {SCALER_PATH}")
        except Exception as e:
            logger.error(f"Error loading scaler: {str(e)}")
    return _scaler


def preprocess_features(features: Dict) -> np.ndarray:
    """Preprocess features for model prediction."""
    # Feature order must match training order
    feature_order = [
        'working_hours_per_day',
        'overtime_hours',
        'meeting_hours',
        'leave_count',
        'late_arrivals',
        'task_count',
        'task_completion_percent',
        'performance_rating',
        'experience_years',
        'project_count',
    ]
    
    values = []
    for feature in feature_order:
        values.append(features.get(feature, 0))
    
    X = np.array(values).reshape(1, -1)
    
    # Scale features if scaler is available
    scaler = load_scaler()
    if scaler is not None:
        X = scaler.transform(X)
    
    return X


def predict_burnout(features: Dict) -> Tuple[str, float]:
    """
    Predict employee burnout risk.
    
    Returns:
        Tuple of (burnout_risk_category, burnout_score)
        burnout_risk_category: 'Low', 'Medium', 'High'
        burnout_score: probability score (0-1)
    """
    try:
        model = load_burnout_model()
        
        if model is None:
            logger.warning("Burnout model not available, returning default prediction")
            return "Unknown", 0.5
        
        # Preprocess features
        X = preprocess_features(features)
        
        # Get prediction
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        
        # Map numeric prediction to category
        burnout_categories = ['Low', 'Medium', 'High']
        burnout_risk = burnout_categories[int(prediction)] if int(prediction) < len(burnout_categories) else 'Unknown'
        burnout_score = float(np.max(probabilities))
        
        return burnout_risk, burnout_score
    except Exception as e:
        logger.error(f"Error in burnout prediction: {str(e)}")
        return "Unknown", 0.5


def predict_productivity(features: Dict) -> float:
    """
    Predict employee productivity score.
    
    Returns:
        Productivity score (0-100)
    """
    try:
        model = load_productivity_model()
        
        if model is None:
            logger.warning("Productivity model not available, returning default prediction")
            return 50.0
        
        # Preprocess features
        X = preprocess_features(features)
        
        # Get prediction
        prediction = model.predict(X)[0]
        
        # Ensure score is between 0-100
        productivity_score = float(np.clip(prediction, 0, 100))
        
        return productivity_score
    except Exception as e:
        logger.error(f"Error in productivity prediction: {str(e)}")
        return 50.0
