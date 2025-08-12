# Log Analyzer GUI - Installation Guide

This guide will help you install and run the Log Analyzer GUI tool on your Windows PC.

## Option 1: Using the Installer (Recommended)

1. Download the `LogAnalyzer.exe` installer from the Download page.
2. Run the installer and follow the on-screen instructions.
3. After installation, launch "Log Analyzer" from the Start menu.

## Option 2: Manual Installation (For Developers)

### Prerequisites

- Python 3.9+ installed on your system
- pip (Python package manager)

### Installation Steps

1. Clone or download the Log Analyzer repository:
   ```
   git clone https://github.com/your-organization/log-analyzer.git
   cd log-analyzer
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Launch the GUI:
   ```
   python log_analyzer_gui.py
   ```

   Alternatively, you can use the provided batch file:
   ```
   start_log_analyzer_gui.bat
   ```

4. For testing purposes, you can generate sample log data:
   ```
   python test_gui.py --data-only --rows 100
   ```

## Building the Executable (For Developers)

If you want to build the standalone executable yourself:

1. Make sure cx_Freeze is installed:
   ```
   pip install cx_Freeze
   ```

2. Build the executable:
   ```
   python setup.py build
   ```

3. The executable will be created in the `build` directory

## Using the Tool

1. Launch the Log Analyzer GUI application
2. In the "Upload & Process" tab:
   - Click "Browse..." to select your CSV log file
   - Specify a JSON output file
   - Optionally check "Use hybrid approach" or "Save results to database"
   - Click "Process CSV" to analyze the logs

3. Check the "Results" tab to view analysis results

4. Configure database settings in the "Configuration" tab if needed

## Troubleshooting

- **Missing Python error**: Make sure Python is added to your PATH environment variable
- **Missing dependencies**: Run `pip install -r requirements.txt` to install required packages
- **Database connection errors**: Check your PostgreSQL server is running and accessible
- **Model loading errors**: Verify that the model files are in the correct location

## System Requirements

- Operating System: Windows 10 or 11
- Memory: 4GB RAM minimum (8GB recommended)
- Disk Space: 500MB free space
- Python 3.9+ (if installing manually)
- PostgreSQL (optional, for database storage) 