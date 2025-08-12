# Log Analyzer Test Data Setup Instructions

To add test users and device log data to your PostgreSQL database for the Log Analyzer application, follow these steps:

## 1. Database Configuration

First, create a `.env` file in the root directory with your PostgreSQL credentials:

```
# Database credentials
DB_USER=postgres
DB_HOST=localhost
DB_NAME=log_analyzer
DB_PASSWORD=your_password_here
DB_PORT=5432
```

Replace `your_password_here` with your actual PostgreSQL password.

## 2. Option 1: Insert Test Data with Script

After setting up your `.env` file, you can run the script to insert test data:

```
node insert-test-data.js
```

## 3. Option 2: Manual SQL Insertion

If the script approach doesn't work, you can manually execute the SQL statements:

1. Connect to your PostgreSQL database:
   ```
   psql -U postgres -d log_analyzer
   ```
   (Enter your password when prompted)

2. Run the SQL commands from the `test-data.sql` file:
   ```sql
   -- Insert test users
   INSERT INTO Users (Email, Password, Company, User_Name) VALUES 
   ('mohamed@logai.com', 'pass123', 'softtech', 'mohamed'),
   ('admin@loganalyzer.ai', 'admin1234', 'logai', 'admin'),
   ('mohamedtarek@eagle.ai', 'E12345@#', 'Eagle', 'mohamed'),
   ('George_waston@microsft.com', 'mic12345%$', 'microsoft', 'George');

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
   ```

## 4. Option 3: pgAdmin Interface

If you prefer a graphical interface:

1. Open pgAdmin
2. Connect to your database server
3. Create or select the `log_analyzer` database
4. Open the Query Tool
5. Paste the SQL commands from the `test-data.sql` file
6. Execute the query

## 5. Testing

After inserting the test data, you can test the application:

1. Start the backend server:
   ```
   node server.js
   ```

2. Start the frontend:
   ```
   cd Front-End
   npm start
   ```

3. Log in with any of the test user credentials:
   - Email: `mohamed@logai.com`, Password: `pass123`
   - Email: `admin@loganalyzer.ai`, Password: `admin1234`
   - Email: `mohamedtarek@eagle.ai`, Password: `E12345@#`
   - Email: `George_waston@microsft.com`, Password: `mic12345%$`

4. Navigate to the Dashboard to see the devices and device details 