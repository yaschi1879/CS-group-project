import random
from c_coding.a_api_functions import get_profile, get_league, get_transfer_history, get_achievements, get_stadium_name

def classify_position(position):
    if "Goalkeeper" in position:
        return "Goalkeeper"
    elif "Back" in position:
        return "Defender"
    elif "Midfield" in position:
        return "Midfielder"
    elif "Winger" in position or "Forward" in position or "Striker" in position:
        return "Striker"
# sortiert die Positionen zu: Goalkeeper, Defender, Midfielder und Striker

def sort_titles(player_id):
    achievements = get_achievements(player_id)
    titles = []
    for i in achievements:
        title = i["title"]
        if title == "World Cup winner":
            titles.append("World Cup")
        elif title == "European champion":
            titles.append("European Championship")
        elif title == "Champions League winner":
            titles.append("Champions League")
        elif any(league in title.lower() for league in ["spanish champion", "italian champion", "english champion", "german champion", "french champion"]):
            titles.append("Top 5 League")
    if not titles:
        return ["none"]
    return list(set(titles))
# geht durch alle Titel durch und retourniert eine Liste mit folgenden Titeln (falls diese gewonnen wurden)
# [WC, EC, CL, league]
# mit league ist der Titel in einer Top 5 Liga gemeint, aber nicht spezifiziert in welcher Liga
# falls keiner dieser Titel gwonnen wurde, wird "none" retourniert

print(sort_titles(132098))

def stadium_name(player_id):
    old_clubs = [i["from"]["clubID"] for i in get_transfer_history(player_id)]
    while len(old_clubs) > 0:
        random_club = random.choice(old_clubs)
        old_clubs.remove(random_club)
        stadium_name = get_stadium_name(random_club)
        if stadium_name != "n.a.":
            return stadium_name
    if len(old_clubs) == 0:
        return "no old stadium"
    
# gibt den stadion namen eines zufälligen alten clubs zurück

def player_dictionary(player_id):
    player_dictionary = {}
    profile = get_profile(player_id)
    league = get_league(profile["club"]["id"])
    old_clubs = get_transfer_history(player_id)
    
    player_dictionary["id"] = profile["id"]
    player_dictionary["name"] = profile["name"]
    player_dictionary["age"] = int(profile["age"])
    player_dictionary["height"] = int(float(profile["height"].replace(",", ".").replace("m", "")) * 100)
    # gibt grösse in centimeter als integer zurück
    player_dictionary["image"] = profile["imageURL"]
    player_dictionary["country"] = profile["citizenship"][0]
    player_dictionary["classified_position"] = classify_position(profile["position"]["main"])
    # gibt klassifizierte position zurück
    player_dictionary["position"] = [profile["position"]["main"]] + profile["position"].get("other", [])
    # achtung!!! gibt mehrere positionen als liste zurück
    # falls der spieler keine andere positionen hat, bleibt es bei der Hauptposition
    player_dictionary["shirt_number"] = profile["shirtNumber"].replace("#", "")
    player_dictionary["club_id"] = profile["club"]["id"]
    player_dictionary["club_name"] = profile["club"]["name"]
    player_dictionary["league_id"] = league[0]
    player_dictionary["league_name"] = league[1]
    player_dictionary["old_clubs_ids"] = [i["from"]["clubID"] for i in old_clubs]
    # gibt die club id's aller ehemaligen clubs als liste zurück
    player_dictionary["old_clubs_name"] = [i["from"]["clubName"] for i in old_clubs]
    # gibt die club namen aller ehemaligen clubs als liste zurück
    player_dictionary["titels"] = sort_titles(player_id)
    
    player_dictionary["old_stadium"] = stadium_name(player_id)
    player_dictionary["foot"] = profile["foot"]
    player_dictionary["joined_date"] = profile["club"]["joined"]
    # werden als Startpunkt verwendet
    
    return player_dictionary