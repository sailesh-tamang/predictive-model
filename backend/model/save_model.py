"""Train the production multiclass model (H/D/A) and save artifacts.

This script trains the Flask app's deployed model using the target FTR.
It keeps preprocessing fit only on the training split to avoid leakage.
"""
import os
import json
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_recall_fscore_support, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, '..', 'EPL_cleaned.csv')
OUT_DIR = os.path.join(ROOT, 'model')
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Features used in the production web-app model (numeric match stats + crowd)
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

X = df[FEATURES].copy().fillna(0)
y = df[TARGET].copy()

label_map = {'H': 0, 'D': 1, 'A': 2}
inv_label_map = {v: k for k, v in label_map.items()}
y_num = y.map(label_map)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_num,
    test_size=0.2,
    random_state=42,
    stratify=y_num,
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Training XGBoost multiclass model (H/D/A)...")
model = XGBClassifier(
    objective='multi:softprob',
    num_class=3,
    n_estimators=200,
    learning_rate=0.05,
    use_label_encoder=False,
    eval_metric='mlogloss',
    random_state=42,
)
model.fit(X_train_scaled, y_train)

print("Evaluating production model on the hold-out set...")
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
macro_f1 = f1_score(y_test, y_pred, labels=[0, 1, 2], average='macro')
weighted_f1 = f1_score(y_test, y_pred, labels=[0, 1, 2], average='weighted')
roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='macro')

precision, recall, f1_scores, _ = precision_recall_fscore_support(
    y_test,
    y_pred,
    labels=[0, 1, 2],
    zero_division=0,
)

cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2])
metrics = {
    'model': 'XGBoost',
    'task': 'multiclass',
    'target': 'FTR',
    'classes': ['H', 'D', 'A'],
    'accuracy': float(accuracy),
    'macro_f1': float(macro_f1),
    'weighted_f1': float(weighted_f1),
    'roc_auc_macro_ovr': float(roc_auc),
    'precision': {
        'H': float(precision[0]),
        'D': float(precision[1]),
        'A': float(precision[2]),
    },
    'recall': {
        'H': float(recall[0]),
        'D': float(recall[1]),
        'A': float(recall[2]),
    },
    'f1': {
        'H': float(f1_scores[0]),
        'D': float(f1_scores[1]),
        'A': float(f1_scores[2]),
    },
    'confusion_matrix': cm.tolist(),
}

print(f"Accuracy: {accuracy:.4f}")
print(f"Macro F1: {macro_f1:.4f}")
print(f"Weighted F1: {weighted_f1:.4f}")
print(f"ROC-AUC (macro OVR): {roc_auc:.4f}")
print("Per-class metrics:")
for idx, label in enumerate(['H', 'D', 'A']):
    print(f"  {label}: precision={precision[idx]:.4f}, recall={recall[idx]:.4f}, f1={f1_scores[idx]:.4f}")
print("Confusion matrix:")
print(cm)

print("Saving artifacts...")
joblib.dump(model, os.path.join(OUT_DIR, 'model.pkl'))
joblib.dump(scaler, os.path.join(OUT_DIR, 'scaler.pkl'))
with open(os.path.join(OUT_DIR, 'features.json'), 'w') as f:
    json.dump(FEATURES, f)
with open(os.path.join(OUT_DIR, 'labels.json'), 'w') as f:
    json.dump({'label_map': label_map, 'inv_label_map': inv_label_map}, f)
with open(os.path.join(OUT_DIR, 'model_metrics.json'), 'w') as f:
    json.dump(metrics, f, indent=2)

print("Done. Saved model.pkl, scaler.pkl, features.json, labels.json, and model_metrics.json in backend/model/")
