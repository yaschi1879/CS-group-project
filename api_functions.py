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
    market_value = player_profile["marketValue"].replace("€", "")
    if "m" in market_value:
        market_value = float(market_value.replace("m", ""))
    elif "k" in market_value:
        market_value = float(market_value.replace("k", "")) / 1000
    else:
        market_value = float(market_value)
    return market_value
# gibt Markwert in mio als float zurück z.B. 10.34, Markwert ist in Euro
# player_id als integer

def get_age(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    player_profile = response.json()
    return int(player_profile["age"])
# gibt Alter als integer zurück
# player_id als integer

def get_club_name_user_input(club_name):
    url = f"https://transfermarkt-api.fly.dev/clubs/search/{club_name}"
    response = requests.get(url)
    clubs = response.json()
    return clubs["results"][0]["id"]
# gibt den korrekten club namen als id zurück
# club_name als string

def get_club_image(club_id):
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/profile"
    response = requests.get(url)
    image = response.json()
    return image["image"]
# gibt url für club logo zrück

def get_player_name_user_input(player_name):
    url = f"https://transfermarkt-api.fly.dev/players/search/{player_name}"
    response = requests.get(url)
    players = response.json()
    return players["results"][0]["id"]
# gibt den korrekten spieler namen als id zurück
# club_name als string

def get_league_name_user_input(competition_name):
    url = f"https://transfermarkt-api.fly.dev/competitions/search/{competition_name}"
    response = requests.get(url)
    league = response.json()
    return [i["id"] for i in league["results"]]
# achtung: gibt eine liste aller ligen id's zurück, die z.B. zu super league passen      
# competintion_name als string

def get_league_id(club_id):
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/profile"
    response = requests.get(url)
    league = response.json()
    return league["league"]["id"]

def get_league_name(club_id):
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/profile"
    response = requests.get(url)
    league = response.json()
    return league["league"]["name"]
# gibt Lige des Clubs als name zurück

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