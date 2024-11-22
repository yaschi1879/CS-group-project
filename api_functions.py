import requests

def get_club_players(club_id, season_id="2024"):
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/players"
    response = requests.get(url, season_id)
    club_players = response.json()
    club_players = club_players["players"]
    club_player_id = []
    for players in club_players:
        club_player_id.append(players["id"])
    return club_player_id
# gibt die jeweiligen Spieler ID's des Clubs als Liste zurück, mit default aktuelle Saison
# club_id als integer, season_id als string

def get_marketvalue(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    player_profile = response.json()
    return player_profile["marketValue"].replace("€", "")
# gibt Markwert im Format '10.00m' zurück, Markwert ist in Euro
# player_id als integer

def get_age(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    player_profile = response.json()
    return player_profile["age"]
# gibt Alter als String zurück
# player_id als integer

def get_club_name(club_name):
    url = f"https://transfermarkt-api.fly.dev/clubs/search/{club_name}"
    response = requests.get(url)
    clubs = response.json()
    return clubs["results"][0]["name"]
# gibt den korrekten club namen zurück
# club_name als string

def get_player_name(player_name):
    url = f"https://transfermarkt-api.fly.dev/players/search/{player_name}"
    response = requests.get(url)
    players = response.json()
    return players["results"][0]["name"]
# gibt den korrekten club namen zurück
# club_name als string


# geben jeweils 1 zu 1 das von API wieder:
# player_id als integer
def get_profile(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    return response.json()

def get_marketvalue_history(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/market_value"
    response = requests.get(url)
    return response.json()

def get_transfer_history(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/transfers"
    response = requests.get(url)
    return response.json()

def get_stats(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/stats"
    response = requests.get(url)
    return response.json()

def get_achievements(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/achievements"
    response = requests.get(url)
    return response.json()