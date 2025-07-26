from fastapi import APIRouter, HTTPException
from finwiseai.ml_service.models.lstm_model import LSTMStockModel
import torch
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

router = APIRouter(prefix="/ml", tags=["LSTM"])

@router.get("/predict")
def predict_next_close(csv_path: str = "sample_ohlcv_stock_data.csv"):
    if not os.path.exists("lstm_model.pth"):
        raise HTTPException(status_code=404, detail="Model not trained. Run training first.")

    df = pd.read_csv(csv_path)
    data = df[['Open', 'High', 'Low', 'Close', 'Volume']].values

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    last_seq = torch.tensor([scaled_data[-50:]], dtype=torch.float32)

    model = LSTMStockModel()
    model.load_state_dict(torch.load("lstm_model.pth"))
    model.eval()

    with torch.no_grad():
        pred = model(last_seq).item()

    close_index = 3  # 'Close'
    close_max = scaler.data_max_[close_index]
    close_min = scaler.data_min_[close_index]
    predicted_close = pred * (close_max - close_min) + close_min

    return {"predicted_close_price": round(predicted_close, 2)}