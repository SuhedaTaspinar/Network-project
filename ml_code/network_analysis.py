import plotly.express as px
import plotly.graph_objects as go
from keplergl import KeplerGl
from .data_processing import load_and_process_data

def create_map(df, title, color_column, size_column, hover_data):
    fig = px.scatter_geo(df,
                         lat='latitude',
                         lon='longitude',
                         hover_name='city',
                         hover_data=hover_data,
                         size=size_column,
                         color=color_column,
                         title=title)

    fig.update_layout(geo=dict(
        showland=True,
        landcolor='white',
        showcountries=True,
        countrycolor='lightgrey'
    ))

    return fig

def create_network_map(related_attacks):
    fig = create_map(related_attacks,
                     title='Network of Related Attacks',
                     color_column='gname',
                     size_column='eventid',
                     hover_data=['country_txt', 'city', 'nkill'])

    edges = []
    for idx, row in related_attacks.iterrows():
        related_events = related_attacks[related_attacks['gname'] == row['gname']]
        for idx2, row2 in related_events.iterrows():
            if row['eventid'] != row2['eventid']:
                edges.append(
                    go.Scattergeo(
                        lon=[row['longitude'], row2['longitude']],
                        lat=[row['latitude'], row2['latitude']],
                        mode='lines',
                        line=dict(width=0.5, color='grey'),
                        opacity=0.5
                    )
                )

    for edge in edges:
        fig.add_trace(edge)

    return fig

def create_kepler_map(df, title):
    map_1 = KeplerGl()
    map_1.add_data(data=df, name=title)
    return map_1

def create_top_100_attacks_kepler_map(file_path):
    df = load_and_process_data(file_path)[0]
    return create_kepler_map(df, 'Top 100 Largest Terrorist Attacks')

def create_most_attacked_regions_kepler_map(file_path):
    df = load_and_process_data(file_path)[1]
    return create_kepler_map(df, 'Top 100 Most Attacked Regions')

def create_related_attacks_kepler_map(file_path):
    df = load_and_process_data(file_path)[2]
    return create_kepler_map(df, 'Network of Related Attacks')
