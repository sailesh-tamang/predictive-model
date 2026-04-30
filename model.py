import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(folder, "EPL_cleaned.csv"))

# ================================================
# STEP 1: Define features and target
# ================================================
features = [
    "crowd_present",   # your KEY variable
    "HS", "AS",        # shots
    "HST", "AST",      # shots on target
    "HF", "AF",        # fouls
    "HC", "AC",        # corners
    "HY", "AY",        # yellow cards
    "HR", "AR",        # red cards
]

X = df[features]
y = df["home_win"]

print(f"STEP 1 done — Features: {X.shape[1]}, Samples: {X.shape[0]}")

# ================================================
# STEP 2: Split into train and test
# 80% train, 20% test
# ================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"STEP 2 done — Train: {len(X_train)} rows, Test: {len(X_test)} rows")

# ================================================
# STEP 3: Scale the data
# ================================================
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

print(f"STEP 3 done — Data scaled")

# ================================================
# STEP 4: Train 3 models
# ================================================
print(f"\nSTEP 4 — Training models...")

# Model 1: Logistic Regression
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train_sc, y_train)
print(f"  Logistic Regression trained")

# Model 2: Random Forest
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
print(f"  Random Forest trained")

# Model 3: XGBoost
xgb = XGBClassifier(n_estimators=300, learning_rate=0.05,
                    random_state=42, eval_metric="logloss")
xgb.fit(X_train, y_train)
print(f"  XGBoost trained")

# ================================================
# STEP 5: Evaluate all 3 models
# ================================================
print(f"\n=== STEP 5: MODEL RESULTS ===\n")

models = {
    "Logistic Regression": (lr, X_test_sc),
    "Random Forest"      : (rf, X_test),
    "XGBoost"            : (xgb, X_test),
}

for name, (model, X_eval) in models.items():
    preds = model.predict(X_eval)
    proba = model.predict_proba(X_eval)[:, 1]
    acc   = accuracy_score(y_test, preds)
    auc   = roc_auc_score(y_test, proba)
    print(f"--- {name} ---")
    print(f"Accuracy : {acc:.3f}")
    print(f"AUC-ROC  : {auc:.3f}")
    print(classification_report(y_test, preds,
          target_names=["No Win", "Home Win"]))