# WORKING SOLUTION RIGHT NOW

## **✅ CORRECT WAY TO GET SINGLE VALUES**

### **❌ WRONG (what you tried):**
```bash
# This gives: {"detail":"Method \"GET\" not allowed."}
curl "https://iot-khgd.onrender.com/api/sensors/bulk/"
```

### **✅ CORRECT (what works):**
```bash
# POST sensor data and get ONLY the values back
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_001","spo2":98.5}'

# Output: 98.5 (just the value)
```

### **✅ MORE EXAMPLES:**
```bash
# Send ECG data, get ECG value back
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_001","ecg_heart_rate":75}'
# Output: 75

# Send multiple values, get all back
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_001","spo2":98.5,"ecg_heart_rate":75,"x_axis":0.12}'
# Output: 
# 75
# 98.5  
# 0.12
```

## **🎯 For Your ESP32:**
```cpp
// Send data via POST and get values back
HTTPClient http;
http.begin("https://iot-khgd.onrender.com/api/sensors/bulk/");
http.addHeader("Content-Type", "application/json");

String postData = "{\"device_id\":\"ESP32_001\",\"spo2\":98.5}";
int httpCode = http.POST(postData);
String response = http.getString();  // Gets "98.5"

float value = response.toFloat();  // Convert to number
```

## **📊 What You Get:**
- ✅ **Just the number** (no JSON)
- ✅ **HTTP 201 status** (success)
- ✅ **Plain text response**
- ✅ **Works right now!**

**The bulk POST endpoint returns only the sensor values - exactly what you want!**
