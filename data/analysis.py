#!/usr/bin/env python3

import pandas as pd

with open("Datathon_Results_MOBILITY_2022_original_Students.csv") as f:
    df = pd.read_csv(f)

print(df.head(n=10))
