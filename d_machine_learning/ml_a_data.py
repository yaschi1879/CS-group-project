from c_support.a_api_functions import get_profile, get_marketvalue_history, get_filter_criteria
from datetime import datetime
from dateutil.relativedelta import relativedelta

def time_left(contract, reference_date):
    if not contract:
        return "n.a."
    date = datetime.strptime(contract, "%b %d, %Y")
    reference = datetime.strptime(reference_date, "%Y-%m-%d")
    difference = relativedelta(date, reference)
    months = difference.years * 12 + difference.months
    return months

def last_market_value(values, reference_date):
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

def diff_market_value(values, reference_date, sec_reference_date):
    market_value_1 = last_market_value(values, reference_date)
    market_value_2 = last_market_value(values, sec_reference_date)
    if market_value_1 == "n.a." or market_value_2 == "n.a.":
        return "n.a."
    return market_value_1 - market_value_2

def calculate_age(birth_date, reference_date):
    birth = datetime.strptime(birth_date, "%b %d, %Y")
    reference = datetime.strptime(reference_date, "%Y-%m-%d")
    age = reference.year - birth.year
    if (reference.month, reference.day) < (birth.month, birth.day):
        age -= 1
    return age
    
def training_dictionary(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)
    # Beispiel für einen Forecast, der 1 Jahr in die zukunft prognostizieren soll
    reference_date = "2023-12-01" # immer 2024-12-01 minus die anzahl jahre
    sec_reference_date = "2022-12-01" # immer 2024-12-01 minus die anzahl jahre +1
    dict = {}
    print(player_id)
    dict["market_value_t+1"] = get_filter_criteria(player_id)[0]
    dict["u25"] = calculate_age(profile["dateOfBirth"], reference_date) <= 25
    dict["o30notGK"] = calculate_age(profile["dateOfBirth"], reference_date) >= 30 and not profile["position"]["main"] == "Goalkeeper"
    dict["GKo34"] = calculate_age(profile["dateOfBirth"], reference_date) >= 34 and profile["position"]["main"] == "Goalkeeper"
    dict["time_left"] = time_left(profile.get("club", {}).get("contractExpires"), reference_date)
    dict["market_value_t"] = last_market_value(values, reference_date)
    dict["diff_market_value"] = diff_market_value(values, reference_date, sec_reference_date)
    return dict
    
def forecast_dictionary(player_id):
    profile = get_profile(player_id)
    values = get_marketvalue_history(player_id)["marketValueHistory"]
    reference_date = "2024-12-01"
    sec_reference_date = "2023-12-01"
    dict = {}
    dict["u25"] = calculate_age(profile["dateOfBirth"], reference_date) <= 25
    dict["o30notGK"] = calculate_age(profile["dateOfBirth"], reference_date) >= 30 and not profile["position"]["main"] == "Goalkeeper"
    dict["GKo34"] = calculate_age(profile["dateOfBirth"], reference_date) >= 34 and profile["position"]["main"] == "Goalkeeper"
    dict["time_left"] = time_left(profile.get("club", {}).get("contractExpires"), reference_date)
    dict["market_value_t"] = last_market_value(values, reference_date)
    dict["diff_market_value"] = diff_market_value(values, reference_date, sec_reference_date)
    return dict