const { Pool } = require('pg');
require('dotenv').config();

const dbConfig = {
  user: process.env.DB_USER || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'log_analyzer',
  password: process.env.DB_PASSWORD || 'logai',
  port: process.env.DB_PORT || 5432,
};

const pool = new Pool(dbConfig);

async function updateLogStatuses() {
  try {
    // First, let's insert some sample data
    await pool.query(`
      INSERT INTO logs (user_id, device_name, device_mac, device_ip, log, status, time) VALUES
      (1, 'Workstation-01', '00:1B:44:11:3A:B7', '192.168.1.10', 'Login successful', 'non-anomaly', '2025-01-03 08:12:32'),
      (1, 'Workstation-01', '00:1B:44:11:3A:B7', '192.168.1.10', 'Port scan detected', 'anomaly', '2025-01-04 13:22:10'),
      (1, 'Server-01', '00:1B:44:11:3A:B8', '192.168.1.20', 'Failed login attempt', 'anomaly', '2025-02-15 18:45:09'),
      (1, 'Server-01', '00:1B:44:11:3A:B8', '192.168.1.20', 'Antivirus updated', 'non-anomaly', '2025-02-20 09:17:55'),
      (1, 'Workstation-02', '00:1B:44:11:3A:B9', '192.168.1.11', 'Firewall rule added', 'non-anomaly', '2025-03-01 14:30:44'),
      (1, 'Workstation-02', '00:1B:44:11:3A:B9', '192.168.1.11', 'Multiple failed logins', 'anomaly', '2025-03-10 07:12:12'),
      (1, 'Workstation-03', '00:1B:44:11:3A:BA', '192.168.1.12', 'Unusual traffic pattern detected', 'anomaly', '2025-04-05 22:47:39'),
      (1, 'Server-02', '00:1B:44:11:3A:BB', '192.168.1.21', 'Log cleared by admin', 'anomaly', '2025-04-20 12:05:03'),
      (1, 'Workstation-04', '00:1B:44:11:3A:BC', '192.168.1.13', 'Software installed', 'non-anomaly', '2025-05-02 16:21:09'),
      (1, 'Workstation-04', '00:1B:44:11:3A:BC', '192.168.1.13', 'System rebooted', 'non-anomaly', '2025-05-10 03:33:25'),

      (2, 'Laptop-01', '00:1B:44:11:3A:C1', '10.0.0.5', 'Login successful', 'non-anomaly', '2025-01-05 08:45:11'),
      (2, 'Laptop-01', '00:1B:44:11:3A:C1', '10.0.0.5', 'Suspicious IP connection', 'anomaly', '2025-01-15 12:01:48'),
      (2, 'Desktop-01', '00:1B:44:11:3A:C2', '10.0.0.6', 'Failed login attempt', 'anomaly', '2025-02-12 14:23:56'),
      (2, 'Desktop-01', '00:1B:44:11:3A:C2', '10.0.0.6', 'Antivirus updated', 'non-anomaly', '2025-02-28 09:17:02'),
      (2, 'Laptop-02', '00:1B:44:11:3A:C3', '10.0.0.7', 'Firewall configuration changed', 'anomaly', '2025-03-08 22:15:33'),
      (2, 'Laptop-02', '00:1B:44:11:3A:C3', '10.0.0.7', 'System rebooted', 'non-anomaly', '2025-03-15 18:22:10'),
      (2, 'Desktop-02', '00:1B:44:11:3A:C4', '10.0.0.8', 'Multiple failed logins', 'anomaly', '2025-04-01 07:11:56'),
      (2, 'Desktop-02', '00:1B:44:11:3A:C4', '10.0.0.8', 'Software installed', 'non-anomaly', '2025-04-12 10:44:22'),
      (2, 'Server-03', '00:1B:44:11:3A:C5', '10.0.0.9', 'Admin privileges escalated', 'anomaly', '2025-05-03 13:55:09'),
      (2, 'Server-03', '00:1B:44:11:3A:C5', '10.0.0.9', 'Antivirus scan completed', 'non-anomaly', '2025-05-15 06:29:49'),

      (3, 'Node-01', '00:1B:44:11:3A:D1', '172.16.0.1', 'Port scan detected', 'anomaly', '2025-01-20 14:40:01'),
      (3, 'Node-01', '00:1B:44:11:3A:D1', '172.16.0.1', 'System rebooted', 'non-anomaly', '2025-01-23 08:15:25'),
      (3, 'Node-02', '00:1B:44:11:3A:D2', '172.16.0.2', 'Unauthorized file access', 'anomaly', '2025-02-14 21:03:59'),
      (3, 'Node-02', '00:1B:44:11:3A:D2', '172.16.0.2', 'Login successful', 'non-anomaly', '2025-02-16 06:22:35'),
      (3, 'Server-04', '00:1B:44:11:3A:D3', '172.16.0.3', 'Suspicious outbound traffic', 'anomaly', '2025-03-05 11:33:42'),
      (3, 'Server-04', '00:1B:44:11:3A:D3', '172.16.0.3', 'System backup completed', 'non-anomaly', '2025-03-10 15:55:18'),
      (3, 'Node-03', '00:1B:44:11:3A:D4', '172.16.0.4', 'Malware detected', 'anomaly', '2025-04-02 19:28:33'),
      (3, 'Node-03', '00:1B:44:11:3A:D4', '172.16.0.4', 'Security patch installed', 'non-anomaly', '2025-04-05 08:40:15'),
      (3, 'Server-05', '00:1B:44:11:3A:D5', '172.16.0.5', 'Brute force attack detected', 'anomaly', '2025-05-01 02:15:50'),
      (3, 'Server-05', '00:1B:44:11:3A:D5', '172.16.0.5', 'System maintenance completed', 'non-anomaly', '2025-05-05 10:05:27')
    `);

    console.log('Sample log data inserted successfully');
    await pool.end();
    
  } catch (error) {
    console.error('Error updating log statuses:', error);
  }
}

updateLogStatuses(); 