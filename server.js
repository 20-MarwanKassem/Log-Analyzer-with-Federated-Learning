const express = require('express');
const cors = require('cors');
const path = require('path');
const userRoutes = require('./routes/userRoutes');
const logRoutes = require('./routes/logRoutes');
const deviceRoutes = require('./routes/deviceRoutes');
const contactRoutes = require('./routes/contactRoutes');
const { createUsersTable } = require('./models/userModel');
const { createLogsTable } = require('./models/logModel');
const { createContactTable } = require('./models/contactModel');
const db = require('./models/db');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Route to check if server is running
app.get('/api/status', (req, res) => {
  res.json({ status: 'Server is running' });
});

// Initialize database and tables
const initializeDatabase = async () => {
  try {
    // First initialize the database connection
    await db.initializeDatabase();
    console.log('Database connected successfully!');

    // Create tables in sequence
    await createUsersTable();
    await createLogsTable();
    await createContactTable();
    
    console.log('Database tables initialized');
    
    // Start the server only after database is ready
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
    console.error('Error initializing application:', error);
    process.exit(1);
  }
};

// API Routes
app.use('/api/users', userRoutes);
app.use('/api/logs', logRoutes);
app.use('/api/devices', deviceRoutes);
app.use('/api/contact', contactRoutes);

// Serve static files from the downloads directory
// This makes the downloads folder accessible at /downloads URL path
app.use('/downloads', express.static(path.join(__dirname, 'Front-End/public/downloads')));

// Serve static files from the React frontend app
app.use(express.static(path.join(__dirname, 'Front-End/dist')));

// Anything that doesn't match the above, send back the index.html file
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'Front-End/dist/index.html'));
});

// Start the application
initializeDatabase();

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  console.log('UNHANDLED REJECTION! 💥 Shutting down...');
  console.log(err.name, err.message);
  process.exit(1);
}); 