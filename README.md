This repository contains the firmware, circuit diagram, and system architecture for an ESP32-based IoT water quality monitoring and control system. The system measures key aquaculture parameters including pH, dissolved oxygen, ammonia, and temperature, and transmits telemetry using MQTT while automatically controlling an aeration actuator based on environmental thresholds.


Features:
- Multi-sensor data acquisition using ESP32 ADC and DHT22
- MQTT telemetry publishing via Wi-Fi
- JSON data serialization using ArduinoJson
- Threshold-based aerator control logic
- Real-time water quality monitoring
