#!/bin/bash

# IoT Device Individual Sensor URLs
BASE_URL="https://iot-khgd.onrender.com/api"

echo "=== INDIVIDUAL DEVICE SENSOR URLs ==="
echo "Base URL: $BASE_URL"
echo ""

echo "1. ECG Sensor:"
echo "   URL: $BASE_URL/ecg/"
echo -n "   Value: "
curl -s "$BASE_URL/ecg/"
echo ""

echo "2. SpO2 (Pulse Oximeter):"
echo "   URL: $BASE_URL/spo2/"
echo -n "   Value: "
curl -s "$BASE_URL/spo2/"
echo ""

echo "3. MAX30102 Heart Rate:"
echo "   URL: $BASE_URL/max30102/"
echo -n "   Value: "
curl -s "$BASE_URL/max30102/"
echo ""

echo "4. Accelerometer X-axis:"
echo "   URL: $BASE_URL/accel/x/"
echo -n "   Value: "
curl -s "$BASE_URL/accel/x/"
echo ""

echo "5. Accelerometer Y-axis:"
echo "   URL: $BASE_URL/accel/y/"
echo -n "   Value: "
curl -s "$BASE_URL/accel/y/"
echo ""

echo "6. Accelerometer Z-axis:"
echo "   URL: $BASE_URL/accel/z/"
echo -n "   Value: "
curl -s "$BASE_URL/accel/z/"
echo ""

echo ""
echo "=== USAGE EXAMPLES ==="
echo "To get ECG reading: curl https://iot-khgd.onrender.com/api/ecg/"
echo "To get SpO2 reading: curl https://iot-khgd.onrender.com/api/spo2/"
echo "To get Heart Rate: curl https://iot-khgd.onrender.com/api/max30102/"
echo "To get Accel X: curl https://iot-khgd.onrender.com/api/accel/x/"
echo "To get Accel Y: curl https://iot-khgd.onrender.com/api/accel/y/"
echo "To get Accel Z: curl https://iot-khgd.onrender.com/api/accel/z/"
echo ""
echo "Each URL returns just the plain sensor value (no JSON, no quotes)"
