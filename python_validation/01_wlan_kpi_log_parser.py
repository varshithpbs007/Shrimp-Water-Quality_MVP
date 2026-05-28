"""
PROJECT: WLAN KPI Log parser and CSV report generator

DESCRIPTION:

* This script simulates WLAN validation log analysis for an ESP32-based smart aquaculture IoT system

* Since the project so far is implemented and validated using wokwi simulation, real router, driver, iperf, or packet-capture logs are NOT available.

* Therefore simulated WLAN KPI logs are used to demonstrate Python-based validation automation flow.

  The script performs the following operations in order:
  
  1. A Regex pattern is developed, which matches the log pattern which contains the key KPIs.
  2. It parses the simulated WLAN KPI logs using Regular Expressions (Regex)
  3. Then it extracts imp KPIs like: RSSI, MCS Index, PHY rate, TCP throughput, Latency, Retry rate, using re.findall() to extract multiple WLAN test points from logs
  4. Stores the extracted KPIs into dedicated lists which are individually used for: averaging, worst-case analysis, and reporting.
  5. Applies threshold-based validation logic to classify each test point as: PASS/ WARNING / FAIL
  6. Generates a CSV validation report using csv.DictWriter()
  
"""



import re #pythons "regular expression" library, we use it to search patterns inside text logs
import csv #pythons built-in library for writing .csv files, which can be opened in excel

#mutli-line string containing many simulated WLAN log lines
#This automation flow can be applied to real-router, driver, iperf, or packet-capture logs

print("Sample log:\n")
sample_log = """
[10:00:01] DEVICE=ESP32_AQUA RSSI=-42 dBm MCS=9 PHY_RATE=1201 Mbps TCP_THROUGHPUT=845 Mbps LATENCY=12 ms RETRY=3% MQTT_publish=SUCCESS 
[10:00:01] DEVICE=ESP32_AQUA RSSI=-55 dBm MCS=7 PHY_RATE=864 Mbps TCP_THROUGHPUT=620 Mbps LATENCY=18 ms RETRY=7% MQTT_publish=SUCCESS
[10:00:01] DEVICE=ESP32_AQUA RSSI=-68 dBm MCS=5 PHY_RATE=432 Mbps TCP_THROUGHPUT=290 Mbps LATENCY=35 ms RETRY=15% MQTT_publish=SUCCESS
[10:00:01] DEVICE=ESP32_AQUA RSSI=-78 dBm MCS=3 PHY_RATE=144 Mbps TCP_THROUGHPUT=85 Mbps LATENCY=72 ms RETRY=31% MQTT_publish=FAIL
"""

print(sample_log)

#Regex pattern is used to search structured patterns inside text logs
#Regex extracts strings, so later while storing we convert a number to an integer
# re.search() finds only the first match, so we use re.findall() to find all matching lines and
# return them as a list

pattern = (
    r"RSSI=(-?\d+)\s*dBm\s*"
    r"MCS=(\d+)\s*"
    r"PHY_RATE=(\d+)\s*Mbps\s*"
    r"TCP_THROUGHPUT=(\d+)\s*Mbps\s*"
    r"LATENCY=(\d+)\s*ms\s*"
    r"RETRY=(\d+)%"
)

matches = re.findall(pattern, sample_log)


rssi_values = []
mcs_values = []
phy_rate_values =[]
tcp_throughput_values =[]
latency_values = []
retry_values = []

report_rows = []

print("ESP32 Aquaculture WLAN KPI Validation Report")
print("-"*90)

for index, match in enumerate(matches, start=1): 
    rssi = int(match[0])
    mcs = int(match[1])
    phy_rate = int(match[2])
    tcp_throughput = int(match[3])
    latency = int(match[4])
    retry = int(match[5])
    
    rssi_values.append(rssi)
    mcs_values.append(mcs)
    phy_rate_values.append(phy_rate)
    tcp_throughput_values.append(tcp_throughput)
    latency_values.append(latency)
    retry_values.append(retry)
    
   # Now every WLAN test point should be judged.
   # We use the following thresholds for that:
   # PASS ---> tcp_throughput > 500, Latency < 30, Retry < 10
   # WARNING ---> tcp_throughput > 150, Latency < 60, Retry < 25
   # FAIL ---> Anything worse
    
    if tcp_throughput > 500 and latency < 30 and retry < 10:
        status = "PASS"
    elif tcp_throughput > 150 and latency < 60 and retry < 25:
        status = "WARNING"
    else:
        status = "FAIL"
        
    report_rows.append({
        
     "test_point" : index,
     "rssi_dBm" : rssi,
     "mcs" : mcs,
     "phy_rate_Mbps" : phy_rate,
     "tcp_throughput_Mbps" : tcp_throughput,
     "latency_ms" : latency,
     "retry_percent" : retry,
     "status" : status
        
    })
    
    print(
        f"Test {index}: "
        f"RSSI={rssi} dBm | "
        f"MCS={mcs} | "
        f"PHY={phy_rate} Mbps | "
        f"Throughput={tcp_throughput} Mbps | "
        f"Latency={latency} ms | "
        f"Retry={retry} % | "
        f"Status={status}  "
    )
    
    print("-"*90)
    



if matches:
    print("Summary")
    print(f"Total Test Points : {len(matches)}")
    print(f"Average RSSI : {sum(rssi_values) / len(rssi_values):.2f} dBm")
    print(f"Average PHY rate : {sum(phy_rate_values) / len(phy_rate_values):.2f} Mbps")
    print(f"Average tcp rate : {sum(tcp_throughput_values) / len(tcp_throughput_values):.2f} Mbps")
    print(f"Average latency : {sum(latency_values) / len(latency_values):.2f} ms")
    print(f"Average Retry Rate : {sum(retry_values) / len(retry_values):.2f}%")
    print(f"Worst RSSI : {min(rssi_values)} dBm")
    print(f"Best Throughput : {max(tcp_throughput_values)} Mbps")
        
        
        
    with open("wlan_kpi_report.csv", "w" , newline="") as file:
        fieldnames =[
                "test_point",
                "rssi_dBm",
                "mcs",
                "phy_rate_Mbps",
                "tcp_throughput_Mbps",
                "latency_ms",
                "retry_percent",
                "status"
        ]
            
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_rows)
            
            
        print("\nCSV report generated as : wlan_kpi_report.csv")
        
        
else:
        print("No valid KPI logs found")











