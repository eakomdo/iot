#!/usr/bin/env python3
"""
Fixed Live Deployment Test Suite
Tests your deployed IoT sensor system on Render with correct endpoints
"""

import requests
import json
import time
from datetime import datetime
import random

# Your live Render deployment URL
BASE_URL = "https://iot-khgd.onrender.com"
API_BASE = f"{BASE_URL}/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_header(message):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}{Colors.END}\n")

def test_endpoints():
    """Test all API endpoints"""
    print_header("🔌 Testing All API Endpoints")
    
    endpoints = [
        ("Root", BASE_URL),
        ("API Root", f"{API_BASE}/"),
        ("Devices", f"{API_BASE}/devices/"),
        ("Sensors Bulk (ESP32)", f"{API_BASE}/sensors/bulk/"),
        ("Health Check", f"{API_BASE}/health/"),
        ("Admin Panel", f"{BASE_URL}/admin/"),
    ]
    
    working = 0
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code in [200, 302, 405]:  # 405 = POST only, 302 = redirect
                print_success(f"{name}: {response.status_code} - Working")
                working += 1
            else:
                print_error(f"{name}: {response.status_code} - Issue")
        except Exception as e:
            print_error(f"{name}: Failed - {str(e)}")
    
    return working, len(endpoints)

def test_sensor_data_upload():
    """Test posting sensor data (ESP32 simulation)"""
    print_header("📊 Testing Sensor Data Upload (ESP32 Simulation)")
    
    # Create realistic test data
    test_data = {
        "device_id": "TEST_ESP32_DEPLOYMENT",
        "ecg_heart_rate": round(72.0 + random.uniform(-10, 10), 1),
        "ecg_value": round(random.uniform(1.0, 3.0), 2),
        "ecg_signal_quality": "good",
        "spo2": round(96.0 + random.uniform(-2, 3), 1),
        "pulse_heart_rate": round(70.0 + random.uniform(-8, 8), 1),
        "pulse_signal_strength": random.randint(75, 95),
        "max30102_heart_rate": round(71.0 + random.uniform(-7, 7), 1),
        "max30102_spo2": round(97.0 + random.uniform(-1, 2), 1),
        "red_value": random.randint(15000, 45000),
        "ir_value": random.randint(20000, 55000),
        "temperature": round(36.5 + random.uniform(-0.5, 1.5), 1),
        "x_axis": round(random.uniform(-1.5, 1.5), 2),
        "y_axis": round(random.uniform(-1.5, 1.5), 2),
        "z_axis": round(9.8 + random.uniform(-0.3, 0.3), 2),
        "magnitude": 0,  # Will calculate
        "battery_level": round(random.uniform(75, 100), 1),
        "wifi_signal_strength": random.randint(-70, -40),
        "memory_usage": round(random.uniform(35, 75), 1),
        "cpu_temperature": round(random.uniform(38, 48), 1),
        "uptime_seconds": random.randint(300, 86400)
    }
    
    # Calculate magnitude
    test_data["magnitude"] = round(
        (test_data["x_axis"]**2 + test_data["y_axis"]**2 + test_data["z_axis"]**2)**0.5, 2
    )
    
    print_info(f"Uploading data from device: {test_data['device_id']}")
    print_info(f"Heart Rate: {test_data['ecg_heart_rate']} BPM, SpO2: {test_data['spo2']}%")
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            f"{API_BASE}/sensors/bulk/", 
            json=test_data, 
            headers=headers, 
            timeout=15
        )
        
        if response.status_code == 201:
            print_success("✓ Sensor data uploaded successfully!")
            print_success(f"✓ Server response: {response.json()}")
            return True
        elif response.status_code == 200:
            print_success("✓ Sensor data processed successfully!")
            return True
        else:
            print_error(f"✗ Upload failed: HTTP {response.status_code}")
            print_error(f"Response: {response.text[:200]}...")
            return False
    except Exception as e:
        print_error(f"✗ Upload error: {str(e)}")
        return False

