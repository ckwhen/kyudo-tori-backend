from fastapi import FastAPI
from app.api.v1.routers import shinsas

app = FastAPI(title="Kyudo Tori", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to Kyudo Tori!"}

app.include_router(shinsas.router, prefix="/api/v1")
