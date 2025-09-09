#!/usr/bin/env python3
"""
Test script for the IoT Sensor API
"""
import requests
import json

# API base URL (change this to your Render URL when deployed)
BASE_URL = "http://127.0.0.1:8000/api"

def test_api_overview():
    """Test the API overview endpoint"""
    print("Testing API overview...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_bulk_sensor_data():
    """Test the bulk sensor data endpoint"""
    print("Testing bulk sensor data submission...")
    
    test_data = {
        "device_id": "TEST_ESP32_001",
        "ecg_heart_rate": 75.5,
        "ecg_value": 123.45,
        "ecg_signal_quality": "good",
        "spo2": 98.2,
        "pulse_heart_rate": 74.8,
        "pulse_signal_strength": 85,
        "max30102_heart_rate": 76.1,
        "max30102_spo2": 97.8,
        "red_value": 12345,
        "ir_value": 67890,
        "temperature": 36.9,
        "x_axis": 0.12,
        "y_axis": 0.25,
        "z_axis": 9.81,
        "magnitude": 9.83,
        "battery_level": 87.5,
        "wifi_signal_strength": -42,
        "memory_usage": 45.2,
        "cpu_temperature": 41.8,
        "uptime_seconds": 3661
    }
    
    response = requests.post(
        f"{BASE_URL}/sensors/bulk/",
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_device_readings():
    """Test getting device readings"""
    print("Testing device readings endpoint...")
    device_id = "TEST_ESP32_001"
    response = requests.get(f"{BASE_URL}/devices/{device_id}/readings/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Device: {data['device']['name']}")
        print(f"ECG readings count: {len(data['ecg_readings'])}")
        print(f"Pulse oximeter readings count: {len(data['pulse_oximeter_readings'])}")
        print(f"MAX30102 readings count: {len(data['max30102_readings'])}")
        print(f"Accelerometer readings count: {len(data['accelerometer_readings'])}")
        print(f"Device status count: {len(data['device_status'])}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_devices_list():
    """Test listing all devices"""
    print("Testing devices list endpoint...")
    response = requests.get(f"{BASE_URL}/devices/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        devices = response.json()
        print(f"Number of devices: {len(devices)}")
        for device in devices:
            print(f"  - {device['name']} ({device['device_id']}) - Last seen: {device['last_seen']}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

if __name__ == "__main__":
    print("IoT Sensor API Test Suite")
    print("=" * 50)
    
    try:
        # Test all endpoints
        test_api_overview()
        test_bulk_sensor_data()
        test_device_readings()
        test_devices_list()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the Django development server is running on http://127.0.0.1:8000/")
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        print(f"❌ Error: {str(e)}")
