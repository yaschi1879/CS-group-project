# We hereby declare that the vast majority of the code for this project has been written by us independently. 
# We have utilized ChatGPT as a tool for conceptual purposes and for assistance with small, 
# specific parts of the code, such as generating comments or clarifying implementation ideas.
# However, all critical design decisions, core functionality, 
# and the implementation of the primary codebase were developed through our own efforts and understanding.

# This is Link for the Game application: https://cs-group-project-8c9afmnnkpup2ze7c3yxvo.streamlit.app/ 

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the parent directory to the system path for module access
import pandas as pd
import numpy as np
import time
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import statsmodels.api as sm
import joblib
from d_machine_learning.ml_a_data import training_dictionary
from c_support.a_api_functions import get_club_players

# List of club IDs to fetch players from
club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

# Fetch player IDs for each club
player_list = []

for club in club_id:
    player_list.extend(get_club_players(club))

# Randomly select 20 players for testing purposes
test = random.sample(player_list, 20)

# Generate training data for players
player_data = []
player_data_log = []
for player in player_list:
    player_dict = training_dictionary(player)
    player_data.append(player_dict[0]) # Normal values
    player_data_log.append(player_dict[1]) # Log-transformed values
    time.sleep(1) # Delay to avoid API rate limits

data_frame = pd.DataFrame(player_data)
data_frame_log = pd.DataFrame(player_data_log)

# --------------------------------------------------------------------------------
# Regression analysis: Create models for normal and log-transformed data

# Data cleaning: Remove missing or invalid values
data_frame_clean = data_frame.replace("n.a.", pd.NA).dropna()
data_frame_clean_log = data_frame_log.replace("n.a.", pd.NA).dropna()

# Define target (y) and feature matrix (X) for normal data
y = data_frame_clean["market_value_t+1"].astype(float)
X = data_frame_clean.drop(columns=["market_value_t+1"]).astype(float)
X = sm.add_constant(X) # Add intercept for regression

# Define target (y1) and feature matrix (X1) for log-transformed data
y1 = data_frame_clean_log["market_value_t+1"].astype(float)
X1 = data_frame_clean_log.drop(columns=["market_value_t+1"]).astype(float)
X1 = sm.add_constant(X1) # Add intercept for regression

# Split data into training and testing sets for normal and log-transformed data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.3)

# Fit OLS regression models
model = sm.OLS(y_train, X_train)
results = model.fit()

model_log = sm.OLS(y1_train, X1_train)
results_log = model_log.fit()

# Print summaries of regression results
print("OLS Regression Results:")
print(results.summary())
print("OLS Log Regression Results:")
print(results_log.summary())

# Analyze residuals and fitted values for normal regression
fitted_values = results.fittedvalues
residuals = results.resid

fitted_values_log = results_log.fittedvalues
residuals_log = results_log.resid

# Q-Q plot for residuals
sm.qqplot(residuals, line='45')
plt.title('Q-Q Plot of Residuals (OLS Regression)')
plt.show()

sm.qqplot(residuals_log, line='45')
plt.title('Q-Q Plot of Residuals Log (OLS Regression)')
plt.show()

# Residuals vs. Fitted Values plot
plt.scatter(fitted_values, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs. Fitted Values (OLS Regression)')
plt.show()

plt.scatter(fitted_values_log, residuals_log)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs. Fitted Values Log (OLS Regression)')
plt.show()

# Analyze outliers using Cook's Distance
influence = results.get_influence()
cooks_d, p_values = influence.cooks_distance

influence_log = results_log.get_influence()
cooks_d1, p_values1 = influence_log.cooks_distance

# Identify potential outliers
outliers = np.where(cooks_d > 4 / len(X_train))[0]
print(f"Potentielle Ausreißer (Index): {outliers}")

outliers_log = np.where(cooks_d1 > 4 / len(X1_train))[0]
print(f"Potentielle Ausreißer (Index): {outliers_log}")

# Remove outliers and refit the models if necessary
if len(outliers) > 0:
    X_train_filtered = X_train.drop(index=X_train.index[outliers])
    y_train_filtered = y_train.drop(index=y_train.index[outliers])

    model_filtered = sm.OLS(y_train_filtered, X_train_filtered)
    results_filtered = model_filtered.fit()

    print("OLS Regression Results After Removing Outliers:")
    print(results_filtered.summary())
    
if len(outliers_log) > 0:
    X1_train_filtered = X1_train.drop(index=X1_train.index[outliers_log])
    y1_train_filtered = y1_train.drop(index=y1_train.index[outliers_log])

    model_filtered_log = sm.OLS(y1_train_filtered, X1_train_filtered)
    results_filtered_log = model_filtered_log.fit()

    print("OLS Regression Results Log After Removing Outliers:")
    print(results_filtered_log.summary())

# Re-analyze residuals and fitted values after removing outliers
fitted_values = results_filtered.fittedvalues
residuals = results_filtered.resid

fitted_values_log = results_filtered_log.fittedvalues
residuals_log = results_filtered_log.resid

# Q-Q plot for residuals after outlier removal
sm.qqplot(residuals, line='45')
plt.title('Q-Q Plot of Residuals contr. for Outliners (OLS Regression)')
plt.show()

sm.qqplot(residuals_log, line='45')
plt.title('Q-Q Plot of Residuals Log contr. for Outliners (OLS Regression)')
plt.show()

# Residuals vs. Fitted Values after outlier removal
plt.scatter(fitted_values, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs. Fitted Values contr. for Outliners (OLS Regression)')
plt.show()

plt.scatter(fitted_values_log, residuals_log)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs. Fitted Values Log contr. for Outliners (OLS Regression)')
plt.show()

# ----------------------------------------------------------------------------------------------------
# Build a Random Forest model for normal data

# Redefine target (y) and feature matrix (X) for Random Forest
y = data_frame_clean["market_value_t+1"].astype(float)
X = data_frame_clean.drop(columns=["market_value_t+1"]).astype(float)
X = sm.add_constant(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.3)

# Train Random Forest model
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_model.predict(X_test)

# Calculate R^2 / Evaluate model performance using R^2 score
r2 = r2_score(y_test, y_pred)
print(f"R^2 score of random forest: {r2}")

# Analyze feature importances
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

# Plot feature importances
plt.figure()
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.show()

# Save the Random Forest model
joblib.dump(rf_model, 'random_forest_model.pkl')

# Save feature importances to a CSV file
importances_df = pd.DataFrame(importances, index=X.columns[indices], columns=['Importance'])
importances_df.to_csv('feature_importances.csv')

# Save predictions to a CSV file
predictions_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predictions_df.to_csv('predictions.csv', index=False)