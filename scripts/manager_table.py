import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Load API key from environment variable
API_KEY = os.getenv("SPORTMONKS_API_KEY")
if not API_KEY:
    raise ValueError("SPORTMONKS_API_KEY environment variable not set.")

BASE_URL = "https://api.sportmonks.com/v3/football"

# Function to fetch leagues
def fetch_leagues():
    url = f"{BASE_URL}/leagues?api_token={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        leagues = response.json()["data"]
        for league in leagues:
            print(f"ID: {league['id']}, Name: {league['name']}")
        return leagues
    else:
        print(f"Error fetching leagues: {response.status_code}")
        print(f"Response content: {response.text}")
        return []

# Function to fetch fixtures by date range
def fetch_fixtures_by_date_range(start_date, end_date, league_id):
    url = f"{BASE_URL}/fixtures/between/{start_date}/{end_date}?api_token={API_KEY}&filters[league_id]={league_id}&include=localTeam,visitorTeam"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching fixtures: {response.status_code}")
        print(f"Response content: {response.text}")
        return []

# Function to process fixtures into a DataFrame
def process_fixtures(fixtures):
    fixture_list = []
    for fixture in fixtures:
        local_team = fixture.get("localTeam", {}).get("data", {}).get("name")
        visitor_team = fixture.get("visitorTeam", {}).get("data", {}).get("name")
        fixture_list.append({
            "Fixture Name": fixture["name"],
            "Home Team": local_team,
            "Away Team": visitor_team,
            "Home Score": fixture.get("scores", {}).get("localteam_score"),
            "Away Score": fixture.get("scores", {}).get("visitorteam_score"),
            "League ID": fixture["league_id"],
            "Season ID": fixture["season_id"],
            "Match Date": fixture["starting_at"]
        })
    return pd.DataFrame(fixture_list)

# Function to split date range into chunks of 100 days
def split_date_range(start_date, end_date, max_days=100):
    date_chunks = []
    current_start = start_date
    while current_start < end_date:
        current_end = min(current_start + timedelta(days=max_days), end_date)
        date_chunks.append((current_start, current_end))
        current_start = current_end + timedelta(days=1)
    return date_chunks

# Main script
if __name__ == "__main__":
    # Confirm League ID for the Premier League (run fetch_leagues() if unsure)
    LEAGUE_ID = 8  # Replace with correct ID after confirmation

    # Define the season year and date range for the 2024/25 Premier League season
    season_year = 2024
    START_DATE = datetime.strptime(f"{season_year}-08-01", "%Y-%m-%d")
    END_DATE = datetime.strptime(f"{season_year + 1}-05-31", "%Y-%m-%d")

    # Split the date range into chunks of 100 days
    date_ranges = split_date_range(START_DATE, END_DATE)

    # Fetch fixtures for each date range within the Premier League
    all_fixtures = []
    for start, end in date_ranges:
        print(f"Fetching fixtures for Premier League between {start.date()} and {end.date()}")
        fixtures = fetch_fixtures_by_date_range(start.date(), end.date(), LEAGUE_ID)
        all_fixtures.extend(fixtures)

    # Process and save the results
    if all_fixtures:
        df_fixtures = process_fixtures(all_fixtures)
        print(df_fixtures.head())  # Display first few rows
        df_fixtures.to_csv("premier_league_fixtures_2024_25.csv", index=False)  # Save to CSV
        print("Premier League fixtures for the 2024/25 season saved to premier_league_fixtures_2024_25.csv")
    else:
        print("No fixtures found for the Premier League within the specified date range.")
