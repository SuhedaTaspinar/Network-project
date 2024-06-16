import pandas as pd

def load_and_process_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')

    df = df[['eventid', 'iyear', 'imonth', 'iday', 'country_txt', 'city', 'latitude', 'longitude', 'gname', 'nkill']]
    df = df.dropna(subset=['latitude', 'longitude', 'nkill'])

    grouped_df = df.groupby(['gname', 'country_txt', 'city', 'latitude', 'longitude']).agg({
        'nkill': 'sum',
        'iyear': 'max',
        'imonth': 'max',
        'iday': 'max'
    }).reset_index()

    top_100_attacks = grouped_df.nlargest(100, 'nkill')

    most_attacked_regions = df.groupby(['country_txt', 'city', 'latitude', 'longitude']).size().reset_index(
        name='attack_count')
    most_attacked_regions = most_attacked_regions.nlargest(100, 'attack_count')

    related_attacks = df[df.duplicated(['gname', 'latitude', 'longitude'], keep=False)]
    related_attacks = related_attacks.groupby(['gname', 'country_txt', 'city', 'latitude', 'longitude']).agg({
        'eventid': 'count',
        'nkill': 'sum'
    }).reset_index().nlargest(100, 'eventid')

    return top_100_attacks, most_attacked_regions, related_attacks


def calculate_relationships(top_100_attacks, related_attacks):
    nodes = []
    links = []

    # Add top 100 attacks as nodes
    for index, row in top_100_attacks.iterrows():
        if row['city'] not in nodes:
            nodes.append(row['city'])
        for idx, row2 in related_attacks.iterrows():
            if row['city'] == row2['city']:
                if row2['gname'] not in nodes:
                    nodes.append(row2['gname'])
                links.append({'source': row['city'], 'target': row2['gname'], 'value': row2['eventid']})

    return {'nodes': [{'id': node, 'group': 'top_attacks'} for node in nodes],
            'links': links}