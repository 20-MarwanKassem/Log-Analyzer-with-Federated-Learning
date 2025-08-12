import os
import sys
import traceback
import shutil
import platform

def check_model_path(model_path):
    print(f"Checking model path: {model_path}")
    
    # Check if the path exists
    if not os.path.exists(model_path):
        print(f"❌ ERROR: Path does not exist: {model_path}")
        return False
    
    # Check if it's a directory
    if not os.path.isdir(model_path):
        print(f"❌ ERROR: Path is not a directory: {model_path}")
        return False
    
    # List contents of the directory
    contents = os.listdir(model_path)
    print(f"Directory contents: {contents}")
    
    # Check for required files
    required_files = ["config.json", "model.safetensors", "tokenizer_config.json"]
    roberta_specific = ["vocab.json", "merges.txt"]
    bert_specific = ["vocab.txt"]
    
    # Check if this is a RoBERTa or BERT model
    is_roberta = all(file in contents for file in roberta_specific)
    is_bert = all(file in contents for file in bert_specific)
    
    if is_roberta:
        print("✅ Model appears to be a RoBERTa model")
        required_files.extend(roberta_specific)
    elif is_bert:
        print("✅ Model appears to be a BERT model")
        required_files.extend(bert_specific)
    else:
        print("❌ WARNING: Could not determine model type (neither RoBERTa nor BERT)")
    
    # Check for all required files
    missing_files = [file for file in required_files if file not in contents]
    if missing_files:
        print(f"❌ ERROR: Missing required files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def fix_model_structure():
    """Attempt to fix the model structure by reorganizing files"""
    print("\nAttempting to fix model structure...")
    
    # Check if AI directory exists
    if not os.path.exists('AI'):
        print("Creating AI directory...")
        os.makedirs('AI', exist_ok=True)
    
    # Check for model files in the current directory
    model_files = []
    for file in os.listdir('.'):
        if file in ['config.json', 'model.safetensors', 'tokenizer_config.json', 'vocab.json', 'merges.txt', 'vocab.txt']:
            model_files.append(file)
    
    if model_files:
        print(f"Found model files in current directory: {model_files}")
        
        # Create model directory if it doesn't exist
        model_dir = os.path.join('AI', 'main-federated-roberta-model')
        os.makedirs(model_dir, exist_ok=True)
        
        # Move files to the model directory
        for file in model_files:
            dest_file = os.path.join(model_dir, file)
            if not os.path.exists(dest_file):
                print(f"Moving {file} to {model_dir}")
                shutil.copy(file, dest_file)
        
        print("✅ Model structure fixed. Files have been copied to the correct location.")
        return True
    else:
        print("❌ No model files found in the current directory.")
        return False

def main():
    print("=" * 60)
    print("Log Analyzer AI Model Diagnostic Tool")
    print("=" * 60)
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Operating system: {platform.system()} {platform.release()}")
    print()
    
    # List the contents of the current directory
    print("Contents of current directory:")
    try:
        for item in os.listdir(current_dir):
            if os.path.isdir(os.path.join(current_dir, item)):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
    except Exception as e:
        print(f"Error listing directory: {str(e)}")
    print()
    
    # Check if AI directory exists
    ai_dir = os.path.join(current_dir, "AI")
    if os.path.exists(ai_dir) and os.path.isdir(ai_dir):
        print("✅ AI directory exists")
        print("Contents of AI directory:")
        for item in os.listdir(ai_dir):
            if os.path.isdir(os.path.join(ai_dir, item)):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
    else:
        print("❌ AI directory does not exist")
        # Create AI directory
        try:
            os.makedirs(ai_dir, exist_ok=True)
            print("✅ Created AI directory")
        except Exception as e:
            print(f"❌ Failed to create AI directory: {str(e)}")
    print()
    
    # Check various model paths
    model_paths = [
        os.path.join(current_dir, "AI", "main-federated-roberta-model"),
        os.path.join(current_dir, "main-federated-roberta-model"),
        "AI/main-federated-roberta-model",
        "./AI/main-federated-roberta-model",
        "main-federated-roberta-model"
    ]
    
    print("Checking possible model paths:")
    found_valid_model = False
    for path in model_paths:
        print("\n-----------------------------------")
        if check_model_path(path):
            found_valid_model = True
            print(f"✅ Found valid model at: {path}")
            break
    
    if not found_valid_model:
        print("\n❌ No valid model found. Attempting to fix...")
        if fix_model_structure():
            # Check if the fix worked
            if check_model_path(os.path.join(current_dir, "AI", "main-federated-roberta-model")):
                found_valid_model = True
                print("✅ Model structure has been fixed successfully!")
    
    # Check for log_analyzer_gui.py in the correct location
    gui_file = os.path.join(current_dir, "log_analyzer_gui.py")
    ai_gui_file = os.path.join(current_dir, "AI", "log_analyzer_gui.py")
    
    if os.path.exists(gui_file):
        print("\n✅ log_analyzer_gui.py found in the correct location")
    elif os.path.exists(ai_gui_file):
        print("\n❌ log_analyzer_gui.py found in AI directory but should be in the root directory")
        print("Copying file to the correct location...")
        try:
            shutil.copy(ai_gui_file, gui_file)
            print("✅ log_analyzer_gui.py copied to the root directory")
        except Exception as e:
            print(f"❌ Failed to copy file: {str(e)}")
    else:
        print("\n❌ log_analyzer_gui.py not found")
    
    # Provide suggestions
    print("\n" + "=" * 60)
    print("DIAGNOSIS SUMMARY:")
    
    if found_valid_model:
        print("✅ AI model files are correctly installed")
    else:
        print("❌ AI model files are missing or incorrectly installed")
    
    print("\nSUGGESTIONS:")
    if not found_valid_model:
        print("1. Make sure all model files are extracted to AI/main-federated-roberta-model/")
        print("2. The required files are:")
        print("   - config.json")
        print("   - model.safetensors")
        print("   - tokenizer_config.json")
        print("   - vocab.json (for RoBERTa models)")
        print("   - merges.txt (for RoBERTa models)")
        print("   - vocab.txt (for BERT models)")
        print("3. Re-download the tool if necessary")
    else:
        print("1. Run 'start_log_analyzer_gui.bat' to start the tool")
        print("2. If you still have issues, make sure Python and all required packages are installed:")
        print("   - Run: pip install -r requirements.txt")
    
    print("\nDIRECTORY STRUCTURE:")
    print("The correct directory structure should be:")
    print("- log_analyzer_gui.py (in the root directory)")
    print("- log_analyzer_tool.py (in the root directory)")
    print("- AI/main-federated-roberta-model/ (directory containing model files)")
    print("  - config.json")
    print("  - model.safetensors")
    print("  - tokenizer_config.json")
    print("  - vocab.json (for RoBERTa models)")
    print("  - merges.txt (for RoBERTa models)")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in diagnostic tool: {str(e)}")
        traceback.print_exc()
    
    # Keep the window open
    input("\nPress Enter to exit...") 