import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from c_support.a_api_functions import get_profile, get_marketvalue_history, get_filter_criteria, get_club_players
from datetime import datetime
from dateutil.relativedelta import relativedelta

def time_left(contract, reference_date, last_value):
    try:
        date = datetime.strptime(contract, "%b %d, %Y")
        reference = datetime.strptime(reference_date, "%Y-%m-%d")
        difference = relativedelta(date, reference)
        months = difference.years * 12 + difference.months
        return months * last_value
    except:
        return "n.a."

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

def diff_market_value(values, reference_date, sec_reference_date):
    try:
        market_value_1 = last_market_value(values, reference_date)
        market_value_2 = last_market_value(values, sec_reference_date)
        return market_value_1 - market_value_2
    except:
        return "n.a."

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

def huge_difference(values, reference_date, sec_reference_date, last_value):
    try:
        value = (abs(diff_market_value(values, reference_date, sec_reference_date))/ last_value > 0.3) * last_value
    except:
        value = "n.a."
    return value

def u26(profile, reference_date, last_value):
    try:
        value = (max(0, 26 - calculate_age(profile["dateOfBirth"], reference_date))) * last_value
    except:
        value = "n.a."
    return value

def o29(profile, reference_date, last_value):
    try:
        value = (max(0, calculate_age(profile["dateOfBirth"], reference_date) - 29)) * last_value
    except:
        value = "n.a."
    return (value)^2

def GKo30(profile, reference_date, last_value):
    try:
        value = (calculate_age(profile["dateOfBirth"], reference_date) > 30 and profile["position"]["main"] == "Goalkeeper") * last_value
    except:
        value = "n.a."
    return value
    
def training_dictionary(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    # Beispiel für einen Forecast, der 1 Jahr in die zukunft prognostizieren soll
    reference_date = "2023-12-01" # immer 2024-12-01 minus die anzahl jahre
    sec_reference_date = "2022-12-01" # immer 2024-12-01 minus die anzahl jahre +1
    last_value = last_market_value(values, reference_date)
    dict = {}
    print(player_id)
    dict["market_value_t+1"] = get_filter_criteria(player_id)[0]
    dict["u26"] = u26(profile, reference_date, last_value)
    dict["o29"] = o29(profile, reference_date, last_value)
    #dict["GKo30"] = GKo30(profile, reference_date, last_value)
    #dict["time_left"] = time_left(profile.get("club", {}).get("contractExpires"), reference_date, last_value)
    dict["market_value_t"] = last_value
    dict["diff_market_value"] = diff_market_value(values, reference_date, sec_reference_date)
    dict["huge_difference"] = huge_difference(values, reference_date, sec_reference_date, last_value)
    return dict
    
def forecast_dictionary(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    reference_date = "2024-12-01"
    sec_reference_date = "2023-12-01"
    last_value = last_market_value(values, reference_date)
    dict = {}
    dict["u26"] = max(0, 26 - calculate_age(profile["dateOfBirth"], reference_date))
    dict["o30notGK"] = max(0, calculate_age(profile["dateOfBirth"], reference_date) - 30)
    dict["GKo30"] = calculate_age(profile["dateOfBirth"], reference_date) > 30 and profile["position"]["main"] == "Goalkeeper"
    dict["time_left"] = time_left(profile.get("club", {}).get("contractExpires"), reference_date)
    dict["market_value_t"] = last_value
    dict["diff_market_value"] = diff_market_value(values, reference_date, sec_reference_date)
    return dict

club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

player_list = []

for club in club_id:
    player_list.extend(get_club_players(club))
    
# -> lenght of playerlist = 1084 -> divide it in 4 samples
    
sample_1 = random.sample(player_list, 271)
player_list1 = [player for player in player_list if player not in sample_1]
print("ok")

sample_2 = random.sample(player_list1, 271)
player_list2 = [player for player in player_list if player not in sample_2]

sample_3 = random.sample(player_list2, 271)
player_list3 = [player for player in player_list if player not in sample_3]

sample_4 = player_list3 = [player for player in player_list if player not in sample_3]