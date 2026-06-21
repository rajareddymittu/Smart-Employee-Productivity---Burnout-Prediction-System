"""
ML Model Training Script
Generates synthetic data and trains burnout and productivity prediction models
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

def generate_synthetic_data(n_records=10000):
    """Generate synthetic employee data for training."""
    
    print(f"Generating {n_records} synthetic employee records...")
    
    data = {
        'employee_id': range(1, n_records + 1),
        'age': np.random.randint(22, 65, n_records),
        'experience_years': np.random.uniform(0, 40, n_records),
        'department': np.random.choice(['IT', 'HR', 'Finance', 'Sales', 'Operations'], n_records),
        'working_hours_per_day': np.random.uniform(6, 12, n_records),
        'overtime_hours': np.random.exponential(2, n_records),
        'meeting_hours': np.random.uniform(0, 8, n_records),
        'leave_count': np.random.randint(0, 30, n_records),
        'late_arrivals': np.random.randint(0, 20, n_records),
        'task_count': np.random.randint(1, 50, n_records),
        'task_completion_percent': np.random.uniform(30, 100, n_records),
        'performance_rating': np.random.uniform(1, 5, n_records),
        'project_count': np.random.randint(0, 10, n_records),
        'work_from_home_days': np.random.randint(0, 5, n_records),
    }
    
    df = pd.DataFrame(data)
    
    # Create target variables based on features (with some randomness)
    # Burnout Risk: High if overtime + meetings are high and task completion is low
    burnout_score = (
        (df['overtime_hours'] / 10) * 0.3 +
        (df['meeting_hours'] / 8) * 0.3 +
        (1 - df['task_completion_percent'] / 100) * 0.2 +
        (df['late_arrivals'] / 20) * 0.2 +
        np.random.normal(0, 0.1, n_records)
    )
    burnout_score = np.clip(burnout_score, 0, 1)
    df['burnout_label'] = np.where(burnout_score < 0.33, 0, 
                                   np.where(burnout_score < 0.66, 1, 2))
    
    # Productivity Score: High if task completion is high and performance rating is high
    productivity_score = (
        (df['task_completion_percent'] / 100) * 40 +
        (df['performance_rating'] / 5) * 30 +
        (1 - df['overtime_hours'] / 10) * 15 +
        (1 - df['meeting_hours'] / 8) * 15 +
        np.random.normal(0, 5, n_records)
    )
    df['productivity_score'] = np.clip(productivity_score, 0, 100)
    
    # Encode categorical variables
    df['department_encoded'] = pd.factorize(df['department'])[0]
    
    return df


def prepare_features(df):
    """Prepare features for model training."""
    
    print("Preparing features...")
    
    feature_columns = [
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
    
    X = df[feature_columns].copy()
    
    # Handle any missing values
    X = X.fillna(X.mean())
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, X.columns.tolist(), scaler


def train_burnout_model(X, y, test_size=0.2):
    """Train burnout classification model."""
    
    print("Training burnout classification model...")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"\nBurnout Model Performance:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    
    # Feature importance
    print("\nTop 5 Important Features (Burnout):")
    feature_importance = sorted(
        zip(model.feature_importances_, ['working_hours_per_day', 'overtime_hours', 'meeting_hours', 
                                        'leave_count', 'late_arrivals', 'task_count', 
                                        'task_completion_percent', 'performance_rating', 
                                        'experience_years', 'project_count']),
        reverse=True
    )
    for importance, feature in feature_importance[:5]:
        print(f"  {feature}: {importance:.4f}")
    
    return model


def train_productivity_model(X, y, test_size=0.2):
    """Train productivity regression model."""
    
    print("\nTraining productivity regression model...")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nProductivity Model Performance:")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE:  {mae:.4f}")
    print(f"  R²:   {r2:.4f}")
    
    # Feature importance
    print("\nTop 5 Important Features (Productivity):")
    feature_importance = sorted(
        zip(model.feature_importances_, ['working_hours_per_day', 'overtime_hours', 'meeting_hours', 
                                        'leave_count', 'late_arrivals', 'task_count', 
                                        'task_completion_percent', 'performance_rating', 
                                        'experience_years', 'project_count']),
        reverse=True
    )
    for importance, feature in feature_importance[:5]:
        print(f"  {feature}: {importance:.4f}")
    
    return model


def save_models(burnout_model, productivity_model, scaler, model_dir='./models'):
    """Save trained models to disk."""
    
    print(f"\nSaving models to {model_dir}...")
    
    os.makedirs(model_dir, exist_ok=True)
    
    burnout_path = os.path.join(model_dir, 'burnout_model.pkl')
    productivity_path = os.path.join(model_dir, 'productivity_model.pkl')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    
    joblib.dump(burnout_model, burnout_path)
    joblib.dump(productivity_model, productivity_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"  Burnout model saved to {burnout_path}")
    print(f"  Productivity model saved to {productivity_path}")
    print(f"  Scaler saved to {scaler_path}")


def main():
    """Main training pipeline."""
    
    print("=" * 60)
    print("ML Model Training Pipeline")
    print(f"Started at: {datetime.now()}")
    print("=" * 60)
    
    # Generate data
    df = generate_synthetic_data(n_records=10000)
    print(f"Generated dataset shape: {df.shape}")
    
    # Prepare features
    X, feature_names, scaler = prepare_features(df)
    
    # Train models
    burnout_model = train_burnout_model(X, df['burnout_label'])
    productivity_model = train_productivity_model(X, df['productivity_score'])
    
    # Save models
    save_models(burnout_model, productivity_model, scaler)
    
    print("\n" + "=" * 60)
    print(f"Training completed at: {datetime.now()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
