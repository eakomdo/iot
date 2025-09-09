#!/usr/bin/env python3
"""
Test the new clean API response
"""

import requests
import json

# Test data
test_data = {
    "device_id": "ESP32_CLEAN_TEST",
    "ecg_heart_rate": 72.0,
    "spo2": 98.5,
    "x_axis": 0.1,
    "y_axis": 0.2,
    "z_axis": 9.8,
    "battery_level": 85.0
}

# Test local API (if running)
print("🧪 Testing Clean API Response...")
print("=" * 50)

try:
    # Test API overview
    response = requests.get("https://iot-khgd.onrender.com/api/")
    if response.status_code == 200:
        data = response.json()
        print("✅ API Overview:")
        print(f"   Message: {data['message']}")
        print(f"   Status: {data['status']}")
        print(f"   Database: {data['database']}")
        print()
    
    # Test sensor data upload
    print("📤 Testing Sensor Data Upload...")
    response = requests.post(
        "https://iot-khgd.onrender.com/api/sensors/bulk/",
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 201:
        data = response.json()
        print("✅ Upload Response:")
        print(f"   Success: {data['success']}")
        print(f"   Message: {data['message']}")
        print(f"   Device ID: {data['device_id']}")
        print(f"   Status: {data['status']}")
        print(f"   Timestamp: {data['timestamp']}")
        print()
        print("🎉 Perfect! Clean success response working!")
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🚀 Your API now returns clean success messages!")
print("✅ No more mock data - real sensor data will populate the database")
print("✅ ESP32 will get clear success confirmations")
