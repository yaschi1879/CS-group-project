from api_functions import get_profile, get_league_id, get_club_image

def classify_position(position):
    if "Goalkeeper" in position:
        return "Goalkeeper"
    elif "Back" in position:
        return "Defender"
    elif "Midfield" in position:
        return "Midfielder"
    elif "Winger" in position or "Forward" in position:
        return "Striker"
    
def create_player_dictionary(player_id):
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
    player_dictionary["club_id"] = profile["club"]["id"]
    player_dictionary["club_image"] = get_club_image(profile["club"]["id"])
    player_dictionary["league_id"] = get_league_id(profile["club"]["id"])

    return player_dictionary