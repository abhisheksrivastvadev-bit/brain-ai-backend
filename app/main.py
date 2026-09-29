
from app.db.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, auth

app = FastAPI(
    title="Brain AI Backend API",
    description="Backend service for Brain AI",
    version="0.0.1"
)

app.include_router(chat.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get('/')
def root():
    return{
        "message":"Welcome to the Brain AI Backend API",
        "status": "running",
    }