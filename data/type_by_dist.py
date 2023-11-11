import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Datathon_Results_MOBILITY_2022_original_Students.csv')

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

cpuni = pd.read_csv("cp-uni.csv")

dg = pd.merge(
    df["transport_types"],
    cpuni["dist"],
    left_index=True,
    right_index=True
)

