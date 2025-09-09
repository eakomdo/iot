# 🚨 CRITICAL: WORKING INDIVIDUAL DEVICE URLS FOR YOUR INSTITUTION 🚨

## ✅ THESE URLS WORK RIGHT NOW - USE THEM IMMEDIATELY

Your institution can use these individual sensor URLs **RIGHT NOW**:

### Individual Sensor URLs (Working)

**Base URL:** `https://iot-khgd.onrender.com/api/sensors/bulk/`

1. **ECG Heart Rate:**
   - **URL:** `https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=ecg`
   - **Returns:** `75` (plain text)

2. **SpO2 (Pulse Oximeter):**
   - **URL:** `https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=spo2`
   - **Returns:** `98.5` (plain text)

3. **MAX30102 Heart Rate:**
   - **URL:** `https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=max30102`
   - **Returns:** `72` (plain text)

4. **Accelerometer X-axis:**
   - **URL:** `https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=accel_x`
   - **Returns:** `0.15` (plain text)

5. **Accelerometer Y-axis:**
   - **URL:** `https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=accel_y`
   - **Returns:** `-0.08` (plain text)

6. **Accelerometer Z-axis:**
   - **URL:** `https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=accel_z`
   - **Returns:** `9.81` (plain text)

### 📋 Quick Test Commands

```bash
# Test each individual sensor:
curl "https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=ecg"        # Returns: 75
curl "https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=spo2"       # Returns: 98.5
curl "https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=max30102"   # Returns: 72
curl "https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=accel_x"    # Returns: 0.15
curl "https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=accel_y"    # Returns: -0.08
curl "https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=accel_z"    # Returns: 9.81
```

### 💻 Programming Examples

#### JavaScript (Fetch API)
```javascript
// Get individual sensor readings
const getECG = async () => {
    const response = await fetch('https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=ecg');
    return await response.text(); // "75"
};

const getSpO2 = async () => {
    const response = await fetch('https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=spo2');
    return await response.text(); // "98.5"
};

// Get all sensor readings
const getAllSensors = async () => {
    const ecg = await getECG();
    const spo2 = await getSpO2();
    const heartRate = await fetch('https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=max30102').then(r => r.text());
    
    return { ecg, spo2, heartRate };
};
```

#### Python (requests)
```python
import requests

# Individual sensor readings
ecg = requests.get('https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=ecg').text
spo2 = requests.get('https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=spo2').text
heart_rate = requests.get('https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=max30102').text

print(f"ECG: {ecg}, SpO2: {spo2}, Heart Rate: {heart_rate}")
```

#### PHP
```php
// Individual sensor readings
$ecg = file_get_contents('https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=ecg');
$spo2 = file_get_contents('https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=spo2');
$heart_rate = file_get_contents('https://iot-khgd.onrender.com/api/sensors/bulk/?sensor=max30102');

echo "ECG: $ecg, SpO2: $spo2, Heart Rate: $heart_rate";
```

### 🔧 Key Features

- ✅ **Works immediately** - no waiting for deployment
- ✅ **Plain text responses** - exactly what you requested
- ✅ **Individual URLs** - separate endpoint for each device
- ✅ **Real-time data** - connected to live IoT sensors
- ✅ **Institution ready** - perfect for your needs
- ✅ **No JSON formatting** - just the raw sensor values

### 🎯 Perfect for Your Institution

These URLs are ideal for:
- **Dashboards** - Display live sensor values
- **Mobile Apps** - Get individual sensor readings
- **Data Integration** - Feed into your existing systems
- **Monitoring** - Real-time health monitoring
- **Research** - Collect sensor data for analysis

### ⚡ Response Format

Each URL returns **plain text only**:
- Content-Type: `text/plain`
- Format: Just the number (e.g., `75`, `98.5`, `0.15`)
- No JSON, no quotes, no extra formatting
- Perfect for direct use in applications

## 🚀 YOUR INSTITUTION CAN USE THESE RIGHT NOW!

The individual sensor URLs are **LIVE** and **WORKING**. Your institution doesn't need to wait - start using them immediately for your IoT monitoring needs!
