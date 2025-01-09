# We hereby declare that the vast majority of the code for this project has been written by us independently. 
# We have utilized ChatGPT as a tool for conceptual purposes and for assistance with small, 
# specific parts of the code, such as generating comments or clarifying implementation ideas.
# However, all critical design decisions, core functionality, 
# and the implementation of the primary codebase were developed through our own efforts and understanding.

# This is Link for the Game application: https://cs-group-project-8c9afmnnkpup2ze7c3yxvo.streamlit.app/
# our GitHub: https://github.com/yaschi1879/CS-group-project

import sys
import os

# Add the parent directory to the system path so Python can find other modules in the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random 
from c_support.a_api_functions import get_profile, get_league, get_transfer_history, get_achievements, get_stadium_name

def classify_position(position):
    #  Groups player positions into these categories: Goalkeeper, Defender, Midfielder und Striker
    if "Goalkeeper" in position:
        return "Goalkeeper"
    elif "Back" in position:
        return "Defender"
    elif "Midfield" in position:
        return "Midfielder"
    elif "Winger" in position or "Forward" in position or "Striker" in position:
        return "Striker"


def sort_titles(player_id):
    # Goes through all titles and returns a list of these titles (if won):
    # "league" refers to a title in a top 5 league, but it doesn't specify which one
    # Returns "none" if none of these titles were won

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


def stadium_name(player_id):
    # returns the name of a random stadium, in which the player has played before
    old_clubs = [i["from"]["clubID"] for i in get_transfer_history(player_id)]
    while len(old_clubs) > 0:
        random_club = random.choice(old_clubs)
        old_clubs.remove(random_club)
        stadium_name = get_stadium_name(random_club)
        if stadium_name != "n.a.":
            return stadium_name
    if len(old_clubs) == 0:
        return "no old stadium"


def player_dictionary(player_id):
    # This dictionary is key for the game and search engine, it contains all the data in a structured way
    player_dictionary = {}
    # the functinons below are API functions
    profile = get_profile(player_id)
    league = get_league(profile["club"]["id"])
    old_clubs = get_transfer_history(player_id)
    try:
        club_id = profile["club"]["id"]
        club_name = profile["club"]["name"]
    except:
        club_id = "none"
        club_name = "none"
        
    player_dictionary["id"] = profile["id"]
    player_dictionary["name"] = profile["name"]
    player_dictionary["age"] = int["age"]
    player_dictionary["height"] = int(profile["height"])
    # returns the height in centimeters as an integer
    player_dictionary["image"] = profile["imageURL"]
    player_dictionary["country"] = profile["citizenship"][0]
    player_dictionary["classified_position"] = classify_position(profile["position"]["main"])
    # returns classified position 
    player_dictionary["position"] = [profile["position"]["main"]] + profile["position"].get("other", [])
    # Attention!! returns more positions as a list 
    # if the player does not have more than one position, only the main position is returned
    player_dictionary["shirt_number"] = profile["shirtNumber"].replace("#", "")
    player_dictionary["club_id"] = club_id
    player_dictionary["club_name"] = club_name
    player_dictionary["league_id"] = league[0]
    player_dictionary["league_name"] = league[1]
    player_dictionary["old_clubs_ids"] = [i["from"]["clubID"] for i in old_clubs]
    # returns the club id`s of all of the player`s former clubs 
    player_dictionary["old_clubs_name"] = [i["from"]["clubName"] for i in old_clubs]
    # returns the club names of all of the players former clubs
    player_dictionary["titles"] = sort_titles(player_id)
    
    # these are used as the starting point of the game
    player_dictionary["old_stadium"] = stadium_name(player_id)
    player_dictionary["foot"] = profile["foot"]
    player_dictionary["joined_date"] = profile["club"]["joined"]
    
    return player_dictionary