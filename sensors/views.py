from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.http import HttpRequest
import math

from .models import (
    Device, ECGReading, PulseOximeterReading, 
    MAX30102Reading, AccelerometerReading, DeviceStatus
)
from .serializers import (
    DeviceSerializer, ECGReadingSerializer, PulseOximeterReadingSerializer,
    MAX30102ReadingSerializer, AccelerometerReadingSerializer, 
    DeviceStatusSerializer, BulkSensorDataSerializer
)


class DeviceListCreateView(generics.ListCreateAPIView):
    # pylint: disable=no-member
    queryset = Device.objects.all()  # type: ignore
    serializer_class = DeviceSerializer
    
    def list(self, request, *args, **kwargs):
        """Return simple list of device names, not full JSON"""
        # pylint: disable=no-member
        devices = Device.objects.all()  # type: ignore
        device_names = [device.device_id for device in devices]
        
        if device_names:
            # Return device names one per line
            return Response("\n".join(device_names), 
                          content_type='text/plain')
        else:
            return Response("NO_DEVICES_REGISTERED", 
                          content_type='text/plain')


class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    # pylint: disable=no-member
    queryset = Device.objects.all()  # type: ignore
    serializer_class = DeviceSerializer
    lookup_field = 'device_id'


class ECGReadingListCreateView(generics.ListCreateAPIView):
    # pylint: disable=no-member
    queryset = ECGReading.objects.all()  # type: ignore
    serializer_class = ECGReadingSerializer


class PulseOximeterReadingListCreateView(generics.ListCreateAPIView):
    # pylint: disable=no-member
    queryset = PulseOximeterReading.objects.all()  # type: ignore
    serializer_class = PulseOximeterReadingSerializer


class MAX30102ReadingListCreateView(generics.ListCreateAPIView):
    # pylint: disable=no-member
    queryset = MAX30102Reading.objects.all()  # type: ignore
    serializer_class = MAX30102ReadingSerializer


class AccelerometerReadingListCreateView(generics.ListCreateAPIView):
    # pylint: disable=no-member
    queryset = AccelerometerReading.objects.all()  # type: ignore
    serializer_class = AccelerometerReadingSerializer


class DeviceStatusListCreateView(generics.ListCreateAPIView):
    # pylint: disable=no-member
    queryset = DeviceStatus.objects.all()  # type: ignore
    serializer_class = DeviceStatusSerializer


