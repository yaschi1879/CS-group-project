# We hereby declare that the vast majority of the code for this project has been written by us independently. 
# We have utilized ChatGPT as a tool for conceptual purposes and for assistance with small, 
# specific parts of the code, such as generating comments or clarifying implementation ideas.
# However, all critical design decisions, core functionality, 
# and the implementation of the primary codebase were developed through our own efforts and understanding.

# This is Link for the Game application: https://cs-group-project-8c9afmnnkpup2ze7c3yxvo.streamlit.app/ 

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the parent directory to the system path for module access
from c_support.a_api_functions import get_profile, get_marketvalue_history
from datetime import datetime
import math

# Extract the last valid market value of a player before a given reference date
def last_market_value(values, reference_date):
    try:
        date_reference = datetime.strptime(reference_date, "%Y-%m-%d")
        last_update = None
        for value in values:
            value_date = datetime.strptime(value["date"], "%b %d, %Y")
            if value_date < date_reference:
                if last_update is None or value_date > datetime.strptime(last_update["date"], "%b %d, %Y"):
                    last_update = value
        if last_update is None:
            return "n.a."
        market_value =  last_update["value"].replace("€", "")
        if "m" in market_value:
            market_value = float(market_value.replace("m", ""))
        elif "k" in market_value:
            market_value = float(market_value.replace("k", "")) / 1000
        return market_value
    except:
        return "n.a."

# Extract current market value
def value_t1(player_profile):
    try:
        value = player_profile["marketValue"].replace("€", "")
        if "m" in value:
            value = float(value.replace("m", ""))
        elif "k" in value:
            value = float(value.replace("k", "")) / 1000
        return [value, math.log(value)]
    except:
        return ["n.a.", "n.a."]

# Apply log transformation to a market value
def log_value_t(last_value):
    try:
        return math.log(last_value)
    except:
        return "n.a."

# Calculate the age of a player as of a reference date
def calculate_age(birth_date, reference_date):
    try:
        birth = datetime.strptime(birth_date, "%b %d, %Y")
        reference = datetime.strptime(reference_date, "%Y-%m-%d")
        age = reference.year - birth.year
        if (reference.month, reference.day) < (birth.month, birth.day):
            age -= 1
        return age
    except:
        return "n.a."

# Calculate U25 contribution factor (age-related boost for players under 25)
def u25(profile, reference_date, last_value):
    try:
        value = ((max(0, 25 - calculate_age(profile["dateOfBirth"], reference_date)))**2) * last_value
        value_log = math.log(max(((max(0, 25 - calculate_age(profile["dateOfBirth"], reference_date)))**2) * last_value, 1))
        return [value, value_log]
    except:
        return ["n.a.", "n.a."]
    

# Calculate O30 contribution factor (age-related decrease for players over 30)
def o30(profile, reference_date, last_value):
    try:
        value = (((max(0, calculate_age(profile["dateOfBirth"], reference_date) - 30)))**2) * last_value
        value_log = math.log(max(((max(0, calculate_age(profile["dateOfBirth"], reference_date) - 30))**2) * last_value, 1))
        return [value, value_log]
    except:
        return ["n.a.", "n.a."]
    
# Calculate the difference between two market values
def diff_market_value(values, reference_date, sec_reference_date, last_value):
    try:
        market_value_1 = last_market_value(values, reference_date)
        market_value_2 = last_market_value(values, sec_reference_date)
        value = market_value_1 - market_value_2
        log_value = value / last_value
        return [value, log_value]
    except:
        return ["n.a.", "n.a."]

# Check for significant market value differences exceeding a threshold
def huge_diff(values, reference_date, sec_reference_date, last_value):
    try:
        if abs(diff_market_value(values, reference_date, sec_reference_date, last_value)[1]) > 0.5:
            value = diff_market_value(values, reference_date, sec_reference_date, last_value)[0]
            log_value = diff_market_value(values, reference_date, sec_reference_date, last_value)[1]
        else:
            value = 0
            log_value = 0
        return [value, log_value]
    except:
        return ["n.a.", "n.a."]
    
# Create a dictionary for training machine learning models based on player data
# Hypothesis:
# current market value serves as an anchor for future market value
# age has a positive influence on young players, no influence on mid-aged players and a negative influence on old players
# the last trend (diff_market_value) has a positive influence
# a huge last trend has a negative influce due to regression toward the mean effect
def training_dictionary(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    # Example for a forecast that should predict 2 years into the future 
    reference_date = "2022-12-01" # always 2024-12-01 minus the wanted years into the future
    sec_reference_date = "2021-12-01" # always 2024-12-01 minus the wanted years into the future + 1
    last_value = last_market_value(values, reference_date)
    b1 = value_t1(profile)
    b3 = u25(profile, reference_date, last_value)
    b4 = o30(profile, reference_date, last_value)
    b5 = diff_market_value(values, reference_date, sec_reference_date, last_value)
    b6 = huge_diff(values, reference_date, sec_reference_date, last_value)
    
    dict = {}
    print(player_id)
    dict["market_value_t+1"] = b1[0]
    dict["market_value_t"] = last_value
    dict["u25"] = b3[0]
    dict["o30"] = b4[0]
    dict["diff_market_value"] = b5[0]
    dict["huge_diff"] = b6[0]
    
    log_dict = {}
    log_dict["market_value_t+1"] = b1[1]
    log_dict["market_value_t"] = log_value_t(last_value)
    log_dict["u25"] = b3[1]
    log_dict["o30"] = b4[1]
    log_dict["diff_market_value"] = b5[1]
    log_dict["huge_diff"] = b6[1]
    return [dict, log_dict]

# Generate features for predicting market value
def forecast(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    reference_date = "2024-12-01" # Reference date for the prediction year
    sec_reference_date = "2023-12-01" # Secondary reference date for year-over-year change
    last_value = last_market_value(values, reference_date)
    b3 = u25(profile, reference_date, last_value)
    b4 = o30(profile, reference_date, last_value)
    b5 = diff_market_value(values, reference_date, sec_reference_date, last_value)
    b6 = huge_diff(values, reference_date, sec_reference_date, last_value)
    
    dict = {}
    dict["market_value_t"] = last_value
    dict["u25"] = b3[0]
    dict["o30"] = b4[0]
    dict["diff_market_value"] = b5[0]
    dict["huge_diff"] = b6[0]
    return dict