club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

from API_functions import get_club_players
from API_functions import get_age
from API_functions import get_marketvalue

meta_player_list = []

for club in club_id:
    meta_player_list.extend(get_club_players(club))

