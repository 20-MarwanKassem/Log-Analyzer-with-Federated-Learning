import os
import sys
import csv
import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, logging
import traceback

# Set transformers logging to show only errors
logging.set_verbosity_error()

class LogAnalyzerTool:
    def __init__(self, model_path='AI/main-federated-roberta-model', 
                 db_config=None, use_hybrid_approach=False):
        """
        Initialize the Log Analyzer tool
        
        Args:
            model_path: Path to the RoBERTa model directory
            db_config: Database configuration dictionary
            use_hybrid_approach: Whether to use hybrid model+heuristic approach (default: False)
        """
        # Set default database config if none provided
        if db_config is None:
            self.db_config = {
                'user': os.environ.get('DB_USER', 'postgres'),
                'host': os.environ.get('DB_HOST', 'localhost'),
                'database': os.environ.get('DB_NAME', 'log_analyzer'),
                'password': os.environ.get('DB_PASSWORD', 'logai'),
                'port': os.environ.get('DB_PORT', 5432),
            }
        else:
            self.db_config = db_config
        
        # Flag to determine if we should use hybrid model+heuristic approach
        self.use_hybrid_approach = use_hybrid_approach
        
        # Set model path
        self.model_path = model_path
        
        # Flag to track if model is loaded successfully
        self.model_loaded = False
        
        # Debug information
        print(f"Python version: {sys.version}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Starting model path: {model_path}")
        
        # Check if path exists before proceeding
        if not os.path.exists(model_path):
            print(f"WARNING: Initial model path does not exist: {model_path}")
        
        # Set up device (GPU if available, else CPU)
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"Using device: {self.device}")
            print(f"PyTorch version: {torch.__version__}")
            
            if self.device.type == 'cuda':
                print(f"CUDA device name: {torch.cuda.get_device_name(0)}")
                print(f"CUDA version: {torch.version.cuda}")
                
        except Exception as e:
            print(f"Error setting up device: {str(e)}")
            self.device = torch.device("cpu")
            print("Falling back to CPU")
        
        # Define anomaly keywords for heuristic
        self.anomaly_keywords = [
            'failed', 'failure', 'error', 'denied', 'unauthorized', 'suspicious',
            'violation', 'attack', 'multiple', 'unusual', 'malware', 'virus',
            'blocked', 'scan', 'breach', 'compromise', 'brute force', 'port scan',
            'detection', 'detected', 'critical', 'down', 'outage', 'timeout'
        ]
        
        # Try to load the model
        try:
            print("Attempting to load AI model...")
            self._load_model()
            print("Model loaded successfully. System will use AI-based analysis!")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            traceback.print_exc()
            print("\nDIAGNOSTIC INFORMATION:")
            
            try:
                # Check transformers version
                import transformers
                print(f"Transformers version: {transformers.__version__}")
                
                # Check if model directory exists
                if os.path.exists(self.model_path):
                    print(f"Model directory exists at: {self.model_path}")
                    print(f"Contents: {os.listdir(self.model_path)}")
                else:
                    print(f"Model directory does not exist at: {self.model_path}")
                
                # Check for common issues
                print("\nPossible issues:")
                print("1. Missing or incorrect model files")
                print("2. Incompatible transformers or torch versions")
                print("3. Incorrect model path")
                print("4. Try using a different model: 'AI/roberta-log-model', 'AI/bert-log-model', or 'AI/bgl-roberta-model'")
            except Exception as diag_e:
                print(f"Error during diagnostics: {diag_e}")
            
            print("\nContinuing in heuristic-only mode...")
            self.model_loaded = False
            self.use_hybrid_approach = True  # Force hybrid approach to use heuristic fallback
    
    def _load_model(self):
        """
        Load the tokenizer and model from the specified path
        """
        # Check if model directory exists
        if not os.path.exists(self.model_path):
            print(f"Model directory not found: {self.model_path}")
            print(f"Current directory: {os.getcwd()}")
            print(f"Directory contents: {os.listdir('.')}")
            if os.path.exists('AI'):
                print(f"AI directory contents: {os.listdir('AI')}")
            
            # Try some alternative paths
            alternative_paths = [
                os.path.join(os.getcwd(), self.model_path),
                os.path.join(os.getcwd(), 'AI', 'main-federated-roberta-model'),
                os.path.join(os.path.dirname(__file__), 'AI', 'main-federated-roberta-model'),
                'AI/main-federated-roberta-model',
                './AI/main-federated-roberta-model',
                '../AI/main-federated-roberta-model',
                'AI/roberta-log-model',  # Try other models
                'AI/bert-log-model',
                'AI/bgl-roberta-model',
                'AI/hdfs_roberta_model',
                'AI/bgl-bert-base-model'
            ]
            
            for alt_path in alternative_paths:
                if os.path.exists(alt_path):
                    print(f"Found model at alternative path: {alt_path}")
                    self.model_path = alt_path
                    break
            
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model directory not found at any path")
        
        # Try to load model
        print(f"Loading model from {self.model_path}...")
        
        # Verify model directory contents
        print(f"Model directory contents: {os.listdir(self.model_path)}")
        
        # Check for essential files
        essential_files = ['config.json', 'model.safetensors']
        for file in essential_files:
            if not os.path.exists(os.path.join(self.model_path, file)):
                raise FileNotFoundError(f"Essential file '{file}' missing from model directory")
        
        # Try loading tokenizer first
        print("Loading tokenizer...")
        try:
            self.tokenizer = RobertaTokenizer.from_pretrained(self.model_path)
            print("Tokenizer loaded successfully")
        except Exception as e:
            print(f"Failed to load tokenizer: {str(e)}")
            traceback.print_exc()
            raise
        
        # Then try loading model
        print("Loading model...")
        try:
            self.model = RobertaForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            self.model_loaded = True
            print("Model loaded successfully")
        except Exception as e:
            print(f"Failed to load model: {str(e)}")
            traceback.print_exc()
            raise
        
        print(f"Using {'hybrid' if self.use_hybrid_approach else 'model-only'} approach")
    
    def ensure_db_table_exists(self):
        """
        Ensure that the logs table exists in the database
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            # Check if table exists
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'logs'
                );
            """)
            
            table_exists = cur.fetchone()[0]
            
            if not table_exists:
                print("Logs table does not exist. Creating it...")
                # Create the logs table
                cur.execute("""
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
                """)
                conn.commit()
                print("Logs table created successfully.")
            
            cur.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error ensuring database table exists: {str(e)}")
            return False
    
    def analyze_csv(self, csv_file_path):
        """
        Analyze logs from a CSV file
        
        Args:
            csv_file_path: Path to the CSV file containing logs
            
        Returns:
            A list of dictionaries containing analysis results
        """
        try:
            # Read the CSV file
            print(f'Reading CSV file: {csv_file_path}')
            df = pd.read_csv(csv_file_path)
            print(f'Found {len(df)} log entries')
            
            # Check if the required columns exist
            required_columns = ['log']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f'CSV file must contain a "{col}" column')
                    
            results = []
            
            # Process each log entry
            print('Processing log entries...')
            for index, row in df.iterrows():
                log_text = row['log']
                print(f'Analyzing log: {log_text[:30]}...')
                
                # Extract available metadata
                metadata = {col: row[col] for col in df.columns if col != 'log'}
                
                # Get prediction from model
                prediction = self.predict(log_text)
                
                # Create result dictionary
                result = {
                    **metadata,
                    'log': log_text,
                    'status': prediction['label'],
                    'confidence': prediction['score'],
                    'method': prediction.get('method', 'unknown')
                }
                
                print(f'Result: {prediction["label"]} (confidence: {prediction["score"]:.4f}, method: {prediction.get("method", "unknown")})')
                results.append(result)
            
            print('Analysis complete')
            return results
        
        except Exception as e:
            print(f'Error analyzing CSV: {str(e)}')
            traceback.print_exc()
            raise
    
    def predict(self, log_text):
        """
        Make a prediction for a single log entry using the model or hybrid approach
        
        Args:
            log_text: The log text to analyze
            
        Returns:
            Dictionary with prediction label, confidence score and method used
        """
        try:
            # If model is not loaded or we're using hybrid approach, check heuristic first
            if not self.model_loaded or self.use_hybrid_approach:
                heuristic_result = self._predict_with_keywords(log_text)
                
                # If model is not loaded, return heuristic result
                if not self.model_loaded:
                    heuristic_result['method'] = 'heuristic (model not loaded)'
                    return heuristic_result
            
            # If we're not using the hybrid approach, return the model result
            if not self.use_hybrid_approach:
                model_result = self._predict_with_model(log_text)
                model_result['method'] = 'model'
                return model_result
                
            # Use the hybrid approach
            try:
                model_result = self._predict_with_model(log_text)
                
                # If the model seems to be predicting the same for everything, 
                # use the heuristic instead
                if model_result['score'] > 0.85:
                    heuristic_result['method'] = 'hybrid (favoring heuristic)'
                    return heuristic_result
                else:
                    model_result['method'] = 'hybrid (favoring model)'
                    return model_result
                
            except Exception as e:
                print(f"Model prediction failed: {e}. Falling back to heuristic.")
                heuristic_result['method'] = 'heuristic (fallback)'
                return heuristic_result
            
        except Exception as e:
            print(f'Error in prediction: {str(e)}')
            traceback.print_exc()
            return {"label": "unknown", "score": 0.0, "method": "error"}
    
    def _predict_with_model(self, log_text):
        """
        Make a prediction using the RoBERTa model
        
        Args:
            log_text: The log text to analyze
            
        Returns:
            Dictionary with prediction label and confidence score
        """
        if not self.model_loaded:
            raise RuntimeError("Model is not loaded. Cannot make prediction.")
            
        try:
            # Tokenize the log text
            inputs = self.tokenizer(log_text, return_tensors="pt", truncation=True, padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get model prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            # Get probabilities
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
            
            # Get the predicted class (CORRECTED: 0 = anomaly, 1 = normal)
            predicted_class = torch.argmax(probs).item()
            confidence = probs[predicted_class].item()
            
            # Return the result - labels are swapped in this model
            return {
                "label": "normal" if predicted_class == 1 else "anomaly",
                "score": confidence
            }
            
        except Exception as e:
            print(f'Error in model prediction: {str(e)}')
            traceback.print_exc()
            raise
    
    def _predict_with_keywords(self, log_text):
        """
        Make a prediction using keyword-based heuristics
        
        Args:
            log_text: The log text to analyze
            
        Returns:
            Dictionary with prediction label and confidence score
        """
        log_text_lower = log_text.lower()
        
        # Check for anomaly keywords
        for keyword in self.anomaly_keywords:
            if keyword in log_text_lower:
                return {"label": "anomaly", "score": 0.8}
        
        # If no keywords found, return normal
        return {"label": "normal", "score": 0.7}
    
    def save_to_json(self, results, output_path):
        """
        Save analysis results to a JSON file
        
        Args:
            results: List of result dictionaries
            output_path: Path to save the JSON file
        """
        try:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f'Results saved to {output_path}')
            return True
        except Exception as e:
            print(f'Error saving results to JSON: {str(e)}')
            return False
    
    def save_to_database(self, results):
        """
        Save analysis results to the database
        
        Args:
            results: List of result dictionaries
            
        Returns:
            Number of records inserted
        """
        try:
            # Ensure the table exists
            self.ensure_db_table_exists()
            
            # Connect to the database
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            # Prepare data for insertion
            data_to_insert = []
            for result in results:
                # Extract fields or use defaults
                user_id = result.get('user_id', 1)  # Default to user_id 1 if not provided
                device_name = result.get('device_name')
                device_mac = result.get('device_mac')
                device_ip = result.get('device_ip')
                log_text = result.get('log')
                status = result.get('status')
                log_time = result.get('time')
                
                # Add to data to insert
                data_to_insert.append((
                    user_id, device_name, device_mac, device_ip, log_text, status, log_time
                ))
            
            # Insert data
            execute_values(
                cur,
                """
                INSERT INTO logs (user_id, device_name, device_mac, device_ip, log, status, time)
                VALUES %s
                RETURNING id
                """,
                data_to_insert
            )
            
            # Get the inserted IDs
            inserted_ids = [row[0] for row in cur.fetchall()]
            
            # Commit the transaction
            conn.commit()
            
            # Close the connection
            cur.close()
            conn.close()
            
            print(f'Inserted {len(inserted_ids)} records into the database')
            return len(inserted_ids)
            
        except Exception as e:
            print(f'Error saving to database: {str(e)}')
            traceback.print_exc()
            return 0

def main():
    """
    Main function to run the log analyzer tool
    """
    import argparse
    parser = argparse.ArgumentParser(description='Analyze logs and store results')
    parser.add_argument('--csv', required=True, help='Path to CSV file with logs')
    parser.add_argument('--json', help='Path to save JSON results', default='analysis_results.json')
    parser.add_argument('--model', default='AI/main-federated-roberta-model', help='Path to model directory')
    parser.add_argument('--save-db', action='store_true', help='Save results to database')
    parser.add_argument('--hybrid', action='store_true', help='Use hybrid model+heuristic approach')
    
    args = parser.parse_args()
    
    # Initialize the analyzer
    analyzer = LogAnalyzerTool(
        model_path=args.model,
        use_hybrid_approach=args.hybrid
    )
    
    # Analyze the CSV file
    results = analyzer.analyze_csv(args.csv)
    
    # Save results to JSON
    analyzer.save_to_json(results, args.json)
    
    # Save to database if requested
    if args.save_db:
        analyzer.save_to_database(results)

if __name__ == '__main__':
    main()
