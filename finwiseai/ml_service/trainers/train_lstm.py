# finwiseai/ml_service/trainers/train_lstm.py
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
import os
from finwiseai.ml_service.models.lstm_model import LSTMStockModel

def train_lstm_model(csv_path: str, model_save_path: str = "finwiseai/ml_service/models/lstm_model.pth", epochs: int = 5):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Load and validate data
    df = pd.read_csv(csv_path)
    required_cols = ["Open", "High", "Low", "Close", "Volume"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    data = df[required_cols].values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    # Prepare training sequences
    seq_length = 50
    x, y = [], []
    for i in range(len(scaled_data) - seq_length):
        x.append(scaled_data[i:i+seq_length])
        y.append(scaled_data[i+seq_length][3])  # Close price index
    x, y = np.array(x), np.array(y)

    # Convert to tensors
    x_tensor = torch.tensor(x, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)

    # Initialize model
    model = LSTMStockModel()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Train loop
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        output = model(x_tensor)
        loss = criterion(output.squeeze(), y_tensor)
        loss.backward()
        optimizer.step()

    # Save model
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    torch.save(model.state_dict(), model_save_path)

    return {"status": "success", "model_path": model_save_path, "loss": loss.item()}