#!/bin/bash

echo "=== WRONG ENDPOINT (gives JSON docs) ==="
curl -s "https://iot-khgd.onrender.com/" | python3 -m json.tool | head -10

echo -e "\n=== CORRECT ENDPOINT 1: Device List ==="
curl -s "https://iot-khgd.onrender.com/api/devices/"

echo -e "\n=== CORRECT ENDPOINT 2: Raw Sensor Values ==="
curl -s "https://iot-khgd.onrender.com/api/devices/ESP32_001/raw/"

echo -e "\n=== CORRECT ENDPOINT 3: Individual Sensor Values ==="
echo "ECG Heart Rate:"
curl -s "https://iot-khgd.onrender.com/api/sensors/ecg/"
echo -e "\nSpO2:"
curl -s "https://iot-khgd.onrender.com/api/sensors/pulse-oximeter/"
echo -e "\nMAX30102:"
curl -s "https://iot-khgd.onrender.com/api/sensors/max30102/"
