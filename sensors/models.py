from django.db import models
from django.utils import timezone


class Device(models.Model):
    """Model for IoT devices"""
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=50, default='ESP32')
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.device_id})"


class SensorReading(models.Model):
    """Base model for all sensor readings"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    sensor_type = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['-timestamp']


class ECGReading(models.Model):
    """Model for ECG sensor readings"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='ecg_readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    heart_rate = models.FloatField(help_text="Heart rate in BPM")
    ecg_value = models.FloatField(help_text="Raw ECG value")
    signal_quality = models.CharField(max_length=20, default='good', 
                                    choices=[('poor', 'Poor'), ('fair', 'Fair'), ('good', 'Good')])
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"ECG - {self.device.name} - HR: {self.heart_rate} BPM"


class PulseOximeterReading(models.Model):
    """Model for Pulse Oximeter readings"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='pulse_ox_readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    spo2 = models.FloatField(help_text="Blood oxygen saturation (%)")
    heart_rate = models.FloatField(help_text="Heart rate in BPM")
    signal_strength = models.IntegerField(help_text="Signal strength (0-100)")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Pulse Ox - {self.device.name} - SpO2: {self.spo2}%, HR: {self.heart_rate} BPM"


class MAX30102Reading(models.Model):
    """Model for MAX30102 Heart Rate sensor readings"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='max30102_readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    heart_rate = models.FloatField(help_text="Heart rate in BPM")
    spo2 = models.FloatField(null=True, blank=True, help_text="Blood oxygen saturation (%)")
    red_value = models.IntegerField(help_text="Red LED value")
    ir_value = models.IntegerField(help_text="IR LED value")
    temperature = models.FloatField(null=True, blank=True, help_text="Temperature in Celsius")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"MAX30102 - {self.device.name} - HR: {self.heart_rate} BPM"


class AccelerometerReading(models.Model):
    """Model for Accelerometer readings"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='accel_readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    x_axis = models.FloatField(help_text="X-axis acceleration (g)")
    y_axis = models.FloatField(help_text="Y-axis acceleration (g)")
    z_axis = models.FloatField(help_text="Z-axis acceleration (g)")
    magnitude = models.FloatField(help_text="Acceleration magnitude")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Accel - {self.device.name} - Mag: {self.magnitude:.2f}g"


class DeviceStatus(models.Model):
    """Model for device status and health monitoring"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='status_reports')
    timestamp = models.DateTimeField(auto_now_add=True)
    battery_level = models.FloatField(null=True, blank=True, help_text="Battery level (%)")
    wifi_signal_strength = models.IntegerField(null=True, blank=True, help_text="WiFi signal strength (dBm)")
    memory_usage = models.FloatField(null=True, blank=True, help_text="Memory usage (%)")
    cpu_temperature = models.FloatField(null=True, blank=True, help_text="CPU temperature (°C)")
    uptime_seconds = models.IntegerField(null=True, blank=True, help_text="Device uptime in seconds")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Status - {self.device.name} - {self.timestamp}"
