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
        return [value, math.log(value)]
    except:
        return ["n.a.", "n.a."]

def log_value_t(last_value):
    try:
        return math.log(last_value)
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

def u25(profile, reference_date, last_value):
    try:
        value = ((max(0, 25 - calculate_age(profile["dateOfBirth"], reference_date)))**2) * last_value
        value_log = math.log(max(((max(0, 25 - calculate_age(profile["dateOfBirth"], reference_date)))**2) * last_value, 1))
        return [value, value_log]
    except:
        return ["n.a.", "n.a."]
    

def o30(profile, reference_date, last_value):
    try:
        value = (((max(0, calculate_age(profile["dateOfBirth"], reference_date) - 30)))**2) * last_value
        value_log = math.log(max(((max(0, calculate_age(profile["dateOfBirth"], reference_date) - 30))**2) * last_value, 1))
        return [value, value_log]
    except:
        return ["n.a.", "n.a."]
    

def diff_market_value(values, reference_date, sec_reference_date, last_value):
    try:
        market_value_1 = last_market_value(values, reference_date)
        market_value_2 = last_market_value(values, sec_reference_date)
        value = market_value_1 - market_value_2
        log_value = value / last_value
        return [value, log_value]
    except:
        return ["n.a.", "n.a."]

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
    

def training_dictionary(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    # Beispiel für einen Forecast, der 2 Jahre in die zukunft prognostizieren soll
    reference_date = "2022-12-01" # immer 2024-12-01 minus die gewünschten jahre in die zukunft
    sec_reference_date = "2021-12-01" # immer 2024-12-01 minus die gewünschten jahre in die zukunft + 1
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


def forecast_1year(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    reference_date = "2024-12-01"
    sec_reference_date = "2023-12-01"
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

def forecast_2year(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    reference_date = "2024-12-01"
    sec_reference_date = "2022-12-01"
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