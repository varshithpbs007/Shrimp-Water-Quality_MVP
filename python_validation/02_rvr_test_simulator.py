import csv

test_data = [
    {"distance": 1,  "rssi": -35, "throughput": 920, "latency": 8,  "packet_loss": 0.1},
    {"distance": 3,  "rssi": -45, "throughput": 820, "latency": 11, "packet_loss": 0.3},
    {"distance": 5,  "rssi": -55, "throughput": 640, "latency": 18, "packet_loss": 1.2},
    {"distance": 8,  "rssi": -65, "throughput": 410, "latency": 32, "packet_loss": 3.5},
    {"distance": 12, "rssi": -75, "throughput": 160, "latency": 68, "packet_loss": 8.9},
    {"distance": 15, "rssi": -82, "throughput": 55,  "latency": 120, "packet_loss": 18.5}
]

def classify_result(throughput, latency, packet_loss):
    if throughput >= 500 and latency <= 30 and packet_loss <= 2:
        return "PASS"
    elif throughput >= 150 and latency <= 80 and packet_loss <= 10:
        return "DEGRADED"
    else:
        return "FAIL"

print("RvR Test Report: Range vs Rate")
print("-" * 75)
print("Distance(m) | RSSI(dBm) | Throughput(Mbps) | Latency(ms) | Loss(%) | Status")
print("-" * 75)

for row in test_data:
    status = classify_result(row["throughput"], row["latency"], row["packet_loss"])
    row["status"] = status

    print(f"{row['distance']:>11} | {row['rssi']:>9} | {row['throughput']:>16} | "
          f"{row['latency']:>11} | {row['packet_loss']:>7} | {status}")

with open("rvr_report.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["distance", "rssi", "throughput", "latency", "packet_loss", "status"])
    writer.writeheader()
    writer.writerows(test_data)

print("-" * 75)
print("CSV report generated: rvr_report.csv")
