const fs = require('fs');
const path = require('path');

// Path to the db.js file
const dbFilePath = path.join(__dirname, 'models', 'db.js');

// Read the current content of db.js
let dbFileContent = fs.readFileSync(dbFilePath, 'utf8');

// Replace the problematic part of the code
// The issue is that dbClient is initialized to mockDB and then it attempts to connect to PostgreSQL
// But never updates dbClient to the pool if successful

// Find the initialization section
const initializationPattern = /\/\/ Initialize DB client\r?\nlet dbClient;\r?\n\r?\n\/\/ Try to connect to PostgreSQL.*?\r?\n}/s;

// New initialization code
const newInitCode = `// Initialize DB client
let dbClient = mockDB; // Default to mock DB initially

// Create a PostgreSQL pool
const pool = new Pool({
  user: process.env.DB_USER || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'log_analyzer',
  password: process.env.DB_PASSWORD || 'logai',
  port: process.env.DB_PORT || 5432,
});

// Test the connection immediately
console.log('Attempting to connect to PostgreSQL...');
console.log('Database: log_analyzer, User: ' + (process.env.DB_USER || 'postgres') + ', Host: ' + (process.env.DB_HOST || 'localhost'));

// Switch to real pool if it connects successfully
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.log('PostgreSQL connection failed, using mock database:', err.message);
  } else {
    console.log('PostgreSQL connected successfully:', res.rows[0].now);
    dbClient = pool; // Update the dbClient to use the real database
    console.log('SWITCHED TO REAL DATABASE');
  }
})`;

// Replace the old code with the new code
if (initializationPattern.test(dbFileContent)) {
  dbFileContent = dbFileContent.replace(initializationPattern, newInitCode);
  
  // Write the updated content back to the file
  fs.writeFileSync(dbFilePath, dbFileContent, 'utf8');
  
  console.log('Successfully updated db.js with the new connection logic');
  console.log('Please restart your application to use the updated connection logic');
} else {
  console.log('Could not find the initialization pattern in db.js');
  console.log('Please manually update the file to fix the database connection issue');
} 