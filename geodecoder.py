import geocoder
import pandas as pd
import re
import numpy
import math

with open("data/Datathon_Results_MOBILITY_2022_original_Students.csv") as f:
    df = pd.read_csv(f)

#postal_codes = df[df.columns[6]].dropna().astype(int)
#grouped_pc = postal_codes.value_counts()

#grouped_pc.to_csv("codes.csv")

codes = df.columns[6]
univs = df.columns[3]

univs_pcodes = pd.unique(df[codes]) #.dropna().astype(int)
sigla = re.compile(r"\([A-Z]+\)")
filter_sigla = numpy.vectorize(lambda s: sigla.search(str(s)).group(0))

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

def sanitize_cp(str):
    if math.isnan(float(str)):
        return 0
    return int(float(str))

k = 0

areas = {}


with open("alumni.csv", 'w') as f:
    f.write("id,lon,lat,genere,codi_postal,uni,any,dies,a_s1,a_s2,a_s3,t_s1,t_s2,t_3\n")
    for i, row in df.iterrows():
        
        lon = 3
        lat = 45

        f.write(str(row["id"]) + ",")
        f.write(str(lon) + ",")
        f.write(str(lat) + ",")
        f.write(str(row["Which of the following options do you identify with most?"]) + ",")
        f.write(str(sanitize_cp(row["Please indicate the postal code from where you usually start your trip to the university:"])) + ",")
        
        f.write("\n")

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
