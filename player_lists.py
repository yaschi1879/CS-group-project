club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

from API_functions import get_club_players
from API_functions import get_age
from API_functions import get_marketvalue

meta_player_list = []

for club in club_id:
    meta_player_list.extend(get_club_players(club))

difficult_list = []

for player in meta_player_list:
    market_value = get_marketvalue(player_id)
    age = int(get_age(player_id))  # Alter wird in einen Integer umgewandelt

    # Marktwert umwandeln (z. B. '10.00m' -> 10_000_000)
    if "m" in market_value:
        market_value = float(market_value.replace("m", "")) * 1_000_000
    elif "k" in market_value:
        market_value = float(market_value.replace("k", "")) * 1_000
    else:
        market_value = float(market_value)

    # Überprüfen, ob der Spieler die Kriterien erfüllt
    if age <= 30 and market_value <= 40_000_000:
        schwierig.append(player)
    elif 30 < age <= 32 and market_value <= 15_000_000:
        schwierig.append(player)
    elif age > 32 and market_value <= 10_000_000:
        schwierig.append(player)

# Ergebnis: Die Liste 'schwierig' enthält nur Spieler, die die Kriterien erfüllen
