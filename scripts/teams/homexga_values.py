import pandas as pd  # Import pandas for data manipulation

# Step 1: Load the new dataset
data = {
    "Team": [
        "Arsenal", "Aston Villa", "Liverpool", "Nottingham Forest", "Bournemouth",
        "Newcastle United", "Fulham", "Chelsea", "Manchester City", "Brighton",
        "Brentford", "Everton", "Wolverhampton Wanderers", "Manchester United",
        "Crystal Palace", "Tottenham", "Leicester", "Ipswich", "West Ham", "Southampton"
    ],
    "M": [9, 10, 9, 9, 9, 9, 10, 9, 9, 9, 10, 9, 9, 10, 10, 10, 9, 9, 10, 10],
    "home_xGA": [
        6.23, 8.73, 8.79, 9.03, 10.79, 11.03, 11.67, 12.53, 12.75, 13.09,
        14.35, 14.89, 15.61, 15.94, 16.76, 18.18, 19.42, 21.46, 23.05, 26.98
    ]
}

df = pd.DataFrame(data)

# Step 2: Calculate xGA per game
df["home_xGA_per_game"] = df["home_xGA"] / df["M"]  # xGA divided by games played

# Step 3: Assign Original Tiers
# Sort teams by xGA_per_game
df = df.sort_values("home_xGA_per_game").reset_index(drop=True)

# Assign original tiers based on proximity to adjacent teams
df["Original_Tier"] = 1
for i in range(1, len(df)):
    if df.loc[i, "home_xGA_per_game"] - df.loc[i - 1, "home_xGA_per_game"] > (
        df.loc[i + 1, "home_xGA_per_game"] - df.loc[i, "home_xGA_per_game"]
        if i + 1 < len(df) else float("inf")
    ):
        df.loc[i:, "Original_Tier"] += 1

# Step 4: Adjust Tiers to Avoid Single-Team Tiers
df["Adjusted_Tier"] = df["Original_Tier"]  # Start with original tiers
tier_counts = df["Original_Tier"].value_counts()

for tier in df["Original_Tier"].unique():
    if tier_counts[tier] == 1:  # Check for single-team tiers
        team_index = df[df["Original_Tier"] == tier].index[0]
        above_tier = tier - 1
        below_tier = tier + 1

        # Determine where to merge the single-team tier
        if above_tier in tier_counts and below_tier in tier_counts:
            if abs(
                df.loc[team_index, "home_xGA_per_game"] - df[df["Original_Tier"] == above_tier]["home_xGA_per_game"].mean()
            ) < abs(
                df.loc[team_index, "home_xGA_per_game"] - df[df["Original_Tier"] == below_tier]["home_xGA_per_game"].mean()
            ):
                df.loc[team_index, "Adjusted_Tier"] = above_tier
            else:
                df.loc[team_index, "Adjusted_Tier"] = below_tier
        elif above_tier in tier_counts:
            df.loc[team_index, "Adjusted_Tier"] = above_tier
        elif below_tier in tier_counts:
            df.loc[team_index, "Adjusted_Tier"] = below_tier

# Reorder Adjusted_Tier to have no gaps
unique_adjusted_tiers = sorted(df["Adjusted_Tier"].unique())
tier_mapping = {old: new for new, old in enumerate(unique_adjusted_tiers, 1)}
df["Adjusted_Tier"] = df["Adjusted_Tier"].map(tier_mapping)

# Step 5: Save Results to a CSV
df.to_csv("home_xga_tiers_original_and_adjusted.csv", index=False)
print("Results saved to 'home_xga_tiers_original_and_adjusted.csv'")