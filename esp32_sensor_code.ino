/*
  ESP32 IoT Sensor Data Collection and Transmission
  
  This code collects data from multiple sensors:
  - ECG sensor
  - Pulse Oximeter
  - MAX30102 Heart Rate sensor
  - Accelerometer (MPU6050 or similar)
  
  And sends the data to a Django REST API hosted on Render
*/

// Arduino IDE compatible includes
#ifdef ARDUINO_ARCH_ESP32
  #include <WiFi.h>
  #include <HTTPClient.h>
#else
  // For VS Code IntelliSense (won't affect Arduino compilation)
  typedef int WiFiClient;
  typedef int HTTPClient;
  #define WL_CONNECTED 3
  #define WiFi_RSSI() (-50)
#endif

#include <ArduinoJson.h>
#include <Wire.h>
#include <math.h>

// WiFi credentials
const char* ssid = "Galaxy AO3 3614";
const char* password = "qwerty87";

// API endpoint - Your live Render deployment
const char* apiEndpoint = "https://iot-khgd.onrender.com/api/sensor-data/bulk/";

// Device configuration
const String deviceId = "ESP32_001"; // Unique device identifier

// Sensor pins (adjust according to your wiring)
const int ECG_PIN = A0;
const int MAX30102_SDA = 21;
const int MAX30102_SCL = 22;

// Timing variables
unsigned long lastSensorRead = 0;
unsigned long lastDataSend = 0;
// Timing configuration for real-time data transmission
const unsigned long SENSOR_INTERVAL = 500;  // Read sensors every 0.5 seconds - more responsive
const unsigned long SEND_INTERVAL = 3000;   // Send data every 3 seconds - more frequent updates

// Sensor data structures
struct SensorData {
  // ECG data
  float ecg_heart_rate;
  float ecg_value;
  String ecg_signal_quality;
  
  // Pulse Oximeter data
  float spo2;
  float pulse_heart_rate;
  int pulse_signal_strength;
  
  // MAX30102 data
  float max30102_heart_rate;
  float max30102_spo2;
  int red_value;
  int ir_value;
  float temperature;
  
  // Accelerometer data
  float x_axis;
  float y_axis;
  float z_axis;
  float magnitude;
  
  // Device status
  float battery_level;
  int wifi_signal_strength;
  float memory_usage;
  float cpu_temperature;
  int uptime_seconds;
};

SensorData currentReading;

void setup() {
  Serial.begin(115200);
  
  // Initialize WiFi
  initWiFi();
  
  // Initialize sensors
  initSensors();
  
  Serial.println("ESP32 IoT Sensor System Started");
  Serial.println("Device ID: " + deviceId);
}

void loop() {
  // Check WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected, attempting to reconnect...");
    initWiFi();
  }
  
  // Read sensors periodically
  if (millis() - lastSensorRead >= SENSOR_INTERVAL) {
    readAllSensors();
    lastSensorRead = millis();
  }
  
  // Send data periodically
  if (millis() - lastDataSend >= SEND_INTERVAL) {
    sendSensorData();
    lastDataSend = millis();
  }
  
  delay(100); // Small delay to prevent watchdog reset
}

void initWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("WiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("WiFi connection failed!");
  }
}

void initSensors() {
  // Initialize I2C for sensors
  Wire.begin(MAX30102_SDA, MAX30102_SCL);
  
  // Initialize your specific sensors here
  // This is where you would initialize:
  // - MAX30102 sensor
  // - MPU6050 accelerometer
  // - ECG sensor (if using dedicated IC)
  // - Pulse oximeter sensor
  
  Serial.println("Sensors initialized");
}

