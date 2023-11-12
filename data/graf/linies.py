#!/usr/bin/env python3

import json
import graph
import harversine

result_path = "../../geojson-to-graph/result.json"
with open(result_path, "r") as f:
    j = json.loads(f.read())

g = graph.Co2Graph.from_json(j)

def get_closest(lon, lat):
    min_station = j["nodes"][0]
    min_d = float("inf")
    for station in j["nodes"]:
        coo = station["coords"]
        d = harversine.distance(coo[1], lat, coo[0], lon)
        if min_d < d:
            min_d = d
            min_station = station
    return min_station


path, co2 = g.dijkstra(0, 1000)
print(path)
print(co2)
print(get_closest(2.1, 41.3))
