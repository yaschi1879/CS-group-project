import sys
import os

# Add the parent directory to the system path so Python can find other modules in the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from c_support.a_api_functions import get_filter_criteria
import streamlit as st

# This function checks if the player fits the difficulty
# if yes this function returns true, if no then it returns false


def check_player_criteria(player_id):
    difficulty = st.session_state.difficulty # Get the current difficulty level from session state
    info = get_filter_criteria(player_id) # Retrieve player market value and age
    market_value = info[0]
    age = info[1]
    
    #if there is no market value than false will be returned
    if market_value == "n.a.":
        return False
    
    # Criteria for "Random" difficulty
    # Rejects players based on market value and age thresholds in various ranges
    elif difficulty == "Random":
        if age < 26 and market_value < 10: ## Young players with low market value are rejected
            return False
        elif 26 <= age < 30 and market_value < 5: # Mid-aged players with very low market value are rejected
            return False
        elif 30 <= age and market_value < 1: # Older players with negligible market value are rejected
            return False
        else:
            return True # All other players are accepted
    
    # Criteria for "Easy" difficulty
    # Accepts players with high market value across different age ranges
    elif difficulty == "Easy":
        if age < 26 and market_value >= 80: # Very young and highly valued players are accepted
            return True
        elif 26 <= age <= 30 and market_value >= 60: # Prime-aged players with high value are accepted
            return True
        elif 30 < age <= 33 and market_value >= 25: # Slightly older players with decent value are accepted
            return True
        elif age > 33 and market_value > 10: # Older players with modest value are accepted
            return True
        else:
            return False # Reject others

    # Criteria for "Medium" difficulty
    # Accepts players with moderate market value based on age ranges
    elif difficulty == "Medium":
        if age < 26 and 50 < market_value < 80: # Young players with medium-high value
            return True
        elif 26 <= age <= 30 and 40 <= market_value < 60: # Prime-aged players with medium value
            return True
        elif 30 < age <= 33 and 15 <= market_value < 25:  # Older players with modest value
            return True
        elif age > 33 and 3 < market_value <= 10: # Very old players with low value
            return True
        else:
            return False # Reject others

    # Criteria for "Hard" difficulty
    # Accepts players with low market value based on age ranges
    elif difficulty == "Hard":
        if age < 26 and 10 <= market_value <= 50: # Young players with low to moderate value
            return True
        elif 26 <= age <= 30 and 5 <= market_value < 40: # Prime-aged players with low value
            return True
        elif 30 < age <= 33 and 1 <= market_value < 15: # Older players with very low value
            return True
        elif age > 33 and market_value <= 3: # Very old players with negligible value
            return True
        else:
            return False # Reject others