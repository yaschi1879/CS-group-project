from api_functions import get_filter_criteria

# diese funktion checkt, ob der spieler die kriterien für den schwierigkeitsgrad erfüllt
def check_player_criteria(player_id, difficulty):
    info = get_filter_criteria(player_id)
    market_value = info[0]
    age = info[1]
    
    if market_value == "not_availabe":
        return False
    
    elif difficulty == "no":
        return True
    
    elif difficulty == "easy":
        if age < 30 and market_value >= 65:
            return True
        elif 30 <= age <= 32 and market_value >= 30:
            return True
        elif age > 32 and market_value >= 25:
            return True
        else:
            return False

    elif difficulty == "medium":
        if age < 30 and 40 <= market_value < 65:
            return True
        elif 30 <= age <= 32 and 20 <= market_value < 30:
            return True
        elif age > 32 and 10 <= market_value < 25:
            return True
        else:
            return False

    elif difficulty == "difficult":
        if age < 30 and market_value < 30:
            return True
        elif 30 <= age <= 32 and market_value < 15:
            return True
        elif age > 32 and market_value < 10:
            return True
        else:
            return False