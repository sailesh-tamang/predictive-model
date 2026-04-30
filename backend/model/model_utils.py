import os
import json
import joblib
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(ROOT, 'model')

def load_artifacts(model_path=None, scaler_path=None, features_path=None):
    model_path = model_path or os.path.join(MODEL_DIR, 'model.pkl')
    scaler_path = scaler_path or os.path.join(MODEL_DIR, 'scaler.pkl')
    features_path = features_path or os.path.join(MODEL_DIR, 'features.json')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Run model/save_model.py first.")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None
    with open(features_path, 'r') as f:
        features = json.load(f)

    labels_path = os.path.join(MODEL_DIR, 'labels.json')
    labels = None
    if os.path.exists(labels_path):
        with open(labels_path, 'r') as f:
            labels = json.load(f)

    return model, scaler, features, labels

def prepare_input(payload, features, scaler=None):
    """Given a JSON payload with feature values, return numpy array suitable for model."""
    row = []
    for f in features:
        # Expect numeric values; if missing, default to 0
        val = payload.get(f, 0)
        try:
            row.append(float(val))
        except Exception:
            row.append(0.0)

    arr = pd.DataFrame([row], columns=features)
    if scaler is not None:
        arr = scaler.transform(arr)
        return pd.DataFrame(arr, columns=features)
    return arr
