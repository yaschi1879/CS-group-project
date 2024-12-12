import sys
import os

# Add the parent directory to the system path so Python can find other modules in the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests # Library for making HTTP requests

def get_stadium_name(club_id):
    #returns stadium name, if this information is missing, it returns false
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/profile"
    response = requests.get(url)
    club_info = response.json()
    stadium_name = club_info.get("stadiumName", "n.a.")
    return stadium_name



def get_club_players(club_id, season_id="2024"):
   # Returns a list of player IDs for the club, defaulting to the current season
    # club_id as an integer, season_id as a string
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/players"
    response = requests.get(url, season_id)
    club_players = response.json()
    club_players = club_players["players"]
    club_player_id = []
    for players in club_players:
        club_player_id.append(players["id"])
    return club_player_id


def get_filter_criteria(player_id):
    # Returns market value in millions as a float, e.g., 10.34, with value in Euros
    # If no market value is available, returns "not_available"
    # Returns age as an integer; player_id is an integer
    # Gets a player's market value and age. Converts value to millions if applicable.

    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    player_profile = response.json()
    if "marketValue" in player_profile:
        market_value = player_profile["marketValue"].replace("€", "")
        if "m" in market_value:
            market_value = float(market_value.replace("m", ""))
        elif "k" in market_value:
            market_value = float(market_value.replace("k", "")) / 1000
    else:
        market_value = "n.a."
    age = int(player_profile["age"])
    return [market_value, age]


def get_club_name_user_input(club_name):
    # Searches for a club by name and returns its ID and official name.
    # Item 0 returns the correct club ID
    # Item 1 returns the correct club name
    # club_name as a string

    url = f"https://transfermarkt-api.fly.dev/clubs/search/{club_name}"
    response = requests.get(url)
    clubs = response.json()["results"]
    if not clubs:
        return ["n.a.", "n.a."]
    
    return [clubs[0]["id"], clubs[0]["name"]]


def get_player_name_user_input(player_name):
    # Searches for a player by name and returns their ID and name if not retired.
    # Item 0 returns the correct player ID
    # Item 1 returns the correct player name
    # player_name as a string

    url = f"https://transfermarkt-api.fly.dev/players/search/{player_name}"
    response = requests.get(url)
    players = response.json()["results"]
    if not players:
        return ["n.a.", "n.a."]
    while len(players) > 0:
        current_player = players.pop(0)
        club_name = current_player["club"]["name"]
        if club_name != "Retired":
            return [current_player["id"], current_player["name"]]
    else:
        return ["n.a.", "n.a."]


def get_league(club_id):
    # Retrieves league ID and name for a given club. Returns 'n.a.' if unavailable.
    # Returns the league of the club as a list
    # Item 0 -> League ID
    # Item 1 -> League Name

    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/profile"
    response = requests.get(url)
    league = response.json()
    try:
        data = [league["league"]["id"], league["league"]["name"]]
    except:
        data = ["n.a.", "none"]
    return data


# Directly returns the data from the API as is
# player_id as an integer
def get_profile(player_id):
    # Retrieves the full profile of a player based on their ID.

    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    return response.json()

def get_marketvalue_history(player_id):
    # Retrieves the market value history of a player. Returns 'n.a.' if unavailable.

    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/market_value"
    response = requests.get(url)
    history = response.json()
    try:
        values = history["marketValueHistory"]
    except:
        values = "n.a."
    return values

def get_transfer_history(player_id):
    # Retrieves the transfer history of a player as a list of records.
    #returns list of transfers
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/transfers"
    response = requests.get(url)
    return response.json()["transfers"]


def get_stats(player_id):
    # Retrieves detailed statistics of a player from their profile.
    
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/stats"
    response = requests.get(url)
    return response.json()["stats"]

def get_achievements(player_id):
# Retrieves a player's achievements. Returns placeholder if unavailable.

    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/achievements"
    response = requests.get(url)
    try:
        titles = response.json()["achievements"]
    except:
        titles = [{"title": "none"}]
    return titles