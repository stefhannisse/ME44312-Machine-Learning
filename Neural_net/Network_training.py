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

data = pd.read_json(os.getcwd() + r'/Cleaning/training_data.json', convert_dates=False)
# print(data.head())

#create df with only inputs and a df with labels (arrival_time)
X = data[['to_port','to_bow','to_stern', 'to_starboard','speed','draught','distance_to_end']] #No heading and course (results in NaN's) 
y = data['arrival_time']

#scale all data except type and time
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
X = pd.DataFrame(X, columns=['to_port','to_bow','to_stern', 'to_starboard','speed','draught','distance_to_end'])

#convert categorical data with one hot encoding
# encoder = OneHotEncoder(sparse_output=True)
# cat_type = encoder.fit_transform(data[['type']])
# X['type'] = cat_type.toarray()

#convert input time to estimate time-to-arrival (can apparently be easier for learning)
y = data['arrival_time'] - data['time']
y = np.clip(y, 0, None)  # Clip negative values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.22222, random_state=1) #This gives 70/20/10 split as this is the 90 part
print(X_train.head())
print(y_train.head())

#export X_test and y_test to json
X_test.to_json('X_test.json', orient='records')
y_test.to_json('y_test.json', orient='records')

#scale target data
y_scaler = MinMaxScaler()
y_train = y_scaler.fit_transform(y_train.values.reshape(-1, 1))
y_test = y_scaler.transform(y_test.values.reshape(-1, 1))

print(X.isna().sum())  # Check for NaNs

#build model
input_dim = X_train.shape[1]
model = keras.models.Sequential([
    keras.layers.InputLayer(input_shape=(input_dim,)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1)
])

optimizer = tf.keras.optimizers.Adam(clipnorm=1.0)

# Implement early stopping
early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss', 
    patience=15,  # Stop training if validation loss doesn't improve for 15 epochs
    restore_best_weights=True
)
model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['mean_squared_error'])

#train model
history = model.fit(
    X_train, 
    y_train, 
    epochs=200, 
    validation_data=(X_test, y_test), 
    callbacks=[early_stopping]
)

loss, mse = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test mse:', mse)

# Save the model to a file
model.save('trained_model.h5')
print("Model saved to 'trained_model.h5'")

# Make predictions
predictions = model.predict(X_test)
print(predictions)

#plot training performance
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()


# inverse transform scaled data
predictions = y_scaler.inverse_transform(predictions)
y_test = y_scaler.inverse_transform(y_test)

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
error = predictions - y_test
plt.scatter(y_test, error, alpha=0.6)
plt.axhline(0, color='red', linestyle='--')

plt.xlabel('Actual Time to arrival [s]')
plt.ylabel('Error [s]')
plt.grid(True)
plt.show()


rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
print('Root Mean Squared Error:', rmse)