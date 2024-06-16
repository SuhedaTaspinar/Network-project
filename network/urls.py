from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.terrorist_attacks_map, name='terrorist_attacks_map'),
    path('graph/', views.network_graph, name='network_graph'),
    path('graph/data/', views.network_graph_data, name='network_graph_data'),
]