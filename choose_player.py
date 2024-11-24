from filter_criteria import check_player_criteria
from meta_player_list import player_list
import random

# Schwierigkeit kann easy, medium oder difficult sein    
difficulty = "difficult"

def select_player(player_list, difficulty):
    selected_player = False

    # Solange ein Spieler gefunden wird, der die Kriterien erfüllt, random einen Spieler auswählen
    while not selected_player:
        player = random.choice(player_list)

        if check_player_criteria(player, difficulty):
            selected_player = player
        else:
            player_list.remove(player)

    return selected_player

print(select_player(player_list, difficulty))