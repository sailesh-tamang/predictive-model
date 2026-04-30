import pandas as pd
import os
import matplotlib.pyplot as plt

folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(folder, "EPL_cleaned.csv"))

# ================================================
# STEP 1: Home win rate per team WITH crowd
# ================================================
with_crowd    = df[df["crowd_present"] == 1]
without_crowd = df[df["crowd_present"] == 0]

with_rate = with_crowd.groupby("HomeTeam")["home_win"].mean() * 100
without_rate = without_crowd.groupby("HomeTeam")["home_win"].mean() * 100

# ================================================
# STEP 2: Combine and calculate drop
# ================================================
team_df = pd.DataFrame({
    "With Crowd %"   : with_rate,
    "Without Crowd %": without_rate,
}).dropna()  # only keep teams that appear in both periods

team_df["Drop %"] = team_df["With Crowd %"] - team_df["Without Crowd %"]
team_df = team_df.sort_values("Drop %", ascending=False)

# ================================================
# STEP 3: Print results
# ================================================
print("=" * 60)
print("   TEAM BY TEAM CROWD IMPACT ON HOME WIN RATE")
print("=" * 60)
print(f"{'Team':<20} {'With Crowd':>12} {'No Crowd':>10} {'Drop':>8}")
print("-" * 60)

for team, row in team_df.iterrows():
    drop_str = f"{row['Drop %']:+.1f}%"
    print(f"{team:<20} {row['With Crowd %']:>10.1f}%  "
          f"{row['Without Crowd %']:>8.1f}%  {drop_str:>8}")

print("=" * 60)
print(f"\nMost affected team  : {team_df.index[0]} "
      f"({team_df['Drop %'].iloc[0]:+.1f}%)")
print(f"Least affected team : {team_df.index[-1]} "
      f"({team_df['Drop %'].iloc[-1]:+.1f}%)")

# ================================================
# STEP 4: Home goals per team WITH vs WITHOUT crowd
# ================================================
home_goals_with    = with_crowd.groupby("HomeTeam")["FTHG"].mean()
home_goals_without = without_crowd.groupby("HomeTeam")["FTHG"].mean()

goals_df = pd.DataFrame({
    "Goals With Crowd"   : home_goals_with,
    "Goals Without Crowd": home_goals_without,
}).dropna()

goals_df["Goal Drop"] = goals_df["Goals With Crowd"] - \
                        goals_df["Goals Without Crowd"]
goals_df = goals_df.sort_values("Goal Drop", ascending=False)

print("\n" + "=" * 60)
print("   TEAM BY TEAM GOAL SCORING IMPACT")
print("=" * 60)
print(f"{'Team':<20} {'With Crowd':>12} {'No Crowd':>10} {'Drop':>8}")
print("-" * 60)

for team, row in goals_df.iterrows():
    drop_str = f"{row['Goal Drop']:+.2f}"
    print(f"{team:<20} {row['Goals With Crowd']:>10.2f}  "
          f"{row['Goals Without Crowd']:>8.2f}  {drop_str:>8}")

print("=" * 60)

# ================================================
# STEP 5: Chart 1 — Top 10 most affected teams
# ================================================
top10 = team_df.head(10)
bot5  = team_df.tail(5)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Left chart — most affected
colors_top = ["#D85A30" if x > 0 else "#378ADD"
              for x in top10["Drop %"]]
bars = axes[0].barh(top10.index[::-1],
                    top10["Drop %"][::-1],
                    color=colors_top[::-1])
axes[0].axvline(0, color="black", linewidth=0.8)
axes[0].set_title("Top 10 Most Affected Teams\n(Home Win Rate Drop Without Crowd)",
                  fontweight="bold")
axes[0].set_xlabel("Drop in Home Win Rate (%)")
for bar, val in zip(bars, top10["Drop %"][::-1]):
    axes[0].text(bar.get_width() + 0.3,
                 bar.get_y() + bar.get_height() / 2,
                 f"{val:+.1f}%", va="center", fontsize=9)

# Right chart — with vs without side by side for big 6
big6 = ["Man City", "Liverpool", "Chelsea",
        "Arsenal", "Man United", "Tottenham"]
big6_df = team_df[team_df.index.isin(big6)]

x      = range(len(big6_df))
width  = 0.35
axes[1].bar([i - width/2 for i in x],
            big6_df["With Crowd %"],
            width, label="With Crowd", color="#378ADD")
axes[1].bar([i + width/2 for i in x],
            big6_df["Without Crowd %"],
            width, label="Without Crowd", color="#D85A30")
axes[1].set_xticks(list(x))
axes[1].set_xticklabels(big6_df.index, rotation=15)
axes[1].set_title("Big 6 Teams — Home Win Rate\nWith vs Without Crowd",
                  fontweight="bold")
axes[1].set_ylabel("Home Win Rate (%)")
axes[1].legend()

plt.suptitle("Team-Level Crowd Impact — Premier League 2018-2022",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(folder, "team_analysis.png"), dpi=150)
plt.close()

# ================================================
# STEP 6: Chart 2 — All teams bubble chart
# ================================================
plt.figure(figsize=(12, 7))
colors = ["#D85A30" if d > 0 else "#378ADD"
          for d in team_df["Drop %"]]
plt.scatter(team_df["With Crowd %"],
            team_df["Without Crowd %"],
            c=colors, s=120, alpha=0.8)

# Label each dot with team name
for team, row in team_df.iterrows():
    plt.annotate(team,
                 (row["With Crowd %"], row["Without Crowd %"]),
                 textcoords="offset points",
                 xytext=(6, 4), fontsize=8)

# Diagonal line — if team is on this line, crowd made no difference
min_val = min(team_df["With Crowd %"].min(),
              team_df["Without Crowd %"].min()) - 5
max_val = max(team_df["With Crowd %"].max(),
              team_df["Without Crowd %"].max()) + 5
plt.plot([min_val, max_val], [min_val, max_val],
         "k--", linewidth=1, label="No crowd effect line")

plt.xlabel("Home Win Rate WITH Crowd (%)")
plt.ylabel("Home Win Rate WITHOUT Crowd (%)")
plt.title("Every Team: Home Win Rate With vs Without Crowd\n"
          "(Teams below diagonal line = hurt by crowd removal)",
          fontweight="bold")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(folder, "team_scatter.png"), dpi=150)
plt.close()

print("\nCharts saved:")
print("  team_analysis.png")
print("  team_scatter.png")
print("\nDone!")