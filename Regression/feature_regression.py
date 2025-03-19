from math import isnan

import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import os

#Change the path to the location of the cleaned data
path_to_data = os.getcwd() + r'\..\Cleaning\boats_cleaned.json'

# Import the boats_cleaned
data = pd.read_json(path_to_data, convert_dates=False)

#Print the head
print(data.head())

#Print all the available columns
print(data.columns)

#Columns to check the correlation with the ETA
columns_to_check = ['speed', 'distance_to_end', 'time', 'draught', 'course', 'to_port', 'to_bow', 'to_stern', 'to_starboard']

#Normalize the data
data[columns_to_check] = (data[columns_to_check] - data[columns_to_check].mean()) / data[columns_to_check].std()

#For every feature, create a linear regression model to check the correlation with the ETA
for feature in data.columns:
    if feature not in columns_to_check:
        continue

    #Create a linear regression model
    model = LinearRegression()

    #Get the feature values
    X = data[feature].values.reshape(-1, 1)

    #Check if X contains NaN values
    if np.isnan(np.min(X)):
        print('NaN values found in feature', feature)
        continue

    #Get the ETA values
    y = data['arrival_time'].values

    #Fit the model
    model.fit(X, y)

    #Print the score
    print('Score for feature', feature, 'is', model.score(X, y))

    #Print the coefficients
    print('Coefficients for feature', feature, 'are', model.coef_)

    #Print the intercept
    print('Intercept for feature', feature, 'is', model.intercept_)

    print('------------------------------------')

    #Print the prediction for the first 5 values
    print('Predictions for feature', feature, 'are', model.predict(X[:5]))
    print('------------------------------------')
    print('------------------------------------')