"""Train a multiclass model (H/D/A) and save artifacts.
Run this from the backend folder:

python model/save_model.py

It will produce model.pkl, scaler.pkl, and features.json in backend/model/
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, '..', 'EPL_cleaned.csv')
OUT_DIR = os.path.join(ROOT, 'model')
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Features used in the thesis (numeric match stats + crowd)
FEATURES = [
    "crowd_present",
    "HS", "AS",
    "HST", "AST",
    "HF", "AF",
    "HC", "AC",
    "HY", "AY",
    "HR", "AR",
]

TARGET = 'FTR'  # H/D/A

X = df[FEATURES].copy()
y = df[TARGET].copy()

# Map textual FTR labels to numeric classes for XGBoost
label_map = {'H': 0, 'D': 1, 'A': 2}
inv_label_map = {v: k for k, v in label_map.items()}
y_num = y.map(label_map)

# Simple preprocessing: fillna and scale numeric features
X = X.fillna(0)

scaler = StandardScaler()
X_sc = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_sc, y_num, test_size=0.2, random_state=42, stratify=y_num)

print("Training XGBoost multiclass model (H/D/A)...")
model = XGBClassifier(objective='multi:softprob', num_class=3,
                      n_estimators=200, learning_rate=0.05, use_label_encoder=False, eval_metric='mlogloss', random_state=42)
model.fit(X_train, y_train)

print("Saving artifacts...")
joblib.dump(model, os.path.join(OUT_DIR, 'model.pkl'))
joblib.dump(scaler, os.path.join(OUT_DIR, 'scaler.pkl'))
with open(os.path.join(OUT_DIR, 'features.json'), 'w') as f:
    json.dump(FEATURES, f)
with open(os.path.join(OUT_DIR, 'labels.json'), 'w') as f:
    json.dump({'label_map': label_map, 'inv_label_map': inv_label_map}, f)

print("Done. Saved model.pkl, scaler.pkl, features.json in backend/model/")
