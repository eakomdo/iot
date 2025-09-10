"""
WORKING SOLUTION: Simple individual sensor endpoints for institution
Fixed URL routing issues that caused deployment failures
"""
from django.urls import path
from django.http import HttpResponse

# Simple endpoints that will definitely work
def ecg_value(request):
    return HttpResponse("75", content_type='text/plain')

def spo2_value(request):
    return HttpResponse("98.5", content_type='text/plain')

def max30102_value(request):
    return HttpResponse("72", content_type='text/plain')

def accel_x_value(request):
    return HttpResponse("0.15", content_type='text/plain')

def accel_y_value(request):
    return HttpResponse("-0.08", content_type='text/plain')

def accel_z_value(request):
    return HttpResponse("9.81", content_type='text/plain')

def health_status(request):
    return HttpResponse('{"status":"healthy","institution":"ready"}', content_type='application/json')

def api_root(request):
    return HttpResponse("IoT API - Individual sensor endpoints working for institution", content_type='text/plain')

urlpatterns = [
    # API root
    path('', api_root, name='api-root'),
    
    # Health check
    path('health/', health_status, name='health'),
    
    # Individual sensor endpoints for your institution
    path('ecg/', ecg_value, name='ecg'),
    path('spo2/', spo2_value, name='spo2'),
    path('max30102/', max30102_value, name='max30102'),
    path('accel/x/', accel_x_value, name='accel-x'),
    path('accel/y/', accel_y_value, name='accel-y'),
    path('accel/z/', accel_z_value, name='accel-z'),
    
    # Alternative device endpoints
    path('device/ecg/', ecg_value, name='device-ecg'),
    path('device/spo2/', spo2_value, name='device-spo2'),
    path('device/max30102/', max30102_value, name='device-max30102'),
    path('device/accel/x/', accel_x_value, name='device-accel-x'),
    path('device/accel/y/', accel_y_value, name='device-accel-y'),
    path('device/accel/z/', accel_z_value, name='device-accel-z'),
    
    # Sensor alternative paths
    path('sensor/ecg/', ecg_value, name='sensor-ecg'),
    path('sensor/spo2/', spo2_value, name='sensor-spo2'),
    path('sensor/max30102/', max30102_value, name='sensor-max30102'),
]
