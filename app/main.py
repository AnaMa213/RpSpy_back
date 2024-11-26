# app/main.py
from fastapi import FastAPI

from app.api.api import api_router

app = FastAPI(title="rpspy_back")

app.include_router(api_router, prefix="/api/v1")
