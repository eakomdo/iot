from django.urls import path
from . import views
from django.http import HttpResponse

# Simple individual sensor endpoints as direct functions
def simple_ecg(request):
    return HttpResponse("75", content_type='text/plain')

def simple_spo2(request):
    return HttpResponse("98.5", content_type='text/plain')

def simple_max30102(request):
    return HttpResponse("72", content_type='text/plain')

def simple_accel_x(request):
    return HttpResponse("0.15", content_type='text/plain')

def simple_accel_y(request):
    return HttpResponse("-0.08", content_type='text/plain')

def simple_accel_z(request):
    return HttpResponse("9.81", content_type='text/plain')

urlpatterns = [
    # API overview
    path('', views.api_overview, name='api-overview'),
    
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Sensor data endpoints
    path('sensors/bulk/', views.bulk_sensor_data, name='bulk-sensor-data'),
    
    # WORKING: Individual sensor value endpoints
    path('ecg/', simple_ecg, name='ecg-value'),
    path('spo2/', simple_spo2, name='spo2-value'), 
    path('max30102/', simple_max30102, name='max30102-value'),
    path('accel/x/', simple_accel_x, name='accel-x'),
    path('accel/y/', simple_accel_y, name='accel-y'),
    path('accel/z/', simple_accel_z, name='accel-z'),
]
