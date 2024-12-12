import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the parent directory to the system path for module access
from d_machine_learning.ml_a_data import forecast_1year, forecast_2year
from c_support.a_api_functions import get_marketvalue_history

# Function to clean and standardize market value strings
def clean_value(value):
    value = value.replace('€', '').replace(',', '')
    if 'm' in value:
        return float(value.replace('m', ''))
    elif 'k' in value:
        return float(value.replace('k', '')) / 1000

# Regression data
# market_value t+1 = β0 + β1*market_value t + β2*u25 + β3*o30 + β4*diff_market_value + B5*huge_diff + ϵ

date_1 = "Dec 1, 2025"
market_value_t_1 = 0.8412
u25_1 = 0.0072
o30_1 = -0.0270
diff_market_value_1 = 0.4542
huge_diff_1 = -0.2903

date_2 = "Dec 1, 2026"
market_value_t_2 = 0.7121
u25_2 = 0.0210
o30_2 = -0.0695
diff_market_value_2 = 0.4773
huge_diff_2 = -0.2159

# Generate market value forecasts for one and two years into the future   
def forecast(player_id):
    data1 = forecast_1year(player_id)
    data2 = forecast_2year(player_id)
    
    try:
        # Compute forecasted values for year 1
        value_11 = data1["market_value_t"] * market_value_t_1
        value_12 = data1["u25"] * u25_1
        value_13 = data1["o30"] * o30_1
        value_14 = data1["diff_market_value"] * diff_market_value_1
        value_15 = data1["huge_diff"] * huge_diff_1
        
        # Compute forecasted values for year 2
        value_21 = data2["market_value_t"] * market_value_t_2
        value_22 = data2["u25"] * u25_2
        value_23 = data2["o30"] * o30_2
        value_24 = data2["diff_market_value"] * diff_market_value_2
        value_25 = data2["huge_diff"] * huge_diff_2
    
        # Get current market value from historical data
        value_list = get_marketvalue_history(player_id)
        current = clean_value(value_list[len(value_list) - 1]["value"])
        
        # Calculate the forecasts for years 1 and 2, ensuring non-negative results
        forecast_1 = max(0, value_11 + value_12 + value_13 + value_14 + value_15)
        forecast_2 = max(0, value_21 + value_22 + value_23 + value_24 + value_25)
        
        # Create forecast data items
        item_0 = {"date": "Dec 12, 2024", "value": current}
        item_1 = {"date": date_1, "value": forecast_1}
        item_2 = {"date": date_2, "value": forecast_2}
        
    except:
        # Handle errors and provide fallback items
        item_0 = "no forecast available"
        item_1 = "no forecast available"
        item_2 = "no forecast available"
    
    return [item_0, item_1, item_2]