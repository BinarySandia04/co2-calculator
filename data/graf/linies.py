#!/usr/bin/env python3

import json
import graph
import harversine

result_path = "../../geojson-to-graph/result.json"
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



path, dist, co2, time = g.dijkstra(get_closest(2.156951683482, 41.437703385), get_closest(1.86273657118123, 41.669071244295))
for p in path:
    print(j["nodes"][p])
print("Dist: " + str(dist))
print("CO2:  " + str(co2))
print("Time: " + str(time))
