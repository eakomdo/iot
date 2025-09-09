#!/bin/bash

echo "=== DEPLOYMENT TEST ==="
echo "1. Testing new live endpoint:"
curl -s "https://iot-khgd.onrender.com/api/live/" || echo "NOT DEPLOYED YET"

echo -e "\n2. Testing individual sensor endpoint:"  
curl -s "https://iot-khgd.onrender.com/api/spo2/" || echo "NOT DEPLOYED YET"

echo -e "\n3. Sending test data:"
curl -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"DEPLOYMENT_TEST","spo2":99.9}' \
  -s || echo "UPLOAD FAILED"

echo -e "\n4. Testing problematic API root:"
curl -s "https://iot-khgd.onrender.com/api/" | head -c 100
echo "..."

echo -e "\n=== DIAGNOSIS ==="
if curl -s "https://iot-khgd.onrender.com/api/live/" | grep -q "LIVE IOT STATUS"; then
    echo "✅ New deployment IS working"
    echo "❌ Old JSON response might be cached"
else
    echo "❌ New deployment NOT working yet"
    echo "⏳ Still deploying or cache issue"
fi
