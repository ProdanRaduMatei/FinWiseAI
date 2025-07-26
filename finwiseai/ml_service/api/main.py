from fastapi import FastAPI
from ..db import db

app = FastAPI()

@app.get("/ml/ping")
def ping():
    return {"message": "ML microservice is alive!"}

@app.get("/ml/test-db")
def test_db():
    db.logs.insert_one({"service": "ml", "status": "working"})
    return {"status": "Inserted ML log"}