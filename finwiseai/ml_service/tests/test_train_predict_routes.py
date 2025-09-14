from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

@router.get("/")
def root():
    return {"message": "FinWise AI ML Service is running."}

class TrainRequest(BaseModel):
    csv_path: str = Field(..., description="Path to the CSV file with stock data.")

class PredictRequest(BaseModel):
    csv_path: str = Field(..., description="Path to the CSV file used for prediction.")

class TrainResponse(BaseModel):
    message: str
    details: dict

class PredictResponse(BaseModel):
    predicted_close_price: float

@router.post("/train", response_model=TrainResponse, summary="Train LSTM Model", description="Train an LSTM model using a CSV with OHLCV data.")
def train_endpoint(request: TrainRequest):
    ...

@router.post("/predict", response_model=PredictResponse, summary="Predict with LSTM Model", description="Predict the next closing price using the trained LSTM model.")
def predict_endpoint(request: PredictRequest):
    ...