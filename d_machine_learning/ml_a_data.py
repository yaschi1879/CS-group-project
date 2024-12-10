import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from c_support.a_api_functions import get_profile, get_marketvalue_history
from datetime import datetime
import math

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
    
def value_t1(player_profile):
    try:
        value = player_profile["marketValue"].replace("€", "")
        if "m" in value:
            value = float(value.replace("m", ""))
        elif "k" in value:
            value = float(value.replace("k", "")) / 1000
        value = math.log(value)
    except:
        value = "n.a."
    return value

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

def u25(profile, reference_date):
    try:
        value = (max(0, 25 - calculate_age(profile["dateOfBirth"], reference_date)))
    except:
        value = "n.a."
    return value

def o30(profile, reference_date):
    try:
        value = ((max(0, calculate_age(profile["dateOfBirth"], reference_date) - 30)))
    except:
        value = "n.a."
    return value

def diff_market_value(values, reference_date, sec_reference_date):
    try:
        market_value_1 = last_market_value(values, reference_date)
        market_value_2 = last_market_value(values, sec_reference_date)
        value= (market_value_1 - market_value_2) / market_value_1
        return value
    except:
        return "n.a."

def training_dictionary(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    # Beispiel für einen Forecast, der 1 Jahr in die zukunft prognostizieren soll
    reference_date = "2023-12-01" # immer 2024-12-01 minus die anzahl jahre
    sec_reference_date = "2022-12-01" # immer 2024-12-01 minus die anzahl jahre +1
    dict = {}
    print(player_id)
    dict["market_value_t+1"] = value_t1(profile)
    dict["u26"] = u25(profile, reference_date)
    dict["o29"] = o30(profile, reference_date)
    dict["market_value_t"] = last_market_value(values, reference_date)
    dict["diff_market_value"] = diff_market_value(values, reference_date, sec_reference_date)
    return dict
    
def forecast_dictionary(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    reference_date = "2024-12-01"
    sec_reference_date = "2023-12-01"
    dict = {}
    dict["market_value_t+1"] = value_t1(profile)
    dict["u26"] = u25(profile, reference_date)
    dict["o29"] = o30(profile, reference_date)
    dict["market_value_t"] = last_market_value(values, reference_date)
    dict["diff_market_value"] = diff_market_value(values, reference_date, sec_reference_date)
    return dict