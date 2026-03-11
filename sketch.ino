#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// PIN DEFINITIONS through MACROS
#define PIN_PH 34         // pH Sensor
#define PIN_DO 35        // Dissolved Oxygen (DO) Sensor
#define PIN_AMMONIA 32    // Ammonia (NH3) Sensor
#define PIN_TEMP 15       // DHT22 Temperature Sensor
#define PIN_ALERT_LED 2
#define PIN_AERATOR 33    // Actuator for Aerator ( Here Blue LED)

DHT dht(PIN_TEMP, DHT22); 
WiFiClient espClient;
PubSubClient client(espClient);

// Global struct variable named WaterData to collect sensor readings
struct WaterData {
  float ph;
  float temp;
  float do_level;
  float ammonia;
  bool aerator_on;
};

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ALERT_LED, OUTPUT);
  pinMode(PIN_AERATOR, OUTPUT);
  dht.begin(); 

  WiFi.begin("Wokwi-GUEST", "", 6);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWiFi Connected");
  client.setServer("broker.hivemq.com", 1883);
}

WaterData readSensors() {
  WaterData data;
  
  // pH Calculation (0-14)
  data.ph = (analogRead(PIN_PH) / 4095.0) * 14.0;
  
  // DO Calculation (Simulated 0-10 mg/L)
  data.do_level = (analogRead(PIN_DO) / 4095.0) * 10.0;
  
  // Ammonia Calculation (Simulated 0-2 ppm)
  data.ammonia = (analogRead(PIN_AMMONIA) / 4095.0) * 2.0;
  
  data.temp = dht.readTemperature();


  // --- Thresholds used ---
  // Parameter: pH, DO, Ammonia (NH3), Temperature(C)
  // Ideal Range: 7.5-8.5, >5.0 mg/L, <0.01 ppm, 28-32 'C
  // Action: Alert if pH is <7 or >9, Turn Aerator ON(Blue LED) if <5.0 mg/L, Turn Aerator ON if > 0.05 ppm (to help gas exchange), Increase aeration if Temp > 30°C (oxygen drops in heat)
  // --------------------------------------------------


  // --- EFFICIENCY LOGIC ---
  // Aerator runs if DO is low (< 5.0) OR if Ammonia is creeping up (> 0.05)
  // Temperature also affects oxygen solubility; at higher temps (> 30°C), we boost DO.
  if (data.do_level < 5.0 || data.ammonia > 0.1 || (data.temp > 30 && data.do_level < 6.0)) {
    data.aerator_on = true;
  } else {
    data.aerator_on = false;
  }
  
  return data;
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  WaterData currentPond = readSensors();
  
  // Physical Actuation
  digitalWrite(PIN_AERATOR, currentPond.aerator_on ? HIGH : LOW);
  
  // Red Alert LED if values are dangerous
  bool danger = (currentPond.ph < 7.0 || currentPond.ph > 9.0 || currentPond.do_level < 3.0);
  digitalWrite(PIN_ALERT_LED, danger ? HIGH : LOW);

  // JSON Telemetry
  StaticJsonDocument<200> doc;
  doc["ph"] = currentPond.ph;
  doc["temp"] = currentPond.temp;
  doc["do"] = currentPond.do_level;
  doc["nh3"] = currentPond.ammonia;
  doc["aerator"] = currentPond.aerator_on ? "ON" : "OFF";

  char payload[200];
  serializeJson(doc, payload);
  Serial.println(payload);
  client.publish("shrimp/telemetry", payload);
  
  delay(5000); 
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ShrimpMVP_Client")) {
      Serial.println("MQTT Connected");
    } else {
      delay(2000);
    }
  }
}
