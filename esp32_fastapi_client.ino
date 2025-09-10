/*
  ESP32 IoT Sensor Client for FastAPI Server
  Similar to your blood values project but for IoT sensors
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "Galaxy AO3 3614";
const char* password = "qwerty87";

// FastAPI server endpoint (like your blood values URL)
const char* apiEndpoint = "https://your-iot-sensors.onrender.com/post_sensor_data";

// Sensor pins (similar to your blood sensor setup)
const int ECG_PIN = A0;
const int PULSE_PIN = A1;
// I2C pins for MAX30102 and accelerometer
const int SDA_PIN = 21;
const int SCL_PIN = 22;

void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println("Ready to send sensor data!");
}

void loop() {
  // Read sensor values (like your red, ir, green values)
  float ecg_value = readECGSensor();          // Like your red value
  float spo2_value = readSpO2Sensor();        // Like your ir value  
  float pulse_value = readPulseSensor();      // Like your green value
  float max30102_value = readMAX30102();      // Additional sensor
  float x_axis = readAccelX();                // Accelerometer X
  float y_axis = readAccelY();                // Accelerometer Y
  float z_axis = readAccelZ();                // Accelerometer Z
  
  // Send data to FastAPI server (like your requests.post)
  sendSensorData(ecg_value, spo2_value, pulse_value, max30102_value, x_axis, y_axis, z_axis);
  
  delay(3000); // Send every 3 seconds (like your project)
}

// Read sensor functions (replace with real sensor code)
float readECGSensor() {
  // Replace with real ECG sensor reading
  return random(60, 100); // Simulated heart rate
}

float readSpO2Sensor() {
  // Replace with real SpO2 sensor reading  
  return random(95, 100); // Simulated oxygen saturation
}

float readPulseSensor() {
  // Replace with real pulse sensor reading
  return random(60, 100); // Simulated pulse rate
}

float readMAX30102() {
  // Replace with real MAX30102 reading
  return random(65, 85); // Simulated heart rate
}

float readAccelX() {
  return (random(-200, 200) / 100.0); // Simulated X acceleration
}

float readAccelY() {
  return (random(-200, 200) / 100.0); // Simulated Y acceleration  
}

float readAccelZ() {
  return 9.8 + (random(-50, 50) / 100.0); // Simulated Z acceleration
}

void sendSensorData(float ecg, float spo2, float pulse, float max30102, float x, float y, float z) {
  HTTPClient http;
  http.begin(apiEndpoint);
  http.addHeader("Content-Type", "application/json");
  
  // Create JSON payload (like your data = {"red": 23, "ir": 45, "green": 13})
  StaticJsonDocument<1024> doc;
  doc["device_id"] = "ESP32_IOT_SENSORS";
  doc["ecg_heart_rate"] = ecg;
  doc["spo2"] = spo2;
  doc["pulse_heart_rate"] = pulse;
  doc["max30102_heart_rate"] = max30102;
  doc["x_axis"] = x;
  doc["y_axis"] = y;  
  doc["z_axis"] = z;
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  Serial.println("Sending sensor data:");
  Serial.println("ECG: " + String(ecg));
  Serial.println("SpO2: " + String(spo2));
  Serial.println("Pulse: " + String(pulse));
  Serial.println("MAX30102: " + String(max30102));
  Serial.println("Accel: X=" + String(x) + ", Y=" + String(y) + ", Z=" + String(z));
  
  int httpResponseCode = http.POST(jsonString);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Server Response:");
    Serial.println(response);
    
    if (httpResponseCode == 200) {
      Serial.println("✅ RESULT_OK - Data sent successfully!");
    }
  } else {
    Serial.println("❌ Error sending data");
  }
  
  http.end();
}
