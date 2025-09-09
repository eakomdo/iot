# 📤 3 ENDPOINTS THAT SEND VALUES TO THE SERVER

## **🎯 The 3 Main Upload Endpoints (Display Values ON Server)**

### **1️⃣ BULK SENSOR DATA UPLOAD** ⭐ **PRIMARY ENDPOINT**
```bash
POST /api/sensors/bulk/
```
**Purpose:** Send multiple sensor values to server in one request  
**Request:**
```json
{
  "device_id": "ESP32_001",
  "ecg_heart_rate": 75,
  "spo2": 98.5,
  "max30102_heart_rate": 74,
  "x_axis": 0.12,
  "y_axis": -0.05,
  "z_axis": 9.81,
  "battery_level": 85,
  "wifi_signal_strength": -45
}
```
**Server Response:**
```
75
98.5
74
0.12
-0.05
9.81
```
**What it does:** Stores ALL sensor values on server, returns the values for confirmation

---

### **2️⃣ ALTERNATIVE BULK UPLOAD** 
```bash
POST /api/sensor-data/bulk/
```
**Purpose:** Same as above, alternative URL for compatibility  
**Request:** Same JSON format as endpoint #1  
**Server Response:** Same plain text values  
**What it does:** Identical to `/api/sensors/bulk/` - just different URL path

---

### **3️⃣ INDIVIDUAL SENSOR UPLOADS** (5 separate endpoints)
```bash
POST /api/sensors/ecg/              # Upload ECG readings
POST /api/sensors/pulse-oximeter/   # Upload pulse oximeter readings  
POST /api/sensors/max30102/         # Upload MAX30102 readings
POST /api/sensors/accelerometer/    # Upload accelerometer readings
POST /api/sensors/status/           # Upload device status
```

**Example - ECG Upload:**
```json
{
  "device": 1,
  "heart_rate": 75,
  "ecg_value": 123.45,
  "signal_quality": "good"
}
```
**Server Response:** JSON confirmation  
**What it does:** Stores specific sensor type data on server

---

## **🚀 ESP32 CODE EXAMPLES**

### **Method 1: Bulk Upload (Recommended)**
```cpp
void sendAllSensors() {
  HTTPClient http;
  http.begin("https://iot-khgd.onrender.com/api/sensors/bulk/");
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{";
  payload += "\"device_id\":\"ESP32_001\",";
  payload += "\"ecg_heart_rate\":" + String(ecgValue) + ",";
  payload += "\"spo2\":" + String(spo2Value) + ",";
  payload += "\"x_axis\":" + String(accelX);
  payload += "}";
  
  int httpCode = http.POST(payload);
  String response = http.getString();  // Gets sensor values back
  Serial.println("Server confirmed: " + response);
}
```

### **Method 2: Individual Sensor Upload**
```cpp
void sendECGOnly() {
  HTTPClient http;
  http.begin("https://iot-khgd.onrender.com/api/sensors/ecg/");
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{";
  payload += "\"device\":1,";
  payload += "\"heart_rate\":" + String(ecgValue) + ",";
  payload += "\"ecg_value\":" + String(rawECG);
  payload += "}";
  
  int httpCode = http.POST(payload);
  String response = http.getString();  // Gets JSON response
}
```

---

## **📊 SERVER STORAGE RESULT**

When you use these endpoints, the server will:

### **✅ Store in Database:**
- Device registration (ESP32_001, HEART_MONITOR, etc.)
- ECG readings with timestamps
- Pulse oximeter readings with timestamps  
- MAX30102 readings with timestamps
- Accelerometer readings with timestamps
- Device status with timestamps

### **✅ Make Available via GET:**
```bash
# After uploading, you can retrieve with:
GET /api/ecg/                    # Latest ECG value
GET /api/spo2/                   # Latest SpO2 value  
GET /api/devices/ESP32_001/raw/  # All latest values from ESP32_001
```

---

## **🎯 RECOMMENDATION**

**Use Endpoint #1 (`POST /api/sensors/bulk/`) because:**
- ✅ Sends all sensor values in one request (efficient)
- ✅ Server stores everything with timestamps
- ✅ Returns plain text values for confirmation
- ✅ Perfect for ESP32/Arduino
- ✅ No JSON parsing needed for response

**These 3 endpoints receive your IoT data and display/store it ON the server!**
