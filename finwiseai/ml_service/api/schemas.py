from pydantic import BaseModel

class TrainRequest(BaseModel):
    symbol: str
    epochs: int = 10
    model_version: str = "v1"

class TrainResponse(BaseModel):
    task_id: str

class PredictRequest(BaseModel):
    symbol: str
    model_version: str = "v1"

class PredictResponse(BaseModel):
    prediction: str
    confidence: float