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
├── raw_data_rotterdam/           # Raw AIS datapoints for the Port of Rotterdam
│   ├── raw_ais_data_2021_rotterdam_1609459200.0_1609545600.0.json  # Sample raw AIS data file
│   └── ...                       # Additional raw AIS data files
├── Neural_net/                   # Neural network implementation
│   ├── Network_training.py       # Neural network training pipeline
│   ├── Network_visualisation.py  # Visualization of neural network performance
│   └── trained_model.h5          # Saved trained neural network model
├── Cleaning/                     # Data cleaning scripts and output
│   ├── Cleaning_location.py      # Script to clean and process location data
│   ├── Training_split.py         # Script to split data into training/test sets
│   └── boats_cleaned_*.json      # Cleaned boat data ready for model training
├── Regression/                   # Regression model implementations
│   ├── RandomForestRegressor.py  # Random Forest regression model
│   ├── feature_regression_individual.py  # Individual feature analysis
│   ├── multiple_regression.py    # Multiple linear regression implementation
│   └── multiple_regression_test.py  # Testing the multiple regression model
├── Trip_visualisations/          # Visualizations of ship trips and data
│   ├── plot_nb.ipynb             # Jupyter notebook for creating HTML visualizations
│   └── HTML/                     # HTML-based trip visualizations
│       ├── trudie_trips.html     # Visualization for ship "TRUDIE"
│       └── ...                   # Additional ship visualizations
└── README.md                     # Project documentation
```

## Features

The models predict ship arrival times based on the following features:
- Distance to end of journey
- Ship dimensions (to_port, to_bow, to_stern, to_starboard)
- Speed
- Draught (depth of a ship's keel below the water)
- Location coordinates

## Data Processing

The project processes raw AIS data from the Port of Rotterdam (stored in `raw_data_rotterdam/`). The data cleaning process in the `Cleaning/` directory:
1. Identifies ship trips between ports using geofencing
2. Calculates distances between consecutive positions and to destination
3. Processes time data to determine time-to-arrival values
4. Splits data into training and testing sets

## Model Approaches

### Neural Network
Located in the `Neural_net/` directory, this approach uses TensorFlow/Keras to build a deep learning model with fully connected layers. The model is trained to predict time-to-arrival based on scaled input features.

### Regression Models
The `Regression/` directory contains multiple regression approaches:
- Linear Regression with individual features
- Multiple Linear Regression combining several features
- Random Forest Regression for handling non-linear relationships

## Performance

Models are evaluated using metrics such as:
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)

Visualizations in the `Trip_visualisations/` directory include:
- Actual vs. Predicted arrival time plots
- Error distribution plots
- Training performance plots for neural networks
- Interactive HTML visualizations of ship routes and trips

## Usage

To use these models:
1. Clean and prepare your ship data using scripts in `Cleaning/`
2. Train a model using either `Neural_net/Network_training.py` or the regression models
3. Test the model's performance with the corresponding test scripts
4. Visualize trips using the Jupyter notebook in `Trip_visualisations/`

## Requirements

- Python 3.11
- TensorFlow/Keras
- scikit-learn
- pandas
- numpy
- matplotlib
- geopy
- Jupyter (for visualization notebook)