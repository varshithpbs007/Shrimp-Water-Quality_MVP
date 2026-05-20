# ESP32-Based Smart Aquaculture Monitoring and Control System

This repository contains the firmware, circuit design, WLAN validation practice scripts, and system architecture for an ESP32-based IoT water quality monitoring and control system.

The system monitors key aquaculture parameters including:

- pH
- Dissolved Oxygen (DO)
- Ammonia (NH3)
- Temperature

The ESP32 performs real-time sensing, threshold-based decision making, MQTT telemetry transmission over Wi-Fi, and automatic aerator control for maintaining healthy aquaculture conditions.

---

# Features

- Multi-sensor data acquisition using ESP32 ADC and DHT22
- MQTT telemetry publishing via Wi-Fi
- JSON serialization using ArduinoJson
- Threshold-based aerator control logic
- Real-time environmental monitoring
- Embedded edge-decision logic
- WLAN connectivity using IEEE 802.11 Wi-Fi
- Python-based WLAN KPI analysis and validation scripts
- Simulated RvR (Range vs Rate) testing workflows
- MQTT telemetry validation and regression-style testing

---

# System Architecture

## Hardware Components

- ESP32 DevKit
- DHT22 Temperature Sensor
- Analog pH Sensor (simulated)
- Dissolved Oxygen Sensor (simulated)
- Ammonia Sensor (simulated)
- Alert LED
- Aerator Actuator (Blue LED in simulation)

## Communication Stack

- Wi-Fi Connectivity (802.11 WLAN)
- MQTT Protocol
- TCP/IP Networking
- JSON Telemetry Serialization

---

# Functional Overview

The ESP32 periodically reads sensor data and evaluates environmental thresholds.

## Aerator Logic

The aerator is automatically activated when:

- Dissolved Oxygen falls below safe limits
- Ammonia concentration increases
- Temperature rises and oxygen availability decreases

## Alert Logic

The alert LED activates during dangerous environmental conditions such as:

- Unsafe pH levels
- Critically low dissolved oxygen

Telemetry packets are serialized as JSON and transmitted to an MQTT broker over Wi-Fi.

---

# WLAN / Wi-Fi Validation

This project was extended to include WLAN validation-oriented workflows relevant to embedded wireless testing environments.

The ESP32 acts as a Wi-Fi station and publishes telemetry over MQTT while Python automation scripts are used to simulate WLAN testing workflows such as:

- RSSI analysis
- Throughput monitoring
- Latency analysis
- Retry-rate observation
- Packet-loss evaluation
- MQTT telemetry validation
- WLAN regression-style testing
- Simulated Range vs Rate (RvR) analysis

These workflows align with concepts used in:

- IEEE 802.11ac
- IEEE 802.11ax (Wi-Fi 6)
- WLAN performance testing
- Embedded wireless validation
- Router/device interoperability environments

---

# Python Validation Scripts

The repository includes Python-based WLAN validation practice scripts inside:

```text
python_validation/
```

## Included Scripts

### 1. WLAN KPI Log Parser

Extracts and analyzes:

- RSSI
- MCS Index
- PHY Rate
- Throughput
- Latency
- Retry Rate

### 2. RvR Test Simulator

Simulates Range vs Rate testing under varying signal conditions.

### 3. MQTT Telemetry Validator

Validates:

- JSON packet structure
- Sensor ranges
- Aerator decision logic

### 4. WLAN Regression Framework

Implements regression-style validation for:

- Association
- Throughput
- Latency
- Packet loss
- Reconnection timing

---

# Core areas

## Embedded Systems

- ESP32 Firmware Development
- GPIO
- ADC Interfacing
- Sensor Integration
- Real-Time Control Logic

## Wireless Communication

- IEEE 802.11 WLAN
- MQTT over TCP/IP
- Wi-Fi Telemetry
- RSSI and Throughput Concepts
- WLAN Stability Analysis

## Validation and Testing

- Functional Testing
- Regression Testing
- Stress Testing
- KPI Extraction
- Log Parsing
- WLAN Performance Analysis



# Future Scope and Improvements

- Real hardware sensor calibration
- Real-time dashboard visualization
- Database/cloud integration
- WPA2/WPA3 validation workflows
- SoftAP testing
- Wi-Fi roaming analysis
- Real router interoperability testing
- OTA firmware update support

---

# Author

Varshith Poodi  
M.E. Communication Engineering  
BITS Pilani Hyderabad Campus
