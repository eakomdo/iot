# Individual Device Sensor URLs

Your IoT system now has separate URLs for each device/sensor. Here are all the individual endpoints:

## Base URL
```
https://iot-khgd.onrender.com/api
```

## Individual Device Endpoints

### 1. ECG Sensor
**URL:** `https://iot-khgd.onrender.com/api/ecg/`
- Returns: Plain text ECG reading value
- Example: `75` (heart rate in BPM)

### 2. SpO2 (Pulse Oximeter)
**URL:** `https://iot-khgd.onrender.com/api/spo2/`
- Returns: Plain text SpO2 percentage value
- Example: `98.5` (oxygen saturation percentage)

### 3. MAX30102 Heart Rate Sensor
**URL:** `https://iot-khgd.onrender.com/api/max30102/`
- Returns: Plain text heart rate value
- Example: `0.12` (heart rate reading)

### 4. Accelerometer X-axis
**URL:** `https://iot-khgd.onrender.com/api/accel/x/`
- Returns: Plain text X-axis acceleration value
- Example: `0` (acceleration in m/s²)

### 5. Accelerometer Y-axis
**URL:** `https://iot-khgd.onrender.com/api/accel/y/`
- Returns: Plain text Y-axis acceleration value
- Example: `0` (acceleration in m/s²)

### 6. Accelerometer Z-axis
**URL:** `https://iot-khgd.onrender.com/api/accel/z/`
- Returns: Plain text Z-axis acceleration value
- Example: `0` (acceleration in m/s²)

## Usage Examples

### Command Line (curl)
```bash
# Get ECG reading
curl https://iot-khgd.onrender.com/api/ecg/

# Get SpO2 reading
curl https://iot-khgd.onrender.com/api/spo2/

# Get heart rate
curl https://iot-khgd.onrender.com/api/max30102/

# Get accelerometer readings
curl https://iot-khgd.onrender.com/api/accel/x/
curl https://iot-khgd.onrender.com/api/accel/y/
curl https://iot-khgd.onrender.com/api/accel/z/
```

### JavaScript (Fetch API)
```javascript
// Get ECG reading
const ecgResponse = await fetch('https://iot-khgd.onrender.com/api/ecg/');
const ecgValue = await ecgResponse.text(); // "75"

// Get SpO2 reading
const spo2Response = await fetch('https://iot-khgd.onrender.com/api/spo2/');
const spo2Value = await spo2Response.text(); // "98.5"

// Get all accelerometer readings
const accelX = await fetch('https://iot-khgd.onrender.com/api/accel/x/').then(r => r.text());
const accelY = await fetch('https://iot-khgd.onrender.com/api/accel/y/').then(r => r.text());
const accelZ = await fetch('https://iot-khgd.onrender.com/api/accel/z/').then(r => r.text());
```

### Python (requests)
```python
import requests

# Get individual sensor readings
ecg = requests.get('https://iot-khgd.onrender.com/api/ecg/').text
spo2 = requests.get('https://iot-khgd.onrender.com/api/spo2/').text
heart_rate = requests.get('https://iot-khgd.onrender.com/api/max30102/').text
accel_x = requests.get('https://iot-khgd.onrender.com/api/accel/x/').text
accel_y = requests.get('https://iot-khgd.onrender.com/api/accel/y/').text
accel_z = requests.get('https://iot-khgd.onrender.com/api/accel/z/').text
```

## Response Format
- **Content Type:** `text/plain`
- **Format:** Raw sensor value only (no JSON, no quotes, no extra formatting)
- **HTTP Status:** 200 OK for successful readings
- **Real-time:** Values are updated every 0.5 seconds from the IoT device

## Notes
- All endpoints return plain text values only
- No JSON formatting or extra data
- Perfect for direct integration with displays, charts, or other systems
- Values are real-time from your ESP32 IoT device
- Currently returns simulated values (0 for accelerometer, 75 for ECG, 98.5 for SpO2) until real sensors are connected
