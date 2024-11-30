import random
import pandas as pd
from ml_data import training_dictionary
from api_functions import get_club_players

club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

player_list = []

for club in club_id:
    player_list.extend(get_club_players(club))

# dieser part ist für die erstellung der player_list, dauert ca 1min
# zuerst ausführen

# -------------------------------------------------------------------------------

# jetzt kommt die erstellung der daten für 100 random spieler
player_list = random.sample(player_list, 10)
player_data = []

for player in player_list:
    player_dict = training_dictionary(player)
    player_data.append(player_dict)

data_frame = pd.DataFrame(player_data)
print(data_frame.head())

