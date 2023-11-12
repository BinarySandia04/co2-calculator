import geocoder
import pandas as pd
import re
import numpy
import math

with open("../data/input/Datathon_Results_MOBILITY_2022_original_Students.csv") as f:
    df = pd.read_csv(f)

#postal_codes = df[df.columns[6]].dropna().astype(int)
#grouped_pc = postal_codes.value_counts()

#grouped_pc.to_csv("codes.csv")

postal_codes = df[df.columns[6]].dropna().astype(int)
grouped_pc = postal_codes.value_counts()

grouped_pc.to_csv("../data/output/codes.csv")

with open("../data/output/codes.csv") as f:
    pc = pd.read_csv(f, names=["codi_postal", "n"])
    pc = pc.iloc[1:]

k = 0

areas = {}

for i, row in pc.iterrows():

    cp = str(row["codi_postal"])
    cp = cp[:-2]
    cp = '0' * (5 - len(cp)) + cp
    
    loc = geocoder.osm(cp + ", Spain")
    if not (loc.latlng is None):
        areas[cp] = [loc.json["bbox"]["northeast"], loc.json["bbox"]["southwest"]]
        k = k + 1
        print(areas[cp])
        print(str(k) + "/" + str(len(pc)))

with open("../data/output/boxes.csv", 'w') as f:
    f.write("cp,ne_lon,ne_lat,sw_lon,sw_lat\n")
    for k in areas.keys():
       f.write(str(k) + ",")
       f.write(str(areas[k][0][0]) + "," + str(areas[k][0][1]) + "," + str(areas[k][1][0]) + "," + str(areas[k][1][1]) + "\n")
