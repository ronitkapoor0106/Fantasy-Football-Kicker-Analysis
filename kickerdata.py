import requests
from bs4 import BeautifulSoup

# Base URL with a placeholder for the week number
base_url = "https://www.fftoday.com/stats/playerstats.php?Season=2022&GameWeek={}&PosID=80&LeagueID="

all_kicker_data = []

# Loop through weeks 5 to 18
for week in range(5, 19):
    url = base_url.format(week)

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all rows in the table
    rows = soup.find_all('tr')

    # Loop through each row
    for row in rows:
        # Find all <td> elements in the row
        columns = row.find_all('td')

        if len(columns) > 0 and columns[0].get('align') == 'LEFT':
            # Extract kicker's name from the first <td>
            kicker_name_tag = columns[0].find('a')
            if kicker_name_tag:
                kicker_name = kicker_name_tag.text.strip()

                # Extract team from the second <td>
                team = columns[1].text.strip()

                # Extract fantasy points from the <td> with bgcolor="#e0e0e0"
                fantasy_points_tag = row.find('td', bgcolor="#e0e0e0")
                if fantasy_points_tag:
                    fantasy_points = fantasy_points_tag.text.strip()

                    # Store the kicker's data
                    all_kicker_data.append({
                        'Week': week,
                        'Kicker Name': kicker_name,
                        'Team': team,
                        'Fantasy Points': fantasy_points
                    })

# Print the extracted kicker data
for data in all_kicker_data:
    print(data)
