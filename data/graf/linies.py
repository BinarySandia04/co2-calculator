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


path, co2 = g.dijkstra(0, 1000)
print(path)
print(co2)
print(get_closest(2.1, 41.3))
print(g.dijkstra(get_closest(2.168169319461955, 41.423716007440184), get_closest(2.1134082704685526,41.38960859091039)))