void readAllSensors() {
  // Initialize all readings to zero - will be filled by actual sensors when connected
  
  // ECG sensor readings (ready for real sensor connection)
  currentReading.ecg_value = 0.0; // Will be filled by actual ECG sensor
  currentReading.ecg_heart_rate = 0.0; // Will be filled by ECG processing
  currentReading.ecg_signal_quality = "waiting"; // Will show sensor status
  
  // Pulse Oximeter readings (ready for real sensor connection)
  currentReading.spo2 = 0.0; // Will be filled by pulse oximeter
  currentReading.pulse_heart_rate = 0.0; // Will be filled by pulse sensor
  currentReading.pulse_signal_strength = 0; // Will show signal quality
  
  // MAX30102 sensor readings (ready for real sensor connection)
  currentReading.max30102_heart_rate = 0.0; // Will be filled by MAX30102
  currentReading.max30102_spo2 = 0.0; // Will be filled by MAX30102
  currentReading.red_value = 0; // Will be filled by MAX30102 red LED
  currentReading.ir_value = 0; // Will be filled by MAX30102 IR LED
  currentReading.temperature = 0.0; // Will be filled by MAX30102 temp sensor
  
  // Accelerometer readings (ready for real sensor connection)
  currentReading.x_axis = 0.0; // Will be filled by accelerometer X
  currentReading.y_axis = 0.0; // Will be filled by accelerometer Y
  currentReading.z_axis = 0.0; // Will be filled by accelerometer Z
  currentReading.magnitude = 0.0; // Will be calculated from X,Y,Z
  
  // TODO: CONNECT YOUR REAL SENSORS HERE
  // Uncomment and modify these sections when you connect actual hardware:
  
  /*
  // REAL ECG SENSOR (AD8232) - Uncomment when connected:
  // currentReading.ecg_value = analogRead(ECG_PIN) * (3.3 / 4095.0);
  // currentReading.ecg_heart_rate = calculateHeartRateFromECG();
  // currentReading.ecg_signal_quality = "good";
  
  // REAL PULSE OXIMETER - Uncomment when connected:
  // currentReading.spo2 = pulseOximeter.getSpO2();
  // currentReading.pulse_heart_rate = pulseOximeter.getHeartRate();
  // currentReading.pulse_signal_strength = pulseOximeter.getSignalStrength();
  
  // REAL MAX30102 SENSOR - Uncomment when connected:
  // currentReading.max30102_heart_rate = particleSensor.getHeartRate();
  // currentReading.max30102_spo2 = particleSensor.getSpO2();
  // currentReading.red_value = particleSensor.getRed();
  // currentReading.ir_value = particleSensor.getIR();
  // currentReading.temperature = particleSensor.readTemperature();
  
  // REAL ACCELEROMETER (MPU6050) - Uncomment when connected:
  // int16_t ax, ay, az;
  // accel.getAcceleration(&ax, &ay, &az);
  // currentReading.x_axis = ax / 16384.0;  // Convert to g
  // currentReading.y_axis = ay / 16384.0;
  // currentReading.z_axis = az / 16384.0;
  // currentReading.magnitude = sqrt(pow(currentReading.x_axis, 2) + 
  //                                 pow(currentReading.y_axis, 2) + 
  //                                 pow(currentReading.z_axis, 2));
  */
  
  // Device status (always available)
  currentReading.battery_level = (float)random(70, 100); // Simulated for now
  currentReading.wifi_signal_strength = WiFi.RSSI(); // Real WiFi signal
  currentReading.memory_usage = (float)random(30, 80); // Simulated for now
  currentReading.cpu_temperature = (float)random(35, 45); // Simulated for now
  currentReading.uptime_seconds = (int)(millis() / 1000); // Real uptime
  
  // Print sensor status to serial for debugging
  Serial.println("Sensor Status:");
  Serial.println("  ECG: " + String(currentReading.ecg_heart_rate) + " BPM (0 = no sensor)");
  Serial.println("  Pulse Ox: SpO2 " + String(currentReading.spo2) + "%, HR " + String(currentReading.pulse_heart_rate) + " BPM (0 = no sensor)");
  Serial.println("  MAX30102: HR " + String(currentReading.max30102_heart_rate) + " BPM (0 = no sensor)");
  Serial.println("  Accel: X=" + String(currentReading.x_axis) + ", Y=" + String(currentReading.y_axis) + ", Z=" + String(currentReading.z_axis) + " (0 = no sensor)");
  Serial.println("  Battery: " + String(currentReading.battery_level) + "%");
}

