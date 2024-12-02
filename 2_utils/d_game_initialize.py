import random
from a_api_functions import get_club_players
from c_filter_criteria import check_player_criteria

club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

club_id_test = [281, 418, 27, 31, 12]

player_list = []

for club in club_id_test:
    player_list.extend(get_club_players(club))

# dieser part ist für die erstellung der player_list, dauert ca 1min
# zuerst ausführen
# -------------------------------------------------------------------------------
# der part der jetzt kommt ist für die wahl eines spielers
# immer separat ausführen, sonst wird der erste teil auch immer ausgeführt
# separat ausführen indem teil markieren und mit shift + enter ausführen
 
difficulty = "none"
# Schwierigkeit kann easy, medium oder difficult oder none für keine schwierigkeit sein
selected_player = False

# Solange ein Spieler kein gefunden wird, der die Kriterien erfüllt, werden zufällig weitere Spieler ausgewählt
while not selected_player:
    player = random.choice(player_list)
    if check_player_criteria(player, difficulty):
        selected_player = player
    else:
        player_list.remove(player)

print(selected_player)