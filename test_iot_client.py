import requests

# Your FastAPI IoT sensor server URL (when deployed)
url = 'https://your-iot-sensors.onrender.com/post_sensor_data'

# Simulate IoT device sending sensor data (like your blood values example)
sensor_data = {
    "device_id": "ESP32_HEART_MONITOR",
    "ecg_heart_rate": 75,      # ECG sensor reading
    "spo2": 98,                # Pulse oximeter SpO2 
    "pulse_heart_rate": 74,    # Pulse sensor reading
    "max30102_heart_rate": 76, # MAX30102 heart rate
    "x_axis": 0.12,            # Accelerometer X
    "y_axis": -0.05,           # Accelerometer Y  
    "z_axis": 9.81             # Accelerometer Z
}

# Send sensor data to server
result = requests.post(url, json=sensor_data)

print("Server Response:")
print(result.text)

# Expected response: 
# 75
# 98
# 74
# 76
# 0.12
# -0.05
# 9.81

print("\nRESULT_OK")
