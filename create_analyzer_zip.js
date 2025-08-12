const fs = require('fs-extra');
const path = require('path');
const archiver = require('archiver');

// Create the zip file for the Log Analyzer tool
async function createLogAnalyzerZip() {
  const outputDir = path.join(__dirname, 'Front-End/public/downloads');
  const outputFile = path.join(outputDir, 'log_analyzer_tool.zip');
  
  // Create directory if it doesn't exist
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // Create output stream
  const output = fs.createWriteStream(outputFile);
  const archive = archiver('zip', {
    zlib: { level: 9 } // Maximum compression
  });
  
  // Pipe archive to output file
  archive.pipe(output);
  
  // Individual files to include
  const filesToInclude = [
    'log_analyzer_tool.py',
    'requirements.txt',
    'start_log_analyzer_gui.bat',
    'log_analyzer_readme.md',
    'test_model_path.py'
  ];
  
  // Add individual files to the archive
  for (const file of filesToInclude) {
    const filePath = path.join(__dirname, file);
    
    if (fs.existsSync(filePath)) {
      archive.file(filePath, { name: path.basename(file) });
    } else {
      console.warn(`Warning: File not found: ${file}`);
    }
  }
  
  // Add the log_analyzer_gui.py file
  const guiFilePath = path.join(__dirname, 'AI/log_analyzer_gui.py');
  if (fs.existsSync(guiFilePath)) {
    archive.file(guiFilePath, { name: 'log_analyzer_gui.py' });
  } else {
    console.warn(`Warning: File not found: AI/log_analyzer_gui.py`);
  }
  
  // Create AI directory structure
  // Add the AI directory with the model
  const aiDir = path.join(__dirname, 'AI');
  if (fs.existsSync(aiDir)) {
    // Create the AI directory in the zip
    archive.append(null, { name: 'AI/' });
    
    // Add the model directory with proper structure
    const modelDir = path.join(aiDir, 'main-federated-roberta-model');
    if (fs.existsSync(modelDir)) {
      // Create the model directory in the zip
      archive.append(null, { name: 'AI/main-federated-roberta-model/' });
      
      // Add all files from the model directory
      const modelFiles = fs.readdirSync(modelDir);
      for (const file of modelFiles) {
        const filePath = path.join(modelDir, file);
        if (fs.statSync(filePath).isFile()) {
          archive.file(filePath, { name: `AI/main-federated-roberta-model/${file}` });
          console.log(`Adding model file: ${file}`);
        }
      }
    } else {
      console.warn(`Warning: Model directory not found: ${modelDir}`);
    }
    
    // Check for other model directories and include them as well
    const otherModelDirs = [
      'bert-log-model',
      'bgl-bert-base-model',
      'bgl-roberta-model',
      'hdfs_roberta_model',
      'roberta-log-model'
    ];
    
    for (const modelName of otherModelDirs) {
      const modelPath = path.join(aiDir, modelName);
      if (fs.existsSync(modelPath)) {
        console.log(`Adding additional model: ${modelName}`);
        // Create the model directory in the zip
        archive.append(null, { name: `AI/${modelName}/` });
        
        // Add all files from the model directory
        const modelFiles = fs.readdirSync(modelPath);
        for (const file of modelFiles) {
          const filePath = path.join(modelPath, file);
          if (fs.statSync(filePath).isFile()) {
            archive.file(filePath, { name: `AI/${modelName}/${file}` });
          }
        }
      }
    }
  } else {
    console.warn(`Warning: AI directory not found: ${aiDir}`);
  }
  
  // Create a basic README file with instructions
  const readmeContent = `# Log Analyzer Tool

## Instructions for Use
1. Make sure you have Python 3.8 or higher installed
2. Install required packages: \`pip install -r requirements.txt\`
3. Run \`start_log_analyzer_gui.bat\` to start the analyzer GUI
4. Follow the instructions in the application

## Troubleshooting
If you encounter issues with the AI model:
1. Run \`python test_model_path.py\` to diagnose model path issues
2. Follow the suggestions in the output

For more details, see the log_analyzer_readme.md file.

## Important Note
The tool expects the following directory structure:
- log_analyzer_gui.py (in the root directory)
- log_analyzer_tool.py
- AI/main-federated-roberta-model/ (directory containing model files)

Do not change this structure or the tool may not work correctly.
`;
  
  archive.append(readmeContent, { name: 'README.md' });
  
  // Create a sample CSV file for testing
  const sampleCsvContent = `log,device_name,device_ip,device_mac
"User login successful",Server01,192.168.1.10,00:1A:2B:3C:4D:5E
"Failed login attempt - incorrect password",Server01,192.168.1.10,00:1A:2B:3C:4D:5E
"System shutdown initiated",Server02,192.168.1.11,00:1A:2B:3C:4D:5F
"Error: Unable to connect to database",Server03,192.168.1.12,00:1A:2B:3C:4D:60
"Warning: Disk space below 10%",Server02,192.168.1.11,00:1A:2B:3C:4D:5F
"Suspicious activity detected from IP 203.0.113.42",Server01,192.168.1.10,00:1A:2B:3C:4D:5E
"Service started successfully",Server03,192.168.1.12,00:1A:2B:3C:4D:60
"Backup completed successfully",Server02,192.168.1.11,00:1A:2B:3C:4D:5F
"Network connection lost",Server01,192.168.1.10,00:1A:2B:3C:4D:5E
"Security update installed",Server03,192.168.1.12,00:1A:2B:3C:4D:60`;
  
  archive.append(sampleCsvContent, { name: 'sample_logs.csv' });
  
  // Finalize the archive
  await archive.finalize();
  
  console.log('Log Analyzer Tool zip file created successfully!');
}

// Create the zip file for the Log Collector tool
async function createLogCollectorZip() {
  const outputDir = path.join(__dirname, 'Front-End/public/downloads');
  const outputFile = path.join(outputDir, 'log_collector_tool.zip');
  
  // Create directory if it doesn't exist
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // Create output stream
  const output = fs.createWriteStream(outputFile);
  const archive = archiver('zip', {
    zlib: { level: 9 } // Maximum compression
  });
  
  // Pipe archive to output file
  archive.pipe(output);
  
  // Since we don't have a collector tool yet, create a placeholder
  const readmeContent = `# Log Collector Tool

## Coming Soon
This tool is currently under development. 

In the meantime, you can use the Log Analyzer GUI tool to analyze your logs locally.

## Instructions
1. Collect your logs in CSV format with the following columns:
   - log: The log message text
   - device_name (optional): Name of the device
   - device_ip (optional): IP address of the device
   - device_mac (optional): MAC address of the device
   - time (optional): Timestamp of the log

2. Use the Log Analyzer GUI tool to analyze these logs.

Stay tuned for updates!
`;
  
  // Add the readme to the archive
  archive.append(readmeContent, { name: 'README.md' });
  
  // Finalize the archive
  await archive.finalize();
  
  console.log('Log Collector Tool zip file created successfully!');
}

// Run both zip creation functions
async function createAllZips() {
  try {
    await createLogAnalyzerZip();
    await createLogCollectorZip();
    console.log('All zip files created successfully!');
  } catch (error) {
    console.error('Error creating zip files:', error);
  }
}

createAllZips(); 