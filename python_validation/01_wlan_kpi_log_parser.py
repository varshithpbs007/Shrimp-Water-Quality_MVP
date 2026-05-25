"""
Project: WLAN KPI Log Parser for ESP32 Aquaculture IoT Simulation

Description:
This script parses simulated WLAN validation logs related to an ESP32-based
smart aquaculture monitoring system.

Since the current project is implemented using Wokwi simulation, real router
or Wi-Fi driver logs are not available. Therefore, this script uses simulated
WLAN test logs to practice Python-based validation automation.

The parser extracts:
- RSSI
- MCS index
- PHY rate
- TCP throughput
- Latency
- Retry rate
- MQTT publish status

It then classifies each test point as PASS, WARNING, or FAIL.

Relevance:
This demonstrates Python skills useful in WLAN validation roles:
- Log parsing
- KPI extraction
- Pass/fail decision logic
- Report generation
- Embedded Wi-Fi telemetry validation thinking
"""

import re
import csv


sample_log = """
[10:00:01] DEVICE=ESP32_AQUA RSSI=-42 dBm MCS=9 PHY_RATE=1201 Mbps TCP_THROUGHPUT=845 Mbps LATENCY=12 ms RETRY=3% MQTT=SUCCESS
[10:00:06] DEVICE=ESP32_AQUA RSSI=-55 dBm MCS=7 PHY_RATE=864 Mbps TCP_THROUGHPUT=620 Mbps LATENCY=18 ms RETRY=7% MQTT=SUCCESS
[10:00:11] DEVICE=ESP32_AQUA RSSI=-68 dBm MCS=5 PHY_RATE=432 Mbps TCP_THROUGHPUT=290 Mbps LATENCY=35 ms RETRY=15% MQTT=SUCCESS
[10:00:16] DEVICE=ESP32_AQUA RSSI=-78 dBm MCS=3 PHY_RATE=144 Mbps TCP_THROUGHPUT=85 Mbps LATENCY=72 ms RETRY=31% MQTT=FAIL
"""


pattern = (
    r"RSSI=\s*(-?\d+)\s*dBm\s*"
    r"MCS=\s*(\d+)\s*"
    r"PHY_RATE=\s*(\d+)\s*Mbps\s*"
    r"TCP_THROUGHPUT=\s*(\d+)\s*Mbps\s*"
    r"LATENCY=\s*(\d+)\s*ms\s*"
    r"RETRY=\s*(\d+)%\s*"
    r"MQTT=\s*(SUCCESS|FAIL)"
)


def classify_test_result(throughput, latency, retry, mqtt_status):
    """
    Classifies WLAN test result based on validation thresholds.
    """

    if mqtt_status == "FAIL":
        return "FAIL"

    if throughput > 500 and latency < 30 and retry < 10:
        return "PASS"

    elif throughput > 150 and latency < 60 and retry < 25:
        return "WARNING"

    else:
        return "FAIL"


def main():
    matches = re.findall(pattern, sample_log)

    if not matches:
        print("No valid WLAN KPI logs found.")
        return

    rssi_values = []
    throughput_values = []
    latency_values = []
    retry_values = []
    report_rows = []

    print("ESP32 Aquaculture WLAN KPI Validation Report")
    print("-" * 100)

    for index, match in enumerate(matches, start=1):
        rssi = int(match[0])
        mcs = int(match[1])
        phy_rate = int(match[2])
        throughput = int(match[3])
        latency = int(match[4])
        retry = int(match[5])
        mqtt_status = match[6]

        status = classify_test_result(
            throughput,
            latency,
            retry,
            mqtt_status
        )

        rssi_values.append(rssi)
        throughput_values.append(throughput)
        latency_values.append(latency)
        retry_values.append(retry)

        report_rows.append({
            "test_point": index,
            "rssi_dbm": rssi,
            "mcs": mcs,
            "phy_rate_mbps": phy_rate,
            "tcp_throughput_mbps": throughput,
            "latency_ms": latency,
            "retry_percent": retry,
            "mqtt_status": mqtt_status,
            "validation_status": status
        })

        print(
            f"Test {index}: "
            f"RSSI={rssi} dBm | "
            f"MCS={mcs} | "
            f"PHY={phy_rate} Mbps | "
            f"TCP={throughput} Mbps | "
            f"Latency={latency} ms | "
            f"Retry={retry}% | "
            f"MQTT={mqtt_status} | "
            f"Status={status}"
        )

    print("-" * 100)
    print("Summary")
    print(f"Average RSSI       : {sum(rssi_values) / len(rssi_values):.2f} dBm")
    print(f"Average Throughput : {sum(throughput_values) / len(throughput_values):.2f} Mbps")
    print(f"Average Latency    : {sum(latency_values) / len(latency_values):.2f} ms")
    print(f"Average Retry Rate : {sum(retry_values) / len(retry_values):.2f}%")
    print(f"Worst RSSI         : {min(rssi_values)} dBm")
    print(f"Best Throughput    : {max(throughput_values)} Mbps")

    with open("wlan_kpi_report.csv", "w", newline="") as file:
        fieldnames = [
            "test_point",
            "rssi_dbm",
            "mcs",
            "phy_rate_mbps",
            "tcp_throughput_mbps",
            "latency_ms",
            "retry_percent",
            "mqtt_status",
            "validation_status"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_rows)

    print("\nCSV report generated: wlan_kpi_report.csv")


if __name__ == "__main__":
    main()
