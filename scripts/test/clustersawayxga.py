import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Step 1: Define data as a dictionary
data_dict = {
    "Liverpool": {"away_xGA": 9.07, "games_played": 9},
    "Arsenal": {"away_xGA": 14.18, "games_played": 11},
    "Fulham": {"away_xGA": 12.24, "games_played": 9},
    "Nottingham Forest": {"away_xGA": 15.68, "games_played": 11},
    "Tottenham": {"away_xGA": 14.17, "games_played": 9},
    "Bournemouth": {"away_xGA": 16.37, "games_played": 10},
    "Crystal Palace": {"away_xGA": 15.04, "games_played": 9},
    "Manchester United": {"away_xGA": 17.97, "games_played": 10},
    "Newcastle United": {"away_xGA": 17.82, "games_played": 11},
    "Everton": {"away_xGA": 18.15, "games_played": 10},
    "Brighton": {"away_xGA": 17.34, "games_played": 10},
    "Wolverhampton Wanderers": {"away_xGA": 17.55, "games_played": 10},
    "Chelsea": {"away_xGA": 19.08, "games_played": 11},
    "Manchester City": {"away_xGA": 18.25, "games_played": 10},
    "West Ham": {"away_xGA": 18.93, "games_played": 10},
    "Southampton": {"away_xGA": 21.76, "games_played": 10},
    "Aston Villa": {"away_xGA": 19.90, "games_played": 9},
    "Brentford": {"away_xGA": 20.35, "games_played": 10},
    "Ipswich": {"away_xGA": 25.80, "games_played": 10},
    "Leicester": {"away_xGA": 26.32, "games_played": 10},
}

# Step 2: Create DataFrame
df = pd.DataFrame.from_dict(data_dict, orient="index").reset_index()
df.columns = ["Team", "Away_xGA", "Games_Played"]
df["Away_xGA_per_Game"] = df["Away_xGA"] / df["Games_Played"]

# Step 3: Assign default tiers (based on clustering or initial logic)
df = df.sort_values(by="Away_xGA_per_Game").reset_index(drop=True)
threshold = 0.2
tiers = []
current_tier = 1
first_value = df.loc[0, "Away_xGA_per_Game"]

for i, row in df.iterrows():
    if row["Away_xGA_per_Game"] - first_value <= threshold:
        tiers.append(current_tier)
    else:
        current_tier += 1
        tiers.append(current_tier)
        first_value = row["Away_xGA_per_Game"]

df["Tier"] = tiers

# Step 4: Visualize the initial plot
plt.figure(figsize=(14, 10))

# Assign colors dynamically
unique_tiers = df["Tier"].unique()
colors = plt.cm.RdYlGn_r((df["Tier"] - 1) / (unique_tiers.max() - 1))
color_map = dict(zip(df["Tier"], colors))

# Plot data points
plt.scatter(
    df["Away_xGA_per_Game"],
    df["Team"],
    c=df["Tier"].map(color_map),  # Map tier to color
    s=100,
    edgecolor="black"
)
for i, row in df.iterrows():
    plt.text(row["Away_xGA_per_Game"] + 0.02, row["Team"], f"{row['Away_xGA_per_Game']:.2f}", fontsize=8, va="center")

# Create a legend with tiers and team names
tier_summary = df.groupby("Tier")["Team"].apply(list).reset_index()
legend_elements = [
    Patch(
        facecolor=color_map[tier["Tier"]],
        edgecolor="black",
        label=f"Tier {tier['Tier']}: {', '.join(tier['Team'])}"
    )
    for _, tier in tier_summary.iterrows()
]

plt.legend(
    handles=legend_elements,
    loc="lower right",
    bbox_to_anchor=(1.0, 0.0),
    title="Tiers (Initial)",
    fontsize=8,
    title_fontsize=10,
    frameon=True
)

# Customize the plot
plt.xlabel("Away xGA per Game")
plt.ylabel("Teams")
plt.title("Clusters of Teams Based on Away xGA per Game (Initial)")
plt.grid(axis="x", linestyle="--", alpha=0.6)

# Save the plot
initial_output_file = "clusters_away_xga_initial.png"
plt.savefig(initial_output_file, bbox_inches="tight")
plt.show(block=False)

# Step 5: Export tiers for manual adjustment
csv_file = "tiers_for_editing.csv"
df.to_csv(csv_file, index=False)
print(f"Tiers exported to '{csv_file}'. Please edit the 'Tier' column and save.")

# Step 6: Re-import edited tiers and re-visualize
input("Once you've updated the CSV file, press Enter to re-import and visualize...")
df = pd.read_csv(csv_file)

# Step 5: Create a scatter plot with tiers
plt.figure(figsize=(14, 10))

# Generate a green-to-red color gradient
unique_tiers = df["Tier"].unique()
unique_tiers.sort()  # Ensure consistent tier ordering
color_map = {tier: plt.cm.RdYlGn(1 - (tier - 1) / (len(unique_tiers) - 1)) for tier in unique_tiers}

# Plot data points
plt.scatter(
    df["Away_xGA_per_Game"],
    df["Team"],
    c=df["Tier"].map(color_map),  # Map tier to color
    s=100,
    edgecolor="black"
)
for i, row in df.iterrows():
    plt.text(row["Away_xGA_per_Game"] + 0.02, row["Team"], f"{row['Away_xGA_per_Game']:.2f}", fontsize=8, va="center")

# Create a legend with tiers and team names
tier_summary = df.groupby("Tier")["Team"].apply(list).reset_index()
legend_elements = [
    Patch(
        facecolor=color_map[tier["Tier"]],
        edgecolor="black",
        label=f"Tier {tier['Tier']}: {', '.join(tier['Team'])}"
    )
    for _, tier in tier_summary.iterrows()
]

plt.legend(
    handles=legend_elements,
    loc="lower right",
    bbox_to_anchor=(1.0, 0.0),
    title="Tiers (Updated)",
    fontsize=8,
    title_fontsize=10,
    frameon=True
)

# Customize the plot
plt.xlabel("Away xGA per Game")
plt.ylabel("Teams")
plt.title("Clusters of Teams Based on Away xGA per Game (Updated)")
plt.grid(axis="x", linestyle="--", alpha=0.6)

# Save the plot
output_file = "clusters_away_xga_updated.png"
plt.savefig(output_file, bbox_inches="tight")
plt.show(block=False)  # Non-blocking mode

# Notify the user
print(f"Updated plot saved as '{output_file}'")