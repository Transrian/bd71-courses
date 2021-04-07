#!/usr/bin/env python3

# From https://www.kaggle.com/htagholdings/aus-real-estate-sales-march-2019-to-april-2020

import csv
import random
import json

groups = ["groupe1", "groupe2", "groupe3", "groupe4"]
uniqness = 2

with open('master.json', 'w', newline='') as output:
    with open("raw.csv", newline='') as inputcsv:
        reader = csv.reader(inputcsv, delimiter=',', quotechar='"')
        headers = next(reader, None)
        new_header = []
        for row in reader:
            data = {}
            for i, v in enumerate(row):
                data[headers[i]] = v

            if data["price"] == "NULL":
                data["price"] = None
            
            if not data["lat"] in [None, "NULL"] and not data["lon"] in [None, "NULL"]:
                data["location"] = data["lat"] + "," + data["lon"]

            data.pop("lat", None)
            data.pop("lon", None)
            data.pop("loc_pid", None)
            data.pop("lga_pid", None)
            data.pop("state", None)

            data["groupes"] = random.sample(groups, k=uniqness)

            if len(new_header) == 0:
                new_header = list(data.keys())

            rows_values = list(data.values())

            if data["bedrooms"] != "0":
                output.write(json.dumps(data) + "\n")
