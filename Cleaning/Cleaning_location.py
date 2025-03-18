#This python script will try to predict the amount of ships at a specific location
import pandas as pd
import glob
import os
import json
import geopy.distance
from datetime import datetime
import sys
import warnings

# Set the folder path where your files are stored
folder_path = os.getcwd() + r'\..\raw_data_rotterdam'

print('path = ',folder_path)

# Get a list of all JSON files in the folder
file_list = glob.glob(os.path.join(folder_path, "raw_ais_data_*.json"))

# Initialize an empty list to store DataFrames
dfs = []

#Suppress FutureWarnings to avoid cluttering the output
warnings.simplefilter(action='ignore', category=FutureWarning)

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
        'lat': 51.8805442,
        'long': 4.2363681,
        'radius': 2
    },
    {
        'name': 'Maasvlakte Moerdijk',
        'lat': 51.9524623,
        'long': 4.0190481,
        'radius': 4
    },
    {
        'name': 'Waalhaven',
        'lat': 51.8878903,
        'long': 4.4227321,
        'radius': 4
    },
    {
        'name': 'FrankFurt Osthaven',
        'lat': 51.8805442,
        'long': 4.2363681,
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

def print_progress_bar(iteration, total, length=50):
    percent = (iteration + 1) / total
    filled_length = int(length * percent)
    bar = "█" * filled_length + "-" * (length - filled_length)
    sys.stdout.write(f"\r[{bar}] {percent * 100:.2f}% ({iteration + 1}/{total})")
    sys.stdout.flush()


if __name__ == '__main__':
    #Check for every reading if the ship is at a specific location, if so start the trip
    start = datetime.now()

    total = full_data.shape[0]
    for index in range(total):
        if index % 100 == 0 or index == total - 1:  # Update every 100 iterations
            print_progress_bar(index, total)

        for boat in boats:
            if boat['mmsi'] == full_data.iloc[index][0]['device']['mmsi']:
                location = checkLocation(full_data.iloc[index][0]['navigation']['location']['lat'],
                                         full_data.iloc[index][0]['navigation']['location']['long'])

                if location['port'] and (len(boat['trips']) == 0 or boat['trips'][-1]['arrival_time'] is not None):
                    boat['trips'].append({
                        'departure_time': datetime.fromisoformat(
                            full_data.iloc[index][0]['navigation']['time']).timestamp(),
                        'departure': {
                            'lat': location['destination']['lat'],
                            'long': location['destination']['long'],
                            'name': location['destination']['name']
                        },
                        'arrival_time': None,
                        'arrival': None,
                        'eta': full_data.iloc[index][0]['navigation']['destination']['eta'],
                        'recordings': []
                    })

                if not location['port'] and len(boat['trips']) > 0:
                    boat['trips'][-1]['recordings'].append({
                        'draught': full_data.iloc[index][0]['navigation']['draught'],
                        'time': datetime.fromisoformat(full_data.iloc[index][0]['navigation']['time']).timestamp(),
                        'speed': full_data.iloc[index][0]['navigation']['speed'],
                        'heading': full_data.iloc[index][0]['navigation']['heading'],
                        'location': {
                            'lat': full_data.iloc[index][0]['navigation']['location']['lat'],
                            'long': full_data.iloc[index][0]['navigation']['location']['long']
                        },
                        'course': full_data.iloc[index][0]['navigation']['course']
                    })

                if location['port'] and location['destination']['name'] != boat['trips'][-1]['departure']['name']:
                    boat['trips'][-1]['arrival_time'] = datetime.fromisoformat(
                        full_data.iloc[index][0]['navigation']['time']).timestamp()
                    boat['trips'][-1]['arrival'] = {
                        'lat': location['destination']['lat'],
                        'long': location['destination']['long'],
                        'name': location['destination']['name']
                    }

    sys.stdout.write("\nDone!\n")

    #Save the data to a JSON file
    #with open('boats.json', 'w') as outfile:
    #    json.dump(boats, outfile, indent=4)
    #

    print('Calculating distances...')
    #Toegevoegd
    for boat in boats:
        for trip in boat['trips']:
            if (trip['arrival_time'] == None):
                continue

            for i in range(0, len(trip['recordings'])):
                if (i == len(trip['recordings']) - 1):
                    distance = geopy.distance.geodesic(
                        (trip['recordings'][i]['location']['lat'], trip['recordings'][i]['location']['long']),
                        (trip['arrival']['lat'], trip['arrival']['long']))
                    # This is the last recording
                    trip['recordings'][i].update({
                        'distance_untill_next': distance.km * 1000
                    })
                    continue

                # Calculate the distance between this recording and the next one
                distance = geopy.distance.geodesic(
                    (trip['recordings'][i]['location']['lat'], trip['recordings'][i]['location']['long']),
                    (trip['recordings'][i + 1]['location']['lat'], trip['recordings'][i + 1]['location']['long']))

                # Add this distance to the recording information
                trip['recordings'][i].update({
                    'distance_untill_next': distance.m
                })

    print('Getting the location between each recording...')

    # Now add the distance between each recording to get distance to end destination
    for boat in boats:
        for trip in boat['trips']:
            if (trip['arrival_time'] == None):
                continue

            for i in range(len(trip['recordings']) - 1, -1, -1):  # Reverse loop to begin with the last recording
                if i == len(trip['recordings']) - 1:
                    trip['recordings'][i].update({
                        'distance_to_end': trip['recordings'][i]['distance_untill_next']
                    })
                else:
                    trip['recordings'][i].update({
                        'distance_to_end': trip['recordings'][i]['distance_untill_next'] + trip['recordings'][i + 1][
                            'distance_to_end']
                    })

    print('Saving it all in one big json file...')

    result = []
    indexFault = 0
    # For every boat and every trip, check if the arrival information is not null
    for boat in boats:
        boat_info = {
            'mmsi': boat['mmsi'],
            'name': boat['name'],
            'to_port': boat['to_port'],
            'to_bow': boat['to_bow'],
            'to_stern': boat['to_stern'],
            'to_starboard': boat['to_starboard'],
            'callsign': boat['callsign'],
            'subtype': boat['subtype'],
            'type': boat['type'],
            'imo': boat['imo'],
        }

        for trip in boat['trips']:
            if (trip['arrival_time'] == None):
                continue

            trip_info = {
                'arrival_time': trip['arrival_time'],
                'arrival_lat': trip['arrival']['lat'],
                'arrival_long': trip['arrival']['long'],
                'arrival_name': trip['arrival']['name'],
                #'eta': trip['arrival']['eta'],
            }

            for recording in trip['recordings']:
                recording_info = {
                    'draught': recording['draught'],
                    'time': recording['time'],
                    'speed': recording['speed'],
                    'heading': recording['heading'],
                    'location_lat': recording['location']['lat'],
                    'location_long': recording['location']['long'],
                    'course': recording['course'],
                    'distance_to_end': recording['distance_to_end']
                }

                if(recording['time'] > trip['arrival_time']):
                    indexFault += 1
                    continue

                #Check if the boat needs an impossible speed to reach the destination
                timetillend = trip['arrival_time'] - recording['time'] # Time till end in seconds

                if(recording['distance_to_end'] / timetillend > 10):
                    indexFault += 1
                    continue

                result.append({
                    **boat_info,
                    **trip_info,
                    **recording_info
                })

    print('Done with that, saving...')
    print('Entire process took: {}'.format(datetime.now() - start))
    print('Amount of records: {}'.format(len(result)))
    print('Found {} faults based on the speed or arrival time which were skipped'.format(indexFault))

    # print(json.dumps(result, indent=4))
    # Save the data to a JSON file
    with open('boats_cleaned.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)