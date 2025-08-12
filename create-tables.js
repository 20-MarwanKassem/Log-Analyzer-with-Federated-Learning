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

console.log('Connecting to PostgreSQL database to create tables...');
const pool = new Pool(dbConfig);

// SQL for creating all tables
const createTableSQL = `
-- Create users table with lowercase name (PostgreSQL convention)
CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  company VARCHAR(255),
  user_name VARCHAR(255) NOT NULL
);

-- Create logs table
CREATE TABLE IF NOT EXISTS logs (
  log_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
  device_name VARCHAR(255),
  device_mac VARCHAR(255),
  device_ip VARCHAR(255),
  log TEXT,
  status VARCHAR(50),
  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create contact table
CREATE TABLE IF NOT EXISTS contact (
  message_id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  message TEXT NOT NULL
);

-- Insert admin user
INSERT INTO users (email, password, company, user_name)
VALUES ('admin@loganalyzer.ai', 'admin1234', 'logai', 'admin')
ON CONFLICT (email) DO NOTHING;

-- Insert sample user
INSERT INTO users (email, password, company, user_name)
VALUES ('mohamed@logai.com', 'pass123', 'softtech', 'mohamed')
ON CONFLICT (email) DO NOTHING;
`;

async function createTables() {
  try {
    await pool.query(createTableSQL);
    console.log('✅ All tables created successfully!');
    
    // Verify tables were created
    const tables = await pool.query(
      "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    );
    console.log('\nDatabase tables:');
    tables.rows.forEach(table => {
      console.log(`- ${table.table_name}`);
    });
    
    // Check users
    const users = await pool.query('SELECT email, user_name FROM users');
    console.log('\nUsers in database:');
    users.rows.forEach(user => {
      console.log(`- ${user.email} (${user.user_name})`);
    });
    
  } catch (error) {
    console.error('Error creating tables:', error);
  } finally {
    pool.end();
  }
}

createTables(); 