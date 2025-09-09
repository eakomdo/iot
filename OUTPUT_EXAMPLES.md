# EXACT OUTPUT EXAMPLES

## **📊 What Your Endpoints Return**

### **Example 1: ECG Heart Rate**
```bash
$ curl "https://iot-khgd.onrender.com/api/ecg/"
75
```
**Output:** Just the number `75` (no quotes, no JSON, just the value)  
**HTTP Status:** 200 OK

### **Example 2: SpO2 Level**  
```bash
$ curl "https://iot-khgd.onrender.com/api/spo2/"
98.5
```
**Output:** Just the number `98.5`  
**HTTP Status:** 200 OK

### **Example 3: MAX30102 Heart Rate**
```bash
$ curl "https://iot-khgd.onrender.com/api/max30102/"
74
```
**Output:** Just the number `74`  
**HTTP Status:** 200 OK

### **Example 4: Accelerometer X-Axis**
```bash
$ curl "https://iot-khgd.onrender.com/api/accel/x/"
0.12
```
**Output:** Just the number `0.12`  
**HTTP Status:** 200 OK

### **Example 5: Accelerometer Y-Axis**
```bash
$ curl "https://iot-khgd.onrender.com/api/accel/y/"
-0.05
```
**Output:** Just the number `-0.05`  
**HTTP Status:** 200 OK

### **Example 6: Accelerometer Z-Axis**
```bash
$ curl "https://iot-khgd.onrender.com/api/accel/z/"
9.81
```
**Output:** Just the number `9.81`  
**HTTP Status:** 200 OK

---

## **📤 Upload Example**
```bash
$ curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32","spo2":98.5,"ecg_heart_rate":75}'

75
98.5
```
**Output:** Each value on a new line (no JSON, no brackets)  
**HTTP Status:** 201 Created

---

## **🎯 Perfect for Arduino/ESP32:**
```cpp
// ESP32 code to get just the value
HTTPClient http;
http.begin("https://iot-khgd.onrender.com/api/spo2/");
int httpCode = http.GET();  // Returns 200
String payload = http.getString();  // Returns "98.5"
float spo2 = payload.toFloat();  // Convert to 98.5
```

**No JSON parsing needed!** Just convert the string to number.
