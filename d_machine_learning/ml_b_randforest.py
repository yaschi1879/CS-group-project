import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np
import joblib
from d_machine_learning.ml_a_data import training_dictionary, sample_1

# Collecting the data
player_data = []
for player in sample_1:
    player_dict = training_dictionary(player)
    player_data.append(player_dict)

data_frame = pd.DataFrame(player_data)

# Drop 'n.a.' and NA values
data_frame_clean = data_frame.replace("n.a.", pd.NA).dropna()

# Target and Features
y = data_frame_clean["market_value_t+1"].astype(float)
X = data_frame_clean.drop(columns=["market_value_t+1"]).astype(float)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Training the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predictions on the test set
y_pred = rf_model.predict(X_test)

# Calculate R^2
r2 = r2_score(y_test, y_pred)
print(f"R^2 score: {r2}")

# Feature importances
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

# Plot feature importances
plt.figure()
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.show()

# Save the model
joblib.dump(rf_model, 'random_forest_model.pkl')

# Save feature importances
importances_df = pd.DataFrame(importances, index=X.columns[indices], columns=['Importance'])
importances_df.to_csv('feature_importances.csv')

# Save predictions
predictions_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predictions_df.to_csv('predictions.csv', index=False)
