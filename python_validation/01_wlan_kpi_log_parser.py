
import re

sample_log = """
[10:00:01] RSSI=-42 dBm MCS=9 PHY_RATE=1201 Mbps TCP_THROUGHPUT=845 Mbps LATENCY=12 ms RETRY=3%
[10:00:06] RSSI=-55 dBm MCS=7 PHY_RATE=864 Mbps TCP_THROUGHPUT=620 Mbps LATENCY=18 ms RETRY=7%
[10:00:11] RSSI=-68 dBm MCS=5 PHY_RATE=432 Mbps TCP_THROUGHPUT=290 Mbps LATENCY=35 ms RETRY=15%
[10:00:16] RSSI=-78 dBm MCS=3 PHY_RATE=144 Mbps TCP_THROUGHPUT=85 Mbps LATENCY=72 ms RETRY=31%
"""

pattern = r"RSSI=(-?\d+) dBm MCS=(\d+) PHY_RATE=(\d+) Mbps TCP_THROUGHPUT=(\d+) Mbps LATENCY=(\d+) ms RETRY=(\d+)%"

matches = re.findall(pattern, sample_log)

rssi_values = []
throughput_values = []
latency_values = []
retry_values = []

print("Parsed WLAN KPI Report")
print("-" * 60)

for match in matches:
    rssi = int(match[0])
    mcs = int(match[1])
    phy_rate = int(match[2])
    throughput = int(match[3])
    latency = int(match[4])
    retry = int(match[5])

    rssi_values.append(rssi)
    throughput_values.append(throughput)
    latency_values.append(latency)
    retry_values.append(retry)

    if throughput > 500 and latency < 30 and retry < 10:
        status = "PASS"
    elif throughput > 150 and latency < 60 and retry < 25:
        status = "WARNING"
    else:
        status = "FAIL"

    print(f"RSSI: {rssi} dBm | MCS: {mcs} | PHY: {phy_rate} Mbps | "
          f"TCP: {throughput} Mbps | Latency: {latency} ms | Retry: {retry}% | {status}")

print("-" * 60)
print("Summary")
print(f"Average RSSI       : {sum(rssi_values) / len(rssi_values):.2f} dBm")
print(f"Average Throughput : {sum(throughput_values) / len(throughput_values):.2f} Mbps")
print(f"Average Latency    : {sum(latency_values) / len(latency_values):.2f} ms")
print(f"Average Retry Rate : {sum(retry_values) / len(retry_values):.2f}%")
