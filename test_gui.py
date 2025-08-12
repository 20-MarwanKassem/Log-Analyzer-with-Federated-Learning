import os
import pandas as pd
import random
import argparse
from datetime import datetime, timedelta

def generate_test_data(num_rows=50, output_file="test_logs.csv"):
    """Generate test log data for GUI testing"""
    
    # Sample devices
    devices = [
        {"name": "Workstation-01", "ip": "192.168.1.101", "mac": "00:1B:44:11:3A:B7"},
        {"name": "Workstation-02", "ip": "192.168.1.102", "mac": "00:1B:44:11:3A:C9"},
        {"name": "Server-01", "ip": "192.168.1.10", "mac": "00:1B:63:84:45:E6"}
    ]
    
    # Sample log templates
    normal_logs = [
        "System started normally",
        "User logged in successfully",
        "Backup completed successfully",
        "Software update check completed",
        "Network connection established",
        "File sync completed",
        "System scan completed: no threats found",
        "Memory usage normal",
        "CPU usage normal",
        "Disk check completed successfully"
    ]
    
    anomaly_logs = [
        "Failed login attempt detected",
        "Unusual network traffic detected",
        "System error: service failed to start",
        "Memory usage exceeds threshold",
        "Potential malware detected",
        "Firewall breach attempt detected",
        "Unexpected system shutdown",
        "CPU usage critical",
        "Multiple authentication failures detected",
        "Unusual process activity detected"
    ]
    
    # Create data
    data = []
    start_time = datetime.now() - timedelta(days=1)
    
    for i in range(num_rows):
        # Select a random device
        device = random.choice(devices)
        
        # 70% normal logs, 30% anomaly logs
        if random.random() < 0.7:
            log = random.choice(normal_logs)
        else:
            log = random.choice(anomaly_logs)
        
        # Generate a timestamp
        log_time = start_time + timedelta(minutes=random.randint(1, 1440))
        
        # Create the entry
        entry = {
            "user_id": random.randint(1, 3),
            "device_name": device["name"],
            "device_mac": device["mac"],
            "device_ip": device["ip"],
            "time": log_time.strftime("%Y-%m-%d %H:%M:%S"),
            "log": log
        }
        
        data.append(entry)
    
    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Generated {num_rows} test log entries in '{output_file}'")

def run_gui_test():
    """Start the GUI application for testing"""
    print("Starting Log Analyzer GUI...")
    try:
        # Generate test data
        generate_test_data()
        
        # Import and run the GUI
        # Note: We import here to avoid circular import if this module gets imported elsewhere
        from log_analyzer_gui import main
        main()
    except Exception as e:
        print(f"Error starting GUI: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Log Analyzer GUI")
    parser.add_argument("--data-only", action="store_true", help="Only generate test data, don't launch the GUI")
    parser.add_argument("--rows", type=int, default=50, help="Number of log rows to generate")
    parser.add_argument("--output", type=str, default="test_logs.csv", help="Output CSV file")
    
    args = parser.parse_args()
    
    if args.data_only:
        generate_test_data(args.rows, args.output)
    else:
        run_gui_test() 