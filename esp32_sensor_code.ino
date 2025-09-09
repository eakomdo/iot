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
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

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
const unsigned long SENSOR_INTERVAL = 1000; // Read sensors every 1 second
const unsigned long SEND_INTERVAL = 10000; // Send data every 10 seconds

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
  // Read ECG sensor (simulated values - replace with actual sensor code)
  currentReading.ecg_value = analogRead(ECG_PIN) * (3.3 / 4095.0); // Convert to voltage
  currentReading.ecg_heart_rate = 70 + random(-10, 11); // Simulated heart rate
  currentReading.ecg_signal_quality = "good";
  
  // Read Pulse Oximeter (simulated values)
  currentReading.spo2 = 95.0 + random(-3, 4);
  currentReading.pulse_heart_rate = 68 + random(-8, 9);
  currentReading.pulse_signal_strength = random(70, 100);
  
  // Read MAX30102 sensor (simulated values)
  currentReading.max30102_heart_rate = 72 + random(-8, 9);
  currentReading.max30102_spo2 = 96.0 + random(-2, 3);
  currentReading.red_value = random(10000, 50000);
  currentReading.ir_value = random(15000, 60000);
  currentReading.temperature = 36.5 + random(-1, 2);
  
  // Read Accelerometer (simulated values)
  currentReading.x_axis = (random(-200, 201) / 100.0);
  currentReading.y_axis = (random(-200, 201) / 100.0);
  currentReading.z_axis = 9.8 + (random(-50, 51) / 100.0);
  currentReading.magnitude = sqrt(pow(currentReading.x_axis, 2) + 
                                  pow(currentReading.y_axis, 2) + 
                                  pow(currentReading.z_axis, 2));
  
  // Read device status
  currentReading.battery_level = (float)random(70, 100);
  currentReading.wifi_signal_strength = WiFi.RSSI();
  currentReading.memory_usage = (float)random(30, 80);
  currentReading.cpu_temperature = (float)random(35, 45);
  currentReading.uptime_seconds = (int)(millis() / 1000);
  
  // Print sensor data to serial for debugging
  Serial.println("Sensor readings:");
  Serial.println("  ECG: " + String(currentReading.ecg_heart_rate) + " BPM, Value: " + String(currentReading.ecg_value));
  Serial.println("  Pulse Ox: SpO2 " + String(currentReading.spo2) + "%, HR " + String(currentReading.pulse_heart_rate) + " BPM");
  Serial.println("  MAX30102: HR " + String(currentReading.max30102_heart_rate) + " BPM, SpO2 " + String(currentReading.max30102_spo2) + "%");
  Serial.println("  Accel: X=" + String(currentReading.x_axis) + ", Y=" + String(currentReading.y_axis) + ", Z=" + String(currentReading.z_axis));
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
        break;
      case 201:
        Serial.println("✅ 201 CREATED - Data stored successfully");
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
