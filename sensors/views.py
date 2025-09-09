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
                
                return Response({
                    'message': 'Sensor data received successfully',
                    'device_id': device_id,
                    'device_created': created,
                    'readings_created': readings_created,
                    'timestamp': timezone.now()
                }, status=status.HTTP_201_CREATED)
                
        except (ValueError, KeyError, TypeError) as e:
            return Response({
                'error': f'Error processing sensor data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# pylint: disable=unused-argument
@api_view(['GET'])
def device_readings(request: HttpRequest, device_id: str) -> Response:
    """Get all recent readings for a specific device"""
    try:
        # pylint: disable=no-member
        device = Device.objects.get(device_id=device_id)  # type: ignore
    except Device.DoesNotExist:  # type: ignore
        return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get recent readings (last 100 for each sensor type)
    # pylint: disable=no-member
    ecg_readings = ECGReading.objects.filter(device=device)[:100]  # type: ignore
    pulse_readings = PulseOximeterReading.objects.filter(device=device)[:100]  # type: ignore
    max30102_readings = MAX30102Reading.objects.filter(device=device)[:100]  # type: ignore
    accel_readings = AccelerometerReading.objects.filter(device=device)[:100]  # type: ignore
    status_readings = DeviceStatus.objects.filter(device=device)[:100]  # type: ignore
    
    return Response({
        'device': DeviceSerializer(device).data,
        'ecg_readings': ECGReadingSerializer(ecg_readings, many=True).data,
        'pulse_oximeter_readings': PulseOximeterReadingSerializer(pulse_readings, many=True).data,
        'max30102_readings': MAX30102ReadingSerializer(max30102_readings, many=True).data,
        'accelerometer_readings': AccelerometerReadingSerializer(accel_readings, many=True).data,
        'device_status': DeviceStatusSerializer(status_readings, many=True).data,
    })


# pylint: disable=unused-argument
@api_view(['GET'])
def api_overview(request: HttpRequest) -> Response:
    """API endpoint overview"""
    return Response({
        'message': 'IoT Sensor Data API',
        'version': '1.0',
        'endpoints': {
            'devices': '/api/devices/',
            'bulk_sensor_data': '/api/sensors/bulk/',
            'device_readings': '/api/devices/{device_id}/readings/',
            'ecg_readings': '/api/sensors/ecg/',
            'pulse_oximeter_readings': '/api/sensors/pulse-oximeter/',
            'max30102_readings': '/api/sensors/max30102/',
            'accelerometer_readings': '/api/sensors/accelerometer/',
            'device_status': '/api/sensors/status/',
        },
        'documentation': {
            'bulk_data_format': {
                'device_id': 'string (required)',
                'ecg_heart_rate': 'float (optional)',
                'ecg_value': 'float (optional)',
                'spo2': 'float (optional)',
                'pulse_heart_rate': 'float (optional)',
                'max30102_heart_rate': 'float (optional)',
                'red_value': 'int (optional)',
                'ir_value': 'int (optional)',
                'x_axis': 'float (optional)',
                'y_axis': 'float (optional)',
                'z_axis': 'float (optional)',
                'battery_level': 'float (optional)',
                'wifi_signal_strength': 'int (optional)',
            }
        }
    })


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
    
    return Response({
        'status': 'healthy' if db_status == "healthy" else 'degraded',
        'timestamp': timezone.now().isoformat(),
        'database': db_status,
        'statistics': {
            'total_devices': device_count,
            'total_readings': total_readings,
            'ecg_readings': ecg_count,
        },
        'version': '1.0',
        'deployment': 'render'
    })
