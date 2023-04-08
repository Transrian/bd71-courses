# Just simplify the ville location csv

import csv
import json

# Open the CSV file for reading
with open('villes_france_shorten.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # Create an empty dictionary to store the output
    output_dict = {}

    # Loop over each row in the CSV file
    for row in reader:
        # Extract the relevant fields from the row
        ville = row['ville']
        longitude = float(row['long'])
        latitude = float(row['lat'])
        altitude_min = int(row['altitude_min']) if row['altitude_min'] != "NULL" else None
        altitude_max = int(row['altitude_max']) if row['altitude_max'] != "NULL" else None

        # Create a dictionary to represent the location and altitude data
        location_dict = {"emplacement": {"lat": latitude, "long": longitude}}
        altitude_dict = {"altitude": {"min": altitude_min, "max": altitude_max}}

        # Combine the location and altitude dictionaries into a single dictionary
        row_dict = {**location_dict, **altitude_dict}

        # Add the row dictionary to the output dictionary using the ville as the key
        output_dict[ville] = row_dict

# Write the output dictionary to a JSON file
with open('output.json', 'w') as jsonfile:
    json.dump(output_dict, jsonfile, indent=4)
