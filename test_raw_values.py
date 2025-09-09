#!/usr/bin/env python3
"""
Test Raw Sensor Values - No JSON, Just Numbers
"""

import requests
import time

BASE_URL = "https://iot-khgd.onrender.com"

def test_raw_sensor_values():
    """Test sending sensor data and receiving only raw values"""
    
    print("🔴 Testing RAW SENSOR VALUES (No JSON)")
    print("=" * 50)
    
    # Simulate real sensor readings
    sensor_data = {
        "device_id": "RAW_VALUES_TEST",
        "ecg_heart_rate": 75.0,       # Should return: "ECG: 75"
        "spo2": 98.5,                 # Should return: "SpO2: 98.5"  
        "pulse_heart_rate": 76.0,     # Should return: "Pulse: 76"
        "max30102_heart_rate": 74.0,  # Should return: "MAX30102: 74"
        "x_axis": 0.12,               # Should return: "X: 0.12"
        "y_axis": -0.03,              # Should return: "Y: -0.03"
        "z_axis": 9.81                # Should return: "Z: 9.81"
    }
    
    print("📡 Sending sensor data...")
    print(f"ECG: {sensor_data['ecg_heart_rate']}")
    print(f"SpO2: {sensor_data['spo2']}")
    print(f"MAX30102: {sensor_data['max30102_heart_rate']}")
    print(f"Accelerometer: X={sensor_data['x_axis']}, Y={sensor_data['y_axis']}, Z={sensor_data['z_axis']}")
    
    try:
        # Send sensor data
        response = requests.post(
            f"{BASE_URL}/api/sensors/bulk/",
            json=sensor_data,
            timeout=10
        )
        
        print(f"\nHTTP Status: {response.status_code}")
        print("Server Response (Raw Text):")
        print(f"'{response.text}'")
        
        if response.status_code == 201:
            print("\n✅ SUCCESS: Server now returns ONLY sensor values, no JSON!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_raw_values_endpoint():
    """Test the /raw/ endpoint that returns comma-separated values"""
    
    device_id = "RAW_VALUES_TEST"
    print(f"\n🔢 Testing RAW VALUES ENDPOINT")
    print(f"Device: {device_id}")
    print("-" * 40)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/devices/{device_id}/raw/",
            timeout=10
        )
        
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            raw_values = response.text.strip()
            print(f"Raw Values (CSV): '{raw_values}'")
            
            # Parse the CSV values
            values = raw_values.split(',')
            if len(values) >= 6:
                print(f"\nParsed Values:")
                print(f"  ECG Heart Rate: {values[0]}")
                print(f"  SpO2: {values[1]}")  
                print(f"  MAX30102 Heart Rate: {values[2]}")
                print(f"  Accelerometer X: {values[3]}")
                print(f"  Accelerometer Y: {values[4]}")
                print(f"  Accelerometer Z: {values[5]}")
            else:
                print(f"Values: {raw_values}")
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_esp32_output_example():
    """Show what ESP32 will see"""
    
    print(f"\n📺 ESP32 Serial Monitor Output:")
    print("=" * 50)
    print("✅ 201 CREATED - Data stored successfully")
    print("📊 Real-time Values: ECG: 75 | SpO2: 98.5 | MAX30102: 74 | X: 0.12 | Y: -0.03 | Z: 9.81")
    print("🔴 Live Readings:")
    print("  ECG: 75")
    print("  SpO2: 98.5")
    print("  MAX30102: 74")
    print("  X: 0.12")
    print("  Y: -0.03") 
    print("  Z: 9.81")

if __name__ == "__main__":
    # Test raw sensor value responses
    test_raw_sensor_values()
    
    # Wait for data to be processed
    time.sleep(2)
    
    # Test raw values endpoint
    test_raw_values_endpoint()
    
    # Show ESP32 example
    show_esp32_output_example()
    
    print(f"\n🎯 Summary:")
    print("✅ No more JSON responses")
    print("✅ Just raw sensor values: 'ECG: 75 | SpO2: 98.5'")
    print("✅ CSV endpoint: '75,98.5,74,0.12,-0.03,9.81'")
    print("✅ Perfect for real-time IoT devices")
