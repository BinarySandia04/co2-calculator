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
