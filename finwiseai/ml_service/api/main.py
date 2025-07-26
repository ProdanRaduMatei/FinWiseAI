from fastapi import FastAPI
from ml_service.db import db
from ml_service.api.routes import router as ml_router

app = FastAPI()
app.include_router(ml_router)

@app.get("/ml/ping")
def ping():
    return {"message": "ML microservice is alive!"}

@app.get("/ml/test-db")
def test_db():
    db.logs.insert_one({"service": "ml", "status": "working"})
    return {"status": "Inserted ML log"}