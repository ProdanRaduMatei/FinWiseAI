from fastapi import FastAPI

app = FastAPI()

@app.get("/ml/ping")
def ping():
    return {"message": "ML microservice is alive!"}