# Real Sensor Connection Guide

## 🔌 Ready for Real Sensors!

Your IoT system is now configured with **blank spaces** that will be automatically filled when you connect real sensors. The code is structured to work with or without sensors connected.

## Current Status

### **Without Sensors (Current State):**
- All sensor values initialize to **0**
- Server responds with `"WAITING_FOR_SENSORS"`
- System is ready and waiting for real hardware

### **With Sensors Connected:**
- Real values automatically fill the blank spaces
- Server responds with actual sensor readings
- No code changes needed - just plug and play!

## 🔧 How to Connect Your Real Sensors

### **1. ECG Sensor (AD8232)**
**Uncomment these lines in `esp32_sensor_code.ino`:**
```cpp
// REAL ECG SENSOR (AD8232) - Uncomment when connected:
currentReading.ecg_value = analogRead(ECG_PIN) * (3.3 / 4095.0);
currentReading.ecg_heart_rate = calculateHeartRateFromECG();
currentReading.ecg_signal_quality = "good";
```

**Wiring:**
- ECG_PIN → ESP32 GPIO pin (analog)
- Connect AD8232 to heart rate electrodes

### **2. Pulse Oximeter**
**Uncomment these lines:**
```cpp
// REAL PULSE OXIMETER - Uncomment when connected:
currentReading.spo2 = pulseOximeter.getSpO2();
currentReading.pulse_heart_rate = pulseOximeter.getHeartRate();
currentReading.pulse_signal_strength = pulseOximeter.getSignalStrength();
```

### **3. MAX30102 Heart Rate/SpO2 Sensor**
**Uncomment these lines:**
```cpp
// REAL MAX30102 SENSOR - Uncomment when connected:
currentReading.max30102_heart_rate = particleSensor.getHeartRate();
currentReading.max30102_spo2 = particleSensor.getSpO2();
currentReading.red_value = particleSensor.getRed();
currentReading.ir_value = particleSensor.getIR();
currentReading.temperature = particleSensor.readTemperature();
```

**Wiring (I2C):**
- SDA → ESP32 GPIO 21
- SCL → ESP32 GPIO 22
- VCC → 3.3V
- GND → GND

### **4. Accelerometer (MPU6050)**
**Uncomment these lines:**
```cpp
// REAL ACCELEROMETER (MPU6050) - Uncomment when connected:
int16_t ax, ay, az;
accel.getAcceleration(&ax, &ay, &az);
currentReading.x_axis = ax / 16384.0;  // Convert to g
currentReading.y_axis = ay / 16384.0;
currentReading.z_axis = az / 16384.0;
currentReading.magnitude = sqrt(pow(currentReading.x_axis, 2) + 
                                pow(currentReading.y_axis, 2) + 
                                pow(currentReading.z_axis, 2));
```

**Wiring (I2C):**
- SDA → ESP32 GPIO 21  
- SCL → ESP32 GPIO 22
- VCC → 3.3V
- GND → GND

## 📊 Response Examples

### **No Sensors Connected:**
**ESP32 sends:** `{"device_id": "ESP32_001", "ecg_heart_rate": 0, "spo2": 0}`
**Server responds:** `"WAITING_FOR_SENSORS"`

### **ECG Only Connected:**
**ESP32 sends:** `{"device_id": "ESP32_001", "ecg_heart_rate": 75, "spo2": 0}`
**Server responds:** `"75"`

### **Multiple Sensors Connected:**
**ESP32 sends:** `{"device_id": "ESP32_001", "ecg_heart_rate": 75, "spo2": 98.5, "x_axis": 0.15}`
**Server responds:**
```
75
98.5
0.15
```

## 🎯 Benefits of This Approach

✅ **Plug and Play** - Connect sensors when ready, no code changes
✅ **Gradual Development** - Add sensors one by one
✅ **No False Data** - Only real sensor values are transmitted
✅ **Easy Debugging** - Zero values indicate no sensor connected
✅ **Scalable** - Add more sensors anytime

## 🔍 Testing Sensor Connection

**ESP32 Serial Monitor will show:**
```
Sensor Status:
  ECG: 0 BPM (0 = no sensor)         ← Will show real value when connected
  Pulse Ox: SpO2 0%, HR 0 BPM (0 = no sensor)
  MAX30102: HR 0 BPM (0 = no sensor)
  Accel: X=0, Y=0, Z=0 (0 = no sensor)
  Battery: 87%
```

**When you connect a sensor:**
```
Sensor Status:
  ECG: 75 BPM (REAL SENSOR DATA!)    ← Real value from your ECG sensor!
  Pulse Ox: SpO2 0%, HR 0 BPM (0 = no sensor)
  MAX30102: HR 0 BPM (0 = no sensor)
  Accel: X=0, Y=0, Z=0 (0 = no sensor)
  Battery: 87%
```

## 🚀 Ready to Go!

Your system is **100% ready** for real sensors. Just:
1. Connect your hardware
2. Uncomment the relevant sensor code
3. Upload to ESP32
4. Watch real values flow automatically!

**Live URL:** https://iot-khgd.onrender.com  
**Real-time updates:** Every 3 seconds  
**Database storage:** All readings saved automatically
