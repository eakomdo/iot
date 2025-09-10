/*
  ESP32 IoT Sensor Client - FIXED VERSION
  Sends real sensor data to Django server at correct endpoint
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "Galaxy AO3 3614";
const char* password = "qwerty87";

// CORRECT Django server endpoint 
const char* apiEndpoint = "https://iot-khgd.onrender.com/api/post_sensor_data/";

// Sensor pins (adjust based on your actual hardware)
const int ECG_PIN = A0;
const int PULSE_PIN = A1;
// I2C pins for MAX30102 and accelerometer
const int SDA_PIN = 21;
const int SCL_PIN = 22;

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 IoT Sensors - Starting...");
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println();
  Serial.println("✅ Connected to WiFi!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("Ready to send sensor data to Django server!");
  Serial.println("==================================================");
}

void loop() {
  // Read sensor values
  float ecg_value = readECGSensor();          
  float spo2_value = readSpO2Sensor();        
  float max30102_value = readMAX30102();      
  float x_axis = readAccelX();                
  float y_axis = readAccelY();                
  float z_axis = readAccelZ();                
  
  // Display readings
  Serial.println("📊 Sensor Readings:");
  Serial.println("ECG Heart Rate: " + String(ecg_value) + " BPM");
  Serial.println("SpO2: " + String(spo2_value) + "%");
  Serial.println("MAX30102 HR: " + String(max30102_value) + " BPM");
  Serial.println("Accelerometer: X=" + String(x_axis) + ", Y=" + String(y_axis) + ", Z=" + String(z_axis));
  
  // Send data to Django server
  sendSensorData(ecg_value, spo2_value, max30102_value, x_axis, y_axis, z_axis);
  
  Serial.println("⏱️  Waiting 5 seconds before next reading...");
  Serial.println("==================================================");
  delay(5000); // Send every 5 seconds
}

// Sensor reading functions - Replace with your actual sensor code
float readECGSensor() {
  // Replace with real ECG sensor code
  // For testing, generate realistic varying values
  static float lastValue = 75;
  lastValue += random(-5, 6); // Vary by ±5
  if (lastValue < 60) lastValue = 60;
  if (lastValue > 100) lastValue = 100;
  return lastValue;
}

float readSpO2Sensor() {
  // Replace with real SpO2 sensor code
  // For testing, generate realistic values
  static float lastValue = 98;
  lastValue += random(-2, 3) * 0.1; // Small variations
  if (lastValue < 95) lastValue = 95;
  if (lastValue > 100) lastValue = 100;
  return lastValue;
}

float readMAX30102() {
  // Replace with real MAX30102 sensor code
  static float lastValue = 72;
  lastValue += random(-3, 4); // Vary by ±3
  if (lastValue < 65) lastValue = 65;
  if (lastValue > 90) lastValue = 90;
  return lastValue;
}

float readAccelX() {
  // Replace with real accelerometer code
  return (random(-50, 51) / 100.0); // -0.5 to +0.5
}

float readAccelY() {
  // Replace with real accelerometer code  
  return (random(-30, 31) / 100.0); // -0.3 to +0.3
}

float readAccelZ() {
  // Replace with real accelerometer code
  return 9.8 + (random(-20, 21) / 100.0); // Around 9.8 ± 0.2
}

void sendSensorData(float ecg, float spo2, float max30102, float x, float y, float z) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ WiFi not connected! Reconnecting...");
    WiFi.begin(ssid, password);
    return;
  }
  
  HTTPClient http;
  http.begin(apiEndpoint);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(10000); // 10 second timeout
  
  // Create JSON payload for Django server
  StaticJsonDocument<1024> doc;
  doc["device_id"] = "ESP32_IOT_SENSORS";
  doc["ecg_heart_rate"] = ecg;
  doc["spo2"] = spo2;
  doc["max30102_heart_rate"] = max30102;
  doc["x_axis"] = x;
  doc["y_axis"] = y;  
  doc["z_axis"] = z;
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  Serial.println("📤 Sending to Django server...");
  Serial.println("URL: " + String(apiEndpoint));
  Serial.println("JSON: " + jsonString);
  
  int httpResponseCode = http.POST(jsonString);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("📥 Server Response Code: " + String(httpResponseCode));
    Serial.println("📥 Server Response: " + response);
    
    if (httpResponseCode == 200) {
      Serial.println("✅ SUCCESS! Data sent to Django server!");
    } else {
      Serial.println("⚠️  Unexpected response code: " + String(httpResponseCode));
    }
  } else {
    Serial.println("❌ HTTP Error: " + String(httpResponseCode));
    Serial.println("❌ Failed to send data to Django server");
  }
  
  http.end();
}
