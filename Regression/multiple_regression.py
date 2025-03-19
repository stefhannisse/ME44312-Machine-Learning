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
path_to_data = os.getcwd() + r'\..\Cleaning\boats_cleaned.json'

# Import the boats_cleaned
data = pd.read_json(path_to_data, convert_dates=False)

#Print the head
#print(data.head())

#Create a regression model, other than the LinearRegression model
model = LinearRegression()

#Get the feature values
X = data[['draught', 'distance_to_end']].values

#Check if X contains NaN values
if np.isnan(np.min(X)):
    print('NaN values found in feature')
    exit()

#Show the amount of data points
print('Amount of data points:', X)

#Get the ETA values
y = data['time_delta'].values

#Fit the model
model.fit(X, y)

#Print the score
print('Score for features draught and distance to end is', model.score(X, y))

#Create a graph to show the correlation
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data['draught'], data['distance_to_end'], y, color='black')

#Plot the regression line
X1 = np.linspace(0, 7.5, 100)
X2 = np.linspace(0, 100000, 100)
X1, X2 = np.meshgrid(X1, X2)
Z = model.predict(np.array([X1.ravel(), X2.ravel()]).T)
Z = Z.reshape(X1.shape)

ax.plot_surface(X1, X2, Z, color='blue', alpha=0.5)
plt.show()

