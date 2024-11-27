from api_functions import get_profile, get_marketvalue_history
from datetime import datetime
from dateutil.relativedelta import relativedelta

def time_left(contract, reference_date):
    date = datetime.strptime(contract, "%b %d, %Y")
    reference = datetime.strptime(reference_date, "%Y-%m-%d")
    difference = relativedelta(date, reference)
    months = difference.years * 12 + difference.months
    return months

def last_transfer_value(values, reference_date):
    date_reference = datetime.strptime(reference_date, "%Y-%m-%d")
    last_update = None
    for value in values:
        value_date = datetime.strptime(value["date"], "%b %d, %Y")
        if value_date < date_reference:
            if last_update is None or value_date > datetime.strptime(last_update["date"], "%b %d, %Y"):
                last_update = value
    market_value =  last_update["value"].replace("€", "")
    if "m" in market_value:
        market_value = float(market_value.replace("m", ""))
    elif "k" in market_value:
        market_value = float(market_value.replace("k", "")) / 1000
    return market_value

def calculate_age(birth_date, reference_date):
    birth = datetime.strptime(birth_date, "%b %d, %Y")
    reference = datetime.strptime(reference_date, "%Y-%m-%d")
    age = reference.year - birth.year
    if (reference.month, reference.day) < (birth.month, birth.day):
        age -= 1
    return age

def training_dictionary(player_id):
    profile = get_profile(player_id)
    history = get_marketvalue_history(player_id)["marketValueHistory"]
    reference_date = "2024-07-01"
    dict = {}
    dict["GK"] = profile["position"]["main"] == "Goalkeeper"
    dict["u26"] = calculate_age(profile["dateOfBirth"], reference_date) < 26
    dict["o30"] = calculate_age(profile["dateOfBirth"], reference_date) > 30
    dict["time_left"] = time_left(profile["club"]["contractExpires"], reference_date)
    dict["market_value"] = last_transfer_value(history, reference_date)
    dict["diff_market_value"] = last_transfer_value(history, reference_date) - last_transfer_value(history, "2023-12-01")
    #dict["min_CL"] =
    #dict["min_EL"] = 
    return dict

print(training_dictionary(139208))
    
def forecast_dictionary(player_id):
    profile = get_profile(player_id)
    history = get_marketvalue_history(player_id)["marketValueHistory"]
    reference_date = "2024-12-01"
    dict = []
    dict["GK"] = profile["position"]["main"] == "Goalkeeper"
    dict["u26"] = calculate_age(profile["age"], reference_date) < 26
    dict["o30"] = calculate_age(profile["age"], reference_date) > 30
    dict["contract"] = time_left(profile["club"]["contractExpires"], reference_date)
    dict["marketValue"] = last_transfer_value(history, reference_date)
    dict["diff_marketValue"] = last_transfer_value(history, reference_date) - last_transfer_value(history, "2024-12-01")
    #dict["min_CL"] =
    #dict["min_EL"] = 
    return dict