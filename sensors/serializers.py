from rest_framework import serializers
from typing import Optional, Any
from .models import (
    Device, ECGReading, PulseOximeterReading, 
    MAX30102Reading, AccelerometerReading, DeviceStatus
)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_id', 'name', 'device_type', 'created_at', 'last_seen', 'is_active']
        read_only_fields = ['id', 'created_at']


class ECGReadingSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(write_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = ECGReading
        fields = ['id', 'device_id', 'device_name', 'timestamp', 'heart_rate', 'ecg_value', 'signal_quality']
        read_only_fields = ['id', 'timestamp', 'device_name']
    
    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        # pylint: disable=no-member
        device, _ = Device.objects.get_or_create(  # type: ignore
            device_id=device_id,
            defaults={'name': f'ECG Device {device_id}', 'device_type': 'ESP32'}
        )
        device.save()  # Update last_seen
        validated_data['device'] = device
        return super().create(validated_data)


class PulseOximeterReadingSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(write_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = PulseOximeterReading
        fields = ['id', 'device_id', 'device_name', 'timestamp', 'spo2', 'heart_rate', 'signal_strength']
        read_only_fields = ['id', 'timestamp', 'device_name']
    
    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        # pylint: disable=no-member
        device, _ = Device.objects.get_or_create(  # type: ignore
            device_id=device_id,
            defaults={'name': f'Pulse Oximeter {device_id}', 'device_type': 'ESP32'}
        )
        device.save()  # Update last_seen
        validated_data['device'] = device
        return super().create(validated_data)


class MAX30102ReadingSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(write_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = MAX30102Reading
        fields = ['id', 'device_id', 'device_name', 'timestamp', 'heart_rate', 'spo2', 
                 'red_value', 'ir_value', 'temperature']
        read_only_fields = ['id', 'timestamp', 'device_name']
    
    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        # pylint: disable=no-member
        device, _ = Device.objects.get_or_create(  # type: ignore
            device_id=device_id,
            defaults={'name': f'MAX30102 {device_id}', 'device_type': 'ESP32'}
        )
        device.save()  # Update last_seen
        validated_data['device'] = device
        return super().create(validated_data)


class AccelerometerReadingSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(write_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = AccelerometerReading
        fields = ['id', 'device_id', 'device_name', 'timestamp', 'x_axis', 'y_axis', 'z_axis', 'magnitude']
        read_only_fields = ['id', 'timestamp', 'device_name']
    
    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        # pylint: disable=no-member
        device, _ = Device.objects.get_or_create(  # type: ignore
            device_id=device_id,
            defaults={'name': f'Accelerometer {device_id}', 'device_type': 'ESP32'}
        )
        device.save()  # Update last_seen
        validated_data['device'] = device
        return super().create(validated_data)


class DeviceStatusSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(write_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = DeviceStatus
        fields = ['id', 'device_id', 'device_name', 'timestamp', 'battery_level', 
                 'wifi_signal_strength', 'memory_usage', 'cpu_temperature', 'uptime_seconds']
        read_only_fields = ['id', 'timestamp', 'device_name']
    
    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        # pylint: disable=no-member
        device, _ = Device.objects.get_or_create(  # type: ignore
            device_id=device_id,
            defaults={'name': f'Device {device_id}', 'device_type': 'ESP32'}
        )
        device.save()  # Update last_seen
        validated_data['device'] = device
        return super().create(validated_data)


class BulkSensorDataSerializer(serializers.Serializer):
    """Serializer for bulk sensor data from ESP32"""
    device_id = serializers.CharField(max_length=100)
    
    # ECG data
    ecg_heart_rate = serializers.FloatField(required=False, allow_null=True)
    ecg_value = serializers.FloatField(required=False, allow_null=True)
    ecg_signal_quality = serializers.CharField(required=False, allow_null=True)
    
    # Pulse Oximeter data
    spo2 = serializers.FloatField(required=False, allow_null=True)
    pulse_heart_rate = serializers.FloatField(required=False, allow_null=True)
    pulse_signal_strength = serializers.IntegerField(required=False, allow_null=True)
    
    # MAX30102 data
    max30102_heart_rate = serializers.FloatField(required=False, allow_null=True)
    max30102_spo2 = serializers.FloatField(required=False, allow_null=True)
    red_value = serializers.IntegerField(required=False, allow_null=True)
    ir_value = serializers.IntegerField(required=False, allow_null=True)
    temperature = serializers.FloatField(required=False, allow_null=True)
    
    # Accelerometer data
    x_axis = serializers.FloatField(required=False, allow_null=True)
    y_axis = serializers.FloatField(required=False, allow_null=True)
    z_axis = serializers.FloatField(required=False, allow_null=True)
    magnitude = serializers.FloatField(required=False, allow_null=True)
    
    # Device status
    battery_level = serializers.FloatField(required=False, allow_null=True)
    wifi_signal_strength = serializers.IntegerField(required=False, allow_null=True)
    memory_usage = serializers.FloatField(required=False, allow_null=True)
    cpu_temperature = serializers.FloatField(required=False, allow_null=True)
    uptime_seconds = serializers.IntegerField(required=False, allow_null=True)
    
    def create(self, validated_data: dict) -> Optional[Any]:
        """This serializer is used for validation only, not for creating objects"""
        # pylint: disable=unused-argument
        return None
    
    def update(self, instance: Any, validated_data: dict) -> Any:
        """This serializer is used for validation only, not for updating objects"""
        # pylint: disable=unused-argument
        return instance
