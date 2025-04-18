'''
This python script will apply regression to estimate the time untill arrival based on the following features:
- Draught
- Distance till end
'''

import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import os
import matplotlib.pyplot as plt

#Change the path to the location of the cleaned data
#path_to_data = os.getcwd() + r'/../Cleaning/boats_cleaned.json'

# Import the boats_cleaned
#data = pd.read_json(path_to_data, convert_dates=False)
#
# Remove the values where the time_delta > 1.5e6

# Import the x_test from Neural net
data = pd.read_json(os.getcwd() + r'\..\Cleaning\test_data.json', convert_dates=False)

#Remove the values where the time_delta > 1.5e6
#data = data[data['time_delta'] < 1.5e6]

#Print the head
#print(data.head())

#Create a regression model, other than the LinearRegression model
model = LinearRegression()

#Get the feature values
X = data[['distance_to_end', 'to_port', 'to_bow', 'to_stern', 'to_starboard', 'draught']].values
y = data['time_delta'].values

'''
Performance so far:
draught: 0.17276758191742603
distance_to_end: 0.736882709816169
distance_to_end & speed: 0.7992994359838999
draught & distance_to_end: 0.751104789407439
draught & to_bow: 0.19082571697052608
distance_to_end & draught & to_bow & to_stern & to_port & to_starboard & speed: 0.8057583594698429,
distance_to_end & draught & to_bow & to_stern & to_port & to_starboard: 0.754534693418768
'''

#Check if X contains NaN values
if np.isnan(np.min(X)):
    print('NaN values found in feature')
    exit()

#Show the amount of data points
print('Amount of data points:', X)

#Get the ETA values
#y = data['time_delta'].values
#Get the y values from the Neural net folder, file y_test.json
#y = pd.read_json(os.getcwd() + r'\..\Cleaning\test_data.json', convert_dates=False).values.flatten()

#indexes = [i for i, v in enumerate(y) if v > 1.5e6]
#Remove these indexes from y and X
#y = np.delete(y, indexes)
#X = np.delete(X, indexes, axis=0)

#Fit the model
fit = model.fit(X, y)
#Print the score
print('Score for features draught and distance to end is', model.score(X, y))

#Calculate the mean squared error
pred = model.predict(X)
rmse = np.sqrt(np.mean((pred - y) ** 2))
print('Root Mean Squared Error:', rmse)

plt.figure(figsize=(8, 6))
#Plot the estimated arrival time and the actual arrival time
plt.scatter(y, pred, alpha=0.6)
plt.xlabel('Actual Time to arrival [s]')
plt.ylabel('Predicted Time to arrival [s]')
#Make sure the x axis and y axis have the same scale

#Plot the predicted line from the model fit
# plt.plot([y.min(), y.max()], [model.predict(X).min(), pred.max()], color='blue', linewidth=3)


#Draw a line on x=y to show the perfect prediction
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--')

plt.grid(True)
plt.ylim(-80000, 2080000)
plt.xlim(-80000, 2080000)
plt.show()

plt.figure(figsize=(8, 6))
error = pred - y
plt.scatter(y, error, alpha=0.6)
plt.axhline(0, color='red', linestyle='--')

plt.xlabel('Actual Time to arrival [s]')
plt.ylabel('Error [s]')
plt.grid(True)
plt.show()

#Create a graph to show the correlation
# fig = plt.figure(figsize=(20, 10))
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(data['draught'], data['distance_to_end'], y, color='black')
#
# #Plot the regression line
# X1 = np.linspace(0, 7.5, 100)
# X2 = np.linspace(0, 100000, 100)
# X1, X2 = np.meshgrid(X1, X2)
# Z = model.predict(np.array([X1.ravel(), X2.ravel()]).T)
# Z = Z.reshape(X1.shape)
#
# ax.plot_surface(X1, X2, Z, color='blue', alpha=0.5)
# plt.show()

