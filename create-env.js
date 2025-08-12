const fs = require('fs');

const envFileContent = `DB_USER=postgres
DB_HOST=localhost
DB_NAME=log_analyzer
DB_PASSWORD=logai
DB_PORT=5432`;

fs.writeFileSync('.env', envFileContent);

console.log('.env file created successfully'); 