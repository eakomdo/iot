# 🚀 DEPLOYMENT GUIDE FOR RENDER

## Your IoT sensor system is ready for deployment! Here's how to deploy it:

### 1. PREPARE FOR DEPLOYMENT

Your project structure is complete:
```
iot/
├── iot_backend/          # Django project
├── sensors/              # Sensor app with models & API
├── esp32_sensor_code.ino # ESP32 code
├── render.yaml           # Render config
├── build.sh             # Render build script
├── requirements.txt      # Python dependencies
├── README.md            # Complete documentation
└── test_api.py          # API testing script
```

### 2. DEPLOY TO RENDER

#### Option A: Using GitHub + Render (Recommended)

1. **Push to GitHub:**
   ```bash
   cd /home/eakomdo/Desktop/iot
   git init
   git add .
   git commit -m "Initial IoT sensor API"
   # Create repo on GitHub and push
   git remote add origin https://github.com/YOUR_USERNAME/iot-sensor-api.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://dashboard.render.com
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically use `render.yaml`

#### Option B: Direct Render Deployment

1. **Create PostgreSQL Database:**
   - New → PostgreSQL
   - Name: `iot-database`
   - Save the connection URL

2. **Create Web Service:**
   - New → Web Service
   - Upload your code or connect GitHub
   - Settings:
     - Build Command: `./build.sh`
     - Start Command: `gunicorn iot_backend.wsgi:application`
     - Environment Variables:
       - `DATABASE_URL`: [Your PostgreSQL URL]
       - `SECRET_KEY`: [Generate secure key]
       - `DEBUG`: `false`

### 3. AFTER DEPLOYMENT

1. **Get Your API URL:**
   Your API will be at: `https://your-app-name.onrender.com/api/`

2. **Update ESP32 Code:**
   Replace in `esp32_sensor_code.ino`:
   ```cpp
   const char* apiEndpoint = "https://your-app-name.onrender.com/api/sensors/bulk/";
   ```

3. **Test the Deployed API:**
   ```bash
   curl -X POST https://your-app-name.onrender.com/api/sensors/bulk/ \
     -H "Content-Type: application/json" \
     -d '{
       "device_id": "TEST_001",
       "ecg_heart_rate": 75.0,
       "spo2": 98.5
     }'
   ```

### 4. ESP32 SETUP

1. **Install Arduino Libraries:**
   - ArduinoJson
   - WiFi (built-in)
   - HTTPClient (built-in)

2. **Configure ESP32:**
   - Update WiFi credentials
   - Update API endpoint URL
   - Upload to ESP32

3. **Hardware Connections:**
   - Connect your sensors (ECG, MAX30102, Accelerometer, etc.)
   - Power up ESP32
   - Monitor serial output for data transmission

### 5. MONITORING

- **Admin Interface:** `https://your-app.onrender.com/admin/`
- **API Overview:** `https://your-app.onrender.com/api/`
- **Device Readings:** `https://your-app.onrender.com/api/devices/{device_id}/readings/`

## 🔧 LOCAL TESTING (before deployment)

The test script works locally:
```bash
# Start local server
python3 manage.py runserver

# Run tests (in another terminal)
python3 test_api.py
```

## ✅ YOUR SYSTEM IS READY!

You now have:
- ✅ Complete Django REST API
- ✅ ESP32 code for data collection
- ✅ Render deployment configuration  
- ✅ Comprehensive documentation
- ✅ Testing scripts

**Ready to deploy to Render!**
