// Script to insert test data into the database

const userModel = require('./models/userModel');
const logModel = require('./models/logModel');
const db = require('./models/db');

// Test users data
const testUsers = [
  { email: 'mohamed@logai.com', password: 'pass123', company: 'softtech', userName: 'mohamed' },
  { email: 'admin@loganalyzer.ai', password: 'admin1234', company: 'logai', userName: 'admin' },
  { email: 'mohamedtarek@eagle.ai', password: 'E12345@#', company: 'Eagle', userName: 'mohamed' },
  { email: 'George_waston@microsft.com', password: 'mic12345%$', company: 'microsoft', userName: 'George' }
];

// Test logs data grouped by device
const testLogs = [
  // Device A logs for User 1
  {
    userId: 1,
    deviceName: 'Device A',
    deviceMAC: 'AA:BB:CC:DD:EE:01',
    deviceIP: '192.168.0.101',
    logs: [
      { log: 'Port scan detected', status: 'Anomaly', time: '2025-04-29 12:45:00' },
      { log: 'Normal access', status: 'Normal', time: '2025-04-29 13:05:00' },
      { log: 'Suspicious login', status: 'Anomaly', time: '2025-04-29 13:25:00' },
      { log: 'System heartbeat', status: 'Normal', time: '2025-04-29 14:10:00' }
    ]
  },
  // Device C logs for User 1
  {
    userId: 1,
    deviceName: 'Device C',
    deviceMAC: '77:88:99:AA:BB:CC',
    deviceIP: '172.16.23.8',
    logs: [
      { log: 'System startup', status: 'Normal', time: '2025-04-29 09:15:00' },
      { log: 'Scheduled backup', status: 'Normal', time: '2025-04-29 10:05:00' }
    ]
  },
  // Device B logs for User 2
  {
    userId: 2,
    deviceName: 'Device B',
    deviceMAC: '11:22:33:44:55:66',
    deviceIP: '10.0.0.55',
    logs: [
      { log: 'Suspicious login attempt', status: 'Anomaly', time: '2025-04-29 10:15:00' },
      { log: 'File access violation', status: 'Anomaly', time: '2025-04-29 10:25:00' },
      { log: 'Normal system update', status: 'Normal', time: '2025-04-29 11:30:00' },
      { log: 'Firewall rule triggered', status: 'Anomaly', time: '2025-04-29 12:45:00' }
    ]
  },
  // Device D logs for User 2
  {
    userId: 2,
    deviceName: 'Device D',
    deviceMAC: 'DE:AD:BE:EF:CA:FE',
    deviceIP: '192.168.1.42',
    logs: [
      { log: 'Malware detected', status: 'Anomaly', time: '2025-04-29 08:30:00' },
      { log: 'Suspicious outbound connection', status: 'Anomaly', time: '2025-04-29 09:05:00' }
    ]
  },
  // Server 1 logs for User 3
  {
    userId: 3,
    deviceName: 'Server 1',
    deviceMAC: 'FF:AA:BB:CC:DD:EE',
    deviceIP: '10.10.10.1',
    logs: [
      { log: 'CPU usage spike', status: 'Anomaly', time: '2025-04-29 15:22:00' },
      { log: 'Database backup complete', status: 'Normal', time: '2025-04-29 16:05:00' },
      { log: 'Multiple login attempts', status: 'Anomaly', time: '2025-04-29 16:45:00' }
    ]
  },
  // Workstation 5 logs for User 3
  {
    userId: 3,
    deviceName: 'Workstation 5',
    deviceMAC: 'CC:DD:EE:FF:00:11',
    deviceIP: '10.10.10.25',
    logs: [
      { log: 'Software update', status: 'Normal', time: '2025-04-29 14:30:00' },
      { log: 'Antivirus updated', status: 'Normal', time: '2025-04-29 14:35:00' },
      { log: 'Unusual file execution', status: 'Anomaly', time: '2025-04-29 17:10:00' }
    ]
  },
  // Laptop W23 logs for User 4
  {
    userId: 4,
    deviceName: 'Laptop W23',
    deviceMAC: '00:1A:2B:3C:4D:5E',
    deviceIP: '192.168.5.10',
    logs: [
      { log: 'VPN connection', status: 'Normal', time: '2025-04-29 07:15:00' },
      { log: 'RDP connection attempt', status: 'Anomaly', time: '2025-04-29 07:45:00' },
      { log: 'Password changed', status: 'Normal', time: '2025-04-29 08:30:00' }
    ]
  },
  // Network Switch logs for User 4
  {
    userId: 4,
    deviceName: 'Network Switch',
    deviceMAC: '66:77:88:99:AA:BB',
    deviceIP: '192.168.0.254',
    logs: [
      { log: 'Port flapping', status: 'Anomaly', time: '2025-04-29 13:10:00' },
      { log: 'High bandwidth usage', status: 'Anomaly', time: '2025-04-29 13:25:00' },
      { log: 'Routing table updated', status: 'Normal', time: '2025-04-29 14:00:00' }
    ]
  }
];

// Custom function to insert log with timestamp
async function insertLogWithTime(userId, deviceName, deviceMAC, deviceIP, log, status, timestamp) {
  try {
    const query = `
      INSERT INTO Logs (User_ID, Device_Name, Device_MAC, Device_IP, Log, Status, Time) 
      VALUES ($1, $2, $3, $4, $5, $6, $7) 
      RETURNING *
    `;
    const result = await db.query(query, [userId, deviceName, deviceMAC, deviceIP, log, status, timestamp]);
    return result.rows[0];
  } catch (error) {
    console.error('Error inserting log with timestamp:', error);
    throw error;
  }
}

// Main function to insert test data
async function insertTestData() {
  try {
    console.log('Starting test data insertion...');
    
    // Create Users table if it doesn't exist
    await userModel.createUsersTable();
    
    // Create Logs table if it doesn't exist
    await logModel.createLogsTable();
    
    // Insert test users
    console.log('Inserting test users...');
    for (const user of testUsers) {
      try {
        await userModel.createUser(user.email, user.password, user.company, user.userName);
        console.log(`User created: ${user.email}`);
      } catch (err) {
        // Skip if user already exists (email unique constraint)
        console.log(`User ${user.email} may already exist, skipping.`);
      }
    }
    
    // Insert test logs
    console.log('Inserting test logs...');
    for (const device of testLogs) {
      for (const logEntry of device.logs) {
        try {
          await insertLogWithTime(
            device.userId,
            device.deviceName,
            device.deviceMAC,
            device.deviceIP,
            logEntry.log,
            logEntry.status,
            logEntry.time
          );
          console.log(`Log created for device ${device.deviceName} (User ID: ${device.userId}): ${logEntry.log}`);
        } catch (err) {
          console.error(`Error inserting log for device ${device.deviceName}:`, err.message);
        }
      }
    }
    
    console.log('Test data insertion completed successfully!');
    
    // Exit the process after completion
    process.exit(0);
  } catch (error) {
    console.error('Error during test data insertion:', error);
    process.exit(1);
  }
}

// Run the insertion function
insertTestData(); 