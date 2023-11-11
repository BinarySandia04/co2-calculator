import geocoder
import pandas as pd
from pyproj import Proj


def convert_to_utm(lat: float, lng: float):
    utm_proj = Proj(proj='utm', zone=10, ellps='WGS84')

    try:
        easting, northing = utm_proj(lng, lat)
        return [easting, northing]
    except Exception as e:
        raise ValueError("Invalid latitude or longitude values.") from e

with open("data/Datathon_Results_MOBILITY_2022_original_Students.csv") as f:
    df = pd.read_csv(f)


postal_codes = df[df.columns[6]].dropna().astype(int)
grouped_pc = postal_codes.value_counts()

grouped_pc.to_csv("codes.csv")
uni_coord = {
    'ESEIAAT'   : (41.5640438, 2.0227191),
    'ETSAB'     : (41.3839393, 2.1139678),
    'ETSEIB'    : (41.3842777, 2.1152962),
    'EPSEM'     : (41.7371279, 1.829041),
    'ETSECCPB'  : (41.38862665004671, 2.1116058263259307),
    'FIB'       : (41.38960859091039, 2.1134082704685526),
    'ETSETB'    : (41.38863897597379, 2.1122826392971750),
    'FME'       : (41.38367192649365, 2.1158767251089436),
    'ETSAV'     : (41.38402502308066, 2.1140131777567777),
    'EEBE'      : (41.41353344047553, 2.2218908797717853),
    'EPSEB'     : (41.38408631709384, 2.1127257951151166),
    'EEABB'     : (41.27587265023666, 1.9868189895146127),
    'FOOT'      : (41.57137629670731, 2.0241172551343480),
    'EPSEVG'    : (41.22222313520440, 1.7316575553370623),
    'EETAC'     : (41.27571168805547, 1.9879474564334807)
}
transport_types = {
    "active": [
        "On foot",
        "Bicycle"
    ],
    "public": [
        "Bus",
        "Renfe",
        "Underground",
        "FGC",
        "Tram"
    ],
    "private": [
        "Combustion vehicle (non-plug-in hybrid, electric or plug-in hybrid with non-renewable source charging),",
        "Combustion or electric motorcycle with non-renewable source charging",
        "Scooter (or other micro-mobility devices) with renewable charging",
        "Taxi",
        "Electric vehicle (with Zero label and renewable source charging)",
        "Scooter (or other micro-mobility devices) with non-renewable charging",
        "Electric motorcycle"
    ]
}

with open("codes.csv") as f:
    pc = pd.read_csv(f, names=["codi_postal", "n"])
    pc = pc.iloc[1:]

k = 0


with open("cv-to-loc.csv", "w") as f:
    f.write("lon, lat, cp, n\n")
    for i, row in pc.iterrows():

        cp = str(row["codi_postal"])
        n = int(row["n"])
        cp = cp[:-2]
        cp = '0' * (5 - len(cp)) + cp
        
        loc = geocoder.osm(cp + ", Spain")
        if not (loc.latlng is None):
            d = [[loc.latlng[0], loc.latlng[1]], cp, n]
            k = k + 1
            print(d)
            print(str(k) + "/" + str(len(pc)))
            f.write(str(d[0][0]) + "," + str(d[0][1]) + "," + str(d[1]) + "," + str(d[2]) + "\n")