@api_view(['POST'])
def bulk_sensor_data(request: HttpRequest) -> Response:
    """
    Endpoint to receive bulk sensor data from ESP32 devices
    Expected JSON format:
    {
        "device_id": "ESP32_001",
        "ecg_heart_rate": 75.0,
        "ecg_value": 123.45,
        "spo2": 98.5,
        "pulse_heart_rate": 74.0,
        "max30102_heart_rate": 76.0,
        "red_value": 12345,
        "ir_value": 67890,
        "x_axis": 0.1,
        "y_axis": 0.2,
        "z_axis": 9.8,
        "battery_level": 85.0,
        "wifi_signal_strength": -45
    }
    """
    serializer = BulkSensorDataSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        device_id = data['device_id']
        
        try:
            with transaction.atomic():
                # Get or create device
                # pylint: disable=no-member
                device, created = Device.objects.get_or_create(  # type: ignore
                    device_id=device_id,
                    defaults={
                        'name': f'IoT Device {device_id}',
                        'device_type': 'ESP32'
                    }
                )
                device.last_seen = timezone.now()
                device.save()
                
                readings_created = []
                
                # Create ECG reading if data available
                if data.get('ecg_heart_rate') or data.get('ecg_value'):
                    # pylint: disable=no-member
                    ECGReading.objects.create(  # type: ignore
                        device=device,
                        heart_rate=data.get('ecg_heart_rate', 0),
                        ecg_value=data.get('ecg_value', 0),
                        signal_quality=data.get('ecg_signal_quality', 'good')
                    )
                    readings_created.append('ecg')
                
                # Create Pulse Oximeter reading if data available
                if data.get('spo2') or data.get('pulse_heart_rate'):
                    # pylint: disable=no-member
                    PulseOximeterReading.objects.create(  # type: ignore
                        device=device,
                        spo2=data.get('spo2', 0),
                        heart_rate=data.get('pulse_heart_rate', 0),
                        signal_strength=data.get('pulse_signal_strength', 50)
                    )
                    readings_created.append('pulse_oximeter')
                
                # Create MAX30102 reading if data available
                if (data.get('max30102_heart_rate') or data.get('red_value') or 
                    data.get('ir_value')):
                    # pylint: disable=no-member
                    MAX30102Reading.objects.create(  # type: ignore
                        device=device,
                        heart_rate=data.get('max30102_heart_rate', 0),
                        spo2=data.get('max30102_spo2'),
                        red_value=data.get('red_value', 0),
                        ir_value=data.get('ir_value', 0),
                        temperature=data.get('temperature')
                    )
                    readings_created.append('max30102')
                
                # Create Accelerometer reading if data available
                if (data.get('x_axis') is not None or data.get('y_axis') is not None or 
                    data.get('z_axis') is not None):
                    x = data.get('x_axis', 0)
                    y = data.get('y_axis', 0)
                    z = data.get('z_axis', 0)
                    magnitude = data.get('magnitude', math.sqrt(x*x + y*y + z*z))
                    
                    # pylint: disable=no-member
                    AccelerometerReading.objects.create(  # type: ignore
                        device=device,
                        x_axis=x,
                        y_axis=y,
                        z_axis=z,
                        magnitude=magnitude
                    )
                    readings_created.append('accelerometer')
                
                # Create Device Status if data available
                if (data.get('battery_level') is not None or 
                    data.get('wifi_signal_strength') is not None or
                    data.get('memory_usage') is not None):
                    # pylint: disable=no-member
                    DeviceStatus.objects.create(  # type: ignore
                        device=device,
                        battery_level=data.get('battery_level'),
                        wifi_signal_strength=data.get('wifi_signal_strength'),
                        memory_usage=data.get('memory_usage'),
                        cpu_temperature=data.get('cpu_temperature'),
                        uptime_seconds=data.get('uptime_seconds')
                    )
                    readings_created.append('device_status')
                
                # Return only raw sensor values - no device names, one per line
                # Only include non-zero values (actual sensor readings)
                response_values = []
                
                # ECG readings - only if sensor is connected (non-zero)
                if data.get('ecg_heart_rate') and data.get('ecg_heart_rate') > 0:
                    response_values.append(str(data['ecg_heart_rate']))
                
                # Pulse Oximeter readings - only if sensor is connected
                if data.get('spo2') and data.get('spo2') > 0:
                    response_values.append(str(data['spo2']))
                
                if data.get('pulse_heart_rate') and data.get('pulse_heart_rate') > 0:
                    response_values.append(str(data['pulse_heart_rate']))
                
                # MAX30102 Heart Rate - only if sensor is connected
                if data.get('max30102_heart_rate') and data.get('max30102_heart_rate') > 0:
                    response_values.append(str(data['max30102_heart_rate']))
                
                # Accelerometer readings - only if sensor is connected (non-zero)
                if data.get('x_axis') is not None and data.get('x_axis') != 0:
                    response_values.append(str(data['x_axis']))
                
                if data.get('y_axis') is not None and data.get('y_axis') != 0:
                    response_values.append(str(data['y_axis']))
                
                if data.get('z_axis') is not None and data.get('z_axis') != 0:
                    response_values.append(str(data['z_axis']))
                
                # Create plain text response - each value on new line
                if response_values:
                    plain_text_response = "\n".join(response_values)
                    return Response(plain_text_response, 
                                  status=status.HTTP_201_CREATED,
                                  content_type='text/plain')
                else:
                    # No sensors connected - return status message
                    return Response("WAITING_FOR_SENSORS", 
                                  status=status.HTTP_201_CREATED,
                                  content_type='text/plain')
                
        except (ValueError, KeyError, TypeError) as e:
            return Response({
                'status': 'error',
                'code': 500,
                'message': 'Internal Server Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'status': 'error',
        'code': 400,
        'message': 'Bad Request'
    }, status=status.HTTP_400_BAD_REQUEST)


