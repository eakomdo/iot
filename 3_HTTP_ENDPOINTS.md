# 3 Essential IoT HTTP Endpoints

## **🔗 Your 3 Main HTTP Endpoints**

### **1. Upload Sensor Data**
```
POST https://iot-khgd.onrender.com/api/sensors/bulk/
```
**Purpose:** Send sensor data from ESP32/IoT devices  
**Content-Type:** `application/json`  
**Body Example:**
```json
{
  "device_id": "ESP32_001",
  "ecg_heart_rate": 75,
  "spo2": 98,
  "x_axis": 0.12
}
```
**Response:** Raw values (one per line)
```
75
98
0.12
```

### **2. Get Device List**
```
GET https://iot-khgd.onrender.com/api/devices/
```
**Purpose:** List all registered IoT devices  
**Response:** Device names (one per line)
```
ESP32_001
ESP32_002
HEART_MONITOR
```

### **3. Get Latest Sensor Values**
```
GET https://iot-khgd.onrender.com/api/devices/{device_id}/raw/
```
**Purpose:** Get current sensor readings in CSV format  
**Example:** `GET /api/devices/ESP32_001/raw/`  
**Response:** Comma-separated values
```
75,98,74,0.12,-0.05,9.81
```

## **📱 Usage Examples**

### **ESP32 Code:**
```cpp
// Endpoint 1: Upload data
const char* uploadEndpoint = "https://iot-khgd.onrender.com/api/sensors/bulk/";

// Send POST request with sensor data
// Server responds with raw values: "75\n98\n74"
```

### **Web App/Dashboard:**
```javascript
// Endpoint 2: Get devices
fetch('https://iot-khgd.onrender.com/api/devices/')
  .then(response => response.text())
  .then(data => console.log(data)); // "ESP32_001\nESP32_002"

// Endpoint 3: Get latest values  
fetch('https://iot-khgd.onrender.com/api/devices/ESP32_001/raw/')
  .then(response => response.text())
  .then(data => console.log(data)); // "75,98,74,0.12,-0.05,9.81"
```

### **Python Client:**
```python
import requests

# Endpoint 1: Upload
response = requests.post('https://iot-khgd.onrender.com/api/sensors/bulk/',
                        json={"device_id": "TEST", "ecg_heart_rate": 75})
print(response.text)  # "75"

# Endpoint 2: List devices
response = requests.get('https://iot-khgd.onrender.com/api/devices/')
print(response.text)  # "TEST\nESP32_001"

# Endpoint 3: Get values
response = requests.get('https://iot-khgd.onrender.com/api/devices/TEST/raw/')
print(response.text)  # "75,0,0,0,0,0"
```

## **🎯 Perfect for IoT!**
- ✅ **Simple URLs** - Easy to remember
- ✅ **Raw responses** - No JSON parsing needed
- ✅ **Real-time ready** - Updates every 3 seconds
- ✅ **Live now** - All endpoints working at iot-khgd.onrender.com
