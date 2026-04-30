import pandas as pd
import os
import shap
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(folder, "EPL_cleaned.csv"))

features = [
    "crowd_present",
    "HS", "AS",
    "HST", "AST",
    "HF", "AF",
    "HC", "AC",
    "HY", "AY",
    "HR", "AR",
]

X = df[features]
y = df["home_win"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================================================
# STEP 1: Train XGBoost model
# ================================================
print("Training XGBoost model...")
xgb = XGBClassifier(n_estimators=300, learning_rate=0.05,
                    random_state=42, eval_metric="logloss")
xgb.fit(X_train, y_train)
print("Model trained!")

# ================================================
# STEP 2: Run SHAP
# ================================================
print("\nRunning SHAP analysis...")
explainer   = shap.Explainer(xgb, X_train)
shap_values = explainer(X_test)
print("SHAP done!")

# ================================================
# STEP 3: Print crowd_present SHAP impact
# ================================================
crowd_idx   = features.index("crowd_present")
crowd_shap  = shap_values.values[:, crowd_idx]

print("\n" + "=" * 45)
print("    CROWD PRESENCE SHAP IMPACT")
print("=" * 45)
print(f"  Average SHAP value : {crowd_shap.mean():.4f}")
print(f"  When crowd = 1     : pushes prediction HIGHER by {crowd_shap[X_test['crowd_present']==1].mean():.4f}")
print(f"  When crowd = 0     : pushes prediction LOWER  by {crowd_shap[X_test['crowd_present']==0].mean():.4f}")
print("=" * 45)
print("\n  Positive value = crowd HELPS home team win")
print("  Negative value = no crowd HURTS home team win")

# ================================================
# STEP 4: Save 3 SHAP charts
# ================================================

# Chart 1: Summary plot — all features ranked by impact
print("\nSaving Chart 1 — Summary plot...")
plt.figure()
shap.summary_plot(shap_values, X_test,
                  feature_names=features, show=False)
plt.title("SHAP Summary — All Features Impact on Home Win")
plt.tight_layout()
plt.savefig(os.path.join(folder, "shap_summary.png"), dpi=150, bbox_inches="tight")
plt.close()

# Chart 2: Bar plot — average importance of each feature
print("Saving Chart 2 — Bar plot...")
plt.figure()
shap.plots.bar(shap_values, show=False)
plt.title("SHAP Feature Importance — Average Impact")
plt.tight_layout()
plt.savefig(os.path.join(folder, "shap_bar.png"), dpi=150, bbox_inches="tight")
plt.close()

# Chart 3: Crowd present vs crowd absent comparison
print("Saving Chart 3 — Crowd impact comparison...")
crowd_with    = shap_values.values[X_test["crowd_present"].values == 1, crowd_idx]
crowd_without = shap_values.values[X_test["crowd_present"].values == 0, crowd_idx]

plt.figure(figsize=(8, 5))
plt.hist(crowd_with,    bins=20, alpha=0.7,
         color="#378ADD", label="With Crowd")
plt.hist(crowd_without, bins=20, alpha=0.7,
         color="#D85A30", label="Without Crowd")
plt.axvline(crowd_with.mean(),    color="#378ADD",
            linestyle="--", linewidth=2,
            label=f"Avg with crowd: {crowd_with.mean():.3f}")
plt.axvline(crowd_without.mean(), color="#D85A30",
            linestyle="--", linewidth=2,
            label=f"Avg without crowd: {crowd_without.mean():.3f}")
plt.title("SHAP Values for Crowd Presence\n(How much crowd shifts the home win prediction)")
plt.xlabel("SHAP Value")
plt.ylabel("Number of Matches")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(folder, "shap_crowd.png"), dpi=150)
plt.close()

print("\n" + "=" * 45)
print("  ALL DONE! 3 charts saved:")
print("  1. shap_summary.png")
print("  2. shap_bar.png")
print("  3. shap_crowd.png")
print("=" * 45)