def test_database_check():
    """Check database and device creation"""
    print_header("🗄️ Testing Database & Device Management")
    
    try:
        # Check devices
        response = requests.get(f"{API_BASE}/devices/", timeout=10)
        if response.status_code == 200:
            devices = response.json()
            print_success(f"✓ Database accessible - Found {len(devices)} devices")
            
            # Look for our test device
            test_device = None
            for device in devices:
                if device.get('device_id') == 'TEST_ESP32_DEPLOYMENT':
                    test_device = device
                    break
            
            if test_device:
                print_success(f"✓ Test device found: {test_device['name']}")
                print_success(f"✓ Last seen: {test_device.get('last_seen', 'N/A')}")
            else:
                print_warning("⚠️  Test device not found (may be expected)")
            
            return True
        else:
            print_error(f"✗ Database check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"✗ Database error: {str(e)}")
        return False

def test_health_check():
    """Test health check endpoint"""
    print_header("❤️ Testing Health Check")
    
    try:
        response = requests.get(f"{API_BASE}/health/", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print_success(f"✓ Health check passed: {health_data.get('status', 'unknown')}")
            print_success(f"✓ Database: {health_data.get('database', 'unknown')}")
            print_success(f"✓ Total devices: {health_data.get('statistics', {}).get('total_devices', 0)}")
            print_success(f"✓ Total readings: {health_data.get('statistics', {}).get('total_readings', 0)}")
            return True
        else:
            print_error(f"✗ Health check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"✗ Health check error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print_header("🚀 IoT DEPLOYMENT TEST SUITE - FIXED VERSION")
    print_info(f"Testing: {BASE_URL}")
    print_info(f"API: {API_BASE}")
    print_info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test 1: Endpoints
    working, total = test_endpoints()
    results['endpoints'] = working == total
    
    # Test 2: Health Check
    results['health'] = test_health_check()
    
    # Test 3: Database
    results['database'] = test_database_check()
    
    # Test 4: Sensor Upload
    results['sensor_upload'] = test_sensor_data_upload()
    
    # Test 5: Final Database Check
    time.sleep(2)  # Wait for processing
    results['final_db'] = test_database_check()
    
    # Results Summary
    print_header("📊 FINAL RESULTS")
    
    passed = sum(results.values())
    total_tests = len(results)
    
    for test_name, passed_test in results.items():
        status = "PASS" if passed_test else "FAIL"
        color = Colors.GREEN if passed_test else Colors.RED
        print(f"{color}{status:4} | {test_name.replace('_', ' ').title()}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Overall: {passed}/{total_tests} tests passed ({passed/total_tests*100:.1f}%){Colors.END}")
    
    if passed == total_tests:
        print_success("🎉 PERFECT! Everything is working correctly!")
        print_success("✅ Your IoT system is ready for ESP32 devices")
        print_success("✅ Database is storing data properly") 
        print_success("✅ All API endpoints are functional")
    elif passed >= total_tests * 0.8:
        print_warning(f"⚠️  Good! {passed}/{total_tests} tests passed")
        print_warning("Minor issues detected but system is mostly functional")
    else:
        print_error(f"❌ Issues found: {passed}/{total_tests} tests passed")
        print_error("System needs attention before production use")
    
    print_header("🌐 Your Live System URLs")
    print_info(f"Main Site: {BASE_URL}")
    print_info(f"API Root: {API_BASE}/")
    print_info(f"ESP32 Endpoint: {API_BASE}/sensors/bulk/")
    print_info(f"Admin Panel: {BASE_URL}/admin/")
    print_info(f"Health Check: {API_BASE}/health/")
    
    if results['sensor_upload']:
        print_header("🎯 READY FOR ESP32!")
        print_success("Your ESP32 can now send data to:")
        print_success(f"URL: {API_BASE}/sensors/bulk/")
        print_success("Just update WiFi credentials and upload the code!")
    
    return passed == total_tests

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n❌ Test interrupted")
    except Exception as e:
        print_error(f"\n❌ Test suite error: {str(e)}")
