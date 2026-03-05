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
    frame: str
    location: str
    delivery_days: int
    shipment: str
    color_palette: str
    copy_original: str
    print_real: str
    environment: str
    mood: str
    lighting: str
    reproduction: str
    audience: str

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

        # Assign numerical value
        new_painting_df['Delivery (days)'] = data.delivery_days

        # Manually set one-hot encoded values
        if f"painter_{data.painter}" in new_painting_df.columns:
            new_painting_df[f"painter_{data.painter}"] = 1

        if f"subject_{data.subject}" in new_painting_df.columns:
            new_painting_df[f"subject_{data.subject}"] = 1

        if f"style_{data.style}" in new_painting_df.columns:
            new_painting_df[f"style_{data.style}"] = 1

        if f"medium_{data.medium}" in new_painting_df.columns:
            new_painting_df[f"medium_{data.medium}"] = 1

        if f"size_{data.size}" in new_painting_df.columns:
            new_painting_df[f"size_{data.size}"] = 1

        if f"frame_{data.frame}" in new_painting_df.columns:
            new_painting_df[f"frame_{data.frame}"] = 1

        if f"location_{data.location}" in new_painting_df.columns:
            new_painting_df[f"location_{data.location}"] = 1

        if f"shipment_{data.shipment}" in new_painting_df.columns:
            new_painting_df[f"shipment_{data.shipment}"] = 1

        if f"color_palette_{data.color_palette}" in new_painting_df.columns:
            new_painting_df[f"color_palette_{data.color_palette}"] = 1

        if f"copy_original_{data.copy_original}" in new_painting_df.columns:
            new_painting_df[f"copy_original_{data.copy_original}"] = 1

        if f"print_real_{data.print_real}" in new_painting_df.columns:
            new_painting_df[f"print_real_{data.print_real}"] = 1

        if f"environment_{data.environment}" in new_painting_df.columns:
            new_painting_df[f"environment_{data.environment}"] = 1

        if f"mood_{data.mood}" in new_painting_df.columns:
            new_painting_df[f"mood_{data.mood}"] = 1

        if f"lighting_{data.lighting}" in new_painting_df.columns:
            new_painting_df[f"lighting_{data.lighting}"] = 1

        if f"reproduction_{data.reproduction}" in new_painting_df.columns:
            new_painting_df[f"reproduction_{data.reproduction}"] = 1

        if f"audience_{data.audience}" in new_painting_df.columns:
            new_painting_df[f"audience_{data.audience}"] = 1

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
