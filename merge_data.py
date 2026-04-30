import pandas as pd
import os

# This automatically uses whatever folder you opened in VS Code
folder = os.path.dirname(os.path.abspath(__file__))

# Load all 4 files
files = {
    "2018_19": "EPL_2018_19.csv",
    "2019_20": "EPL_2019_20.csv",
    "2020_21": "EPL_2020_21.csv",
    "2021_22": "EPL_2021_22.csv",
}

dfs = []
for season, filename in files.items():
    path = os.path.join(folder, filename)
    df = pd.read_csv(path, encoding="latin1")
    df["season"] = season
    dfs.append(df)
    print(f"Loaded {filename} — {len(df)} matches")

# Merge all 4 into one big file
master = pd.concat(dfs, ignore_index=True)

# Save inside your EPL_Data folder
output_path = os.path.join(folder, "EPL_master.csv")
master.to_csv(output_path, index=False)

print(f"\nDone! Total matches: {len(master)}")
print(f"Saved as EPL_master.csv in your EPL_Data folder")