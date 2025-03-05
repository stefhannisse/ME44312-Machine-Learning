#This python script will try to predict the amount of ships at a specific location
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import json

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

# We want this structure:
'''
- boats
    - mmsi(primary key)
    - name
    - to_port
    - to_bow
    - to_stern
    - to_starboard
    - callsign
    - subtype
    - type
    - imo
    - trips
        - eta
        - arrival
            - long
            - lat
        - departure
            - long
            - lat
        - departure_time
        - arrival_time
        - elapsed_time
        - recordings
            - draught
            - time
            - speed
            - heading
            - location
                - long
                - lat
            - course
'''

boats = []
unique_mmsi = []

#First, create a list which contains all the unique boats
for index in range(0, full_data.shape[0]):
    if(full_data.iloc[index][0]['device']['mmsi'] not in unique_mmsi):
        if(full_data.iloc[index][0]['vessel']['name'] == ''):
            continue

        if(full_data.iloc[index][0]['device']['dimensions']['to_port'] == 0):
            continue

        if(full_data.iloc[index][0]['device']['dimensions']['to_bow'] == 0):
            continue

        if(full_data.iloc[index][0]['device']['dimensions']['to_stern'] == 0):
            continue

        if(full_data.iloc[index][0]['vessel']['type'] != 'cargo' and full_data.iloc[index][0]['vessel']['type'] != 'tanker'):
            continue

        unique_mmsi.append(full_data.iloc[index][0]['device']['mmsi'])
        boats.append({
            'mmsi': full_data.iloc[index][0]['device']['mmsi'],
            'name': full_data.iloc[index][0]['vessel']['name'],
            'to_port': full_data.iloc[index][0]['device']['dimensions']['to_port'],
            'to_bow': full_data.iloc[index][0]['device']['dimensions']['to_bow'],
            'to_stern': full_data.iloc[index][0]['device']['dimensions']['to_stern'],
            'to_starboard': full_data.iloc[index][0]['device']['dimensions']['to_starboard'],
            'callsign': full_data.iloc[index][0]['vessel']['callsign'],
            'subtype': full_data.iloc[index][0]['vessel']['subtype'],
            'type': full_data.iloc[index][0]['vessel']['type'],
            'imo': full_data.iloc[index][0]['vessel']['imo'],
            'trips': []
        })

