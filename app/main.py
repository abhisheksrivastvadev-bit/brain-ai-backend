
from fastapi import FastAPI
from app.api.routes import chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Brain AI Backend API",
    description="Backend service for Brain AI",
    version="0.0.1"
)

app.include_router(chat.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return{
        "message":"Welcome to the Brain AI Backend API",
        "status": "running",
    }