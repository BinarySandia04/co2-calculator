#!/usr/bin/env python3

import json
from flask import Flask, request, jsonify
#import geocoder
from linies import *

app = Flask(__name__)


@app.route("/asdasd", methods=["POST"])
def patata():
    j = request.json["fromto"]
    ## fotre aqui el geocode
    coo_from = 0 ## geocode.osm(j["from"]).latlng
    coo_to = 0 ## geocode.osm(j["from"]).latlng
    km, co2, time = get_path_data(
        # orig: lon, lat
        coo_from[1], coo_from[0],
        # dest: lon, lat
        coo_to[1], coo_to[0],
    )
    d = {
        "dist": km,
        "co2": co2,
        "time": time
    }
    return jsonify(d), 200
