import requests

def get_stadium_name(club_id):
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/profile"
    response = requests.get(url)
    club_info = response.json()
    stadium_name = club_info.get("stadiumName", False)
    return stadium_name
# gibt stadion name zurück, falls diese info fehlt, gibt sie false zurück

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

def get_filter_criteria(player_id):
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
        market_value = "not_available"
    age = int(player_profile["age"])
    return [market_value, age]
# gibt Markwert in mio als float zurück z.B. 10.34, Markwert ist in Euro
# falls kein market value vorhanden, wird "not_available" zurückgegeben
# gibt Alter als integer zurück
# player_id als integer

def get_club_name_user_input(club_name):
    url = f"https://transfermarkt-api.fly.dev/clubs/search/{club_name}"
    response = requests.get(url)
    clubs = response.json()
    return clubs["results"][0]["id"]
# gibt den korrekten club namen als id zurück
# club_name als string

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
    if not league["results"]:
        return False
    country_id_mapping = {i["country"]: i["id"] for i in league["results"]}
    return country_id_mapping
# achtung: gibt eine liste aller liga id's als value zurück, mit den entsprechenden ländern als key   
# competintion_name als string

def get_league(club_id):
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/profile"
    response = requests.get(url)
    league = response.json()
    return [league["league"]["id"], league["league"]["name"]]
# gibt die Liga des clubs als Liste zrück
# item = 0 -> Liga ID
# item = 1 -> Liga Name

# geben jeweils 1 zu 1 das von API wieder:
# player_id als integer
def get_profile(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/profile"
    response = requests.get(url)
    return response.json()

def get_marketvalue_history(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/market_value"
    response = requests.get(url)
    return response.json()["marketValueHistory"]

def get_transfer_history(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/transfers"
    response = requests.get(url)
    transfers = response.json()
    return transfers["transfers"]
# gibt liste der transfers zurück

def get_stats(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/stats"
    response = requests.get(url)
    return response.json()["stats"]

def get_achievements(player_id):
    url = f"https://transfermarkt-api.fly.dev/players/{player_id}/achievements"
    response = requests.get(url)
    achievements = response.json()
    return achievements["achievements"]