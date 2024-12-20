import requests
import pandas as pd

# API endpoint
url = "https://api.sportmonks.com/v3/football/teams/seasons/23614?api_token=87tF6xvnn4P1TmWks5F5MUN0k7zq15EuixDD3xYcnOqL6HRPiyhqlZoSNrMY"

# Fetch data
response = requests.get(url)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data['data'])  # Adjust the key to match your JSON structure

# Export to CSV
df.to_csv("football_teams.csv", index=False)
print("Table exported successfully!")