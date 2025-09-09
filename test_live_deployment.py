#!/usr/bin/env python3
"""
Comprehensive Test Suite for Live IoT Deployment
Tests the deployed Django API and PostgreSQL database on Render
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

def test_basic_connectivity():
    """Test basic connectivity to the deployed app"""
    print_header("🌐 Testing Basic Connectivity")
    
    try:
        # Test main app
        response = requests.get(BASE_URL, timeout=10)
        if response.status_code == 200:
            print_success(f"Main app is accessible: {BASE_URL}")
            return True
        else:
            print_error(f"Main app returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to main app: {e}")
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    print_header("🔌 Testing API Endpoints")
    
    endpoints = [
        "/",
        "/devices/",
        "/sensor-data/bulk/"
    ]
    
    all_passed = True
    
    for endpoint in endpoints:
        try:
            url = f"{API_BASE}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code in [200, 405]:  # 405 is OK for POST-only endpoints
                print_success(f"API endpoint accessible: {endpoint}")
                if endpoint == "/":
                    # Try to parse JSON response
                    try:
                        data = response.json()
                        print_info(f"  API root response: {list(data.keys()) if isinstance(data, dict) else 'Valid JSON'}")
                    except:
                        print_info("  API root returned HTML (normal for DRF browsable API)")
            else:
                print_error(f"API endpoint {endpoint} returned status: {response.status_code}")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print_error(f"Failed to connect to API endpoint {endpoint}: {e}")
            all_passed = False
    
    return all_passed

def test_health_check():
    """Test health check endpoint"""
    print_header("❤️ Testing Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success("Health check passed")
            print_info(f"  Status: {data.get('status', 'Unknown')}")
            print_info(f"  Database: {data.get('database', 'Unknown')}")
            print_info(f"  Timestamp: {data.get('timestamp', 'Unknown')}")
            return True
        else:
            print_error(f"Health check failed with status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False

def test_device_creation():
    """Test creating a device"""
    print_header("📱 Testing Device Creation")
    
    device_data = {
        "device_id": f"TEST_DEVICE_{int(time.time())}",
        "device_type": "ESP32",
        "location": "Test Lab",
        "is_active": True
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/devices/",
            json=device_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201:
            device = response.json()
            print_success("Device created successfully")
            print_info(f"  Device ID: {device.get('device_id')}")
            print_info(f"  Database ID: {device.get('id')}")
            return device
        else:
            print_error(f"Device creation failed with status: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"  Error details: {error_data}")
            except:
                print_error(f"  Response text: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Device creation failed: {e}")
        return None

def test_sensor_data_upload():
    """Test uploading sensor data"""
    print_header("📊 Testing Sensor Data Upload")
    
    # Create sensor data similar to what ESP32 would send
    sensor_data = {
        "device_id": f"TEST_DEVICE_{int(time.time())}",
        
        # ECG data
        "ecg_heart_rate": 72.5,
        "ecg_value": 1.23,
        "ecg_signal_quality": "good",
        
        # Pulse Oximeter data
        "spo2": 97.2,
        "pulse_heart_rate": 71.8,
        "pulse_signal_strength": 85,
        
        # MAX30102 data
        "max30102_heart_rate": 73.1,
        "max30102_spo2": 96.8,
        "red_value": 25000,
        "ir_value": 35000,
        "temperature": 36.7,
        
        # Accelerometer data
        "x_axis": 0.15,
        "y_axis": -0.22,
        "z_axis": 9.85,
        "magnitude": 9.87,
        
        # Device status
        "battery_level": 85.0,
        "wifi_signal_strength": -45,
        "memory_usage": 45.0,
        "cpu_temperature": 42.0,
        "uptime_seconds": 1234
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/sensor-data/bulk/",
            json=sensor_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            print_success("Sensor data uploaded successfully")
            print_info(f"  Records created: {result.get('records_created', 'Unknown')}")
            print_info(f"  Device: {result.get('device_id', 'Unknown')}")
            return True
        else:
            print_error(f"Sensor data upload failed with status: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"  Error details: {error_data}")
            except:
                print_error(f"  Response text: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Sensor data upload failed: {e}")
        return False

def test_database_queries():
    """Test database queries through the API"""
    print_header("🗄️ Testing Database Queries")
    
    try:
        # Test devices endpoint
        response = requests.get(f"{API_BASE}/devices/", timeout=10)
        if response.status_code == 200:
            devices = response.json()
            device_count = len(devices) if isinstance(devices, list) else devices.get('count', 0)
            print_success(f"Database query successful - Found {device_count} devices")
            
            if isinstance(devices, list) and devices:
                latest_device = devices[0]
                print_info(f"  Latest device: {latest_device.get('device_id', 'Unknown')}")
                print_info(f"  Created: {latest_device.get('created_at', 'Unknown')}")
            
            return True
        else:
            print_error(f"Database query failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Database query failed: {e}")
        return False

def test_admin_panel():
    """Test admin panel accessibility"""
    print_header("👨‍💼 Testing Admin Panel")
    
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=10)
        if response.status_code == 200:
            print_success("Admin panel is accessible")
            print_info(f"  URL: {BASE_URL}/admin/")
            print_warning("  Note: You need to create a superuser to login")
            print_info("  Run in Render Shell: python manage.py createsuperuser")
            return True
        else:
            print_error(f"Admin panel returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Admin panel test failed: {e}")
        return False

def test_multiple_requests():
    """Test multiple concurrent requests to simulate load"""
    print_header("🚀 Testing Multiple Requests (Load Test)")
    
    success_count = 0
    total_requests = 5
    
    for i in range(total_requests):
        try:
            # Test different endpoints
            endpoints = [
                f"{API_BASE}/",
                f"{BASE_URL}/health/",
                f"{API_BASE}/devices/"
            ]
            
            endpoint = endpoints[i % len(endpoints)]
            response = requests.get(endpoint, timeout=5)
            
            if response.status_code in [200, 405]:
                success_count += 1
                print_success(f"Request {i+1}/{total_requests} successful")
            else:
                print_error(f"Request {i+1}/{total_requests} failed with status: {response.status_code}")
                
        except Exception as e:
            print_error(f"Request {i+1}/{total_requests} failed: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    success_rate = (success_count / total_requests) * 100
    print_info(f"Success rate: {success_rate:.1f}% ({success_count}/{total_requests})")
    
    return success_rate >= 80  # Consider 80%+ success rate as pass

def run_comprehensive_test():
    """Run all tests"""
    print_header("🧪 COMPREHENSIVE IoT DEPLOYMENT TEST")
    print_info(f"Testing deployment: {BASE_URL}")
    print_info(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = {}
    
    # Run all tests
    tests = [
        ("Basic Connectivity", test_basic_connectivity),
        ("API Endpoints", test_api_endpoints),
        ("Health Check", test_health_check),
        ("Database Queries", test_database_queries),
        ("Device Creation", lambda: test_device_creation() is not None),
        ("Sensor Data Upload", test_sensor_data_upload),
        ("Admin Panel", test_admin_panel),
        ("Load Test", test_multiple_requests)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results[test_name] = result
            if result:
                passed += 1
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            test_results[test_name] = False
    
    # Final report
    print_header("📋 FINAL TEST REPORT")
    
    for test_name, result in test_results.items():
        status = "PASS" if result else "FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status:<6}{Colors.END} {test_name}")
    
    success_rate = (passed / total) * 100
    
    print(f"\n{Colors.BOLD}Overall Result: {passed}/{total} tests passed ({success_rate:.1f}%){Colors.END}")
    
    if success_rate >= 90:
        print_success("🎉 EXCELLENT! Your deployment is working perfectly!")
    elif success_rate >= 70:
        print_warning("🔧 GOOD! Minor issues detected, but system is functional")
    else:
        print_error("🚨 ISSUES DETECTED! Check failed tests above")
    
    print_info("\nNext Steps:")
    print("1. Create admin superuser: python manage.py createsuperuser (in Render Shell)")
    print("2. Upload ESP32 code with your WiFi credentials")
    print("3. Monitor data flow through admin panel")
    print(f"4. API Documentation: {API_BASE}/")
    print(f"5. Admin Panel: {BASE_URL}/admin/")

if __name__ == "__main__":
    run_comprehensive_test()
