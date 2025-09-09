# SIMPLE IoT ENDPOINTS - JUST THE VALUES

## **✅ These return ONLY the single number + success code 200**

```bash
# ECG Heart Rate - Returns: 75
curl "https://iot-khgd.onrender.com/api/ecg/"

# SpO2 Level - Returns: 98.5  
curl "https://iot-khgd.onrender.com/api/spo2/"

# MAX30102 Heart Rate - Returns: 74
curl "https://iot-khgd.onrender.com/api/max30102/"

# Accelerometer X - Returns: 0.12
curl "https://iot-khgd.onrender.com/api/accel/x/"

# Accelerometer Y - Returns: -0.05
curl "https://iot-khgd.onrender.com/api/accel/y/"

# Accelerometer Z - Returns: 9.81
curl "https://iot-khgd.onrender.com/api/accel/z/"
```

## **📤 Upload sensor data:**
```bash
# Send data and get values back
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32","spo2":98.5,"ecg_heart_rate":75}'
# Returns: 75\n98.5 (values only, no JSON)
```

## **🎯 EXACTLY WHAT YOU ASKED FOR:**
- ✅ Single value only  
- ✅ Success code 200
- ✅ No JSON format
- ✅ Just the reading from each device

**Wait 2-3 minutes for Render deployment, then test!**
