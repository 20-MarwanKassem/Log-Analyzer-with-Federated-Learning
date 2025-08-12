-- Test data for Log Analyzer application

-- Insert test users
INSERT INTO Users (Email, Password, Company, User_Name) VALUES 
('mohamed@logai.com', 'pass123', 'softtech', 'mohamed'),
('admin@loganalyzer.ai', 'admin1234', 'logai', 'admin'),
('mohamedtarek@eagle.ai', 'E12345@#', 'Eagle', 'mohamed'),
('George_waston@microsft.com', 'mic12345%$', 'microsoft', 'George');

-- Get the User IDs for reference (these will be used in the log entries)
-- User 1: mohamed@logai.com
-- User 2: admin@loganalyzer.ai
-- User 3: mohamedtarek@eagle.ai
-- User 4: George_waston@microsft.com

-- Insert logs for User 1 (mohamed@logai.com)
INSERT INTO Logs (User_ID, Device_Name, Device_MAC, Device_IP, Log, Status, Time) VALUES
(1, 'Device A', 'AA:BB:CC:DD:EE:01', '192.168.0.101', 'Port scan detected', 'Anomaly', '2025-04-29 12:45:00'),
(1, 'Device A', 'AA:BB:CC:DD:EE:01', '192.168.0.101', 'Normal access', 'Normal', '2025-04-29 13:05:00'),
(1, 'Device A', 'AA:BB:CC:DD:EE:01', '192.168.0.101', 'Suspicious login', 'Anomaly', '2025-04-29 13:25:00'),
(1, 'Device A', 'AA:BB:CC:DD:EE:01', '192.168.0.101', 'System heartbeat', 'Normal', '2025-04-29 14:10:00'),
(1, 'Device C', '77:88:99:AA:BB:CC', '172.16.23.8', 'System startup', 'Normal', '2025-04-29 09:15:00'),
(1, 'Device C', '77:88:99:AA:BB:CC', '172.16.23.8', 'Scheduled backup', 'Normal', '2025-04-29 10:05:00');

-- Insert logs for User 2 (admin@loganalyzer.ai)
INSERT INTO Logs (User_ID, Device_Name, Device_MAC, Device_IP, Log, Status, Time) VALUES
(2, 'Device B', '11:22:33:44:55:66', '10.0.0.55', 'Suspicious login attempt', 'Anomaly', '2025-04-29 10:15:00'),
(2, 'Device B', '11:22:33:44:55:66', '10.0.0.55', 'File access violation', 'Anomaly', '2025-04-29 10:25:00'),
(2, 'Device B', '11:22:33:44:55:66', '10.0.0.55', 'Normal system update', 'Normal', '2025-04-29 11:30:00'),
(2, 'Device B', '11:22:33:44:55:66', '10.0.0.55', 'Firewall rule triggered', 'Anomaly', '2025-04-29 12:45:00'),
(2, 'Device D', 'DE:AD:BE:EF:CA:FE', '192.168.1.42', 'Malware detected', 'Anomaly', '2025-04-29 08:30:00'),
(2, 'Device D', 'DE:AD:BE:EF:CA:FE', '192.168.1.42', 'Suspicious outbound connection', 'Anomaly', '2025-04-29 09:05:00');

-- Insert logs for User 3 (mohamedtarek@eagle.ai)
INSERT INTO Logs (User_ID, Device_Name, Device_MAC, Device_IP, Log, Status, Time) VALUES
(3, 'Server 1', 'FF:AA:BB:CC:DD:EE', '10.10.10.1', 'CPU usage spike', 'Anomaly', '2025-04-29 15:22:00'),
(3, 'Server 1', 'FF:AA:BB:CC:DD:EE', '10.10.10.1', 'Database backup complete', 'Normal', '2025-04-29 16:05:00'),
(3, 'Server 1', 'FF:AA:BB:CC:DD:EE', '10.10.10.1', 'Multiple login attempts', 'Anomaly', '2025-04-29 16:45:00'),
(3, 'Workstation 5', 'CC:DD:EE:FF:00:11', '10.10.10.25', 'Software update', 'Normal', '2025-04-29 14:30:00'),
(3, 'Workstation 5', 'CC:DD:EE:FF:00:11', '10.10.10.25', 'Antivirus updated', 'Normal', '2025-04-29 14:35:00'),
(3, 'Workstation 5', 'CC:DD:EE:FF:00:11', '10.10.10.25', 'Unusual file execution', 'Anomaly', '2025-04-29 17:10:00');

-- Insert logs for User 4 (George_waston@microsft.com)
INSERT INTO Logs (User_ID, Device_Name, Device_MAC, Device_IP, Log, Status, Time) VALUES
(4, 'Laptop W23', '00:1A:2B:3C:4D:5E', '192.168.5.10', 'VPN connection', 'Normal', '2025-04-29 07:15:00'),
(4, 'Laptop W23', '00:1A:2B:3C:4D:5E', '192.168.5.10', 'RDP connection attempt', 'Anomaly', '2025-04-29 07:45:00'),
(4, 'Laptop W23', '00:1A:2B:3C:4D:5E', '192.168.5.10', 'Password changed', 'Normal', '2025-04-29 08:30:00'),
(4, 'Network Switch', '66:77:88:99:AA:BB', '192.168.0.254', 'Port flapping', 'Anomaly', '2025-04-29 13:10:00'),
(4, 'Network Switch', '66:77:88:99:AA:BB', '192.168.0.254', 'High bandwidth usage', 'Anomaly', '2025-04-29 13:25:00'),
(4, 'Network Switch', '66:77:88:99:AA:BB', '192.168.0.254', 'Routing table updated', 'Normal', '2025-04-29 14:00:00'); 