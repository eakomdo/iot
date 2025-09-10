#!/bin/bash
# ESP32 IoT API Test Script

echo "🧪 Testing ESP32 IoT API Endpoints"
echo "=================================="

# Test POST endpoint
echo "📤 Testing POST endpoint..."
response=$(curl -s -X POST "https://iot-khgd.onrender.com/api/post_sensor_data/" \
    -H "Content-Type: application/json" \
    -d '{"device_id":"ESP32_TEST_SCRIPT","ecg_heart_rate":78,"spo2":97,"max30102_heart_rate":76,"x_axis":0.2,"y_axis":-0.1,"z_axis":9.9}')

echo "POST Response: $response"

# Wait a moment for data to be saved
sleep 2

echo -e "\n📊 Testing individual endpoints..."

# Test GET endpoints
ecg=$(curl -s "https://iot-khgd.onrender.com/api/ecg/")
spo2=$(curl -s "https://iot-khgd.onrender.com/api/spo2/")
max30102=$(curl -s "https://iot-khgd.onrender.com/api/max30102/")
accel_x=$(curl -s "https://iot-khgd.onrender.com/api/accel/x/")
accel_y=$(curl -s "https://iot-khgd.onrender.com/api/accel/y/")
accel_z=$(curl -s "https://iot-khgd.onrender.com/api/accel/z/")

echo "ECG Heart Rate: $ecg BPM"
echo "SpO2: $spo2%"
echo "MAX30102 HR: $max30102 BPM"
echo "Accelerometer: X=$accel_x, Y=$accel_y, Z=$accel_z"

echo -e "\n✅ Test completed!"
echo "If the values above are different from 75, 98.5, 72 then real data is working!"
