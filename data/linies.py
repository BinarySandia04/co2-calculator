#!/usr/bin/env python3

import json
import graph
import harversine

result_path = "../geojson-to-graph/result.json"
with open(result_path, "r") as f:
    j = json.loads(f.read())

g = graph.Co2Graph.from_json(j)

def get_closest(lon, lat):
    min_d = float("inf")
    min_i = -1
    i = 0
    for station in j["nodes"]:
        coo = station["coords"]
        d = harversine.distance(coo[1], lat, coo[0], lon)
        if min_d > d:
            min_d = d
            min_i = i
        i += 1
    return min_i

def hours_to_string(hf):
    hrs = int(hf)
    min = int(hf*60) - hrs*60
    sec = int(hf*3600) - (hrs*60 + min)*60
    return str(hrs) + "h " + \
           str(min) + "m " + \
           str(sec) + "s"


def get_path_data(lon1, lat1, lon2, lat2):
    try:
        res = g.dijkstra(
            get_closest(lon1, lat1),
            get_closest(lon2, lat2)
        )
        if len(res) != 3:
            return (0,0,0)
        return res
    except:
        return None, None, None
    
'''
print("Followed path:\n")
for p in path:
    print(j["nodes"][p]["name"])
print()
print("Dist: " + str(round(dist, 2)) + "km")
print("CO2:  " + str(round(co2, 3)) + "kg")
print("Time: " + hours_to_string(time))
'''
