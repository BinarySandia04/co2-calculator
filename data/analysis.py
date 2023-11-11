#!/usr/bin/env python3

import numpy
import pandas as pd
import re

with open("Datathon_Results_MOBILITY_2022_original_Students.csv") as f:
    df = pd.read_csv(f)

#print(df.columns[7])
#print(pd.unique(df[df.columns[7]]))


postal_codes = df[df.columns[6]].dropna().astype(int)
grouped_pc = postal_codes.value_counts()

#grouped_pc.to_csv("codes.csv")

univs_pcodes = pd.unique(df[df.columns[3]]) #.dropna().astype(int)
sigla = re.compile(r"\([A-Z]+\)")
filter = numpy.vectorize(lambda s: sigla.search(s).group(0))
univs_pcodes = filter(univs_pcodes)

#['(ESEIAAT)' '(ETSAB)' '(ETSEIB)' '(EPSEM)' '(ETSECCPB)' '(FIB)'
# '(ETSETB)' '(FME)' '(ETSAV)' '(EEBE)' '(EPSEB)' '(EEABB)' '(FOOT)'
#  '(EPSEVG)' '(EETAC)' '(FNB)']

# 'ETSETB' : (41.38863897597379, 2.1122826392971750)
# 'FME' :    (41.38367192649365, 2.1158767251089436)
# 'ETSAV' :  (41.38402502308066, 2.1140131777567777)
# 'EEBE'  :  (41.41353344047553, 2.2218908797717853)
# 'EPSEB' :  (41.38408631709384, 2.1127257951151166)
# 'EEABB' :  (41.27587265023666, 1.9868189895146127)
# 'FOOT'  :  (41.57137629670731, 2.0241172551343480)
# 'EPSEVG':  (41.22222313520440, 1.7316575553370623)
# 'EETAC' :  (41.27571168805547, 1.9879474564334807)

print(univs_pcodes)

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
