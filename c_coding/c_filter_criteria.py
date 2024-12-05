from c_coding.a_api_functions import get_filter_criteria
import streamlit as st

# diese funktion checkt, ob der spieler die kriterien für den schwierigkeitsgrad erfüllt
# falls ja, gibt funktion true zrück, falls nein false

def check_player_criteria(player_id):
    difficulty = st.session_state.difficulty
    info = get_filter_criteria(player_id)
    market_value = info[0]
    age = info[1]
    
    if market_value == "n.a.":
        return False
    
    elif difficulty == "None":
        if age < 26 and market_value < 10:
            return False
        elif 26 <= age < 30 and market_value < 5:
            return False
        elif 30 <= age and market_value < 1:
            return False
        else:
            return True
    
    elif difficulty == "Easy":
        if age < 26 and market_value >= 80:
            return True
        elif 26 <= age <= 30 and market_value >= 60:
            return True
        elif 30 < age <= 33 and market_value >= 25:
            return True
        elif age > 33 and market_value > 10:
            return True
        else:
            return False

    elif difficulty == "Medium":
        if age < 26 and 50 < market_value < 80:
            return True
        elif 26 <= age <= 30 and 40 <= market_value < 60:
            return True
        elif 30 < age <= 33 and 15 <= market_value < 25:
            return True
        elif age > 33 and 3 < market_value <= 10:
            return True
        else:
            return False

    elif difficulty == "Hard":
        if age < 26 and 10 <= market_value <= 50:
            return True
        elif 26 <= age <= 30 and 5 <= market_value < 40:
            return True
        elif 30 < age <= 33 and 1 <= market_value < 15:
            return True
        elif age > 33 and market_value <= 3:
            return True
        else:
            return False