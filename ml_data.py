from api_functions import get_profile, get_marketvalue_history, get_stats, get_filter_criteria
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
    if last_update is None:
        return "n.a."
    return market_value

def diff_market_value(player_id, reference_date, sec_reference_date):
    market_value_1 = last_transfer_value(player_id, reference_date)
    market_value_2 = last_transfer_value(player_id, sec_reference_date)
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

def minutes_played(player_id, reference_date):
    data = get_stats(player_id)
    interest = {"CL": 3, "EL": 2, "UCOL": 1}
    minutes = 0
    if reference_date == "2024-07-01":
        reference = "23/24"
        stop_at = "22/23"
        weight = 0.5
    elif reference_date == "2024-12-01":
        reference = "24/25"
        stop_at = "23/24"
        weight = 1
    for stat in data:
        if stat["seasonID"] == stop_at:
            break
        if stat.get("seasonID") == reference and stat.get("competitionID") in interest:
            competition = stat["competitionID"]
            comp_weight = interest[competition]
            game_time = stat.get("minutesPlayed", "0").replace("'", "")
            minutes += int(game_time) * weight * comp_weight
    return minutes
    
def training_dictionary(player_id):
    profile = get_profile(player_id)
    history = get_marketvalue_history(player_id)["marketValueHistory"]
    reference_date = "2024-07-01"
    sec_reference_date = "2023-12-01"
    dict = {}
    print(player_id)
    dict["market_value_t+1"] = get_filter_criteria(player_id)[0]
    dict["GK"] = profile["position"]["main"] == "Goalkeeper"
    dict["u26"] = calculate_age(profile["dateOfBirth"], reference_date) < 26
    dict["o30"] = calculate_age(profile["dateOfBirth"], reference_date) > 30
    dict["time_left"] = time_left(profile.get("club", {}).get("contractExpires"), reference_date)
    dict["market_value_t"] = last_transfer_value(history, reference_date)
    dict["diff_market_value"] = diff_market_value(player_id, reference_date, sec_reference_date)
    dict["min_europacup"] = minutes_played(player_id, reference_date)
    return dict
    
def forecast_dictionary(player_id):
    profile = get_profile(player_id)
    history = get_marketvalue_history(player_id)["marketValueHistory"]
    reference_date = "2024-12-01"
    sec_reference_date = "2023-12-01"
    dict = {}
    dict["GK"] = profile["position"]["main"] == "Goalkeeper"
    dict["u26"] = calculate_age(profile["dateOfBirth"], reference_date) < 26
    dict["o30"] = calculate_age(profile["dateOfBirth"], reference_date) > 30
    dict["time_left"] = time_left(profile["club"]["contractExpires"], reference_date)
    dict["marketValue"] = last_transfer_value(history, reference_date)
    dict["diff_marketValue"] = diff_market_value(player_id, reference_date, sec_reference_date)
    dict["min_europacup"] = minutes_played(player_id, reference_date)
    return dict