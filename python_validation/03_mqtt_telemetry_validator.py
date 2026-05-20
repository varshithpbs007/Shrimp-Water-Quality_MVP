# my ESP32 project publishes JSON over MQTT, I validated telemetry packets using Python. 
# This checks JSON format, sensor ranges and whether aerator control logic is correct.

import json

mqtt_logs = [
    '{"ph":7.8,"temp":29.5,"do":6.2,"nh3":0.03,"aerator":"OFF"}',
    '{"ph":8.1,"temp":31.2,"do":5.8,"nh3":0.04,"aerator":"OFF"}',
    '{"ph":6.5,"temp":32.5,"do":4.2,"nh3":0.12,"aerator":"ON"}',
    '{"ph":9.4,"temp":30.1,"do":3.1,"nh3":0.08,"aerator":"ON"}'
]

def validate_packet(packet):
    required_keys = ["ph", "temp", "do", "nh3", "aerator"]

    for key in required_keys:
        if key not in packet:
            return False, f"Missing key: {key}"

    if not (0 <= packet["ph"] <= 14):
        return False, "Invalid pH range"

    if not (-10 <= packet["temp"] <= 60):
        return False, "Invalid temperature range"

    if not (0 <= packet["do"] <= 10):
        return False, "Invalid dissolved oxygen range"

    if not (0 <= packet["nh3"] <= 2):
        return False, "Invalid ammonia range"

    if packet["aerator"] not in ["ON", "OFF"]:
        return False, "Invalid aerator state"

    return True, "Valid packet"

print("MQTT Telemetry Validation Report")
print("-" * 70)

valid_count = 0
invalid_count = 0

for index, log in enumerate(mqtt_logs, start=1):
    try:
        packet = json.loads(log)
        is_valid, message = validate_packet(packet)

        expected_aerator = "ON" if (
            packet["do"] < 5.0 or packet["nh3"] > 0.1 or
            (packet["temp"] > 30 and packet["do"] < 6.0)
        ) else "OFF"

        logic_status = "PASS" if packet["aerator"] == expected_aerator else "FAIL"

        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1

        print(f"Packet {index}: {message}")
        print(f"  pH={packet['ph']}, Temp={packet['temp']} C, DO={packet['do']} mg/L, NH3={packet['nh3']} ppm")
        print(f"  Aerator Received={packet['aerator']}, Expected={expected_aerator}, Logic Check={logic_status}")

    except json.JSONDecodeError:
        invalid_count += 1
        print(f"Packet {index}: Invalid JSON format")

    print("-" * 70)

print("Summary")
print(f"Valid packets   : {valid_count}")
print(f"Invalid packets : {invalid_count}")