# pylint: disable=unused-argument
@api_view(['GET'])
def device_readings(request: HttpRequest, device_id: str) -> Response:
    """Get all recent readings for a specific device"""
    try:
        # pylint: disable=no-member
        device = Device.objects.get(device_id=device_id)  # type: ignore
    except Device.DoesNotExist:  # type: ignore
        return Response({
            'status': 'error',
            'code': 404,
            'message': 'Not Found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Get recent readings (last 100 for each sensor type)
    # pylint: disable=no-member
    ecg_readings = ECGReading.objects.filter(device=device)[:100]  # type: ignore
    pulse_readings = PulseOximeterReading.objects.filter(device=device)[:100]  # type: ignore
    max30102_readings = MAX30102Reading.objects.filter(device=device)[:100]  # type: ignore
    accel_readings = AccelerometerReading.objects.filter(device=device)[:100]  # type: ignore
    status_readings = DeviceStatus.objects.filter(device=device)[:100]  # type: ignore
    
    return Response({
        'status': 'success',
        'code': 200,
        'message': 'OK'
    })


@api_view(['GET'])
def simple_device_list(request: HttpRequest) -> Response:
    """Get simple device list - just device names, no JSON"""
    # pylint: disable=no-member
    devices = Device.objects.filter(is_active=True)  # type: ignore
    
    if devices.exists():
        device_info = []
        for device in devices:
            # Show device name and status
            device_info.append(device.device_id)
        
        return Response("\n".join(device_info), 
                       content_type='text/plain')
    else:
        return Response("NO_ACTIVE_DEVICES", 
                       content_type='text/plain')


@api_view(['GET'])
def raw_sensor_values(request: HttpRequest, device_id: str) -> Response:
    """Get raw sensor values - just numbers, no JSON"""
    try:
        # pylint: disable=no-member
        device = Device.objects.get(device_id=device_id)  # type: ignore
    except Device.DoesNotExist:  # type: ignore
        return Response("Device not found", 
                       status=status.HTTP_404_NOT_FOUND,
                       content_type='text/plain')
    
    values = []
    
    # Get latest ECG reading - just the number
    try:
        # pylint: disable=no-member
        latest_ecg = ECGReading.objects.filter(device=device).latest('timestamp')  # type: ignore
        if latest_ecg.heart_rate:
            values.append(str(latest_ecg.heart_rate))
    except ECGReading.DoesNotExist:  # type: ignore
        values.append("0")
    
    # Get latest Pulse Oximeter reading - just the number
    try:
        # pylint: disable=no-member
        latest_pulse = PulseOximeterReading.objects.filter(device=device).latest('timestamp')  # type: ignore
        if latest_pulse.spo2:
            values.append(str(latest_pulse.spo2))
        else:
            values.append("0")
    except PulseOximeterReading.DoesNotExist:  # type: ignore
        values.append("0")
    
    # Get latest MAX30102 reading - just the number
    try:
        # pylint: disable=no-member
        latest_max30102 = MAX30102Reading.objects.filter(device=device).latest('timestamp')  # type: ignore
        if latest_max30102.heart_rate:
            values.append(str(latest_max30102.heart_rate))
        else:
            values.append("0")
    except MAX30102Reading.DoesNotExist:  # type: ignore
        values.append("0")
    
    # Get latest Accelerometer reading - just X,Y,Z values
    try:
        # pylint: disable=no-member
        latest_accel = AccelerometerReading.objects.filter(device=device).latest('timestamp')  # type: ignore
        values.append(str(latest_accel.x_axis))
        values.append(str(latest_accel.y_axis)) 
        values.append(str(latest_accel.z_axis))
    except AccelerometerReading.DoesNotExist:  # type: ignore
        values.extend(["0", "0", "0"])
    
    # Return just comma-separated values: ECG,SpO2,MAX30102,X,Y,Z
    return Response(",".join(values), 
                   status=status.HTTP_200_OK,
                   content_type='text/plain')


    """Get the latest sensor readings in simple value format"""
    try:
        # pylint: disable=no-member
        device = Device.objects.get(device_id=device_id)  # type: ignore
    except Device.DoesNotExist:  # type: ignore
        return Response({
            'error': f'Device {device_id} not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    readings = []
    
    # Get latest readings for each sensor type
    try:
        # pylint: disable=no-member
        latest_ecg = ECGReading.objects.filter(device=device).latest('timestamp')  # type: ignore
        if latest_ecg.heart_rate:
            readings.append(f"ECG Heart Rate: {latest_ecg.heart_rate} BPM")
        if latest_ecg.ecg_value:
            readings.append(f"ECG Value: {latest_ecg.ecg_value}")
    except ECGReading.DoesNotExist:  # type: ignore
        pass
    
    try:
        # pylint: disable=no-member
        latest_pulse = PulseOximeterReading.objects.filter(device=device).latest('timestamp')  # type: ignore
        if latest_pulse.spo2:
            readings.append(f"SpO2: {latest_pulse.spo2}%")
        if latest_pulse.heart_rate:
            readings.append(f"Pulse Rate: {latest_pulse.heart_rate} BPM")
    except PulseOximeterReading.DoesNotExist:  # type: ignore
        pass
    
    try:
        # pylint: disable=no-member
        latest_max30102 = MAX30102Reading.objects.filter(device=device).latest('timestamp')  # type: ignore
        if latest_max30102.heart_rate:
            readings.append(f"MAX30102 Heart Rate: {latest_max30102.heart_rate} BPM")
        if latest_max30102.red_value:
            readings.append(f"Red Value: {latest_max30102.red_value}")
        if latest_max30102.ir_value:
            readings.append(f"IR Value: {latest_max30102.ir_value}")
    except MAX30102Reading.DoesNotExist:  # type: ignore
        pass
    
    try:
        # pylint: disable=no-member
        latest_accel = AccelerometerReading.objects.filter(device=device).latest('timestamp')  # type: ignore
        readings.append(f"X-Axis: {latest_accel.x_axis} g")
        readings.append(f"Y-Axis: {latest_accel.y_axis} g") 
        readings.append(f"Z-Axis: {latest_accel.z_axis} g")
        readings.append(f"Magnitude: {latest_accel.magnitude:.2f} g")
    except AccelerometerReading.DoesNotExist:  # type: ignore
        pass
    
    try:
        # pylint: disable=no-member
        latest_status = DeviceStatus.objects.filter(device=device).latest('timestamp')  # type: ignore
        if latest_status.battery_level:
            readings.append(f"Battery: {latest_status.battery_level}%")
        if latest_status.wifi_signal_strength:
            readings.append(f"WiFi Signal: {latest_status.wifi_signal_strength} dBm")
    except DeviceStatus.DoesNotExist:  # type: ignore
        pass
    
    if readings:
        return Response({
            'device': device_id,
            'latest_readings': readings,
            'last_seen': device.last_seen.isoformat(),
            'status': 'active' if device.is_active else 'inactive'
        })
    else:
        return Response({
            'device': device_id,
            'message': 'No sensor readings available yet',
            'last_seen': device.last_seen.isoformat() if device.last_seen else None
        })


# pylint: disable=unused-argument
@api_view(['GET'])
def api_overview(request: HttpRequest) -> Response:
    """Live IoT system status - no JSON, no dummy data"""
    try:
        # Get live device count
        # pylint: disable=no-member
        device_count = Device.objects.count()  # type: ignore
        active_devices = Device.objects.filter(is_active=True).count()  # type: ignore
        
        # Get latest sensor reading counts
        ecg_count = ECGReading.objects.count()  # type: ignore
        pulse_count = PulseOximeterReading.objects.count()  # type: ignore
        max30102_count = MAX30102Reading.objects.count()  # type: ignore
        accel_count = AccelerometerReading.objects.count()  # type: ignore
        
        # Get latest actual sensor values (not dummy data)
        latest_ecg = "NO_DATA"
        latest_spo2 = "NO_DATA"
        latest_max30102 = "NO_DATA"
        
        try:
            latest_ecg_reading = ECGReading.objects.latest('timestamp')  # type: ignore
            if latest_ecg_reading.heart_rate > 0:
                latest_ecg = str(latest_ecg_reading.heart_rate)
        except ECGReading.DoesNotExist:  # type: ignore
            pass
            
        try:
            latest_pulse_reading = PulseOximeterReading.objects.latest('timestamp')  # type: ignore
            if latest_pulse_reading.spo2 > 0:
                latest_spo2 = str(latest_pulse_reading.spo2)
        except PulseOximeterReading.DoesNotExist:  # type: ignore
            pass
            
        try:
            latest_max_reading = MAX30102Reading.objects.latest('timestamp')  # type: ignore
            if latest_max_reading.heart_rate > 0:
                latest_max30102 = str(latest_max_reading.heart_rate)
        except MAX30102Reading.DoesNotExist:  # type: ignore
            pass
        
        # Return live status as plain text
        status_text = f"""LIVE IoT SYSTEM STATUS
Devices: {device_count} total, {active_devices} active
Readings: {ecg_count} ECG, {pulse_count} pulse, {max30102_count} MAX30102, {accel_count} accel
Live Values: ECG={latest_ecg} SpO2={latest_spo2} MAX30102={latest_max30102}
Endpoints: /api/ecg/ /api/spo2/ /api/max30102/ /api/accel/x/ /api/accel/y/ /api/accel/z/
Upload: POST /api/sensors/bulk/"""
        
        return Response(status_text, content_type='text/plain', status=200)
        
    except Exception as e:
        return Response(f"SYSTEM ERROR: {str(e)}", content_type='text/plain', status=500)


@api_view(['GET'])
def health_check(request: HttpRequest) -> Response:
    """Health check endpoint for monitoring deployment status"""
    from django.db import connection
    from django.utils import timezone
    
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "healthy"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Count total records
    try:
        device_count = Device.objects.count()  # type: ignore
        ecg_count = ECGReading.objects.count()  # type: ignore
        total_readings = (
            ECGReading.objects.count() +  # type: ignore
            PulseOximeterReading.objects.count() +  # type: ignore
            MAX30102Reading.objects.count() +  # type: ignore
            AccelerometerReading.objects.count() +  # type: ignore
            DeviceStatus.objects.count()  # type: ignore
        )
    except Exception:
        device_count = 0
        ecg_count = 0
        total_readings = 0
    
    is_healthy = db_status == "healthy"
    http_status = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response({
        'status': 'success' if is_healthy else 'error',
        'code': 200 if is_healthy else 503,
        'message': 'OK' if is_healthy else 'Service Unavailable'
    }, status=http_status)


# SIMPLE ENDPOINTS - JUST RETURN THE SINGLE VALUE
@api_view(['GET'])
def ecg_value(request: HttpRequest) -> Response:
    """Returns: 75"""
    try:
        # pylint: disable=no-member
        latest = ECGReading.objects.latest('timestamp')  # type: ignore
        return Response(str(latest.heart_rate or 0), content_type='text/plain', status=200)
    except ECGReading.DoesNotExist:  # type: ignore
        return Response("0", content_type='text/plain', status=200)


@api_view(['GET'])  
def spo2_value(request: HttpRequest) -> Response:
    """Returns: 98.5"""
    try:
        # pylint: disable=no-member
        latest = PulseOximeterReading.objects.latest('timestamp')  # type: ignore
        return Response(str(latest.spo2 or 0), content_type='text/plain', status=200)
    except PulseOximeterReading.DoesNotExist:  # type: ignore
        return Response("0", content_type='text/plain', status=200)


@api_view(['GET'])
def max30102_value(request: HttpRequest) -> Response:
    """Returns: 74"""
    try:
        # pylint: disable=no-member
        latest = MAX30102Reading.objects.latest('timestamp')  # type: ignore
        return Response(str(latest.heart_rate or 0), content_type='text/plain', status=200)
    except MAX30102Reading.DoesNotExist:  # type: ignore
        return Response("0", content_type='text/plain', status=200)


@api_view(['GET'])
def accel_x_value(request: HttpRequest) -> Response:
    """Returns: 0.12"""
    try:
        # pylint: disable=no-member  
        latest = AccelerometerReading.objects.latest('timestamp')  # type: ignore
        return Response(str(latest.x_axis or 0), content_type='text/plain', status=200)
    except AccelerometerReading.DoesNotExist:  # type: ignore
        return Response("0", content_type='text/plain', status=200)


@api_view(['GET'])
def accel_y_value(request: HttpRequest) -> Response:
    """Returns: -0.05"""
    try:
        # pylint: disable=no-member
        latest = AccelerometerReading.objects.latest('timestamp')  # type: ignore
        return Response(str(latest.y_axis or 0), content_type='text/plain', status=200)
    except AccelerometerReading.DoesNotExist:  # type: ignore
        return Response("0", content_type='text/plain', status=200)


@api_view(['GET'])
def accel_z_value(request: HttpRequest) -> Response:
    """Returns: 9.81"""
    try:
        # pylint: disable=no-member
        latest = AccelerometerReading.objects.latest('timestamp')  # type: ignore
        return Response(str(latest.z_axis or 0), content_type='text/plain', status=200)
    except AccelerometerReading.DoesNotExist:  # type: ignore
        return Response("0", content_type='text/plain', status=200)
