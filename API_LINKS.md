# 🌐 YOUR COMPLETE API LINK INFORMATION

## **🔗 Base API URL**
```
https://iot-khgd.onrender.com
```

## **🎯 3 MAIN ENDPOINTS FOR YOUR IoT SYSTEM**

### **1️⃣ UPLOAD SENSOR DATA**
```
https://iot-khgd.onrender.com/api/sensors/bulk/
```
**Method:** POST  
**Purpose:** Send sensor data to server  
**Response:** Plain text values

### **2️⃣ GET INDIVIDUAL SENSOR VALUES**
```
https://iot-khgd.onrender.com/api/ecg/           # ECG heart rate
https://iot-khgd.onrender.com/api/spo2/          # SpO2 level
https://iot-khgd.onrender.com/api/max30102/      # MAX30102 heart rate
https://iot-khgd.onrender.com/api/accel/x/       # X-axis accelerometer
https://iot-khgd.onrender.com/api/accel/y/       # Y-axis accelerometer
https://iot-khgd.onrender.com/api/accel/z/       # Z-axis accelerometer
```
**Method:** GET  
**Purpose:** Get latest sensor values  
**Response:** Single plain text value

### **3️⃣ GET ALL DEVICE VALUES**
```
https://iot-khgd.onrender.com/api/devices/{device_id}/raw/
```
**Examples:**
```
https://iot-khgd.onrender.com/api/devices/ESP32_001/raw/
https://iot-khgd.onrender.com/api/devices/HEART_MONITOR/raw/
```
**Method:** GET  
**Purpose:** Get all sensor values from one device  
**Response:** CSV format (75,98.5,74,0.12,-0.05,9.81)

---

## **🚀 QUICK TEST LINKS**

### **Health Check:**
```
https://iot-khgd.onrender.com/api/health/
```

### **Device List:**
```
https://iot-khgd.onrender.com/api/devices/
```

### **API Overview:**
```
https://iot-khgd.onrender.com/api/
```

---

## **📱 FOR ESP32/ARDUINO:**

### **Upload Data:**
```cpp
// POST to this URL:
"https://iot-khgd.onrender.com/api/sensors/bulk/"

// With JSON data:
{"device_id":"ESP32_001","spo2":98.5,"ecg_heart_rate":75}

// Get back plain text:
// 75
// 98.5
```

### **Get Values:**
```cpp
// GET from these URLs:
"https://iot-khgd.onrender.com/api/spo2/"      // Returns "98.5"
"https://iot-khgd.onrender.com/api/ecg/"       // Returns "75"
```

---

## **🌍 COMPLETE API BASE**
**Your IoT API is live at:**
```
🔗 https://iot-khgd.onrender.com
```

**All endpoints start with this base URL!**
