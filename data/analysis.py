#!/usr/bin/env python3

import numpy
import pandas as pd
import re
import harversine

with open("Datathon_Results_MOBILITY_2022_original_Students.csv") as f:
    df = pd.read_csv(f)

#postal_codes = df[df.columns[6]].dropna().astype(int)
#grouped_pc = postal_codes.value_counts()

#grouped_pc.to_csv("codes.csv")

codes = df.columns[6]
univs = df.columns[3]

univs_pcodes = pd.unique(df[codes]) #.dropna().astype(int)
sigla = re.compile(r"\([A-Z]+\)")
filter_sigla = numpy.vectorize(lambda s: sigla.search(str(s)).group(0))
#univs_pcodes = filter_sigla(univs_pcodes)
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

stu = df[[codes, univs]]

# map universities to coords

def univ_coords(u):
    try:
        return uni_coord[sigla.search(u).group(0)[1:-1]]
    except:
        return None

new_uni_coo = stu[univs].apply(univ_coords)

# map postal codes to coords

with open("../cv-to-loc.csv") as f:
    cp_coo = pd.read_csv(f)

cp_to_coo = {}
for (i, row) in cp_coo.iterrows():
    cp_to_coo[int(row[2])] = (row[0], row[1])

def cp_coords(cp):
    try:
        return cp_to_coo[cp]
    except:
        return None

new_cp_coo = stu[codes].apply(cp_coords)

new_df = pd.concat([
    new_cp_coo.to_frame(name="cp"),
    new_uni_coo.to_frame(name="uni"),
    stu[codes].to_frame(name="codi")
], axis=1)

# add a new column to calc þe distance from cp to uni
def get_row_dist(row):
    if row[0] is None or row[1] is None:
        return None
    return harversine.distance(
        row[0][0],
        row[1][0],
        row[0][1],
        row[1][1]
    )

new_df["dist"] = new_df \
    .apply(get_row_dist, axis=1) \
    .dropna()


def maybe_int(f):
    print(f)
    try:
        i = int(f)
        print("ok")
        return i
    except:
        return None

new_df["codi"] = stu[codes].apply(maybe_int)

#new_df[["cp-lat", "cp-lon"]] = pd.DataFrame(
#    new_df["cp"].values.tolist(),
#    columns = ["cp-lat", "cp-lon"]
#)

new_df[["uni-lat", "uni-lon"]] = pd.DataFrame(
    new_df["uni"].values.tolist(),
    columns = ["uni-lat", "uni-lon"]
)

new_df = new_df.drop(columns=["cp", "uni"])

new_df.to_csv("cp-uni.csv")

'''
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
# https://www.cartociudad.es/web/portal/herramientas-calculos/conversor
'''
