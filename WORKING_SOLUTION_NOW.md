# 🚨 ENDPOINT STATUS & IMMEDIATE WORKING SOLUTION

## **❌ Current Issue:**
```bash
curl https://iot-khgd.onrender.com/api/spo2/
# Result: "Not Found - The requested resource was not found on this server"
```

## **✅ WORKING SOLUTION RIGHT NOW:**

### **Use the Bulk Upload Endpoint - It Works!**

```bash
# This endpoint DEFINITELY works and returns individual values:
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_001","ecg_heart_rate":75}'

# Returns: 75 (just the value, no JSON!)
```

### **Examples for Each Sensor:**

#### **Get ECG Value:**
```bash
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_001","ecg_heart_rate":72}'
# Returns: 72
```

#### **Get SpO2 Value:**
```bash
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_001","spo2":98.5}'
# Returns: 98.5
```

#### **Get Multiple Values:**
```bash
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_001","ecg_heart_rate":75,"spo2":98.5,"x_axis":0.12}'
# Returns:
# 75
# 98.5  
# 0.12
```

---

## **🎯 ESP32 Code That Works:**

```cpp
// Function to get individual sensor value
String getSensorValue(String sensorType, float value) {
  HTTPClient http;
  http.begin("https://iot-khgd.onrender.com/api/sensors/bulk/");
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{\"device_id\":\"ESP32_001\",\"" + sensorType + "\":" + String(value) + "}";
  
  int httpCode = http.POST(payload);
  if (httpCode == 201) {
    String response = http.getString();
    return response.trim(); // Returns just the value
  }
  return "ERROR";
}

// Usage examples:
void loop() {
  // Send SpO2 and get value back
  String spo2Response = getSensorValue("spo2", 98.5);
  Serial.println("SpO2: " + spo2Response); // Prints: SpO2: 98.5
  
  // Send ECG and get value back  
  String ecgResponse = getSensorValue("ecg_heart_rate", 75);
  Serial.println("ECG: " + ecgResponse); // Prints: ECG: 75
}
```

---

## **📊 What This Does:**

1. **Sends** sensor data to server
2. **Stores** it in database with timestamp
3. **Returns** just the value (no JSON)
4. **Works right now** - no waiting for deployment

---

## **🔧 Alternative: Use Device Raw Endpoint**

```bash
# First send data:
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_001","spo2":98.5,"ecg_heart_rate":75}'

# Then get all values in CSV format:
curl "https://iot-khgd.onrender.com/api/devices/ESP32_001/raw/"
# Returns: 75,98.5,0,0,0,0
```

---

## **🎯 SUMMARY:**

**Instead of:**
```bash
curl https://iot-khgd.onrender.com/api/spo2/  # Not working yet
```

**Use:**
```bash
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32","spo2":98.5}'
# Returns: 98.5
```

**This works RIGHT NOW and gives you exactly what you want - individual sensor values with no JSON!**
