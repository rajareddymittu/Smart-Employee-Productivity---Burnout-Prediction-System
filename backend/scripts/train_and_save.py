#!/usr/bin/env python
import os
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)
BURNOUT_MODEL_PATH = os.path.join(MODEL_DIR, 'burnout_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

FEATURE_ORDER = [
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

print('Generating synthetic training data...')

def gen_sample(r):
    return {
        'working_hours_per_day': round(r.uniform(6,10),2),
        'overtime_hours': round(r.uniform(0,12),2),
        'meeting_hours': round(r.uniform(0,6),2),
        'leave_count': r.randint(0,15),
        'late_arrivals': r.randint(0,30),
        'task_count': r.randint(1,30),
        'task_completion_percent': round(r.uniform(10,100),2),
        'performance_rating': round(r.uniform(1.0,5.0),2),
        'experience_years': round(r.uniform(0.0,20.0),2),
        'project_count': r.randint(0,12),
    }

# Label function: higher overtime, late_arrivals and low perf/task completion => higher burnout risk

def label_from_features(feat):
    # scale features into comparable ranges
    ot = feat['overtime_hours'] / 12.0
    tc = feat['task_completion_percent'] / 100.0
    pr = feat['performance_rating'] / 5.0
    la = feat['late_arrivals'] / 30.0
    score = 0.5*ot - 0.4*tc - 0.3*pr + 0.2*la
    # add noise
    score += random.uniform(-0.05, 0.05)
    if score > 0.15:
        return 2  # High
    if score > -0.05:
        return 1  # Medium
    return 0  # Low

# create dataset
N = 5000
rng = random.Random(42)
X = []
y = []
for i in range(N):
    s = gen_sample(rng)
    feat_vector = [s[f] for f in FEATURE_ORDER]
    X.append(feat_vector)
    y.append(label_from_features(s))

X = np.array(X)
y = np.array(y)

print('Distribution of labels:', dict(zip(*np.unique(y, return_counts=True))))

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale
scaler = StandardScaler()
scaler.fit(X_train)
X_train_s = scaler.transform(X_train)
X_test_s = scaler.transform(X_test)

# Train
print('Training RandomForestClassifier...')
clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1, class_weight='balanced')
clf.fit(X_train_s, y_train)

# Evaluate
y_pred = clf.predict(X_test_s)
acc = accuracy_score(y_test, y_pred)
print(f'Validation accuracy: {acc:.4f}')
print('Classification report:')
print(classification_report(y_test, y_pred))

# Save
print(f'Saving model to {BURNOUT_MODEL_PATH} and scaler to {SCALER_PATH}')
joblib.dump(clf, BURNOUT_MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)
print('Done')
