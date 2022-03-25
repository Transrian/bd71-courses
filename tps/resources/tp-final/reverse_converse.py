#!/usr/bin/env python3

# From https://www.kaggle.com/htagholdings/aus-real-estate-sales-march-2019-to-april-2020

import csv
import random
import json
import math
import zipfile

target_dir = "students"

with open("master.json") as fp:
   line = fp.readline()
   cnt = 1
   while line:
       line_content = json.loads(line)

       groupes = line_content["groupes"]
       del line_content["groupes"]
       
       for group in groupes:
           f= open(target_dir + "/" + group + ".json","a+")
           f.write(json.dumps(line_content) + "\n")
           f.close()

       line = fp.readline()
       cnt += 1
