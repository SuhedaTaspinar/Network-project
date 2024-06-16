from django.shortcuts import render
from django.conf import settings
from ml_code.network_analysis import create_map, create_network_map, create_top_100_attacks_kepler_map, \
    create_most_attacked_regions_kepler_map, create_related_attacks_kepler_map
from ml_code.data_processing import load_and_process_data, calculate_relationships
import json
from django.http import JsonResponse

def terrorist_attacks_map(request):
    file_path = settings.BASE_DIR / 'data.csv'


    top_100_attacks = load_and_process_data(file_path)[0]
    most_attacked_regions = load_and_process_data(file_path)[1]
    related_attacks = load_and_process_data(file_path)[2]

    top_100_map = create_map(top_100_attacks, 'Top 100 Largest Terrorist Attacks', 'gname', 'nkill',
                             ['country_txt', 'city', 'nkill'])
    most_attacked_map = create_map(most_attacked_regions, 'Top 100 Most Attacked Regions', 'attack_count',
                                   'attack_count', ['country_txt', 'city', 'attack_count'])
    network_map = create_network_map(related_attacks)

    top_100_json = top_100_map.to_json()
    most_attacked_json = most_attacked_map.to_json()
    network_json = network_map.to_json()

    # Kepler.gl haritalarÄ±
    top_100_kepler_map = create_top_100_attacks_kepler_map(file_path)
    most_attacked_kepler_map = create_most_attacked_regions_kepler_map(file_path)
    related_kepler_map = create_related_attacks_kepler_map(file_path)

    return render(request, '../network/templates/analysis/terrorist_attacks_map.html', {
        'top_100_json': top_100_json,
        'most_attacked_json': most_attacked_json,
        'network_json': network_json,
        'top_100_kepler_map': top_100_kepler_map,
        'most_attacked_kepler_map': most_attacked_kepler_map,
        'related_kepler_map': related_kepler_map
    })

def network_graph(request):
    return render(request, '../network/templates/analysis/network_graph.html')

def network_graph_data(request):
    file_path = settings.BASE_DIR / 'data.csv'

    # Load and process data
    top_100_attacks, most_attacked_regions, related_attacks = load_and_process_data(file_path)

    # Calculate relationships
    data = calculate_relationships(top_100_attacks, related_attacks)

    return JsonResponse(data)
