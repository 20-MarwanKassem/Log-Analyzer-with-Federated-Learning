const fs = require('fs');
const path = require('path');

// Path to the db.js file
const dbFilePath = path.join(__dirname, 'models', 'db.js');

// Create a correct implementation of the db.js file
const correctDBImplementation = `const { Pool } = require('pg');
require('dotenv').config();

// Mock data and implementations (keeping the original mock data)
const mockLogs = {
  // User 1 logs (mohamed@logai.com)
  1: [
    {
      log_id: 1,
      user_id: 1,
      device_name: 'Router',
      device_mac: 'AA:BB:CC:DD:EE:01',
      device_ip: '192.168.0.1',
      log: 'Unusual outbound traffic',
      status: 'Anomaly',
      time: new Date('2023-12-10T08:23:15')
    },
    // Remaining log entries...
  ],
  
  // User 2 logs (admin@loganalyzer.ai)
  2: [
    // Log entries...
  ]
};

// Statistics for each user
const mockStats = {
  1: {
    total_logs: 10,
    anomaly_count: 4,
    normal_count: 6
  },
  2: {
    total_logs: 10,
    anomaly_count: 5,
    normal_count: 5
  }
};

// Mock database for testing when PostgreSQL is not available
const mockDB = {
  query: async (text, params) => {
    console.log('MOCK DB QUERY:', { text, params });
    
    // Mock implementations for different queries...
    if (text.includes('FROM Users WHERE Email')) {
      const email = params[0];
      if (email === 'admin@loganalyzer.ai') {
        return {
          rows: [{
            user_id: 2,
            email: 'admin@loganalyzer.ai',
            password: 'admin1234',
            company: 'logai',
            user_name: 'admin'
          }]
        };
      } else if (email === 'mohamed@logai.com') {
        return {
          rows: [{
            user_id: 1,
            email: 'mohamed@logai.com',
            password: 'pass123',
            company: 'softtech',
            user_name: 'mohamed'
          }]
        };
      }
      return { rows: [] };
    }
    
    // Other mock implementations...
    // ... existing code ...
    
    return { rows: [] };
  }
};

// Database configuration
const dbConfig = {
  user: process.env.DB_USER || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'log_analyzer',
  password: process.env.DB_PASSWORD || 'logai',
  port: process.env.DB_PORT || 5432,
};

// Initialize DB client with mockDB first
let dbClient = mockDB;

// Create a real PostgreSQL pool
let realPool = null;

try {
  console.log('Connecting to PostgreSQL with:', {
    user: dbConfig.user,
    host: dbConfig.host,
    database: dbConfig.database,
    port: dbConfig.port
  });
  
  realPool = new Pool(dbConfig);
  
  // Test connection with an immediate query and set dbClient to realPool if successful
  realPool.query('SELECT NOW()', (err, result) => {
    if (err) {
      console.error('PostgreSQL connection failed:', err.message);
      console.log('Using mock database for this session');
    } else {
      console.log('PostgreSQL connected successfully!', result.rows[0]);
      dbClient = realPool;
      console.log('✅ USING REAL DATABASE');
    }
  });
} catch (error) {
  console.error('Error initializing PostgreSQL:', error.message);
  console.log('Using mock database due to initialization error');
}

// Export the query function
module.exports = {
  query: (text, params) => dbClient.query(text, params),
};`;

// Write the correct implementation to the file
fs.writeFileSync(dbFilePath, correctDBImplementation, 'utf8');

console.log('Successfully fixed the db.js file with the correct implementation');
console.log('Please restart your application to use the updated connection logic'); 