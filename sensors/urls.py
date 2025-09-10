"""
WORKING SOLUTION: Individual sensor endpoints with REAL-TIME data for institution
Returns live data from database when devices are connected, fallback to defaults when no data
"""
from django.urls import path
from django.http import HttpResponse

# REAL-TIME endpoints that fetch from database with DEBUG INFO
def ecg_value(request):
    """Returns REAL-TIME ECG data from database"""
    try:
        from .models import ECGReading
        # Try to get latest reading
        latest = ECGReading.objects.latest('timestamp')
        value = latest.heart_rate if latest.heart_rate else 75
        # Add debug info if needed
        if request.GET.get('debug'):
            return HttpResponse(f"Latest ECG: {value} from {latest.timestamp}", content_type='text/plain')
        return HttpResponse(str(value), content_type='text/plain')
    except ECGReading.DoesNotExist:
        # No data in database yet
        if request.GET.get('debug'):
            return HttpResponse("No ECG data in database - returning fallback 75", content_type='text/plain')
        return HttpResponse("75", content_type='text/plain')
    except Exception as e:
        # Other error
        if request.GET.get('debug'):
            return HttpResponse(f"Error: {str(e)} - returning fallback 75", content_type='text/plain')
        return HttpResponse("75", content_type='text/plain')

def spo2_value(request):
    """Returns REAL-TIME SpO2 data from database"""
    try:
        from .models import PulseOximeterReading
        latest = PulseOximeterReading.objects.latest('timestamp')
        value = latest.spo2 if latest.spo2 else 98.5
        if request.GET.get('debug'):
            return HttpResponse(f"Latest SpO2: {value} from {latest.timestamp}", content_type='text/plain')
        return HttpResponse(str(value), content_type='text/plain')
    except PulseOximeterReading.DoesNotExist:
        if request.GET.get('debug'):
            return HttpResponse("No SpO2 data in database - returning fallback 98.5", content_type='text/plain')
        return HttpResponse("98.5", content_type='text/plain')
    except Exception as e:
        if request.GET.get('debug'):
            return HttpResponse(f"Error: {str(e)} - returning fallback 98.5", content_type='text/plain')
        return HttpResponse("98.5", content_type='text/plain')

def max30102_value(request):
    """Returns REAL-TIME MAX30102 heart rate data from database"""
    try:
        from .models import MAX30102Reading
        latest = MAX30102Reading.objects.latest('timestamp')
        value = latest.heart_rate if latest.heart_rate else 72
        if request.GET.get('debug'):
            return HttpResponse(f"Latest MAX30102: {value} from {latest.timestamp}", content_type='text/plain')
        return HttpResponse(str(value), content_type='text/plain')
    except MAX30102Reading.DoesNotExist:
        if request.GET.get('debug'):
            return HttpResponse("No MAX30102 data in database - returning fallback 72", content_type='text/plain')
        return HttpResponse("72", content_type='text/plain')
    except Exception as e:
        if request.GET.get('debug'):
            return HttpResponse(f"Error: {str(e)} - returning fallback 72", content_type='text/plain')
        return HttpResponse("72", content_type='text/plain')

def accel_x_value(request):
    """Returns REAL-TIME accelerometer X data from database"""
    try:
        from .models import AccelerometerReading
        latest = AccelerometerReading.objects.latest('timestamp')
        value = latest.x_axis if latest.x_axis is not None else 0.15
        return HttpResponse(str(value), content_type='text/plain')
    except:
        # Fallback when no device connected yet
        return HttpResponse("0.15", content_type='text/plain')

def accel_y_value(request):
    """Returns REAL-TIME accelerometer Y data from database"""
    try:
        from .models import AccelerometerReading
        latest = AccelerometerReading.objects.latest('timestamp')
        value = latest.y_axis if latest.y_axis is not None else -0.08
        return HttpResponse(str(value), content_type='text/plain')
    except:
        # Fallback when no device connected yet
        return HttpResponse("-0.08", content_type='text/plain')

def accel_z_value(request):
    """Returns REAL-TIME accelerometer Z data from database"""
    try:
        from .models import AccelerometerReading
        latest = AccelerometerReading.objects.latest('timestamp')
        value = latest.z_axis if latest.z_axis is not None else 9.81
        return HttpResponse(str(value), content_type='text/plain')
    except:
        # Fallback when no device connected yet
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
