from d_machine_learning.ml_a_data import forecast_dictionary

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
    data = forecast_dictionary(player_id)
    
    value_11 = data["market_value_t"] * coefficient_11
    value_21 = data["market_value_t"] * coefficient_21
    value_31 = data["market_value_t"] * coefficient_31
    
    forecast_1 = intercept_1 + value_11
    forecast_2 = intercept_2 + value_21
    forecast_3 = intercept_3 + value_31

    forecast_1_str = str(forecast_1)
    forecast_2_str = str(forecast_2)
    forecast_3_str = str(forecast_3)
    
    item_1 = {"date": date_1, "value": forecast_1_str}
    item_2 = {"date": date_2, "value": forecast_2_str}
    item_3 = {"date": date_3, "value": forecast_3_str}
    
    return [item_1, item_2, item_3]
    