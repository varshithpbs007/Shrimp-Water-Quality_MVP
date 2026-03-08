#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// 1. PIN DEFINITIONS (Matching our Wokwi wiring)
#define PIN_PH 34
#define PIN_DO 35
#define PIN_TEMP 15
#define PIN_ALERT_LED 2

// 2. GLOBAL OBJECTS (The "Scope" fix)
DHT dht(PIN_TEMP, DHT22); 
WiFiClient espClient;
PubSubClient client(espClient);

// 3. DATA STRUCTURE
struct WaterData {
  float ph;
  float temp;
  bool alert;
};

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ALERT_LED, OUTPUT);
  
  // Initialize DHT Sensor
  dht.begin(); 

  // WiFi Setup
  WiFi.begin("Wokwi-GUEST", "", 6); // adding the channel 6 hint
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected");

  // MQTT Setup
  client.setServer("broker.hivemq.com", 1883);
}

WaterData readSensors() {
  WaterData data;
  
  // Read pH (Simulated)
  int rawPH = analogRead(PIN_PH);
  data.ph = (rawPH / 4095.0) * 14.0;  
  
  // Read Temp
  data.temp = dht.readTemperature();
  
  // Simple Logic: Alert if pH is outside shrimp safety (7.5 - 8.5)
  data.alert = (data.ph < 2.5 || data.ph > 8.5);
  
  return data;
}

void loop() {
  // Ensure MQTT is connected
  if (!client.connected()) {
    while (!client.connected()) {
      if (client.connect("ShrimpMVP_Client")) {
        Serial.println("MQTT Connected");
      } else {
        delay(2000);
      }
    }
  }
  client.loop();

  // Get Data
  WaterData currentPond = readSensors();
  
  // Visual Feedback
  digitalWrite(PIN_ALERT_LED, currentPond.alert ? HIGH : LOW);

  // Send JSON
  StaticJsonDocument<128> doc;
  doc["ph"] = currentPond.ph;
  doc["temp"] = currentPond.temp;
  doc["status"] = currentPond.alert ? "CRITICAL" : "OK";

  char payload[128];
  serializeJson(doc, payload);
  
  Serial.print("Publishing: ");
  Serial.println(payload);
  client.publish("shrimp/telemetry", payload);
  
  delay(5000); 
}
