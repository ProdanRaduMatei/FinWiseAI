from fastapi import FastAPI
from auth import auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/api/ping")
def ping():
    return {"message": "Backend up!"}