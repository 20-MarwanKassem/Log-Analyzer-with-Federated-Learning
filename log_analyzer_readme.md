# Log Analyzer Tool with Federated Learning Integration

This tool analyzes log data from CSV files using a RoBERTa model for anomaly detection. The tool processes logs, classifies them as anomaly or non-anomaly, and stores the results in both JSON format and a PostgreSQL database.

## Features

- CSV log file processing
- Anomaly detection using RoBERTa model
- Optional hybrid approach that combines model predictions with keyword-based heuristics
- JSON output generation with confidence scores and detection methods
- PostgreSQL database integration
- Command-line interface
- Graphical user interface (GUI) for easier usage

## Requirements

- Python 3.9+
- pandas
- psycopg2-binary
- torch
- transformers
- tkinter (for GUI version)

## Installation

1. Install required packages:
   ```
   pip install pandas psycopg2-binary torch transformers
   ```

2. Configure database connection in the `.env` file or set environment variables:
   ```
   DB_USER=postgres
   DB_HOST=localhost
   DB_NAME=log_analyzer
   DB_PASSWORD=logai
   DB_PORT=5432
   ```

3. Ensure you have the RoBERTa model files in the `AI/main-federated-roberta-model` directory:
   - model.safetensors
   - vocab.json
   - merges.txt
   - tokenizer_config.json
   - config.json
   - special_tokens_map.json

### GUI Installation

For Windows users, you can install the GUI version using the provided installer:

1. Download the LogAnalyzer.exe installer
2. Run the installation wizard
3. Launch the Log Analyzer Tool from your Start menu

To package the GUI version yourself:

1. Install cx_Freeze:
   ```
   pip install cx_Freeze
   ```

2. Build the executable:
   ```
   python setup.py build
   ```

3. The executable will be created in the `build` directory

## Usage

### Command-line Interface

```
python log_analyzer_tool.py --csv path/to/logs.csv --json output_results.json --save-db
```

Parameters:
- `--csv`: Path to CSV file with logs (required)
- `--json`: Path to save JSON results (default: analysis_results.json)
- `--model`: Path to model directory (default: AI/main-federated-roberta-model)
- `--save-db`: Flag to save results to database
- `--hybrid`: Flag to use hybrid model+heuristic approach (optional, default is model-only)

### Graphical User Interface (GUI)

To launch the GUI version:

```
python log_analyzer_gui.py
```

The GUI provides an intuitive interface with these features:
- CSV file upload
- Database configuration
- Model settings
- Results visualization
- Export options

Steps to use the GUI:
1. In the "Upload & Process" tab:
   - Click "Browse..." to select your CSV log file
   - Specify a JSON output file (automatically suggested based on CSV filename)
   - Optionally check "Use hybrid approach" or "Save results to database"
   - Click "Process CSV" to start the analysis

2. In the "Results" tab:
   - View analysis results in the table
   - Export results as CSV if needed

3. In the "Configuration" tab:
   - Set database connection parameters
   - Test the database connection
   - Configure the model path if using a custom model

### As a Library

```python
from log_analyzer_tool import LogAnalyzerTool

# Initialize the analyzer with model-only approach (default)
analyzer = LogAnalyzerTool()

# Or use the hybrid approach (model + heuristics)
# analyzer = LogAnalyzerTool(use_hybrid_approach=True)

# Analyze logs
results = analyzer.analyze_csv('logs.csv')

# Save results to JSON
analyzer.save_to_json(results, 'results.json')

# Save to database
analyzer.save_to_database(results)
```

## CSV Format

The input CSV file should contain at minimum a 'log' column. Additional columns can include:

- user_id: User identifier
- device_name: Name of the device
- device_mac: MAC address of the device
- device_ip: IP address of the device
- time: Timestamp of the log entry

## Output Format

The tool generates JSON files with the following structure:

```json
[
  {
    "user_id": 1,
    "device_name": "Workstation-05",
    "device_mac": "00:1B:44:11:3A:F1",
    "device_ip": "192.168.1.15",
    "time": "2025-06-01 09:23:45",
    "log": "Multiple authentication failures detected",
    "status": "anomaly",
    "confidence": 0.9262951016426086,
    "method": "model"
  },
  {
    "user_id": 1,
    "device_name": "Workstation-05",
    "device_mac": "00:1B:44:11:3A:F1",
    "device_ip": "192.168.1.15",
    "time": "2025-06-01 10:15:22",
    "log": "System update completed successfully",
    "status": "non-anomaly",
    "confidence": 0.9185702800750732,
    "method": "model"
  }
]
```

## Database Schema

The logs are stored in a 'logs' table with the following schema:

```sql
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    device_name VARCHAR(255),
    device_mac VARCHAR(255),
    device_ip VARCHAR(255),
    log TEXT,
    status VARCHAR(50),
    time TIMESTAMP
);
```

## Optional Hybrid Approach

While the tool uses the RoBERTa model by default, it also offers a hybrid approach that combines:

1. **RoBERTa Model**: A transformer-based model fine-tuned for log anomaly detection
2. **Keyword Heuristics**: A rules-based approach that looks for specific keywords associated with anomalies

The hybrid approach can be enabled using the `--hybrid` flag or by setting `use_hybrid_approach=True` when initializing the analyzer. This can be useful in cases where:

- The model hasn't been fine-tuned for your specific log format
- You notice the model is consistently favoring one class over another
- You want to incorporate domain-specific keywords into the anomaly detection

## Model Details

The tool uses a RoBERTa model fine-tuned for log anomaly detection. The model architecture is a sequence classifier that categorizes logs into two classes:
- non-anomaly (class 0)
- anomaly (class 1)

The model has been trained using federated learning on multiple log datasets, including:
- BGL (Blue Gene/L supercomputer logs)
- HDFS (Hadoop Distributed File System logs)
- OpenStack

This approach allows the model to maintain privacy while learning from various log sources and improves its ability to detect anomalies across different systems.

## Testing

A test script and sample data generator are included:

```
# Generate test data
python create_test_data.py

# Run the analyzer with the pure model approach (default)
python test_analyzer.py

# Run the analyzer with the hybrid approach
python test_analyzer.py --hybrid 
```

## Integration with Download Page

The Log Analyzer Tool can be integrated with the Download page of your website, allowing users to download and use the tool with their devices. Follow these steps to integrate:

1. Place the packaged executable in the web server's download directory
2. Update the download link in the Front-End Download.tsx component to point to the executable
3. Add the tool documentation to the download page for user reference 