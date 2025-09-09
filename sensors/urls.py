from django.urls import path
from . import views

urlpatterns = [
    # API overview
    path('', views.api_overview, name='api-overview'),
    
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Device endpoints
    path('devices/', views.DeviceListCreateView.as_view(), name='device-list'),
    path('devices/simple/', views.simple_device_list, name='simple-device-list'),
    path('devices/<str:device_id>/', views.DeviceDetailView.as_view(), name='device-detail'),
    path('devices/<str:device_id>/readings/', views.device_readings, name='device-readings'),
    path('devices/<str:device_id>/latest/', views.latest_readings, name='latest-readings'),
    path('devices/<str:device_id>/raw/', views.raw_sensor_values, name='raw-values'),
    
    # Sensor data endpoints - Multiple URL patterns for compatibility
    path('sensors/bulk/', views.bulk_sensor_data, name='bulk-sensor-data'),
    path('sensor-data/bulk/', views.bulk_sensor_data, name='bulk-sensor-data-alt'),  # Alternative URL
    path('sensors/ecg/', views.ECGReadingListCreateView.as_view(), name='ecg-readings'),
    path('sensors/pulse-oximeter/', views.PulseOximeterReadingListCreateView.as_view(), name='pulse-oximeter-readings'),
    path('sensors/max30102/', views.MAX30102ReadingListCreateView.as_view(), name='max30102-readings'),
    path('sensors/accelerometer/', views.AccelerometerReadingListCreateView.as_view(), name='accelerometer-readings'),
    path('sensors/status/', views.DeviceStatusListCreateView.as_view(), name='device-status'),
]
