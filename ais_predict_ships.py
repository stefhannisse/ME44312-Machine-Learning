#This python script will try to predict the amount of ships at a specific location
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import json

# Set the folder path where your files are stored
folder_path = os.getcwd() + r'/raw_data_rotterdam'

print('path = ',folder_path)

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
#Create a csv file to save all the lat long locations
'''
# Extract the readings where the status is moored or the speed is below 1
stopped_readings = []
for index in range(0, full_data.shape[0]):
    if (full_data.iloc[index][0]['navigation']['speed'] < 0.1):
        stopped_readings.append({ 'lat': full_data.iloc[index][0]['navigation']['location']['lat'], 'long': full_data.iloc[index][0]['navigation']['location']['long'] })

print('stopped readings length ', len(stopped_readings))
#Convert to csv
df = pd.DataFrame(stopped_readings)
df.to_csv('stopped_readings.csv', index=False)

import matplotlib.pyplot as plt
plt.scatter(x=df['long'], y=df['lat'])
plt.show()

exit()
'''

unique_locations = []

for index in range(0, full_data.shape[0]):
    if(full_data.iloc[index][0]['navigation']['destination']['name'] not in unique_locations):
        unique_locations.append(full_data.iloc[index][0]['navigation']['destination']['name'])

print(unique_locations)

exit()

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

#Add all the data in the specific boat in trips
for index in range(0, full_data.shape[0] - 2):
    for boat in boats:
        if boat['mmsi'] == full_data.iloc[index][0]['device']['mmsi']:
            #In the trips list, check in the last list if the last status is moored
            moored = full_data.iloc[index + 1][0]['navigation']['status'] == 'moored'
            previous_moored = full_data.iloc[index][0]['navigation']['status'] == 'moored'
            next_moored = full_data.iloc[index + 2][0]['navigation']['status'] == 'moored'

            if(not moored and previous_moored):
                #The boat just left for a new trip
                boat['trips'].append({
                    'departure_time': full_data.iloc[index + 1][0]['navigation']['time'],
                    'departure': { 'lat': full_data.iloc[index + 1][0]['navigation']['location']['lat'], 'long': full_data.iloc[index + 1][0]['navigation']['location']['long'] },
                    'arrival_time': None,
                    'arrival': None,
                    'elapsed_time': None,
                    'eta': full_data.iloc[index + 1][0]['navigation']['destination']['eta'],
                    'recordings': []
                })

            if(not moored and len(boat['trips']) > 0):
                continue
                # boat['trips'][-1]['recordings'].append({
                #     'draught': full_data.iloc[index + 1][0]['navigation']['draught'],
                #     'time': full_data.iloc[index + 1][0]['navigation']['time'],
                #     'speed': full_data.iloc[index + 1][0]['navigation']['speed'],
                #     'heading': full_data.iloc[index + 1][0]['navigation']['heading'],
                #     'location': {
                #         'lat': full_data.iloc[index + 1][0]['navigation']['location']['lat'],
                #         'long': full_data.iloc[index + 1][0]['navigation']['location']['long']
                #     },
                #     'course': full_data.iloc[index + 1][0]['navigation']['course']
                # })

            if(not moored and next_moored and len(boat['trips']) > 0):
                #The boat just arrived at the destination
                boat['trips'][-1]['arrival_time'] = full_data.iloc[index + 1][0]['navigation']['time']
                boat['trips'][-1]['arrival'] = { 'lat': full_data.iloc[index + 1][0]['navigation']['location']['lat'], 'long': full_data.iloc[index + 1][0]['navigation']['location']['long'] }
                #boat['trips'][-1]['elapsed_time'] = full_data.iloc[index + 1][0]['navigation']['time'] - boat['trips'][-1]['departure_time']

            #Append to this boat
            # boat['trips'].append({
            #     'status': full_data.iloc[index][0]['navigation']['status'],
            #     'eta': full_data.iloc[index][0]['navigation']['destination']['eta'],
            #     'location': {
            #         'lat': full_data.iloc[index][0]['navigation']['location']['lat'],
            #         'long': full_data.iloc[index][0]['navigation']['location']['long']
            #     },
            #     'speed': full_data.iloc[index][0]['navigation']['speed'],
            #     'heading': full_data.iloc[index][0]['navigation']['heading'],
            #     'course': full_data.iloc[index][0]['navigation']['course'],
            #     'time': full_data.iloc[index][0]['navigation']['time'],
            # })


#Convert to csv
df = pd.DataFrame(boats)
print(df.to_html())
#print(df.to_markdown())
#df.to_csv('boats.csv', index=False)

'''
status_list = []
for index in range(0, full_data.shape[0]):
    if full_data.iloc[index, 0]['navigation']['destination']['name'] not in status_list:
        status_list.append(full_data.iloc[index, 0]['navigation']['destination']['name'])

print(status_list)
'''