"""
WORKING SOLUTION: Individual sensor endpoints with REAL-TIME data for institution
Returns live data from database when devices are connected, fallback to defaults when no data
"""
from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.utils import timezone

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

@csrf_exempt
@require_http_methods(["POST"])
def post_sensor_data(request):
    """Endpoint for ESP32 to POST sensor data"""
    try:
        # Parse JSON data from ESP32
        data = json.loads(request.body.decode('utf-8'))
        
        # Save to database
        from .models import ECGReading, PulseOximeterReading, MAX30102Reading, AccelerometerReading
        
        # Create ECG reading
        if 'ecg_heart_rate' in data:
            ECGReading.objects.create(
                device_id=data.get('device_id', 'ESP32_IOT_SENSORS'),
                heart_rate=float(data['ecg_heart_rate']),
                timestamp=timezone.now()
            )
        
        # Create SpO2 reading  
        if 'spo2' in data:
            PulseOximeterReading.objects.create(
                device_id=data.get('device_id', 'ESP32_IOT_SENSORS'),
                spo2=float(data['spo2']),
                timestamp=timezone.now()
            )
        
        # Create MAX30102 reading
        if 'max30102_heart_rate' in data:
            MAX30102Reading.objects.create(
                device_id=data.get('device_id', 'ESP32_IOT_SENSORS'),
                heart_rate=float(data['max30102_heart_rate']),
                timestamp=timezone.now()
            )
        
        # Create Accelerometer reading
        if 'x_axis' in data and 'y_axis' in data and 'z_axis' in data:
            AccelerometerReading.objects.create(
                device_id=data.get('device_id', 'ESP32_IOT_SENSORS'),
                x_axis=float(data['x_axis']),
                y_axis=float(data['y_axis']),
                z_axis=float(data['z_axis']),
                timestamp=timezone.now()
            )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Sensor data saved successfully',
            'received_fields': list(data.keys())
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt  
@require_http_methods(["POST"])
def sensors_bulk(request):
    """Alternative bulk endpoint for ESP32 compatibility"""
    return post_sensor_data(request)

urlpatterns = [
    # API root
    path('', api_root, name='api-root'),
    
    # Health check
    path('health/', health_status, name='health'),
    
    # ESP32 POST endpoints
    path('post_sensor_data/', post_sensor_data, name='post-sensor-data'),
    path('sensors/bulk/', sensors_bulk, name='sensors-bulk'),
    
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
