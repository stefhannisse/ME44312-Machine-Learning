import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load the data
data = pd.read_json('../Cleaning/boats_cleaned.json')

# Display basic information
print(data.info())
print(data.describe())

# Check for missing values
print(data.isnull().sum())

# Convert time columns to datetime
data['time'] = pd.to_datetime(data['time'], unit='s')
data['arrival_time'] = pd.to_datetime(data['arrival_time'], unit='s')

# Feature Engineering
data['time_diff'] = (data['arrival_time'] - data['time']).dt.total_seconds()
data['distance_to_end_km'] = data['distance_to_end'] / 1000

# Select features and target
features = ['location_lat', 'location_long', 'speed', 'course', 'distance_to_end_km']
target = 'time_diff'

X = data[features]
y = data[target]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Plot the results
plt.scatter(y_test, y_pred)
plt.xlabel('Actual Time Difference')
plt.ylabel('Predicted Time Difference')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')  # Perfect prediction line
plt.title('Actual vs Predicted Time Difference')
plt.show()