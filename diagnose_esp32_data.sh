#!/bin/bash

echo "=== ESP32 IoT DIAGNOSTIC SCRIPT ==="
echo "Checking why your device shows mock values instead of real data"
echo ""

echo "1. TESTING API ENDPOINTS WITH DEBUG INFO:"
echo "=========================================="

echo "ECG Debug Info:"
curl -s "https://iot-khgd.onrender.com/api/ecg/?debug=1" 2>/dev/null || echo "API not responding"
echo ""

echo "SpO2 Debug Info:"
curl -s "https://iot-khgd.onrender.com/api/spo2/?debug=1" 2>/dev/null || echo "API not responding"
echo ""

echo "MAX30102 Debug Info:"
curl -s "https://iot-khgd.onrender.com/api/max30102/?debug=1" 2>/dev/null || echo "API not responding"
echo ""

echo "2. TESTING CURRENT VALUES:"
echo "=========================="
echo "ECG Value: $(curl -s https://iot-khgd.onrender.com/api/ecg/ 2>/dev/null || echo 'FAILED')"
echo "SpO2 Value: $(curl -s https://iot-khgd.onrender.com/api/spo2/ 2>/dev/null || echo 'FAILED')"
echo "MAX30102 Value: $(curl -s https://iot-khgd.onrender.com/api/max30102/ 2>/dev/null || echo 'FAILED')"
echo ""

echo "3. TESTING ESP32 DATA SUBMISSION:"
echo "================================="
echo "Manually sending test data to see if API accepts it..."
RESPONSE=$(curl -s -X POST "https://iot-khgd.onrender.com/api/sensors/bulk/" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_001","ecg_heart_rate":85,"spo2":97,"max30102_heart_rate":80}' \
  -w "HTTP_CODE:%{http_code}" 2>/dev/null)

echo "API Response: $RESPONSE"
echo ""

echo "4. CHECKING VALUES AFTER MANUAL DATA:"
echo "====================================="
echo "Waiting 5 seconds for database update..."
sleep 5

echo "ECG Value: $(curl -s https://iot-khgd.onrender.com/api/ecg/ 2>/dev/null || echo 'FAILED')"
echo "SpO2 Value: $(curl -s https://iot-khgd.onrender.com/api/spo2/ 2>/dev/null || echo 'FAILED')"
echo "MAX30102 Value: $(curl -s https://iot-khgd.onrender.com/api/max30102/ 2>/dev/null || echo 'FAILED')"
echo ""

echo "=== DIAGNOSIS RESULTS ==="
echo ""

# Check if values changed
ECG_VAL=$(curl -s https://iot-khgd.onrender.com/api/ecg/ 2>/dev/null)
SPO2_VAL=$(curl -s https://iot-khgd.onrender.com/api/spo2/ 2>/dev/null)
MAX_VAL=$(curl -s https://iot-khgd.onrender.com/api/max30102/ 2>/dev/null)

if [ "$ECG_VAL" == "85" ] && [ "$SPO2_VAL" == "97" ] && [ "$MAX_VAL" == "80" ]; then
    echo "✅ SUCCESS: API is working! Your ESP32 just needs to send data correctly."
    echo ""
    echo "SOLUTION: Check your ESP32 Serial Monitor for:"
    echo "- WiFi connection status"
    echo "- HTTP POST responses"  
    echo "- Any error messages"
    echo ""
    echo "Your ESP32 should be sending to: https://iot-khgd.onrender.com/api/sensors/bulk/"
elif [ "$ECG_VAL" == "75" ] && [ "$SPO2_VAL" == "98.5" ] && [ "$MAX_VAL" == "72" ]; then
    echo "❌ ISSUE: API is returning fallback values"
    echo ""
    echo "POSSIBLE CAUSES:"
    echo "1. ESP32 is not successfully sending data to the API"
    echo "2. ESP32 is sending zero/null values"
    echo "3. Wrong API endpoint in ESP32 code"
    echo "4. Network connectivity issues"
    echo ""
    echo "NEXT STEPS:"
    echo "1. Check ESP32 Serial Monitor output"
    echo "2. Verify WiFi connection on ESP32"
    echo "3. Check if ESP32 code has the correct API endpoint"
else
    echo "🔄 PARTIAL: Some values changed, some didn't"
    echo "This suggests partial success - check ESP32 data format"
fi

echo ""
echo "=== ESP32 CHECKLIST ==="
echo "1. WiFi connected? (Check Serial Monitor)"
echo "2. API endpoint: https://iot-khgd.onrender.com/api/sensors/bulk/"
echo "3. JSON format: {\"device_id\":\"ESP32_001\",\"ecg_heart_rate\":75,...}"
echo "4. HTTP POST working? (Check Serial Monitor for 200/201 responses)"
echo "5. Sensor readings > 0? (Not sending zeros)"