void sendSensorData() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected, cannot send data");
    return;
  }
  
  HTTPClient http;
  http.begin(apiEndpoint);
  http.addHeader("Content-Type", "application/json");
  
  // Create JSON payload with proper error handling
  const size_t JSON_BUFFER_SIZE = 2048;
  DynamicJsonDocument doc(JSON_BUFFER_SIZE);
  doc["device_id"] = deviceId;
  
  // ECG data
  doc["ecg_heart_rate"] = currentReading.ecg_heart_rate;
  doc["ecg_value"] = currentReading.ecg_value;
  doc["ecg_signal_quality"] = currentReading.ecg_signal_quality;
  
  // Pulse Oximeter data
  doc["spo2"] = currentReading.spo2;
  doc["pulse_heart_rate"] = currentReading.pulse_heart_rate;
  doc["pulse_signal_strength"] = currentReading.pulse_signal_strength;
  
  // MAX30102 data
  doc["max30102_heart_rate"] = currentReading.max30102_heart_rate;
  doc["max30102_spo2"] = currentReading.max30102_spo2;
  doc["red_value"] = currentReading.red_value;
  doc["ir_value"] = currentReading.ir_value;
  doc["temperature"] = currentReading.temperature;
  
  // Accelerometer data
  doc["x_axis"] = currentReading.x_axis;
  doc["y_axis"] = currentReading.y_axis;
  doc["z_axis"] = currentReading.z_axis;
  doc["magnitude"] = currentReading.magnitude;
  
  // Device status
  doc["battery_level"] = currentReading.battery_level;
  doc["wifi_signal_strength"] = currentReading.wifi_signal_strength;
  doc["memory_usage"] = currentReading.memory_usage;
  doc["cpu_temperature"] = currentReading.cpu_temperature;
  doc["uptime_seconds"] = currentReading.uptime_seconds;
  
  String jsonString;
  size_t jsonSize = serializeJson(doc, jsonString);
  
  if (jsonSize == 0) {
    Serial.println("Failed to serialize JSON");
    http.end();
    return;
  }
  
  Serial.println("Sending data to server...");
  Serial.println("JSON Size: " + String(jsonSize) + " bytes");
  Serial.println("Payload: " + jsonString);
  
  int httpResponseCode = http.POST(jsonString);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("HTTP Response Code: " + String(httpResponseCode));
    
    // Handle different HTTP status codes
    switch (httpResponseCode) {
      case 200:
        Serial.println("✅ 200 OK - Request successful");
        if (response.length() > 0) {
          Serial.println("📊 Raw Sensor Values: " + response);
        }
        break;
      case 201:
        Serial.println("✅ 201 CREATED - Data stored successfully");
        
        // Display the raw sensor values (one per line)
        if (response.length() > 0) {
          Serial.println("📊 Raw Values Received:");
          
          // Split response by newlines and display each value
          int startIndex = 0;
          int newlineIndex = response.indexOf('\n');
          int valueCount = 1;
          
          while (newlineIndex != -1) {
            String value = response.substring(startIndex, newlineIndex);
            value.trim();
            if (value.length() > 0) {
              Serial.println("  Value " + String(valueCount) + ": " + value);
              valueCount++;
            }
            startIndex = newlineIndex + 1;
            newlineIndex = response.indexOf('\n', startIndex);
          }
          
          // Print the last value (after the last newline)
          String lastValue = response.substring(startIndex);
          lastValue.trim();
          if (lastValue.length() > 0) {
            Serial.println("  Value " + String(valueCount) + ": " + lastValue);
          }
          
          Serial.println(""); // Empty line for readability
        }
        break;
      case 400:
        Serial.println("❌ 400 BAD REQUEST - Invalid data format");
        break;
      case 401:
        Serial.println("❌ 401 UNAUTHORIZED - Authentication required");
        break;
      case 403:
        Serial.println("❌ 403 FORBIDDEN - Access denied");
        break;
      case 404:
        Serial.println("❌ 404 NOT FOUND - Endpoint not found");
        break;
      case 500:
        Serial.println("❌ 500 INTERNAL SERVER ERROR - Server problem");
        break;
      case 502:
        Serial.println("❌ 502 BAD GATEWAY - Server unavailable");
        break;
      case 503:
        Serial.println("❌ 503 SERVICE UNAVAILABLE - Server overloaded");
        break;
      default:
        Serial.println("⚠️  HTTP " + String(httpResponseCode) + " - Unexpected response");
        break;
    }
    
    Serial.println("Server Response: " + response);
  } else {
    Serial.println("❌ HTTP Request Failed");
    Serial.println("Error Code: " + String(httpResponseCode));
    Serial.println("Error: " + http.errorToString(httpResponseCode));
    Serial.println("Check WiFi connection and server URL");
  }
  
  http.end();
}

/*
  TODO: Replace simulated sensor readings with actual sensor code
  
  For ECG sensor:
  - Use AD8232 ECG sensor module
  - Read analog values and process for heart rate detection
  
  For MAX30102:
  - Use MAX30102 library
  - Initialize sensor and read heart rate/SpO2
  
  For Accelerometer:
  - Use MPU6050 or similar
  - Read acceleration values from I2C
  
  For Pulse Oximeter:
  - Use dedicated pulse oximeter sensor
  - Read SpO2 and pulse rate
*/