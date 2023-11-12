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

def has_yes(d, n):
    return d[d.columns[n]].value_counts()["Yes"]

df_aux = df.copy()

for ttype in ["private", "public", "active"]:
    df = df_aux[df_aux["transport_types"] == ttype]
    reasons_type = {
        'Fastest'       : has_yes(df, 14),
        'Cheapest'      : has_yes(df, 15),
        'Comfortable'   : has_yes(df, 16),
        'Only_option'   : has_yes(df, 17),
        'Environmental' : has_yes(df, 18),
        'Healthiest'    : has_yes(df, 19),
        'Need_for_other_trips' : has_yes(df, 20),
        'Other' : sum(df[df.columns[21]].value_counts())
    }
    plt.pie(reasons_type.values(), labels = reasons_type.keys())
    plt.savefig(f"{ttype}.svg")
    plt.clf()
