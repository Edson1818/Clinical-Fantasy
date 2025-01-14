import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Step 1: Define data
data = {
    "Team": [
        "Liverpool", "Arsenal", "Fulham", "Nottingham Forest", "Tottenham",
        "Bournemouth", "Crystal Palace", "Manchester United", "Newcastle United",
        "Everton", "Brighton", "Wolverhampton Wanderers", "Chelsea",
        "Manchester City", "West Ham", "Southampton", "Aston Villa", "Brentford",
        "Ipswich", "Leicester"
    ],
    "Away_xGA_per_Game": [
        1.008, 1.241, 1.360, 1.378, 1.574, 1.637, 1.671, 1.511, 1.681,
        1.727, 1.734, 1.755, 1.780, 1.825, 1.883, 2.176, 2.211, 2.233,
        2.314, 2.664
    ]
}

# Step 2: Create DataFrame
df = pd.DataFrame(data)
df = df.sort_values(by="Away_xGA_per_Game").reset_index(drop=True)

# Step 3: Automatically assign tiers based on proximity criteria
tiers = []
current_tier = 1
for i in range(len(df)):
    if i == 0:  # First team starts with Tier 1
        tiers.append(current_tier)
    else:
        # Compare proximity to teams above and below
        if i == len(df) - 1 or abs(df.loc[i, "Away_xGA_per_Game"] - df.loc[i - 1, "Away_xGA_per_Game"]) <= abs(
            df.loc[i, "Away_xGA_per_Game"] - df.loc[i + 1, "Away_xGA_per_Game"]
        ):
            tiers.append(current_tier)  # Same tier if closer to team above
        else:
            current_tier += 1
            tiers.append(current_tier)  # New tier if closer to team below

df["Tier"] = tiers

# Step 4: Create a scatter plot with table
plt.figure(figsize=(14, 10))

# Plot data points
colors = plt.cm.RdYlGn(1 - df["Tier"] / df["Tier"].max())  # Green-to-Red gradient
plt.scatter(df["Away_xGA_per_Game"], df["Team"], c=colors, s=100, edgecolor="black")
for i, row in df.iterrows():
    plt.text(row["Away_xGA_per_Game"] + 0.02, row["Team"], f"{row['Away_xGA_per_Game']:.2f}", fontsize=8, va="center")

# Create the legend with tiers
tier_summary = df.groupby("Tier")["Team"].apply(list).reset_index()
legend_elements = [
    Patch(
        facecolor=plt.cm.RdYlGn(1 - tier["Tier"] / df["Tier"].max()), 
        edgecolor="black", 
        label=f"Tier {tier['Tier']}: {', '.join(tier['Team'])}"
    )
    for _, tier in tier_summary.iterrows()
]

plt.legend(
    handles=legend_elements,
    loc="lower right",
    bbox_to_anchor=(1.0, 0.0),
    title="Tiers",
    fontsize=8,
    title_fontsize=10,
    frameon=True
)

# Customize the plot
plt.xlabel("Away xGA per Game")
plt.ylabel("Teams")
plt.title("Clusters of Teams Based on Away xGA per Game")
plt.grid(axis="x", linestyle="--", alpha=0.6)

# Save the plot
output_file = "plot_7_away_xga_without_percentiles.png"
plt.savefig(output_file, bbox_inches="tight")
plt.show()

# Print confirmation message
print(f"Plot saved as '{output_file}'")