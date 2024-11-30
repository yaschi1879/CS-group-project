# dieser part ist für die erstellung der player_list, dauert ca 1min
# zuerst ausführen
import random
import pandas as pd
from ml_data import training_dictionary
from api_functions import get_club_players

club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

player_list = []

for club in club_id:
    player_list.extend(get_club_players(club))
# -------------------------------------------------------------------------------
# jetzt kommt die erstellung der daten für 120 random spieler
player_sample = random.sample(player_list, 12)
player_data = []

for player in player_sample:
    player_dict = training_dictionary(player)
    player_data.append(player_dict)

data_frame = pd.DataFrame(player_data)
print(data_frame.head())
# --------------------------------------------------------------------------------
# jetzt kommt die erstellung der regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

y = data_frame["market_value_t+1"]
X = data_frame.drop(columns=["market_value_t+1"])

# alle Zeilen, die n.a. enthalten, ignorieren
data_frame_clean = data_frame.replace("n.a.", pd.NA).dropna()

# Dummies in 1 und 0 konvertieren
X = X.astype(float)

# Daten in Trainings- und Testsets aufteilen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 3. Modell initialisieren und trainieren
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Vorhersagen und Metriken
y_pred = model.predict(X_test)

print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R^2 Score:", r2_score(y_test, y_pred))

# 5. Modell-Koeffizienten und Intercept
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)

# 6. Ergebnisse in einem DataFrame ausgeben
coef_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_
    })
print(coef_df)