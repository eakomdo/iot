#!/usr/bin/env python3
"""
Test Real-Time IoT Values Display
Demonstrates the new value-based responses instead of JSON format
"""

import requests
import json
import time

BASE_URL = "https://iot-khgd.onrender.com"

def send_test_sensor_data():
    """Send test sensor data to see the new value-based response"""
    
    # Simulate real IoT device readings
    test_data = {
        "device_id": "REAL_TIME_TEST",
        "ecg_heart_rate": 71.0,        # This will show as "ECG Heart Rate: 71 BPM"
        "ecg_value": 0.85,
        "spo2": 98.2,                  # This will show as "SpO2: 98.2%"
        "pulse_heart_rate": 72.0,      # This will show as "Pulse Rate: 72 BPM"
        "max30102_heart_rate": 70.5,
        "red_value": 12567,
        "ir_value": 45890,
        "x_axis": 0.15,                # This will show as "X-Axis: 0.15 g"
        "y_axis": -0.05,
        "z_axis": 9.78,
        "battery_level": 87.0,         # This will show as "Battery: 87%"
        "wifi_signal_strength": -42    # This will show as "WiFi Signal: -42 dBm"
    }
    
    print("🚀 Testing Real-Time IoT Value Display")
    print("=" * 50)
    print(f"Sending sensor data from device: {test_data['device_id']}")
    
    try:
        # Send the sensor data
        response = requests.post(
            f"{BASE_URL}/api/sensors/bulk/",
            json=test_data,
            timeout=10
        )
        
        print(f"\nHTTP Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ {data.get('message', 'Success')}")
            
            if 'readings' in data:
                print("\n📊 Live Sensor Values:")
                for reading in data['readings']:
                    print(f"  📈 {reading}")
            
            print(f"\n⏰ Timestamp: {data.get('timestamp', 'Unknown')}")
            
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_latest_readings():
    """Test the new endpoint to get latest readings in simple format"""
    
    device_id = "REAL_TIME_TEST"
    print(f"\n🔍 Testing Latest Readings for Device: {device_id}")
    print("-" * 40)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/devices/{device_id}/latest/",
            timeout=10
        )
        
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Device: {data.get('device', 'Unknown')}")
            print(f"Status: {data.get('status', 'Unknown')}")
            print(f"Last Seen: {data.get('last_seen', 'Unknown')}")
            
            if 'latest_readings' in data:
                print("\n📊 Latest Sensor Values:")
                for reading in data['latest_readings']:
                    print(f"  📈 {reading}")
            else:
                print(f"📝 {data.get('message', 'No data available')}")
                
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def compare_old_vs_new():
    """Show comparison between old JSON format and new value format"""
    
    print("\n📋 Format Comparison")
    print("=" * 50)
    
    print("OLD FORMAT (JSON):")
    print('  {"status": "success", "code": 201, "message": "Created"}')
    
    print("\nNEW FORMAT (Values):")
    print('  ✅ Data received successfully from REAL_TIME_TEST')
    print('  📈 ECG Heart Rate: 71 BPM')
    print('  📈 SpO2: 98.2%')
    print('  📈 Pulse Rate: 72 BPM')
    print('  📈 Battery: 87%')
    print('  📈 WiFi Signal: -42 dBm')

if __name__ == "__main__":
    # Show format comparison first
    compare_old_vs_new()
    
    # Test sending data and getting value-based response
    send_test_sensor_data()
    
    # Wait a moment for data to be processed
    time.sleep(2)
    
    # Test the new latest readings endpoint
    test_latest_readings()
    
    print(f"\n🎯 Real-Time Features:")
    print("   • ESP32 now reads sensors every 0.5 seconds")
    print("   • Data sent every 3 seconds (instead of 10)")
    print("   • Server responds with actual sensor values")
    print("   • No more verbose JSON - just the values you need")
    print("   • Real-time monitoring via /latest/ endpoint")
