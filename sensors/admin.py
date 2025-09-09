from django.contrib import admin
from .models import (
    Device, ECGReading, PulseOximeterReading, 
    MAX30102Reading, AccelerometerReading, DeviceStatus
)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'device_type', 'is_active', 'last_seen', 'created_at']
    list_filter = ['device_type', 'is_active', 'created_at']
    search_fields = ['device_id', 'name']
    readonly_fields = ['created_at', 'last_seen']


@admin.register(ECGReading)
class ECGReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'timestamp', 'heart_rate', 'ecg_value', 'signal_quality']
    list_filter = ['signal_quality', 'timestamp', 'device']
    search_fields = ['device__device_id', 'device__name']
    readonly_fields = ['timestamp']


@admin.register(PulseOximeterReading)
class PulseOximeterReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'timestamp', 'spo2', 'heart_rate', 'signal_strength']
    list_filter = ['timestamp', 'device']
    search_fields = ['device__device_id', 'device__name']
    readonly_fields = ['timestamp']


@admin.register(MAX30102Reading)
class MAX30102ReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'timestamp', 'heart_rate', 'spo2', 'red_value', 'ir_value']
    list_filter = ['timestamp', 'device']
    search_fields = ['device__device_id', 'device__name']
    readonly_fields = ['timestamp']


@admin.register(AccelerometerReading)
class AccelerometerReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'timestamp', 'x_axis', 'y_axis', 'z_axis', 'magnitude']
    list_filter = ['timestamp', 'device']
    search_fields = ['device__device_id', 'device__name']
    readonly_fields = ['timestamp']


@admin.register(DeviceStatus)
class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ['device', 'timestamp', 'battery_level', 'wifi_signal_strength', 'memory_usage']
    list_filter = ['timestamp', 'device']
    search_fields = ['device__device_id', 'device__name']
    readonly_fields = ['timestamp']
