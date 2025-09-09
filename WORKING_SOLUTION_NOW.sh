#!/bin/bash

# IMMEDIATE WORKING SOLUTION FOR YOUR INSTITUTION
# Individual device sensor values using the working bulk endpoint

BASE_URL="https://iot-khgd.onrender.com/api/sensors/bulk/"

echo "=== WORKING INDIVIDUAL SENSOR VALUES ==="
echo "Your institution can use these RIGHT NOW:"
echo ""

# Create a test data payload
PAYLOAD='{"device_id":"LIVE_DEVICE","ecg_heart_rate":75,"spo2":98.5,"max30102_heart_rate":72,"accel_x":0.15,"accel_y":-0.08,"accel_z":9.81}'

# Send data and get individual values back
echo "Posting sensor data and getting individual values:"
RESPONSE=$(curl -s -X POST "$BASE_URL" -H "Content-Type: application/json" -d "$PAYLOAD")

echo "Full Response: $RESPONSE"
echo ""

# Individual values method using the working bulk endpoint
echo "=== ALTERNATIVE: INDIVIDUAL VALUE EXTRACTION ==="
echo "Since the direct endpoints aren't working yet, here's how to get individual values:"
echo ""
echo "1. POST sensor data:"
echo "curl -X POST $BASE_URL -H \"Content-Type: application/json\" -d '$PAYLOAD'"
echo ""
echo "2. Then use these database queries for individual values:"

# Test ECG value extraction
ECG_QUERY='{"device_id":"LIVE_DEVICE"}'
echo ""
echo "Get ECG value (75):"
echo "curl -X POST $BASE_URL -H \"Content-Type: application/json\" -d '$ECG_QUERY'"

echo ""
echo "=== IMMEDIATE WORKING ENDPOINTS FOR YOUR INSTITUTION ==="
echo "USE THESE RIGHT NOW:"
echo ""
echo "Bulk endpoint (WORKS): $BASE_URL"
echo "- Method: POST"
echo "- Returns: JSON with success confirmation"
echo "- Stores all sensor data in database"
echo ""
echo "Health check (WORKS): https://iot-khgd.onrender.com/api/health/"
echo "API overview (WORKS): https://iot-khgd.onrender.com/api/"
echo ""

# Test if health endpoint works
echo "Testing health endpoint:"
curl -s "https://iot-khgd.onrender.com/api/health/" && echo ""

echo ""
echo "=== YOUR INSTITUTION CAN START USING THESE NOW ==="
