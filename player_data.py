import random
from api_functions import get_profile, get_league_id, get_club_image, get_transfer_history, get_achievements, get_stadium_name

def classify_position(position):
    if "Goalkeeper" in position:
        return "Goalkeeper"
    elif "Back" in position:
        return "Defender"
    elif "Midfield" in position:
        return "Midfielder"
    elif "Winger" in position or "Forward" in position:
        return "Striker"
# sortiert die Positionen zu: Goalkeeper, Defender, Midfielder und Striker
    
def sort_titles(player_id):
    achievements = get_achievements(player_id)
    titles = []
    for i in achievements:
        title = i["title"]
        if title == "World Cup winner":
            titles.append("WC")
        elif title == "European champion":
            titles.append("EC")
        elif title == "Champions League winner":
            titles.append("CL")
        elif "spanish champion" or "italian champion" or "english champion" or "german champion" or "french champion" in title.lower():
            titles.append("league")
    if not titles:
        return "none"
    return list(set(titles))
# geht durch alle Titel durch und retourniert eine Liste mit folgenden Titeln (falls diese gewonnen wurden)
# [WC, EC, CL, league]
# mit league ist der Titel in einer Top 5 Liga gemeint, aber nicht spezifiziert in welcher Liga
# falls keiner dieser Titel gwonnen wurde, wird "none" retourniert

def stadium_name(player_id):
    old_clubs = [i["from"]["clubID"] for i in get_transfer_history(player_id)]
    random_club = random.choice(old_clubs)
    stadium_name = get_stadium_name(random_club)
    while not stadium_name:
        old_clubs.remove(random_club)
        random_club = random.choice(old_clubs)
        stadium_name = get_stadium_name(random_club)
    return stadium_name
# gibt den stadion namen eines zufälligen alten clubs zurück

def player_dictionary(player_id):
    player_dictionary = {}
    profile = get_profile(player_id)
    player_dictionary["id"] = profile["id"]
    player_dictionary["name"] = profile["name"]
    player_dictionary["age"] = int(profile["age"])
    player_dictionary["height"] = int(float(profile["height"].replace(",", ".").replace("m", "")) * 100)
    player_dictionary["image"] = profile["imageURL"]
    player_dictionary["country"] = profile["citizenship"][0]
    player_dictionary["classified_position"] = classify_position(profile["position"]["main"])
    player_dictionary["position"] = [profile["position"]["main"]] + profile["position"].get("other", [])
    # achtung!!! gibt mehrere positionen als liste zurück
    # falls der spieler keine andere positionen hat, bleibt es bei der Hauptposition
    player_dictionary["shirt_number"] = profile["shirtNumber"].replace("#", "")
    player_dictionary["club_id"] = profile["club"]["id"]
    player_dictionary["club_image"] = get_club_image(profile["club"]["id"])
    player_dictionary["league_id"] = get_league_id(profile["club"]["id"])
    player_dictionary["old_clubs"] = [i["from"]["clubID"] for i in get_transfer_history(player_id)]
    # gibt die club id's aller ehemaligen clubs zurück
    player_dictionary["titels"] = sort_titles(player_id)
    
    player_dictionary["old_stadium"] = stadium_name(player_id)
    player_dictionary["foot"] = profile["foot"]
    player_dictionary["outfitter"] = profile["outfitter"]
    player_dictionary["joined_date"] = profile["club"]["joined"]
    # werden als Startpunkt verwendet
    
    return player_dictionary

print(player_dictionary(139208))

#def player_regression(player_id):
    