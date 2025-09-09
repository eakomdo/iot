#!/bin/bash

# Quick test of working endpoints to get individual values
echo "=== CURRENT WORKING SOLUTION ==="

echo "1. Latest sensor data (should be CSV format):"
curl -s "https://iot-khgd.onrender.com/api/devices/QUICK_TEST/raw/"

echo -e "\n2. Wake up service with bulk endpoint:"
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"SINGLE_VALUE_TEST","spo2":99.5}' 2>/dev/null

echo -e "\n3. Get the single value we just posted:"
curl -s "https://iot-khgd.onrender.com/api/devices/SINGLE_VALUE_TEST/raw/"

echo -e "\n=== WORKING URLS FOR SINGLE VALUES ==="
echo "URL 1: https://iot-khgd.onrender.com/api/devices/{device_id}/raw/"
echo "URL 2: POST to https://iot-khgd.onrender.com/api/sensors/bulk/ returns the values"
echo "URL 3: GET https://iot-khgd.onrender.com/api/devices/ for device list"
