# 🎯 3 MAIN ENDPOINTS TO DISPLAY DEVICE VALUES

## **📊 The 3 Key Endpoints for Device Values**

### **1️⃣ GET INDIVIDUAL SENSOR VALUES** ⭐ **BEST FOR REAL-TIME**
```bash
GET /api/ecg/           # ECG heart rate → "75"
GET /api/spo2/          # SpO2 level → "98.5"
GET /api/max30102/      # MAX30102 heart rate → "74"
GET /api/accel/x/       # X-axis → "0.12"
GET /api/accel/y/       # Y-axis → "-0.05"
GET /api/accel/z/       # Z-axis → "9.81"
```
**Response Format:** Plain text single value  
**Perfect for:** ESP32, Arduino, real-time displays

### **2️⃣ GET ALL VALUES FROM ONE DEVICE** ⭐ **BEST FOR CSV**
```bash
GET /api/devices/{device_id}/raw/
```
**Examples:**
```bash
GET /api/devices/ESP32_001/raw/     # Returns: "75,98.5,74,0.12,-0.05,9.81"
GET /api/devices/HEART_MONITOR/raw/ # Returns: "72,99.1,73,0,0,0"
```
**Response Format:** CSV (comma-separated values)  
**Perfect for:** Data logging, spreadsheets, batch processing

### **3️⃣ UPLOAD DATA & GET VALUES BACK** ⭐ **BEST FOR IoT DEVICES**
```bash
POST /api/sensors/bulk/
```
**Request:**
```json
{
  "device_id": "ESP32_001",
  "ecg_heart_rate": 75,
  "spo2": 98.5,
  "x_axis": 0.12
}
```
**Response:**
```
75
98.5
0.12
```
**Response Format:** Newline-separated values  
**Perfect for:** ESP32 sending data and getting confirmation

---

## **🔥 USAGE EXAMPLES**

### **Real-Time Dashboard:**
```javascript
// Get latest ECG value
fetch('/api/ecg/')
  .then(response => response.text())
  .then(ecg => document.getElementById('ecg').innerText = ecg + ' BPM');

// Get all values from device
fetch('/api/devices/ESP32_001/raw/')
  .then(response => response.text())
  .then(data => {
    const [ecg, spo2, max30102, x, y, z] = data.split(',');
    updateDisplay(ecg, spo2, max30102, x, y, z);
  });
```

### **ESP32 Code:**
```cpp
// Method 1: Get individual value
http.begin("https://iot-khgd.onrender.com/api/spo2/");
String spo2 = http.getString();  // Gets "98.5"

// Method 2: Get all device values
http.begin("https://iot-khgd.onrender.com/api/devices/ESP32_001/raw/");
String allValues = http.getString();  // Gets "75,98.5,74,0.12,-0.05,9.81"

// Method 3: Send data, get values back
http.POST("{\"device_id\":\"ESP32_001\",\"spo2\":98.5}");
String response = http.getString();  // Gets "98.5"
```

### **Python Data Analysis:**
```python
import requests

# Get all device values as CSV
response = requests.get('https://iot-khgd.onrender.com/api/devices/ESP32_001/raw/')
ecg, spo2, max30102, x, y, z = response.text.split(',')
print(f"Heart Rate: {ecg}, SpO2: {spo2}%")
```

---

## **🎯 RECOMMENDATION**

**For displaying device values, use:**

1. **Individual endpoints** (`/api/spo2/`, `/api/ecg/`) for **real-time single values**
2. **Device raw endpoint** (`/api/devices/{id}/raw/`) for **all values from one device**  
3. **Bulk upload** (`POST /api/sensors/bulk/`) for **IoT devices sending & receiving data**

**All 3 return plain text - no JSON parsing needed!**
