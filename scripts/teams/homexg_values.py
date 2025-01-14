import pandas as pd

data_dict = {
    "Team": ["Arsenal", "Aston Villa", "Liverpool", "Manchester City", "Brentford", "Tottenham", "Chelsea",
             "Bournemouth", "Crystal Palace", "West Ham", "Brighton", "Newcastle United", "Fulham",
             "Manchester United", "Southampton", "Nottingham Forest", "Leicester", "Ipswich",
             "Wolverhampton Wanderers", "Everton"],
    "M": [9, 10, 9, 9, 10, 10, 9, 9, 10, 10, 9, 9, 10, 10, 9, 9, 10, 10, 9, 9],
    "xG": [22.54, 22.07, 20.74, 20.43, 20.42, 20.34, 18.93, 18.59, 17.65, 17.20,
           16.35, 15.96, 15.87, 15.82, 14.36, 14.04, 12.69, 12.00, 10.89, 10.43]
}

data = pd.DataFrame(data_dict)
data.to_csv("xg_table.csv", index=False)
print("xG data saved to 'xg_table.csv'.")

# Step 2: Read the xG data from the CSV file
data = pd.read_csv("xg_table.csv")

# Step 3: Calculate xG per game
data["xG_per_game"] = data["xG"] / data["M"]

# Step 4: Sort teams by xG_per_game
data = data.sort_values(by="xG_per_game", ascending=False).reset_index(drop=True)

# Step 5: Assign original tiers dynamically
original_tiers = []
current_tier = 1

for i in range(len(data)):
    if i == 0:
        original_tiers.append(current_tier)
        continue

    diff_above = abs(data.loc[i, "xG_per_game"] - data.loc[i - 1, "xG_per_game"])
    diff_below = abs(data.loc[i, "xG_per_game"] - data.loc[i + 1, "xG_per_game"]) if i + 1 < len(data) else float("inf")

    if diff_above <= diff_below:
        original_tiers.append(current_tier)
    else:
        current_tier += 1
        original_tiers.append(current_tier)

# Step 6: Adjust tiers for single-team tiers based on closeness
adjusted_tiers = original_tiers.copy()
tier_counts = pd.Series(original_tiers).value_counts()

for i in range(len(data)):
    if tier_counts[original_tiers[i]] == 1:  # Only adjust single-team tiers
        team_value = data.loc[i, "xG_per_game"]

        # Find the closest tier average value
        closest_tier = None
        closest_difference = float("inf")

        for tier in set(original_tiers):  # Iterate through all tiers
            if tier == original_tiers[i] or tier_counts[tier] == 1:  # Skip self and single-team tiers
                continue

            # Calculate average xG_per_game for the tier
            tier_avg = data.loc[[idx for idx, t in enumerate(original_tiers) if t == tier], "xG_per_game"].mean()
            diff = abs(team_value - tier_avg)

            if diff < closest_difference:  # Update closest tier
                closest_difference = diff
                closest_tier = tier

        # Adjust to the closest tier if the difference is within a reasonable range
        if closest_difference <= 0.1:  # Adjust the threshold as needed
            adjusted_tiers[i] = closest_tier

# Step 7: Renumber adjusted tiers sequentially to remove gaps
unique_adjusted_tiers = sorted(set(adjusted_tiers))
tier_mapping = {tier: i + 1 for i, tier in enumerate(unique_adjusted_tiers)}
adjusted_tiers = [tier_mapping[tier] for tier in adjusted_tiers]

# Step 8: Add original and adjusted tiers to the DataFrame
data["Original_Tier"] = original_tiers
data["Adjusted_Tier"] = adjusted_tiers

# Step 9: Save the updated DataFrame to a new CSV file
data.to_csv("xg_tiers_original_and_adjusted_no_gaps.csv", index=False)
print("Updated xG tiers with original and adjusted tiers saved to 'xg_tiers_original_and_adjusted_no_gaps.csv'.")