from api_functions import get_age, get_marketvalue

# diese funktion checkt, ob der spieler die kriterien für den schwierigkeitsgrad erfüllt
def check_player_criteria(player_id, difficulty):
    age = get_age(player_id)
    market_value = get_marketvalue(player_id)
    
    if difficulty == "easy":
        if age < 30 and market_value >= 80:
            return True
        elif 30 <= age <= 32 and market_value >= 30:
            return True
        elif age > 32 and market_value >= 25:
            return True

    elif difficulty == "medium":
        if age < 30 and 40 <= market_value < 80:
            return True
        elif 30 <= age <= 32 and 20 <= market_value < 30:
            return True
        elif age > 32 and 10 <= market_value < 25:
            return True

    elif difficulty == "difficult":
        if age < 30 and market_value < 40:
            return True
        elif 30 <= age <= 32 and market_value < 15:
            return True
        elif age > 32 and market_value < 10:
            return True

# falls kein schwierigkeitsgrad ausgewählt ist
    else:
        return True

# falls die kriterien nicht erfüllt werden
    return False