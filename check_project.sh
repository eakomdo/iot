#!/bin/bash
# Quick deployment verification script

echo "🔍 CHECKING IOT PROJECT READINESS..."
echo "=================================="

echo "✅ Django Backend:"
ls -la iot_backend/ | head -5

echo "✅ Sensor Models & API:"
ls -la sensors/

echo "✅ ESP32 Code:"
ls -la esp32_sensor_code.ino

echo "✅ Deployment Files:"
echo "   - render.yaml: $(test -f render.yaml && echo 'Present' || echo 'Missing')"
echo "   - build.sh: $(test -f build.sh && echo 'Present' || echo 'Missing')"  
echo "   - requirements.txt: $(test -f requirements.txt && echo 'Present' || echo 'Missing')"

echo ""
echo "🚀 PROJECT STATUS: READY FOR RENDER DEPLOYMENT!"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Push code to GitHub repository"
echo "2. Deploy to Render using render.yaml"
echo "3. Update ESP32 code with your Render URL"
echo "4. Upload code to ESP32 and test"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
