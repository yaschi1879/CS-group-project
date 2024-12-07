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
    
    forecast_1 = str(sum(intercept_1, value_11))
    forecast_2 = str(sum(intercept_2, value_21))
    forecast_3 = str(sum(intercept_3, value_31))
    
    item_1 = {"date": date_1, "value": forecast_1}
    item_2 = {"date": date_2, "value": forecast_2}
    item_3 = {"date": date_3, "value": forecast_3}
    
    return [item_1, item_2, item_3]
    