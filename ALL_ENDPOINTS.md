# 📡 COMPLETE IoT API ENDPOINTS REFERENCE

## **🌐 Base URL:** `https://iot-khgd.onrender.com`

---

## **🏠 SYSTEM ENDPOINTS**

### **Root & Health**
```bash
GET /                          # Redirects to /api/
GET /health/                   # Root health check
GET /api/                      # API overview
GET /api/health/               # API health check
```

---

## **📱 DEVICE MANAGEMENT**

### **Device List & Registration**
```bash
GET  /api/devices/             # Get all devices (plain text list)
POST /api/devices/             # Register new device
GET  /api/devices/simple/      # Simple device list
```

### **Individual Device Info**
```bash
GET /api/devices/{device_id}/           # Device details (JSON)
PUT /api/devices/{device_id}/           # Update device
DELETE /api/devices/{device_id}/        # Delete device
```

---

## **📊 DEVICE READINGS**

### **Combined Sensor Data**
```bash
GET /api/devices/{device_id}/readings/  # All readings for device (JSON)
GET /api/devices/{device_id}/latest/    # Latest readings summary
GET /api/devices/{device_id}/raw/       # CSV format: "75,98.5,74,0.12,-0.05,9.81"
```

**Examples:**
```bash
GET /api/devices/ESP32_001/raw/         # Returns: 75,98.5,74,0.12,-0.05,9.81
GET /api/devices/ESP32_001/latest/      # Returns: JSON summary
```

---

## **🎯 INDIVIDUAL SENSOR VALUES** ⭐ **RECOMMENDED**

### **Single Values (Plain Text Response)**
```bash
GET /api/ecg/           # ECG heart rate only → "75"
GET /api/spo2/          # SpO2 level only → "98.5"  
GET /api/max30102/      # MAX30102 heart rate → "74"
GET /api/accel/x/       # X-axis accelerometer → "0.12"
GET /api/accel/y/       # Y-axis accelerometer → "-0.05"
GET /api/accel/z/       # Z-axis accelerometer → "9.81"
```

**Perfect for ESP32/Arduino - No JSON parsing needed!**

---

## **📤 DATA UPLOAD**

### **Bulk Sensor Data** ⭐ **PRIMARY ENDPOINT**
```bash
POST /api/sensors/bulk/         # Upload sensor data, get values back
POST /api/sensor-data/bulk/     # Alternative URL (same function)
```

**Request Example:**
```json
{
  "device_id": "ESP32_001",
  "ecg_heart_rate": 75,
  "spo2": 98.5,
  "max30102_heart_rate": 74,
  "x_axis": 0.12,
  "y_axis": -0.05,
  "z_axis": 9.81
}
```

**Response (Plain Text):**
```
75
98.5
74
0.12
-0.05
9.81
```

---

## **📈 SENSOR TYPE ENDPOINTS** (JSON Responses)

### **Historical Data Collections**
```bash
GET  /api/sensors/ecg/              # All ECG readings (JSON array)
POST /api/sensors/ecg/              # Add ECG reading

GET  /api/sensors/pulse-oximeter/   # All pulse ox readings (JSON array)  
POST /api/sensors/pulse-oximeter/   # Add pulse ox reading

GET  /api/sensors/max30102/         # All MAX30102 readings (JSON array)
POST /api/sensors/max30102/         # Add MAX30102 reading

GET  /api/sensors/accelerometer/    # All accelerometer readings (JSON array)
POST /api/sensors/accelerometer/    # Add accelerometer reading

GET  /api/sensors/status/           # All device status readings (JSON array)
POST /api/sensors/status/           # Add status reading
```

---

## **🎯 RECOMMENDED USAGE FOR IoT DEVICES**

### **For ESP32/Arduino Projects:**
```cpp
// 1. Upload data and get values back (most efficient)
POST /api/sensors/bulk/
// Response: plain text values

// 2. Get individual sensor values  
GET /api/spo2/     // Returns "98.5"
GET /api/ecg/      // Returns "75"
```

### **For Web Dashboards:**
```javascript
// Device list
fetch('/api/devices/')
  .then(response => response.text())
  .then(data => console.log(data)); // "ESP32_001\nESP32_002"

// Individual values
fetch('/api/spo2/')
  .then(response => response.text()) 
  .then(spo2 => console.log(spo2)); // "98.5"
```

### **For Mobile Apps:**
```bash
# CSV format for all sensors from one device
curl /api/devices/ESP32_001/raw/
# Returns: "75,98.5,74,0.12,-0.05,9.81"
```

---

## **✅ RESPONSE FORMATS**

| Endpoint Type | Response Format | Example |
|---------------|----------------|---------|
| Individual values | Plain text | `98.5` |
| CSV format | Comma-separated | `75,98.5,74` |
| Bulk upload | Newline-separated | `75\n98.5\n74` |
| Device list | Newline-separated | `ESP32_001\nESP32_002` |
| Historical data | JSON array | `[{...}, {...}]` |

**🎯 For IoT devices, use the individual value endpoints - no JSON parsing required!**
