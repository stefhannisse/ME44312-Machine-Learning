import json
import geopy.distance
import os
import random

print('dir', os.getcwd())
path = os.getcwd() + r'/Cleaning/boats_cleaned_training.json'

#Import a json file
with open(path, 'r') as f:
    data = json.load(f)

    # Shuffle the data
    random.shuffle(data)

    # Split the data into 90% training and 10% testing
    split_index = int(len(data) * 0.9)
    training_data = data[:split_index]
    test_data = data[split_index:]

    # Save the training data to a JSON file
    with open('training_data.json', 'w') as train_file:
        json.dump(training_data, train_file, indent=4)

    # Save the test data to a JSON file
    with open('test_data.json', 'w') as test_file:
        json.dump(test_data, test_file, indent=4)