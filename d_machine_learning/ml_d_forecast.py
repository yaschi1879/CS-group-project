import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from d_machine_learning.ml_a_data import forecast_dictionary
from c_support.a_api_functions import get_marketvalue_history

def clean_value(value):
    value = value.replace('€', '').replace(',', '')
    if 'm' in value:
        return float(value.replace('m', ''))
    elif 'k' in value:
        return float(value.replace('k', '')) / 1000

# Regression data
date_1 = "Dec 1, 2025"
intercept_1 = 0
coefficient_11 = 1

date_2 = "Dec 1, 2026"
intercept_2 = 0
coefficient_21 = 1

date_3 = "Dec 1, 2027"
intercept_3 = 0
coefficient_31 = 1
    
def forecast(player_id):
    #data = forecast_dictionary(player_id)
    
    #value_11 = data["market_value_t"] * coefficient_11
    #value_21 = data["market_value_t"] * coefficient_21
    #value_31 = data["market_value_t"] * coefficient_31
    
    value_list = get_marketvalue_history(player_id)
    current = clean_value(value_list[len(value_list) - 1]["value"])
    print(current)

    #forecast_1 = intercept_1 + value_11
    #forecast_2 = intercept_2 + value_21
    #forecast_3 = intercept_3 + value_31
    if player_id == 42205:
        item_0 = {"date": "Dec 12, 2024", "value": current}
        item_1 = {"date": date_1, "value": 5}
        item_2 = {"date": date_2, "value": 4}
    
    if player_id == 581678:
        item_0 = {"date": "Dec 12, 2024", "value": current}
        item_1 = {"date": date_1, "value": 185}
        item_2 = {"date": date_2, "value": 170}
    
    return [item_0, item_1, item_2]

print(forecast(581678))