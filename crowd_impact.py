import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import matplotlib.pyplot as plt

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
# ANALYSIS 1: Home win rate WITH vs WITHOUT crowd
# ================================================
with_crowd    = df[df["crowd_present"] == 1]["home_win"].mean() * 100
without_crowd = df[df["crowd_present"] == 0]["home_win"].mean() * 100
difference    = with_crowd - without_crowd

print("=" * 45)
print("    CROWD IMPACT ON HOME WIN RATE")
print("=" * 45)
print(f"  With crowd        : {with_crowd:.1f}% home wins")
print(f"  Without crowd     : {without_crowd:.1f}% home wins")
print(f"  Difference        : {difference:.1f}% drop without crowd")
print("=" * 45)

# ================================================
# ANALYSIS 2: Average goals WITH vs WITHOUT crowd
# ================================================
home_goals_with    = df[df["crowd_present"] == 1]["FTHG"].mean()
home_goals_without = df[df["crowd_present"] == 0]["FTHG"].mean()
away_goals_with    = df[df["crowd_present"] == 1]["FTAG"].mean()
away_goals_without = df[df["crowd_present"] == 0]["FTAG"].mean()

print("\n    GOALS COMPARISON")
print("=" * 45)
print(f"  Home goals WITH crowd    : {home_goals_with:.2f} per game")
print(f"  Home goals WITHOUT crowd : {home_goals_without:.2f} per game")
print(f"  Away goals WITH crowd    : {away_goals_with:.2f} per game")
print(f"  Away goals WITHOUT crowd : {away_goals_without:.2f} per game")
print("=" * 45)

# ================================================
# ANALYSIS 3: Yellow cards WITH vs WITHOUT crowd
# (referee bias check)
# ================================================
hy_with    = df[df["crowd_present"] == 1]["HY"].mean()
hy_without = df[df["crowd_present"] == 0]["HY"].mean()
ay_with    = df[df["crowd_present"] == 1]["AY"].mean()
ay_without = df[df["crowd_present"] == 0]["AY"].mean()

print("\n    REFEREE BIAS CHECK (YELLOW CARDS)")
print("=" * 45)
print(f"  Home yellows WITH crowd    : {hy_with:.2f} per game")
print(f"  Home yellows WITHOUT crowd : {hy_without:.2f} per game")
print(f"  Away yellows WITH crowd    : {ay_with:.2f} per game")
print(f"  Away yellows WITHOUT crowd : {ay_without:.2f} per game")
print("=" * 45)

# ================================================
# ANALYSIS 4: Feature importance from Random Forest
# (shows how important crowd_present is)
# ================================================
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

importance = pd.DataFrame({
    "Feature"   : features,
    "Importance": rf.feature_importances_
}).sort_values("Importance", ascending=False)

print("\n    FEATURE IMPORTANCE RANKING")
print("=" * 45)
for i, row in importance.iterrows():
    bar = "█" * int(row["Importance"] * 200)
    print(f"  {row['Feature']:<15} {row['Importance']:.4f}  {bar}")
print("=" * 45)

# ================================================
# ANALYSIS 5: Save chart
# ================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Chart 1: Win rate
axes[0].bar(["With Crowd", "Without Crowd"],
            [with_crowd, without_crowd],
            color=["#378ADD", "#D85A30"])
axes[0].set_title("Home Win Rate (%)")
axes[0].set_ylabel("Win Rate %")
for i, v in enumerate([with_crowd, without_crowd]):
    axes[0].text(i, v + 0.5, f"{v:.1f}%", ha="center", fontweight="bold")

# Chart 2: Goals
x = np.arange(2)
axes[1].bar(x - 0.2, [home_goals_with, home_goals_without], 0.4,
            label="Home Goals", color="#378ADD")
axes[1].bar(x + 0.2, [away_goals_with, away_goals_without], 0.4,
            label="Away Goals", color="#D85A30")
axes[1].set_xticks(x)
axes[1].set_xticklabels(["With Crowd", "Without Crowd"])
axes[1].set_title("Average Goals Per Game")
axes[1].legend()

# Chart 3: Feature importance
top5 = importance.head(5)
axes[2].barh(top5["Feature"], top5["Importance"], color="#1D9E75")
axes[2].set_title("Top 5 Feature Importance")
axes[2].set_xlabel("Importance Score")
axes[2].invert_yaxis()

plt.suptitle("Crowd Impact on Home Field Advantage — Premier League",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(folder, "crowd_impact.png"), dpi=150)
print("\nChart saved as crowd_impact.png in your EPL_Data folder!") 