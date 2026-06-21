import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os


def generate_synthetic(n=2000):
    rng = np.random.default_rng(123)
    data = {
        'working_hours_per_day': rng.normal(8, 1.5, n).clip(4, 12),
        'overtime_hours': rng.exponential(1.0, n).clip(0, 8),
        'meeting_hours': rng.normal(2, 1, n).clip(0, 8),
        'leave_count': rng.integers(0, 10, n),
        'late_arrivals': rng.integers(0, 20, n),
        'task_completion_percent': rng.uniform(40, 100, n),
        'performance_rating': rng.uniform(1, 5, n),
    }
    df = pd.DataFrame(data)
    # simple heuristic for burnout label
    score = (df['overtime_hours'] * 1.5 + df['meeting_hours'] * 0.5 + df['late_arrivals'] * 0.3 - df['task_completion_percent'] * 0.02 + (5 - df['performance_rating']) * 1.0)
    df['burnout_label'] = pd.cut(score, bins=[-999, 2, 6, 999], labels=['Low', 'Medium', 'High'])
    df['productivity_score'] = (df['task_completion_percent'] * 0.6 + (df['performance_rating'] / 5.0) * 40 - df['overtime_hours'] * 2).clip(0, 100)
    return df


def train_and_save(out_dir='models'):
    os.makedirs(out_dir, exist_ok=True)
    df = generate_synthetic()
    X = df[['working_hours_per_day', 'overtime_hours', 'meeting_hours', 'leave_count', 'late_arrivals', 'task_completion_percent', 'performance_rating']]
    y = df['burnout_label']
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    acc = accuracy_score(y, clf.predict(X))
    print("Train accuracy (on same data):", acc)
    model_path = os.path.join(out_dir, 'burnout_model.pkl')
    joblib.dump(clf, model_path)
    print("Saved model to", model_path)


if __name__ == '__main__':
    train_and_save()
