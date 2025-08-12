import csv
import random
import datetime
import os

# Ensure the output directory exists
os.makedirs("test_data", exist_ok=True)

# Create sample log data
logs = [
    {"user_id": 1, "device_name": "Workstation-05", "device_mac": "00:1B:44:11:3A:F1", "device_ip": "192.168.1.15", "log": "Multiple authentication failures detected", "time": "2025-06-01 09:23:45"},
    {"user_id": 1, "device_name": "Workstation-05", "device_mac": "00:1B:44:11:3A:F1", "device_ip": "192.168.1.15", "log": "System update completed successfully", "time": "2025-06-01 10:15:22"},
    {"user_id": 2, "device_name": "Server-06", "device_mac": "00:1B:44:11:3A:F2", "device_ip": "192.168.1.30", "log": "Unusual outbound traffic pattern detected", "time": "2025-06-02 14:27:33"},
    {"user_id": 2, "device_name": "Server-06", "device_mac": "00:1B:44:11:3A:F2", "device_ip": "192.168.1.30", "log": "Database backup completed", "time": "2025-06-02 22:05:11"},
    {"user_id": 3, "device_name": "Laptop-05", "device_mac": "00:1B:44:11:3A:F3", "device_ip": "192.168.1.45", "log": "Malware signature detected in downloaded file", "time": "2025-06-03 16:42:19"},
    {"user_id": 3, "device_name": "Laptop-05", "device_mac": "00:1B:44:11:3A:F3", "device_ip": "192.168.1.45", "log": "User login successful", "time": "2025-06-03 08:30:05"},
    {"user_id": 1, "device_name": "Router-01", "device_mac": "00:1B:44:11:3A:F4", "device_ip": "192.168.1.1", "log": "Port scan blocked from external IP 45.132.55.23", "time": "2025-06-04 03:17:29"},
    {"user_id": 2, "device_name": "Firewall-01", "device_mac": "00:1B:44:11:3A:F5", "device_ip": "192.168.1.2", "log": "Rule update applied successfully", "time": "2025-06-04 13:05:44"}
]

# Write to CSV
with open("test_data/sample_logs.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["user_id", "device_name", "device_mac", "device_ip", "log", "time"])
    writer.writeheader()
    writer.writerows(logs)

print("Test CSV file created: test_data/sample_logs.csv") 