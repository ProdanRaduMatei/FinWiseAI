import pickle
import numpy as np
import pandas as pd

with open("ml_engine/model/hybrid_model.pkl", "rb") as f:
    model = pickle.load(f)

def hybrid_predict(features: dict) -> str:
    x = pd.DataFrame([features])

    pred = model.predict(x)[0]
    if pred == 0:
        return "HOLD"
    elif pred == 1:
        return "BUY"
    elif pred == 2:
        return "SELL"
    else:
        return "HOLD"