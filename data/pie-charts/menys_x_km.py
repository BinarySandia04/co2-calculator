#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../Datathon_Results_MOBILITY_2022_original_Students.csv')

transport_types_inverted = {
    'On foot': 'active',
    'Bicycle': 'active',
    'Bus': 'public',
    'Renfe': 'public',
    'Underground': 'public',
    'FGC': 'public',
    'Tram': 'public',
    'Combustion vehicle (non-plug-in hybrid, electric or plug-in hybrid with non-renewable source charging),': 'private',
    'Combustion or electric motorcycle with non-renewable source charging': 'private',
    'Scooter (or other micro-mobility devices) with renewable charging': 'private',
    'Taxi': 'private',
    'Electric vehicle (with Zero label and renewable source charging)': 'private',
    'Scooter (or other micro-mobility devices) with non-renewable charging': 'private',
    'Electric motorcycle': 'private',
}

def get_transport_type(t):
    try:
        return transport_types_inverted[t]
    except:
        return None

df["transport_types"] = df[df.columns[7]].apply(get_transport_type)

cpuni = pd.read_csv("../cp-uni.csv")

dg = pd.merge(
    df["transport_types"],
    cpuni["dist"],
    left_index=True,
    right_index=True
)
dg.head()

cols = []
kms = [2.1, 4.7, 10, 21, 47]
for x in kms:
    dg_x = dg[dg["dist"] <= x]["transport_types"].value_counts()
    aux = 1.0 / sum(dg_x)
    d = {row[0]: row[1] * aux for row in dg_x.iteritems()}
    cols.append([row[1] * aux for row in dg_x.iteritems()])
    #plt.pie(d.values(), labels = d.keys())
    #plt.savefig(f"menys_de_{x}.svg")
    #plt.clf()

print(cols)
x = np.array(cols, dtype=float).transpose()

fig = plt.figure()
ax = fig.add_subplot(111)

ax.stackplot(kms, x)
ax.set_title('Relative usage:\nactive-public-private')
ax.set_ylabel('Percent (%)')
ax.set_xlabel('Less than _ km')
#ax.margins(0, 0) # Set margins to avoid "whitespace"

plt.savefig("menys_de_x.svg")
