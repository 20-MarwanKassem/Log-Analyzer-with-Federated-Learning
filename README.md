# Log Analyzer

A full-stack application for monitoring network devices and analyzing logs to detect anomalies.

## Features

- User authentication (register/login)
- Dashboard with device monitoring
- Detailed log analysis
- Anomaly detection
- Risk status calculation
- Responsive UI for desktop and mobile

## Tech Stack

### Backend
- Node.js
- Express.js
- PostgreSQL
- JSON Web Tokens for authentication

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- Shadcn UI
- Recharts for data visualization
- React Router for navigation
- Axios for API requests

## Local Development

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   cd Front-End
   npm install
   ```
3. Set up environment variables (copy env.example to .env)
4. Initialize the database:
   ```
   node scripts/create-tables.js
   ```
5. Start the backend:
   ```
   npm start
   ```
6. Start the frontend:
   ```
   cd Front-End
   npm run dev
   ```

## Deploying to Vercel

### Prerequisites
- Vercel account
- PostgreSQL database (can use services like Supabase, Neon, or ElephantSQL)

### Deployment Steps

1. Fork/clone this repository to your GitHub account
2. Connect your GitHub repository to Vercel
3. Configure the following environment variables in Vercel:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `JWT_SECRET`: Secret key for JWT token generation
   - `NODE_ENV`: Set to "production"
4. Deploy the project
5. After deployment, run the database initialization script:
   ```
   node scripts/create-tables.js
   ```

## Database Schema

- **users**: User accounts and authentication
- **logs**: Device logs with anomaly status
- **contact**: Contact form submissions

## License

MIT # Log-Analyzer-with-Federated-Learning
