# Ship Arrival Time Prediction - ME44312 Project

This project was developed for the course ME44312 at TU Delft by team number 2. It uses machine learning techniques to predict vessel arrival times based on AIS (Automatic Identification System) data.

## Project Team
- J. Lakeman (5171156)
- D. Exterkate (5169917)
- L.J. Schonewille (4878345)
- B. Spée (5414776)
- Stef Hannisse (6061818)

## Project Structure

```
├── .idea/                        # PyCharm IDE configuration files
├── Neural_net/                   # Neural network implementation
│   ├── scaling.py                # Data scaling and neural network training
│   └── test_data.py              # Testing the trained neural network model
├── Cleaning/                     # Data cleaning scripts and output, used for the training of both models
├── Regression/                   # Regression model implementations
│   ├── RandomForestRegressor.py  # Random Forest regression model
│   ├── feature_regression_individual.py  # Individual feature analysis
│   ├── multiple_regression.py    # Multiple linear regression implementation
│   └── multiple_regression_test.py  # Testing the multiple regression model
└── ais_predict_ships.py          # Script for analyzing ship data and building datasets
```

## Features

The models predict ship arrival times based on the following features:
- Distance to end of journey
- Ship dimensions (to_port, to_bow, to_stern, to_starboard)
- Speed
- Draught (depth of a ship's keel below the water)
- Location coordinates

## Model Approaches

### Neural Network
Located in the `Neural_net/` directory, this approach uses TensorFlow/Keras to build a deep learning model with fully connected layers. The model is trained to predict time-to-arrival based on scaled input features.

### Regression Models
The `Regression/` directory contains multiple regression approaches:
- Linear Regression with individual features
- Multiple Linear Regression combining several features
- Random Forest Regression for handling non-linear relationships

## Data Processing

The project uses AIS data from the Port of Rotterdam. Raw data is processed to extract relevant features and create training/testing datasets. The data cleaning process appears to be handled in the `Cleaning/` directory (scripts not visible in this repo snapshot).

## Performance

Models are evaluated using metrics such as:
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)

Visualizations include:
- Actual vs. Predicted arrival time plots
- Error distribution plots
- Training performance plots for neural networks

## Usage

To use these models:
1. Clean and prepare your ship data
2. Train a model using either `Neural_net/scaling.py` or the regression models
3. Test the model's performance with the corresponding test scripts

## Requirements

- Python 3.11
- TensorFlow/Keras
- scikit-learn
- pandas
- numpy
- matplotlib
- geopy