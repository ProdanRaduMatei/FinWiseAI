from fastapi import FastAPI
from routes.portfolio import router as portfolio_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(portfolio_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FinWise AI with Trading212 Backend Active"}