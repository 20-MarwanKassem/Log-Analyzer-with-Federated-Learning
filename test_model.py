import os
from transformers import RobertaTokenizer, RobertaForSequenceClassification

print("Testing model loading...")

model_path = "AI/main-federated-roberta-model"
print(f"Model path: {model_path}")
print(f"Path exists: {os.path.exists(model_path)}")

try:
    print("Loading tokenizer...")
    tokenizer = RobertaTokenizer.from_pretrained(model_path)
    print("Tokenizer loaded successfully!")
    
    print("Loading model...")
    model = RobertaForSequenceClassification.from_pretrained(model_path)
    print("Model loaded successfully!")
    
    print("Model loading test passed!")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    import traceback
    traceback.print_exc()
    print("Model loading test failed!") 