import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load mock dataset
df = pd.read_csv("ml_engine/data/stock_data.csv")

X = df.drop(columns=["target"])
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open("ml_engine/model/hybrid_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved.")