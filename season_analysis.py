import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(folder, "EPL_cleaned.csv"))

# ================================================
# STEP 1: Season by season home win rate
# ================================================
print("=" * 60)
print("   SEASON BY SEASON ANALYSIS")
print("=" * 60)

seasons = ["2018_19", "2019_20", "2020_21", "2021_22"]
season_labels = ["2018/19\n(Normal)", "2019/20\n(COVID hit)", 
                 "2020/21\n(Ghost)", "2021/22\n(Fans back)"]

results = []

for season in seasons:
    s = df[df["season"] == season]
    
    home_win_rate  = s["home_win"].mean() * 100
    avg_home_goals = s["FTHG"].mean()
    avg_away_goals = s["FTAG"].mean()
    avg_home_shots = s["HST"].mean()
    avg_away_shots = s["AST"].mean()
    avg_home_yell  = s["HY"].mean()
    avg_away_yell  = s["AY"].mean()
    total_matches  = len(s)
    ghost_matches  = (s["crowd_present"] == 0).sum()

    results.append({
        "season"        : season,
        "home_win_rate" : home_win_rate,
        "home_goals"    : avg_home_goals,
        "away_goals"    : avg_away_goals,
        "home_shots"    : avg_home_shots,
        "away_shots"    : avg_away_shots,
        "home_yellows"  : avg_home_yell,
        "away_yellows"  : avg_away_yell,
        "total_matches" : total_matches,
        "ghost_matches" : ghost_matches,
    })

    print(f"\n  Season       : {season}")
    print(f"  Total matches: {total_matches}")
    print(f"  Ghost matches: {ghost_matches}")
    print(f"  Home win rate: {home_win_rate:.1f}%")
    print(f"  Home goals   : {avg_home_goals:.2f} per game")
    print(f"  Away goals   : {avg_away_goals:.2f} per game")
    print(f"  Home yellows : {avg_home_yell:.2f} per game")
    print(f"  Away yellows : {avg_away_yell:.2f} per game")
    print("-" * 60)

res = pd.DataFrame(results)

# ================================================
# STEP 2: Home advantage index per season
# (home win rate minus away win rate)
# ================================================
print("\n" + "=" * 60)
print("   HOME ADVANTAGE INDEX PER SEASON")
print("   (Home wins % minus Away wins %)")
print("=" * 60)

for season in seasons:
    s = df[df["season"] == season]
    home_win  = (s["FTR"] == "H").mean() * 100
    away_win  = (s["FTR"] == "A").mean() * 100
    draw      = (s["FTR"] == "D").mean() * 100
    hfa_index = home_win - away_win
    print(f"\n  {season}")
    print(f"  Home wins : {home_win:.1f}%")
    print(f"  Away wins : {away_win:.1f}%")
    print(f"  Draws     : {draw:.1f}%")
    print(f"  HFA Index : {hfa_index:+.1f}  "
          f"{'← GHOST SEASON' if season == '2020_21' else ''}")

print("=" * 60)

# ================================================
# STEP 3: Save charts
# ================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

win_rates   = [r["home_win_rate"] for r in results]
home_goals  = [r["home_goals"]    for r in results]
away_goals  = [r["away_goals"]    for r in results]
home_yell   = [r["home_yellows"]  for r in results]
away_yell   = [r["away_yellows"]  for r in results]

# Ghost season color highlight
colors = ["#378ADD", "#EF9F27", "#D85A30", "#378ADD"]

# Chart 1 — Home win rate per season
axes[0,0].bar(season_labels, win_rates, color=colors)
axes[0,0].set_title("Home Win Rate Per Season", fontweight="bold")
axes[0,0].set_ylabel("Win Rate %")
axes[0,0].set_ylim(0, 60)
for i, v in enumerate(win_rates):
    axes[0,0].text(i, v + 0.5, f"{v:.1f}%",
                   ha="center", fontweight="bold")
axes[0,0].axhspan(0, 60, alpha=0.05)

# Chart 2 — Home vs Away goals per season
x     = np.arange(len(seasons))
width = 0.35
axes[0,1].bar(x - width/2, home_goals, width,
              label="Home Goals", color="#378ADD")
axes[0,1].bar(x + width/2, away_goals, width,
              label="Away Goals", color="#D85A30")
axes[0,1].set_title("Home vs Away Goals Per Season",
                     fontweight="bold")
axes[0,1].set_ylabel("Average Goals Per Game")
axes[0,1].set_xticks(x)
axes[0,1].set_xticklabels(season_labels)
axes[0,1].legend()
for i, (h, a) in enumerate(zip(home_goals, away_goals)):
    axes[0,1].text(i - width/2, h + 0.02, f"{h:.2f}",
                   ha="center", fontsize=8)
    axes[0,1].text(i + width/2, a + 0.02, f"{a:.2f}",
                   ha="center", fontsize=8)

# Chart 3 — Yellow cards per season
axes[1,0].plot(season_labels, home_yell, "o-",
               color="#378ADD", linewidth=2,
               markersize=8, label="Home Yellows")
axes[1,0].plot(season_labels, away_yell, "s-",
               color="#D85A30", linewidth=2,
               markersize=8, label="Away Yellows")
axes[1,0].set_title("Yellow Cards Per Season\n(Referee Bias Indicator)",
                     fontweight="bold")
axes[1,0].set_ylabel("Average Yellow Cards Per Game")
axes[1,0].legend()
axes[1,0].grid(axis="y", alpha=0.3)
for i, (h, a) in enumerate(zip(home_yell, away_yell)):
    axes[1,0].text(i, h + 0.02, f"{h:.2f}",
                   ha="center", fontsize=8, color="#378ADD")
    axes[1,0].text(i, a + 0.02, f"{a:.2f}",
                   ha="center", fontsize=8, color="#D85A30")

# Chart 4 — HFA index per season
hfa_vals = []
for season in seasons:
    s   = df[df["season"] == season]
    hw  = (s["FTR"] == "H").mean() * 100
    aw  = (s["FTR"] == "A").mean() * 100
    hfa_vals.append(hw - aw)

bar_colors = ["#378ADD", "#EF9F27", "#D85A30", "#378ADD"]
axes[1,1].bar(season_labels, hfa_vals, color=bar_colors)
axes[1,1].axhline(0, color="black", linewidth=0.8)
axes[1,1].set_title("Home Field Advantage Index Per Season\n"
                     "(Home wins % minus Away wins %)",
                     fontweight="bold")
axes[1,1].set_ylabel("HFA Index")
for i, v in enumerate(hfa_vals):
    axes[1,1].text(i, v + 0.3, f"{v:+.1f}",
                   ha="center", fontweight="bold")

# Ghost season label on all charts
for ax in axes.flat:
    ax.annotate("Ghost\nSeason", xy=(2, 0),
                xycoords=("data", "axes fraction"),
                xytext=(2, 0.05),
                fontsize=7, color="#D85A30",
                ha="center")

plt.suptitle("Season by Season Crowd Impact — Premier League 2018-2022",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(folder, "season_analysis.png"), dpi=150)
plt.close()

print("\nChart saved as season_analysis.png")
print("\nDone!")