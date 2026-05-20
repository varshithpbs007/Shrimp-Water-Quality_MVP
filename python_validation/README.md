# Python WLAN Validation Practice

This folder contains Python scripts developed to practice WLAN validation automation concepts relevant to embedded Wi-Fi and IoT systems.

## Scripts

### 1. WLAN KPI Log Parser
Parses simulated WLAN logs and extracts:
- RSSI
- MCS index
- PHY rate
- TCP throughput
- Latency
- Retry rate

### 2. RvR Test Simulator
Simulates Range vs Rate testing by analyzing:
- Distance
- RSSI
- Throughput
- Latency
- Packet loss

Generates a CSV report.

### 3. MQTT Telemetry Validator
Validates JSON telemetry packets from the ESP32 aquaculture monitoring system.

Checks:
- JSON format
- Sensor value ranges
- Aerator control logic

### 4. WLAN Regression Framework
A mini regression test suite for:
- Association
- Throughput
- Latency
- Packet loss
- Reconnection time

## Relevance

These scripts demonstrate Python automation skills for WLAN validation, including log parsing, KPI extraction, pass/fail analysis, telemetry validation, and regression-style testing.
