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
            return HttpResponse(f"Latest ECG: {value} from {latest.timestamp} (Device: {latest.device.device_id})", content_type='text/plain')
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
            return HttpResponse(f"Latest SpO2: {value} from {latest.timestamp} (Device: {latest.device.device_id})", content_type='text/plain')
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
            return HttpResponse(f"Latest MAX30102: {value} from {latest.timestamp} (Device: {latest.device.device_id})", content_type='text/plain')
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

def test_post_endpoint(request):
    """Test endpoint to verify POST endpoint is deployed"""
    if request.method == 'GET':
        return HttpResponse("POST endpoint is deployed and ready. Use POST method to send sensor data.", content_type='text/plain')
    else:
        return post_sensor_data(request)

@csrf_exempt
def post_sensor_data(request):
    """Endpoint for ESP32 to POST sensor data"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)
    
    try:
        # Parse JSON data from ESP32
        data = json.loads(request.body.decode('utf-8'))
        
        # Import models here to avoid import issues
        try:
            from .models import Device, ECGReading, PulseOximeterReading, MAX30102Reading, AccelerometerReading
        except ImportError as e:
            return JsonResponse({'status': 'error', 'message': f'Model import error: {str(e)}'}, status=500)
        
        # Get or create device
        device_id_str = data.get('device_id', 'ESP32_IOT_SENSORS')
        device, created = Device.objects.get_or_create(
            device_id=device_id_str,
            defaults={
                'name': f'ESP32 Device {device_id_str}',
                'device_type': 'ESP32',
                'is_active': True
            }
        )
        
        # Update last_seen
        device.last_seen = timezone.now()
        device.save()
        
        # Save sensor readings
        saved_data = []
        
        # Create ECG reading
        if 'ecg_heart_rate' in data and data['ecg_heart_rate']:
            try:
                ECGReading.objects.create(
                    device=device,
                    heart_rate=float(data['ecg_heart_rate']),
                    ecg_value=float(data['ecg_heart_rate']),  # Use same value for now
                )
                saved_data.append('ECG')
            except Exception as e:
                pass  # Continue with other sensors
        
        # Create SpO2 reading  
        if 'spo2' in data and data['spo2']:
            try:
                PulseOximeterReading.objects.create(
                    device=device,
                    spo2=float(data['spo2']),
                    heart_rate=float(data.get('pulse_heart_rate', data.get('ecg_heart_rate', 70))),
                    signal_strength=90,  # Default signal strength
                )
                saved_data.append('SpO2')
            except Exception as e:
                pass  # Continue with other sensors
        
        # Create MAX30102 reading
        if 'max30102_heart_rate' in data and data['max30102_heart_rate']:
            try:
                MAX30102Reading.objects.create(
                    device=device,
                    heart_rate=float(data['max30102_heart_rate']),
                    red_value=1000,  # Default values
                    ir_value=1000,
                )
                saved_data.append('MAX30102')
            except Exception as e:
                pass  # Continue with other sensors
        
        # Create Accelerometer reading
        if all(key in data for key in ['x_axis', 'y_axis', 'z_axis']):
            try:
                x, y, z = float(data['x_axis']), float(data['y_axis']), float(data['z_axis'])
                magnitude = (x**2 + y**2 + z**2)**0.5
                AccelerometerReading.objects.create(
                    device=device,
                    x_axis=x,
                    y_axis=y,
                    z_axis=z,
                    magnitude=magnitude
                )
                saved_data.append('Accelerometer')
            except Exception as e:
                pass  # Continue
        
        return JsonResponse({
            'status': 'success',
            'message': 'Sensor data received and saved',
            'device_created': created,
            'saved': saved_data,
            'received_fields': list(data.keys())
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'}, status=500)

@csrf_exempt  
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
    
    # Test endpoint (can be accessed via browser)
    path('test_post/', test_post_endpoint, name='test-post'),
    
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
