# FastAPI IoT Sensor Deployment Guide

## 🚀 Deploy to Render (Skip Local Setup)

Since you don't have Python locally, let's deploy directly to Render:

### **Option 1: Deploy FastAPI Version to Render**

1. **Commit the FastAPI files:**
```bash
git add .
git commit -m "Add FastAPI IoT sensor server"
git push origin master
```

2. **Create new Render service:**
- Go to https://render.com/dashboard
- Click "New +" → "Web Service"  
- Connect your GitHub repo: `eakomdo/iot`
- Use these settings:
  - **Build Command:** `pip install -r fastapi_requirements.txt`
  - **Start Command:** `python fastapi_iot_server.py`
  - **Environment:** Python 3

### **Option 2: Use Your Existing Django Server**

Your existing Django server at https://iot-khgd.onrender.com is already working!

**Test it right now:**
```bash
# Test current Django server (should work)
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
-H "Content-Type: application/json" \
-d '{
  "device_id": "TEST_DEVICE",
  "ecg_heart_rate": 75,
  "spo2": 98,
  "pulse_heart_rate": 74
}'
```

**Expected response (raw values):**
```
75
98
74
```

## 🎯 Recommended Approach

**Use your existing Django server** - it's already deployed and working perfectly!

### **Test Your Current Server:**
```bash
# 1. Send sensor data
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
-H "Content-Type: application/json" \
-d '{"device_id": "MY_IOT", "ecg_heart_rate": 71, "spo2": 98}'

# 2. Get device list  
curl "https://iot-khgd.onrender.com/api/devices/"

# 3. Get raw values
curl "https://iot-khgd.onrender.com/api/devices/MY_IOT/raw/"
```

## 📱 Use ESP32 with Your Current Server

Update your ESP32 code to use the working Django server:

```cpp
// Use your existing Django server
const char* apiEndpoint = "https://iot-khgd.onrender.com/api/sensors/bulk/";

// Send data (same format as FastAPI)
// Server will respond with raw values like: "71\n98\n74"
```

## ✅ Your Options:

1. **Keep Django** (Recommended) - Already working at https://iot-khgd.onrender.com
2. **Deploy FastAPI** - Create new Render service with FastAPI version  
3. **Run Both** - Have Django for database + FastAPI for simple responses

**Your Django server is already perfect for IoT sensors!** 🎯
