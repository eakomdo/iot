#!/usr/bin/env python3
"""
Test Pure Number Values - One Per Line
No device names, just raw sensor readings
"""

import requests

BASE_URL = "https://iot-khgd.onrender.com"

def show_response_examples():
    """Show exactly what responses will look like"""
    
    print("📊 PURE SENSOR VALUES - One Per Line")
    print("=" * 50)
    
    examples = [
        {
            "name": "ECG Device Reading 71 BPM",
            "input": {"device_id": "ECG_001", "ecg_heart_rate": 71.0},
            "output": "71"
        },
        {
            "name": "Pulse Oximeter Reading 98.2%",
            "input": {"device_id": "PULSE_001", "spo2": 98.2},
            "output": "98.2"
        },
        {
            "name": "Multiple Sensors",
            "input": {
                "device_id": "MULTI_001",
                "ecg_heart_rate": 75.0,
                "spo2": 98.2,
                "max30102_heart_rate": 74.0
            },
            "output": "75\n98.2\n74"
        },
        {
            "name": "Accelerometer Only",
            "input": {
                "device_id": "ACCEL_001",
                "x_axis": 0.12,
                "y_axis": -0.05,
                "z_axis": 9.81
            },
            "output": "0.12\n-0.05\n9.81"
        },
        {
            "name": "All Sensors Combined",
            "input": {
                "device_id": "ALL_001",
                "ecg_heart_rate": 71.0,
                "spo2": 98.5,
                "pulse_heart_rate": 72.0,
                "max30102_heart_rate": 73.0,
                "x_axis": 0.15,
                "y_axis": -0.02,
                "z_axis": 9.78
            },
            "output": "71\n98.5\n72\n73\n0.15\n-0.02\n9.78"
        }
    ]
    
    for example in examples:
        print(f"\n🔹 {example['name']}")
        print("   Input:", example['input'])
        print("   Server Response:")
        for line in example['output'].split('\n'):
            print(f"   {line}")

def show_esp32_output():
    """Show what ESP32 serial monitor will display"""
    
    print(f"\n📺 ESP32 Serial Monitor Output:")
    print("=" * 50)
    print("✅ 201 CREATED - Data stored successfully")
    print("📊 Raw Values Received:")
    print("  Value 1: 71")      # ECG heart rate
    print("  Value 2: 98.5")    # SpO2
    print("  Value 3: 72")      # Pulse heart rate  
    print("  Value 4: 73")      # MAX30102 heart rate
    print("  Value 5: 0.15")    # X-axis
    print("  Value 6: -0.02")   # Y-axis
    print("  Value 7: 9.78")    # Z-axis
    print("")

def test_live_response():
    """Test the actual live response"""
    
    print(f"\n🧪 Testing Live Response:")
    print("-" * 30)
    
    test_data = {
        "device_id": "PURE_TEST",
        "ecg_heart_rate": 68.0,
        "spo2": 97.8,
        "x_axis": 0.08
    }
    
    print("Sending:", test_data)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/sensors/bulk/",
            json=test_data,
            timeout=10
        )
        
        print(f"HTTP Status: {response.status_code}")
        print("Server Response:")
        
        # Show each line of the response
        lines = response.text.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip():
                print(f"  Line {i}: '{line}'")
        
        print(f"\nRaw Response: '{response.text}'")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Show examples
    show_response_examples()
    
    # Show ESP32 output
    show_esp32_output()
    
    # Test live
    test_live_response()
    
    print(f"\n🎯 Summary:")
    print("✅ No device names")
    print("✅ Just pure numbers")
    print("✅ One value per line")
    print("✅ Perfect for real-time parsing")
    print("✅ Easy to process on IoT devices")
