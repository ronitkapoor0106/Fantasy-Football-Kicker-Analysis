import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Base URL of the page to scrape
base_url = "https://www.nflweather.com/week/2022/week-"

# Mapping of full team names to abbreviations
team_abbreviations = {
    "Rams": "LAR",
    "Bills": "BUF",
    "Falcons": "ATL",
    "Saints": "NO",
    "Bears": "CHI",
    "49ers": "SF",
    "Bengals": "CIN",
    "Steelers": "PIT",
    "Lions": "DET",
    "Eagles": "PHI",
    "Dolphins": "MIA",
    "Patriots": "NE",
    "Jets": "NYJ",
    "Ravens": "BAL",
    "Washington": "WAS",
    "Jaguars": "JAC",
    "Panthers": "CAR",
    "Browns": "CLE",
    "Texans": "HOU",
    "Colts": "IND",
    "Titans": "TEN",
    "Giants": "NYG",
    "Vikings": "MIN",
    "Packers": "GB",
    "Cardinals": "ARI",
    "Chiefs": "KC",
    "Chargers": "LAC",
    "Raiders": "LV",
    "Cowboys": "DAL",
    "Buccaneers": "TB",
    "Seahawks": "SEA",
    "Broncos": "DEN"
}

# Function to scrape data for a given week
def scrape_week(week_number):
    url = f"{base_url}{week_number}"
    print(f"Scraping data for week {week_number}...")

    try:
        # Send a GET request to the page
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
    except requests.RequestException as e:
        print(f"Error fetching the page for week {week_number}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize lists to store the team names and wind speeds
    games = []

    # Find all game containers using the correct class name
    game_containers = soup.find_all('div', class_='game-box w-100 d-flex flex-column flex-lg-row align-items-center shadow-box rounded my-2 py-1')

    for container in game_containers:
        try:
            # Extract team names
            away_team_span = container.find('span', class_='fw-bold')
            home_team_span = container.find('span', class_='fw-bold ms-1')

            away_team = away_team_span.text.strip() if away_team_span else "Unknown"
            home_team = home_team_span.text.strip() if home_team_span else "Unknown"

            # Convert to abbreviation
            away_team_abbr = team_abbreviations.get(away_team, away_team)
            home_team_abbr = team_abbreviations.get(home_team, home_team)

            # Extract wind speed
            wind_div = container.find('div', class_='text-break col-md-2 mb-1 px-1 flex-centered')
            if wind_div:
                # Extract and clean the wind speed text
                wind_text = wind_div.get_text(separator=' ').strip()
                wind_text = wind_text.replace('\xa0', ' ')  # Replace non-breaking space with regular space
                # Extract the numerical part of the wind speed using regex
                wind_speed_match = re.search(r'(\d+)\s*mph', wind_text)
                wind_speed = wind_speed_match.group(1) if wind_speed_match else "N/A"
            else:
                wind_speed = "N/A"  # In case wind speed is not available

            # Append formatted result with week number
            games.append({
                'week': week_number,
                'home_team': home_team_abbr,
                'away_team': away_team_abbr,
                'wind_speed': wind_speed
            })

        except Exception as e:
            print(f"Error processing container for week {week_number}: {e}")

    return games

# Scrape data for weeks 5 to 18
all_games = []
for week in range(5, 19):  # Weeks 5 to 18 inclusive
    week_games = scrape_week(week)
    all_games.extend(week_games)
