const { Pool } = require('pg');
require('dotenv').config();

// Get database configuration from .env file
const dbConfig = {
  user: process.env.DB_USER || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'log_analyzer',
  password: process.env.DB_PASSWORD || 'logai',
  port: process.env.DB_PORT || 5432,
};

console.log('Attempting to connect to PostgreSQL with:');
console.log('User:', dbConfig.user);
console.log('Host:', dbConfig.host);
console.log('Database:', dbConfig.database);
console.log('Port:', dbConfig.port);
console.log('Password:', '*******'); // Not showing for security

// Create a new pool
const pool = new Pool(dbConfig);

// Test the connection
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('PostgreSQL connection failed:', err.message);
  } else {
    console.log('PostgreSQL connected successfully!');
    console.log('Current time from database:', res.rows[0].now);
    
    // Try to create a test table
    pool.query(`
      CREATE TABLE IF NOT EXISTS test_connection (
        id SERIAL PRIMARY KEY,
        test_column VARCHAR(255)
      )
    `, (err, res) => {
      if (err) {
        console.error('Failed to create test table:', err.message);
      } else {
        console.log('Test table created or already exists!');
      }
      
      // Close the connection
      pool.end();
    });
  }
}); 