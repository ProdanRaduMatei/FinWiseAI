from fastapi import FastAPI
from finwiseai.ml_service.api.routes import router as ml_router, vader_router

app = FastAPI()

app.include_router(ml_router)
app.include_router(vader_router)

@app.get("/ml/ping")
def ping():
    return {"message": "ML microservice is alive!"}

@app.get("/ml/test-db")
def test_db():
    db.logs.insert_one({"service": "ml", "status": "working"})
    return {"status": "Inserted ML log"}