import pandas as pd  # Import pandas library for data manipulation

# Step 1: Save the away_xG data to a CSV file
away_data_dict = {  # Create a dictionary with teams, matches, and away_xG values
    "Team": ["Liverpool", "Chelsea", "Bournemouth", "Tottenham", "Arsenal", "Newcastle United", "Manchester City",
             "Fulham", "Nottingham Forest", "Manchester United", "Brighton", "Aston Villa", "Crystal Palace",
             "West Ham", "Ipswich", "Leicester", "Southampton", "Wolverhampton Wanderers", "Everton", "Brentford"],
    "M": [9, 10, 10, 9, 10, 10, 10, 9, 10, 9, 10, 9, 9, 9, 9, 9, 10, 10, 9, 9],  # Matches played
    "away_xG": [25.49, 22.25, 21.21, 19.44, 18.92, 17.33, 16.97, 14.19, 13.88, 13.67,
                13.24, 13.06, 12.99, 11.63, 10.15, 9.76, 9.55, 9.44, 9.14, 9.13]  # Away expected goals (away_xG)
}

away_data = pd.DataFrame(away_data_dict)  # Convert the dictionary to a DataFrame
away_data.to_csv("away_xg_table.csv", index=False)  # Save the DataFrame as a CSV file without the index column
print("Away xG data saved to 'away_xg_table.csv'.")  # Confirm the file is saved

# Step 2: Read the away_xG data from the CSV file
away_data = pd.read_csv("away_xg_table.csv")  # Load the CSV file into a DataFrame

# Step 3: Calculate away_xG per game
away_data["away_xG_per_game"] = away_data["away_xG"] / away_data["M"]  # Divide away_xG by matches played

# Step 4: Sort teams by away_xG_per_game
away_data = away_data.sort_values(by="away_xG_per_game", ascending=False).reset_index(drop=True)  # Sort in descending order

# Step 5: Assign original tiers dynamically
original_tiers = []  # Initialize a list to store original tier numbers
current_tier = 1  # Start with tier 1

for i in range(len(away_data)):  # Loop through all rows in the DataFrame
    if i == 0:  # For the first row, assign tier 1
        original_tiers.append(current_tier)
        continue

    # Calculate differences in away_xG_per_game with teams above and below
    diff_above = abs(away_data.loc[i, "away_xG_per_game"] - away_data.loc[i - 1, "away_xG_per_game"])
    diff_below = abs(away_data.loc[i, "away_xG_per_game"] - away_data.loc[i + 1, "away_xG_per_game"]) if i + 1 < len(away_data) else float("inf")

    if diff_above <= diff_below:  # If closer to the team above, keep the same tier
        original_tiers.append(current_tier)
    else:  # Otherwise, increment the tier
        current_tier += 1
        original_tiers.append(current_tier)

# Step 6: Adjust tiers for single-team tiers based on closeness
adjusted_tiers = original_tiers.copy()  # Make a copy of the original tiers
tier_counts = pd.Series(original_tiers).value_counts()  # Count the number of teams in each tier

for i in range(len(away_data)):  # Loop through all rows in the DataFrame
    if tier_counts[original_tiers[i]] == 1:  # Check if the tier has only one team
        team_value = away_data.loc[i, "away_xG_per_game"]  # Get the away_xG_per_game value of the team

        # Find the closest tier average value
        closest_tier = None
        closest_difference = float("inf")

        for tier in set(original_tiers):  # Iterate through all tiers
            if tier == original_tiers[i] or tier_counts[tier] == 1:  # Skip self and single-team tiers
                continue

            # Calculate average away_xG_per_game for the tier
            tier_avg = away_data.loc[[idx for idx, t in enumerate(original_tiers) if t == tier], "away_xG_per_game"].mean()
            diff = abs(team_value - tier_avg)  # Calculate the difference

            if diff < closest_difference:  # Update closest tier
                closest_difference = diff
                closest_tier = tier

        # Adjust to the closest tier if the difference is within a reasonable range
        if closest_difference <= 0.1:  # Adjust the threshold as needed
            adjusted_tiers[i] = closest_tier

# Step 7: Renumber adjusted tiers sequentially to remove gaps
unique_adjusted_tiers = sorted(set(adjusted_tiers))  # Get unique tiers in sorted order
tier_mapping = {tier: i + 1 for i, tier in enumerate(unique_adjusted_tiers)}  # Map old tier numbers to new sequential ones
adjusted_tiers = [tier_mapping[tier] for tier in adjusted_tiers]  # Update adjusted tiers with new numbers

# Step 8: Add original and adjusted tiers to the DataFrame
away_data["Original_Tier"] = original_tiers  # Add original tiers as a new column
away_data["Adjusted_Tier"] = adjusted_tiers  # Add adjusted tiers as a new column

# Step 9: Save the updated DataFrame to a new CSV file
away_data.to_csv("away_xg_tiers_original_and_adjusted_no_gaps.csv", index=False)  # Save the updated data to a CSV file
print("Updated away xG tiers with original and adjusted tiers saved to 'away_xg_tiers_original_and_adjusted_no_gaps.csv'.")  # Confirm completion