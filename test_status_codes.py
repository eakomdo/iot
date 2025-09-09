#!/usr/bin/env python3
"""
Test HTTP Status Code Responses
"""

import requests
import time

BASE_URL = "https://iot-khgd.onrender.com"

def test_status_codes():
    print("🧪 Testing HTTP Status Code Responses")
    print("=" * 50)
    
    tests = [
        ("API Root", f"{BASE_URL}/api/", "GET"),
        ("Health Check", f"{BASE_URL}/health/", "GET"), 
        ("Devices List", f"{BASE_URL}/api/devices/", "GET"),
        ("Sensor Upload", f"{BASE_URL}/api/sensors/bulk/", "POST"),
    ]
    
    # Test data for POST request
    test_data = {
        "device_id": "STATUS_CODE_TEST",
        "ecg_heart_rate": 75.0,
        "battery_level": 80.0
    }
    
    for name, url, method in tests:
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:  # POST
                response = requests.post(url, json=test_data, timeout=10)
            
            print(f"\n{name}:")
            print(f"   URL: {url}")
            print(f"   HTTP Status: {response.status_code}")
            
            try:
                data = response.json()
                if 'status' in data and 'code' in data:
                    print(f"   API Status: {data['status']}")
                    print(f"   API Code: {data['code']}")
                    print(f"   API Message: {data['message']}")
                else:
                    print(f"   Response: {data}")
            except:
                print(f"   Content: {response.text[:100]}...")
                
        except Exception as e:
            print(f"\n{name}: ERROR - {e}")
    
    print(f"\n🎯 Status Code Meanings:")
    print("   200 OK - Request successful")
    print("   201 CREATED - Resource created successfully") 
    print("   400 BAD REQUEST - Invalid request data")
    print("   404 NOT FOUND - Resource not found")
    print("   500 INTERNAL SERVER ERROR - Server error")

if __name__ == "__main__":
    test_status_codes()
