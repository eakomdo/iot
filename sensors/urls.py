from django.urls import path
from . import views

urlpatterns = [
    # API overview
    path('', views.api_overview, name='api-overview'),
    
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Sensor data endpoints
    path('sensors/bulk/', views.bulk_sensor_data, name='bulk-sensor-data'),
    
    # CRITICAL: Individual sensor value endpoints - return just single values
    path('ecg/', views.ecg_value, name='ecg-value'),
    path('spo2/', views.spo2_value, name='spo2-value'), 
    path('max30102/', views.max30102_value, name='max30102-value'),
    path('accel/x/', views.accel_x_value, name='accel-x'),
    path('accel/y/', views.accel_y_value, name='accel-y'),
    path('accel/z/', views.accel_z_value, name='accel-z'),
]
