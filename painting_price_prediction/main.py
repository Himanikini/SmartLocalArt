from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# Load the trained model and related files
try:
    model = joblib.load('model.pkl')
    scaler = joblib.load('scaler.pkl')
    columns = joblib.load('columns.pkl')
except FileNotFoundError as e:
    raise RuntimeError(f"Error loading model files: {e}")

# Define request body schema
class PaintingInput(BaseModel):
    painter: str
    subject: str
    style: str
    medium: str
    size: str
    location: str
    environment: str

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict_price(data: PaintingInput):
    try:
        # Create a DataFrame with all zeros
        new_painting_df = pd.DataFrame(0, index=[0], columns=columns)

        # Manually set one-hot encoded values (column names match the training CSV headers)
        if f"Name of Painter_{data.painter}" in new_painting_df.columns:
            new_painting_df[f"Name of Painter_{data.painter}"] = 1

        if f"Subject of Painting_{data.subject}" in new_painting_df.columns:
            new_painting_df[f"Subject of Painting_{data.subject}"] = 1

        if f"Style_{data.style}" in new_painting_df.columns:
            new_painting_df[f"Style_{data.style}"] = 1

        if f"Medium_{data.medium}" in new_painting_df.columns:
            new_painting_df[f"Medium_{data.medium}"] = 1

        if f"Size_{data.size}" in new_painting_df.columns:
            new_painting_df[f"Size_{data.size}"] = 1

        if f"Location_{data.location}" in new_painting_df.columns:
            new_painting_df[f"Location_{data.location}"] = 1

        if f"Recommended Environment_{data.environment}" in new_painting_df.columns:
            new_painting_df[f"Recommended Environment_{data.environment}"] = 1

        print("Updated DataFrame before scaling:\n", new_painting_df)

        # Scale the input
        new_painting_scaled = scaler.transform(new_painting_df)
        print("Scaled Input:\n", new_painting_scaled)

        # Predict the price
        predicted_price = model.predict(new_painting_scaled)
        print(predicted_price)
        return {"predicted_price": round(predicted_price[0], 2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
