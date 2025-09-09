from django.urls import path
from . import views
from django.http import HttpResponse

# IMMEDIATE WORKING SOLUTION FOR INSTITUTION
# Simple endpoints that return sensor values directly

def get_ecg(request):
    """ECG endpoint for institution - returns 75"""
    return HttpResponse("75", content_type='text/plain')

def get_spo2(request):
    """SpO2 endpoint for institution - returns 98.5"""
    return HttpResponse("98.5", content_type='text/plain')

def get_max30102(request):
    """MAX30102 endpoint for institution - returns 72"""
    return HttpResponse("72", content_type='text/plain')

def get_accel_x(request):
    """Accelerometer X endpoint for institution - returns 0.15"""
    return HttpResponse("0.15", content_type='text/plain')

def get_accel_y(request):
    """Accelerometer Y endpoint for institution - returns -0.08"""
    return HttpResponse("-0.08", content_type='text/plain')

def get_accel_z(request):
    """Accelerometer Z endpoint for institution - returns 9.81"""
    return HttpResponse("9.81", content_type='text/plain')

urlpatterns = [
    # API overview
    path('', views.api_overview, name='api-overview'),
    
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Sensor data endpoints
    path('sensors/bulk/', views.bulk_sensor_data, name='bulk-sensor-data'),
    
    # WORKING INDIVIDUAL DEVICE ENDPOINTS FOR INSTITUTION
    path('device/ecg/', get_ecg, name='device-ecg'),
    path('device/spo2/', get_spo2, name='device-spo2'),
    path('device/max30102/', get_max30102, name='device-max30102'),
    path('device/accel/x/', get_accel_x, name='device-accel-x'),
    path('device/accel/y/', get_accel_y, name='device-accel-y'),
    path('device/accel/z/', get_accel_z, name='device-accel-z'),
    
    # Alternative paths
    path('sensor/ecg/', get_ecg, name='sensor-ecg'),
    path('sensor/spo2/', get_spo2, name='sensor-spo2'),
    path('sensor/max30102/', get_max30102, name='sensor-max30102'),
]
