from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.api import api_v1_router
from .middlewares import LoggingMiddleware

origins = ["*"]

app = FastAPI(title="Kyudo Tori", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

@app.get("/")
def root():
    return {
        "api_name": "Kyudo Tori API",
        "version": "1.0.0",
    }

app.include_router(api_v1_router)
