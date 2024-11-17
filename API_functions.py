import requests

def get_club_players(club_id, season_id):
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/players"
    response = requests.get(url, season_id)
    club_players = response.json()
    return club_players["players"]

def get_marketvalue(player_id):
    url = "https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    player_profile = response.json()
    return player_profile["marketValue"]

def get_age(player_id):
    url = "https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    player_profile = response.json()
    return player_profile["age"]

def get_profile(player_id):
    url = "https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    player_profile = response.json()
    return player_profile


get_marketvalue(340950)