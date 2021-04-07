#!/usr/bin/env python3

# From https://www.kaggle.com/htagholdings/aus-real-estate-sales-march-2019-to-april-2020

import csv
import random
import json
import math
import zipfile

target_dir = "students"

groups = ["prof", "groupe1", "groupe2", "groupe3", "groupe4", "groupe5", "groupe6", "groupe7", "groupe8", "groupe9", "groupe10", "groupe11", "groupe12"]
ratio_data = 0.7
uniqness = math.ceil(len(groups)*ratio_data)

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

            event_groups = random.sample(groups, k=uniqness)
            data["groupes"] = event_groups

            if len(new_header) == 0:
                new_header = list(data.keys())

            rows_values = list(data.values())

            if data["bedrooms"] != "0":
                output.write(json.dumps(data) + "\n")

            data.pop("groupes", None)

            for group in event_groups:
                with open(target_dir + "/" + group + ".json", 'a+') as f:
                    if data["bedrooms"] != "0":
                        f.write(json.dumps(data) + "\n")
