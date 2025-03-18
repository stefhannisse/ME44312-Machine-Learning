import json
import geopy.distance
import os

print('dir', os.getcwd())

#Import a json file
with open('boats.json', 'r') as f:
    data = json.load(f)

#print(json.dumps(data, indent=4))

#Add the distance for every recording
for boat in data:
    for trip in boat['trips']:
        if(trip['arrival_time'] == None):
            continue

        for i in range(0, len(trip['recordings'])):
            if(i == len(trip['recordings']) - 1):
                distance = geopy.distance.geodesic((trip['recordings'][i]['location']['lat'], trip['recordings'][i]['location']['long']), (trip['arrival']['lat'], trip['arrival']['long']))
                #This is the last recording
                trip['recordings'][i].update({
                    'distance_untill_next': distance.km * 1000
                })
                continue

            #Calculate the distance between this recording and the next one
            distance = geopy.distance.geodesic((trip['recordings'][i]['location']['lat'], trip['recordings'][i]['location']['long']), (trip['recordings'][i + 1]['location']['lat'], trip['recordings'][i + 1]['location']['long']))

            #Add this distance to the recording information
            trip['recordings'][i].update({
                'distance_untill_next': distance.m
            })

        
#Save the data to a JSON file
with open('boats_with_distance.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

#Now add the distance between each recording to get distance to end destination
for boat in data:
    for trip in boat['trips']:
        if(trip['arrival_time'] == None):
            continue
        
        for i in range(len(trip['recordings']) - 1, -1, -1): #Reverse loop to begin with the last recording
            if i == len(trip['recordings']) - 1:
                trip['recordings'][i].update({
                    'distance_to_end': trip['recordings'][i]['distance_untill_next']
                })
            else:
                trip['recordings'][i].update({
                    'distance_to_end': trip['recordings'][i]['distance_untill_next'] + trip['recordings'][i + 1]['distance_to_end']
                })


#Save the data to a JSON file
with open('boats_with_end_distance.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

result = []
index = 0
#For every boat and every trip, check if the arrival information is not null
for boat in data:
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
        if(trip['arrival_time'] == None):
            continue

        trip_info = {
            'arrival_time': trip['arrival_time'],
            'arrival_lat': trip['arrival']['lat'],
            'arrival_long': trip['arrival']['long'],
            'arrival_name': trip['arrival']['name'],
            'eta': trip['arrival']['eta'],
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

            # if(recording['time'] > trip['arrival_time']):
            #     print('Deze time ligt later dan de arrival')
            #     index += 1
            #     continue

            result.append({
                **boat_info,
                **trip_info,
                **recording_info
            })


print('oZoveel punten waren ongeldig: {}'.format(index))
#print(json.dumps(result, indent=4))
#Save the data to a JSON file
with open('boats_cleaned.json', 'w') as outfile:
    json.dump(result, outfile, indent=4)