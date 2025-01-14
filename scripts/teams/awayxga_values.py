import pandas as pd  # Importing pandas library to work with DataFrame

# Step 1: Define data
data = {
    "Team": [
        "Liverpool", "Fulham", "Arsenal", "Nottingham Forest", "Tottenham", "Crystal Palace", 
        "Manchester United", "Everton", "Bournemouth", "Newcastle United", "West Ham", 
        "Brighton", "Wolverhampton Wanderers", "Chelsea", "Manchester City", 
        "Aston Villa", "Brentford", "Southampton", "Ipswich", "Leicester"
    ],
    "M": [9, 9, 10, 10, 9, 9, 9, 9, 10, 10, 9, 10, 10, 10, 10, 9, 9, 10, 9, 9],
    "Away_xGA": [
        9.07, 12.24, 12.41, 13.78, 14.17, 15.04, 15.11, 15.54, 16.37, 16.81, 
        16.95, 17.34, 17.55, 17.80, 18.25, 19.90, 20.10, 21.76, 23.14, 23.98
    ],
}

# Step 2: Create DataFrame
df = pd.DataFrame(data)

# Step 3: Calculate xGA per game
df["xGA_per_Game"] = df["Away_xGA"] / df["M"]

# Step 4: Sort DataFrame by xGA per game
df = df.sort_values("xGA_per_Game").reset_index(drop=True)

# Step 5: Assign original tiers
tiers = []  # Start with an empty list for tiers
for i in range(len(df)):  # Iterate through each team to assign tiers
    if i == 0:  # First row
        tiers.append(1)  # Always start with tier 1 for the first row
    elif i == 1:  # Second row
        # Compare only with the first row
        if abs(df.loc[i, "xGA_per_Game"] - df.loc[i - 1, "xGA_per_Game"]) > 0.05:
            tiers.append(tiers[-1] + 1)  # Start a new tier
        else:
            tiers.append(tiers[-1])  # Keep in the same tier
    else:  # General case for rows beyond the second
        if abs(df.loc[i, "xGA_per_Game"] - df.loc[i - 1, "xGA_per_Game"]) > abs(df.loc[i - 1, "xGA_per_Game"] - df.loc[i - 2, "xGA_per_Game"]):
            tiers.append(tiers[-1] + 1)  # Start a new tier
        else:
            tiers.append(tiers[-1])  # Keep in the same tier

df["Original_Tier"] = tiers  # Add the original tier assignments to the DataFrame

# Step 6: Adjust tiers to remove gaps
adjusted_tiers = {}
current_tier = 1
for original_tier in sorted(set(tiers)):  # Iterate through unique tiers
    adjusted_tiers[original_tier] = current_tier
    current_tier += 1

df["Adjusted_Tier"] = df["Original_Tier"].map(adjusted_tiers)

# Step 7: Save the final DataFrame to CSV
output_file = "away_xga_tiers_original_and_adjusted.csv"
df.to_csv(output_file, index=False)

# Step 8: Print confirmation message
print(f"The table has been successfully created and saved as '{output_file}'.")