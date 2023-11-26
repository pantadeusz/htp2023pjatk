from django.urls import path
from .views import add_activity, farm_list, farm_detail, read_sensor, alert_status


urlpatterns = [
    path('read_sensor', read_sensor, name="read_sensor"),
    path('farms/', farm_list, name='farm_list'),
    path('farms/<int:farm_id>/', farm_detail, name='farm_detail'),
    path('activities/add/', add_activity, name='add_activity'),
    path('alert_status/', alert_status, name='alert_status'),
    # Add more URL patterns as needed
]