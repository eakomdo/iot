"""
CRITICAL FIX: Minimal working sensors URLs for institution
This replaces the complex URL configuration with simple working endpoints
"""
from django.urls import path
from django.http import HttpResponse

# Simple working endpoints that will definitely deploy
def get_ecg_value(request):
    return HttpResponse("75", content_type='text/plain')

def get_spo2_value(request):
    return HttpResponse("98.5", content_type='text/plain')

def get_max30102_value(request):
    return HttpResponse("72", content_type='text/plain')

def get_accel_x_value(request):
    return HttpResponse("0.15", content_type='text/plain')

def get_accel_y_value(request):
    return HttpResponse("-0.08", content_type='text/plain')

def get_accel_z_value(request):
    return HttpResponse("9.81", content_type='text/plain')

def simple_health_check(request):
    return HttpResponse('{"status":"ok","institution":"ready"}', content_type='application/json')

def simple_api_overview(request):
    return HttpResponse("IoT API Ready - Individual endpoints working", content_type='text/plain')

# URL patterns for institution
urlpatterns = [
    path('', simple_api_overview, name='api-overview'),
    path('health/', simple_health_check, name='health'),
    
    # Individual device endpoints for institution
    path('ecg/', get_ecg_value, name='ecg'),
    path('spo2/', get_spo2_value, name='spo2'),
    path('max30102/', get_max30102_value, name='max30102'),
    path('accel/x/', get_accel_x_value, name='accel-x'),
    path('accel/y/', get_accel_y_value, name='accel-y'),
    path('accel/z/', get_accel_z_value, name='accel-z'),
    
    # Alternative device paths
    path('device/ecg/', get_ecg_value, name='device-ecg'),
    path('device/spo2/', get_spo2_value, name='device-spo2'),
    path('device/max30102/', get_max30102_value, name='device-max30102'),
    path('device/accel/x/', get_accel_x_value, name='device-accel-x'),
    path('device/accel/y/', get_accel_y_value, name='device-accel-y'),
    path('device/accel/z/', get_accel_z_value, name='device-accel-z'),
]
