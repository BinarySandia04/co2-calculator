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

df_aux = df.copy()

for ttype in ["private", "public", "active"]:
    df = df_aux[df_aux["transport_types"] == ttype]
    reasons_type = {
        'Fastest'       : df[df.columns[14]].value_counts()['Yes'],
        'Cheapest'      : df[df.columns[15]].value_counts()['Yes'],
        'Comfortable'   : df[df.columns[16]].value_counts()['Yes'],
        'Only_option'   : df[df.columns[17]].value_counts()['Yes'],
        'Environmental' : df[df.columns[18]].value_counts()['Yes'],
        'Healthiest'    : df[df.columns[19]].value_counts()['Yes'],
        'Need_for_other_trips' : df[df.columns[20]].value_counts()['Yes'],
        'Other' : sum(df[df.columns[21]].value_counts())
    }
    plt.pie(reasons_type.values(), labels = reasons_type.keys())
    plt.savefig(f"{ttype}.svg")
    plt.clf()
