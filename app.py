import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pickle
import sys
import os

app = FastAPI(title="URL Detection API", description="API to classify Malicious vs Benign URLs")

# Enable CORS (Allows the frontend to communicate with backend easily if separate)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount the static directory to serve HTML/CSS/JS frontend
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/assets", exist_ok=True)


# Load ML Model and Tokenizer at Startup (so it doesn't take time per request)
tokenizer = None
model = None

@app.on_event("startup")
async def load_ml_assets():
    global tokenizer, model
    try:
        with open("tokenizer.pkl", "rb") as f:
            tokenizer = pickle.load(f)
        print("✅ Tokenizer loaded successfully.")
    except Exception as e:
        print("❌ Error loading tokenizer:", e)
        sys.exit(1)

    try:
        model = load_model("urlnet_model.h5")
        print("✅ Model loaded successfully.")
    except Exception as e:
        print("❌ Error loading model:", e)
        sys.exit(1)


class URLRequest(BaseModel):
    url: str

class PredictionResponse(BaseModel):
    url: str
    prediction_score: float
    label: str
    is_malicious: bool

@app.post("/predict", response_model=PredictionResponse)
async def predict_url(request: URLRequest):
    if not model or not tokenizer:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    url = request.url
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    # Preprocess URL
    sequence = tokenizer.texts_to_sequences([url])
    padded_sequence = pad_sequences(sequence, maxlen=200)
    
    # Predict
    prediction = model.predict(padded_sequence, verbose=0)[0][0]
    
    # 0 -> Benign, 1 -> Defacement/Malicious
    is_malicious = bool(prediction > 0.5)
    label = "Defacement (Malicious)" if is_malicious else "Benign (Safe)"

    return PredictionResponse(
        url=url,
        prediction_score=float(prediction),
        label=label,
        is_malicious=is_malicious
    )

# Serve the frontend index.html on the root URL
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/how-it-works", response_class=HTMLResponse)
async def serve_how_it_works():
    with open("static/how_it_works.html", "r", encoding="utf-8") as f:
        return f.read()

app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    # run locally on port 8000
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
