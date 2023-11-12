#!/usr/bin/env python3

import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import geocoder
from linies import *

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/calc", methods=["POST"])
@cross_origin()
def patata():
    fromText = request.json["from"]
    toText = request.json["to"]

    try:
    ## fotre aqui el geocode
        coo_from = geocoder.osm(fromText).latlng
        coo_to = geocoder.osm(toText).latlng
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

        print(d)
        return jsonify(d), 200
    except:
        return jsonify({}), 400


if __name__ == '__main__':
    app.run(host="localhost", port=3001, debug=True)
