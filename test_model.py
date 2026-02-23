import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import sys

# Load tokenizer
try:
    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    print("✅ Tokenizer loaded successfully.")
except Exception as e:
    print("❌ Error loading tokenizer:", e)
    sys.exit()

# Load model
try:
    model = load_model("urlnet_model.h5")
    print("✅ Model loaded successfully.")
except Exception as e:
    print("❌ Error loading model:", e)
    sys.exit()

# URLs to test
test_urls = [
    "http://www.google.com",
    "https://github.com",
    "http://example-malicious-site.com/login",
    "http://secure-update-banking.com",
    "http://localhost/admin/config.php"
]

if len(sys.argv) > 1:
    args_list = sys.argv
    test_urls = args_list[1:]

print("\n--- Testing Model Predictions ---")
for url in test_urls:
    # Preprocess URL
    sequence = tokenizer.texts_to_sequences([url])
    padded_sequence = pad_sequences(sequence, maxlen=200)
    
    # Predict
    prediction = model.predict(padded_sequence, verbose=0)[0][0]
    
    # The model was trained with 'benign': 0, 'defacement': 1
    label = "Defacement (Malicious)" if prediction > 0.5 else "Benign (Safe)"
    print(f"URL: {url}")
    print(f"Prediction Score: {prediction:.4f} -> {label}\n")

print("Finished testing.")
