#!/usr/bin/env python3

import graph

g = graph.Co2Graph.load_json("../../geojson-to-graph/result.json")
path, co2 = g.dijkstra(0, 1000)
print(path)
print(co2)
