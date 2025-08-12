import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["os", "pandas", "numpy", "tkinter", "transformers", "torch", "psycopg2"],
    "excludes": [],
    "include_files": [
        ("AI/main-federated-roberta-model", "AI/main-federated-roberta-model"),
        ("test_data", "test_data"),
        ("log_analyzer_readme.md", "log_analyzer_readme.md")
    ]
}

# Base for the executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Setup configuration
setup(
    name="Log Analyzer Tool",
    version="1.0.0",
    description="AI-powered log analysis tool",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "log_analyzer_gui.py", 
            base=base,
            target_name="LogAnalyzer.exe",
            icon="Front-End/public/LogAnalyzerLogo.ico"
        )
    ]
) 