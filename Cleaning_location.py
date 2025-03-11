#This python script will try to predict the amount of ships at a specific location
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import json
import geopy.distance

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
Moerdijke Rotterdam (51.6849479, 4.5775417)
Maasvlakte Moerdijk (51.9524623,4.0190481)
Waalhaven(51.8878903,4.4227321)
FrankFurt Osthaven(50.1086239,8.7033114)
Oosterhout(51.6625902,4.8455511)
Zwartewaal(51.8805442,4.2363681)
'''

# Define the locations
locations = [
    {
        'name': 'Moerdijke Rotterdam',
        'lat': 51.6849479,
        'long': 4.5775417,
        'radius': 4
    },
    {
        'name': 'Maasvlakte Moerdijk',
        'lat': 51.9524623,
        'long': 4.0190481,
        'radius': 10
    },
    {
        'name': 'Waalhaven',
        'lat': 51.8878903,
        'long': 4.4227321,
        'radius': 4
    },
    {
        'name': 'FrankFurt Osthaven',
        'lat': 50.1086239,
        'long': 8.7033114,
        'radius': 1
    },
    {
        'name': 'Oosterhout',
        'lat': 51.6625902,
        'long': 4.8455511,
        'radius': 1
    },
    {
        'name': 'Zwartewaal',
        'lat': 51.8805442,
        'long': 4.2363681,
        'radius': 1
    }
]

boats = [
    {'mmsi': 211560210, 'name': 'AARBURG', 'to_port': 7, 'to_bow': 120, 'to_stern': 15, 'to_starboard': 4, 'callsign': 'DB4165', 'subtype': None, 'type': 'cargo', 'imo': 0, 'trips': []},
    {'mmsi': 246046000, 'name': 'ORION', 'to_port': 9, 'to_bow': 88, 'to_stern': 10, 'to_starboard': 8, 'callsign': 'PHIA', 'subtype': 'hazardous-cat-c', 'type': 'cargo', 'imo': 9143415, 'trips': []},
    {'mmsi': 244010773, 'name': 'LEVANTE', 'to_port': 4, 'to_bow': 74, 'to_stern': 12, 'to_starboard': 7, 'callsign': 'PF3820', 'subtype': None, 'type': 'cargo', 'imo': 0, 'trips': []},
    {'mmsi': 244650759, 'name': 'HELENA', 'to_port': 5, 'to_bow': 120, 'to_stern': 15, 'to_starboard': 6, 'callsign': 'PC5409', 'subtype': None, 'type': 'cargo', 'imo': 0, 'trips': []},
    {'mmsi': 244750043, 'name': 'TRUDIE', 'to_port': 4, 'to_bow': 70, 'to_stern': 5, 'to_starboard': 4, 'callsign': 'PE9379', 'subtype': None, 'type': 'cargo', 'imo': 0, 'trips': []},
    {'mmsi': 309937000, 'name': 'SUNMI', 'to_port': 9, 'to_bow': 76, 'to_stern': 14, 'to_starboard': 4, 'callsign': 'C6WS3', 'subtype': None, 'type': 'cargo', 'imo': 9073581, 'trips': []},
    {'mmsi': 244630718, 'name': 'JORDY CD1', 'to_port': 24, 'to_bow': 27, 'to_stern': 173, 'to_starboard': 13, 'callsign': '', 'subtype': 'all', 'type': 'cargo', 'imo': 0, 'trips': []},
    {'mmsi': 244700820, 'name': 'CHARL', 'to_port': 24, 'to_bow': 254, 'to_stern': 38, 'to_starboard': 21, 'callsign': 'PB8188', 'subtype': 'all', 'type': 'cargo', 'imo': 0, 'trips': []},
    {'mmsi': 219578000, 'name': 'MAYVIEW MAERSK', 'to_port': 30, 'to_bow': 146, 'to_stern': 253, 'to_starboard': 30, 'callsign': 'OWJN2', 'subtype': None, 'type': 'cargo', 'imo': 9619995, 'trips': []},
    {'mmsi': 219019094, 'name': 'MARIBO MAERSK', 'to_port': 30, 'to_bow': 146, 'to_stern': 253, 'to_starboard': 30, 'callsign': 'OWJJ2', 'subtype': 'hazardous-cat-a', 'type': 'cargo', 'imo': 9619969, 'trips': []}
]

def checkLocation(lat, long):
    #Check if this location is within the radius of the defined loctations
    for location in locations:
        if(geopy.distance.geodesic((lat, long), (location['lat'], location['long'])) < location['radius']):
            return {
                'port': True,
                'destination': {
                    'name': location['name'],
                    'lat': location['lat'],
                    'long': location['long']
                }
            }

    return {
        'port': False,
        'destination': None
    }


if __name__ == '__main__':
    #Check for every reading if the ship is at a specific location, if so start the trip
    for index in range(0, full_data.shape[0]):
        print('index: {} of {}'.format(index, full_data.shape[0]))
        for boat in boats:
            if boat['mmsi'] == full_data.iloc[index][0]['device']['mmsi']:
                #Check if the ship is at a specific location
                location = checkLocation(full_data.iloc[index][0]['navigation']['location']['lat'], full_data.iloc[index][0]['navigation']['location']['long'])

                if(location['port'] and (len(boat['trips']) == 0 or boat['trips'][-1]['arrival_time'] != None)):
                    #The ship is at a specific location
                    boat['trips'].append({
                        'departure_time': full_data.iloc[index][0]['navigation']['time'],
                        'departure': { 'lat': location['destination']['lat'], 'long': location['destination']['long'], 'name': location['destination']['name'] },
                        'arrival_time': None,
                        'arrival': None,
                        'elapsed_time': None,
                        'recordings': []
                    })

                if(not location['port'] and len(boat['trips']) > 0):
                    #The ship is not at a port, add it to the recordings
                    boat['trips'][-1]['recordings'].append({
                        'draught': full_data.iloc[index][0]['navigation']['draught'],
                        'time': full_data.iloc[index][0]['navigation']['time'],
                        'speed': full_data.iloc[index][0]['navigation']['speed'],
                        'heading': full_data.iloc[index][0]['navigation']['heading'],
                        'location': { 'lat': full_data.iloc[index][0]['navigation']['location']['lat'], 'long': full_data.iloc[index][0]['navigation']['location']['long'] },
                        'course': full_data.iloc[index][0]['navigation']['course']
                    })

                if(location['port'] and location['destination']['name'] != boat['trips'][-1]['departure']['name']):
                   #The ship is at a port, update the arrival time
                   boat['trips'][-1]['arrival_time'] = full_data.iloc[index][0]['navigation']['time']
                   boat['trips'][-1]['arrival'] = { 'lat': location['destination']['lat'], 'long': location['destination']['long'], 'name': location['destination']['name'] }
                    #boat['trips'][-1]['elapsed_time'] = boat['trips'][-1]['arrival_time'] - boat['trips'][-1]['departure_time']

    totaltrips = 0

    for boat in boats:
        totaltrips += len(boat['trips'])

    print('Total trips: ', totaltrips)
    #Save the data to a JSON file
    with open('boats.json', 'w') as outfile:
        json.dump(boats, outfile, indent=4)
    #