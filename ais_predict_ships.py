#This python script will try to predict the amount of ships at a specific location
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Set the folder path where your files are stored
folder_path = os.getcwd() + r'\raw_data_rotterdam'

# Get a list of all JSON files in the folder
file_list = glob.glob(os.path.join(folder_path, "raw_ais_data_*.json"))

# Initialize an empty list to store DataFrames
dfs = []

# Loop through each file and read the JSON data
for file in file_list:
    df = pd.read_json(file)  # Read the JSON file into a DataFrame
    dfs.append(df)  # Add it to the list

# Combine all DataFrames into one
full_data = pd.concat(dfs, ignore_index=True)

print(full_data)
'''
Every file contains the ais data of different ships in 1 day!
Dict summary:
- navigation
    - draught
    - time
    - speed
    - heading
    - location
        - long
        - lat
    - course
    - destination
        - name
        - eta
    - status
- device
    - dimensions
        - to_port
        - to_bow
        - to_stern
        - to_starboard
    - mmsi
- vessel
    - callsign
    - subtype
    - type
    - imo
    - name
'''




