import json
import geopy.distance

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

result = []

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
        }

        for recording in trip['recordings']:
            recording_info = {
                'draught': recording['draught'],
                'time': recording['time'],
                'speed': recording['speed'],
                'heading': recording['heading'],
                'location_lat': recording['location']['lat'],
                'location_long': recording['location']['long'],
                'course': recording['course']
            }

            result.append({
                **boat_info,
                **trip_info,
                **recording_info
            })

#print(json.dumps(result, indent=4))
#Save the data to a JSON file
with open('boats_cleaned.json', 'w') as outfile:
    json.dump(result, outfile, indent=4)