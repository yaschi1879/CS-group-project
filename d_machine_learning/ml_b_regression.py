import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import time
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
from d_machine_learning.ml_a_data import training_dictionary
from c_support.a_api_functions import get_club_players

club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

player_list = []

for club in club_id:
    player_list.extend(get_club_players(club))

player_data = []
for player in player_list:
    player_dict = training_dictionary(player)
    player_data.append(player_dict)
    time.sleep(1)

data_frame = pd.DataFrame(player_data)
print(data_frame)
# --------------------------------------------------------------------------------
# jetzt kommt die erstellung der regression

y = data_frame["market_value_t+1"]
X = data_frame.drop(columns=["market_value_t+1"])

# Bereinigung der Daten
data_frame_clean = data_frame.replace("n.a.", pd.NA).dropna()

# Ziel- und Feature-Matrix
y = data_frame_clean["market_value_t+1"].astype(float)
X = data_frame_clean.drop(columns=["market_value_t+1"]).astype(float)

# Hinzufügen einer Spalte für den Intercept
X = sm.add_constant(X)

# Aufteilung in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Statsmodels-Modell fitten
model = sm.OLS(y_train, X_train)
results = model.fit()

# Ausgabe der Zusammenfassung
print(results.summary())

# Plot residuals
fitted_values = results.fittedvalues  # Predicted values
residuals = results.resid  # Residuals

# Q-Q Plot
sm.qqplot(residuals, line='45')
plt.title('Q-Q Plot of Residuals')
plt.show()

# Optional: Residuals vs. Fitted Values
plt.scatter(fitted_values, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs. Fitted Values')
plt.show()