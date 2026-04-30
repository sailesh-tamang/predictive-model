import pandas as pd
import os

folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(folder, "EPL_master.csv"), encoding="latin1")

# ================================================
# STEP 1: Keep only the columns we need
# ================================================
columns_to_keep = [
    "Date",        # match date
    "HomeTeam",    # home team name
    "AwayTeam",    # away team name
    "FTHG",        # full time home goals
    "FTAG",        # full time away goals
    "FTR",         # full time result (H/D/A)
    "HS",          # home shots
    "AS",          # away shots
    "HST",         # home shots on target
    "AST",         # away shots on target
    "HF",          # home fouls
    "AF",          # away fouls
    "HC",          # home corners
    "AC",          # away corners
    "HY",          # home yellow cards
    "AY",          # away yellow cards
    "HR",          # home red cards
    "AR",          # away red cards
    "Referee",     # referee name
    "season",      # season label we added
]

df = df[columns_to_keep]
print(f"STEP 1 done — columns reduced to {df.shape[1]}")

# ================================================
# STEP 2: Fix the date column
# ================================================
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
print(f"STEP 2 done — dates fixed")

# ================================================
# STEP 3: Create crowd_present column
# Ghost games: 17 June 2020 to 23 May 2021
# 0 = no crowd, 1 = crowd present
# ================================================
df["crowd_present"] = (~df["Date"].between("2020-06-17", "2021-05-23")).astype(int)
print(f"STEP 3 done — crowd column created")
print(f"  Matches WITH crowd:    {df['crowd_present'].sum()}")
print(f"  Matches WITHOUT crowd: {(df['crowd_present'] == 0).sum()}")

# ================================================
# STEP 4: Create target variable
# home_win: 1 = home team won, 0 = draw or away win
# ================================================
df["home_win"] = (df["FTR"] == "H").astype(int)
print(f"\nSTEP 4 done — target variable created")
print(f"  Home wins:     {df['home_win'].sum()}")
print(f"  Draws/Away wins: {(df['home_win'] == 0).sum()}")

# ================================================
# STEP 5: Create extra useful columns
# ================================================
df["goal_diff"] = df["FTHG"] - df["FTAG"]        # home goal difference
df["total_goals"] = df["FTHG"] + df["FTAG"]      # total goals in match
df["total_yellow"] = df["HY"] + df["AY"]         # total yellow cards
df["total_shots"] = df["HS"] + df["AS"]          # total shots

print(f"STEP 5 done — extra columns created")

# ================================================
# STEP 6: Check for missing values
# ================================================
missing = df.isnull().sum()
print(f"\nSTEP 6 — Missing values check:")
print(missing[missing > 0] if missing.any() else "  No missing values!")

# ================================================
# STEP 7: Save cleaned file
# ================================================
output = os.path.join(folder, "EPL_cleaned.csv")
df.to_csv(output, index=False)

print(f"\n=== ALL DONE ===")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")
print(f"Saved as: EPL_cleaned.csv")
print(f"\nFirst 3 rows preview:")
print(df.head(3).to_string())