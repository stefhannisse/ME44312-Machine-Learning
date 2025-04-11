import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import json
import geopy.distance
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras import activations

data_full = pd.read_json('Cleaning/boats_cleaned_aarburg.json', convert_dates=False)
X = data_full[['to_port','to_bow','to_stern', 'to_starboard','speed','draught','distance_to_end']] #No heading and course (results in NaN's) 
y_actual = data_full['arrival_time'] - data_full['time']

# Preprocess the data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X = pd.DataFrame(X_scaled, columns=['to_port','to_bow','to_stern', 'to_starboard','speed','draught','distance_to_end'])

y_scaler = MinMaxScaler()
y = y_scaler.fit_transform(y_actual.values.reshape(-1, 1))

model = keras.models.load_model(os.getcwd() + r'/Neural_net/trained_model.h5')

# Evaluate the model on the test data
loss, accuracy = model.evaluate(X, y)
print(f"Test Loss: {loss}")
print(f"Test Accuracy: {accuracy}")

predictions = model.predict(X)
predictions = y_scaler.inverse_transform(predictions)

# Plot the predictions vs the actual values
plt.figure(figsize=(10, 6))
plt.scatter(y_actual, predictions, label='Predictions vs Actual', color='blue', alpha=0.6)
plt.plot([y_actual.min(), y_actual.max()], [y_actual.min(), y_actual.max()], color='red', linestyle='--', label='x = y')
plt.xlabel('Actual Arrival Time')
plt.ylabel('Predicted Arrival Time')
plt.title('Predictions vs Actual Arrival Time')
plt.legend()
plt.grid(True)
plt.show()

rmse = np.sqrt(np.mean((predictions - y) ** 2))
print('Root Mean Squared Error:', rmse)



