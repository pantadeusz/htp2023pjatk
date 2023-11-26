from django.urls import path
from .views import add_activity#, farm_list, farm_detail


urlpatterns = [
    #path('farms/', farm_list, name='farm_list'),
    #path('farms/<int:farm_id>/', farm_detail, name='farm_detail'),
    path('activities/add/', add_activity, name='add_activity'),
    # Add more URL patterns as needed
]