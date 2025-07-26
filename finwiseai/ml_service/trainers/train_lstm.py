import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
from ml_service.models.lstm_model import LSTMStockModel

def load_data(csv_path, sequence_length=50):
    df = pd.read_csv(csv_path)
    data = df[['Open', 'High', 'Low', 'Close', 'Volume']].values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    x, y = [], []
    for i in range(len(scaled_data) - sequence_length):
        x.append(scaled_data[i:i+sequence_length])
        y.append(scaled_data[i+sequence_length][3])  # Predict Close

    return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32), scaler

def train_model(csv_path='sample_ohlcv_stock_data.csv', epochs=30, lr=0.001):
    sequence_length = 50
    x, y, scaler = load_data(csv_path, sequence_length)
    y = y.view(-1, 1)

    model = LSTMStockModel()
    loss_fn = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        output = model(x)
        loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

    torch.save(model.state_dict(), "lstm_model.pth")
    return model, scaler