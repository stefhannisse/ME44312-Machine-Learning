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

data_full = pd.read_json('Cleaning/test_data.json', convert_dates=False)
X = data_full[['to_port','to_bow','to_stern', 'to_starboard','speed','draught','distance_to_end']] #No heading and course (results in NaN's) 
y_test = data_full['arrival_time'] - data_full['time']

# Preprocess the data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X = pd.DataFrame(X_scaled, columns=['to_port','to_bow','to_stern', 'to_starboard','speed','draught','distance_to_end'])

y_scaler = MinMaxScaler()
y = y_scaler.fit_transform(y_test.values.reshape(-1, 1))

model = keras.models.load_model(os.getcwd() + r'/Neural_net/trained_model.h5')

# Evaluate the model on the test data
loss, accuracy = model.evaluate(X, y)
print(f"Test Loss: {loss}")
print(f"Test Accuracy: {accuracy}")

predictions = model.predict(X)
predictions = y_scaler.inverse_transform(predictions)

# Plot actual vs predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, predictions, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')  # Perfect prediction line
plt.xlabel('Actual Time-to-Arrival [s]')
plt.ylabel('Predicted Time-to-Arrival [s]')
plt.ylim(-80000, 2080000)
plt.xlim(-80000, 2080000)
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
error = predictions.flatten() - y_test.values.flatten()
plt.scatter(y_test, error, alpha=0.6)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Actual Time-to-Arrival [s]')
plt.ylabel('Error [s]')
plt.grid(True)
plt.show()


rmse = np.sqrt(np.mean((predictions.flatten() - y_test.values.flatten()) ** 2))
print('Root Mean Squared Error:', rmse)


