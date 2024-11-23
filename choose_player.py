from api_functions import get_club_players
from select_player import check_player_criteria
import random

club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

meta_player_list = []

for club in club_id:
    meta_player_list.extend(get_club_players(club))

# Schwierigkeit kann easy, medium oder difficult sein    
difficulty = "easy"

def select_player(meta_player_list, difficulty):
    selected_player = False

    # Solange ein Spieler gefunden wird, der die Kriterien erfüllt, random einen Spieler auswählen
    while not selected_player:
        player = random.choice(meta_player_list)

        if check_player_criteria(player, difficulty):
            selected_player = player
        else:
            meta_player_list.remove(player)

    return selected_player

print(select_player(meta_player_list, difficulty))




