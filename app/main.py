from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.database import engine
from app.models import Base
from app.routes import shorten, redirect, stats
import os

Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="LinkScope",
    description="A link intelligence platform - shorten, track and analyse URLs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL","http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(shorten.router)
app.include_router(redirect.router)
app.include_router(stats.router)

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.get("/not-found")
async def not_found():
    return {"detail":"Link not found"}

@app.get("/expired")
async def expired():
    return {"detail":"Link has expired or has reached click limit"}