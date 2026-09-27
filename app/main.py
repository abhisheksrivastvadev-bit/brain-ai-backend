
from fastapi import FastAPI
from app.api.routes import chat, chat_history

app = FastAPI(
    title="Brain AI Backend API",
    description="Backend service for Brain AI",
    version="0.0.1"
)

app.include_router(chat.router)
app.include_router(chat_history.router)

@app.get('/')
def root():
    return{
        "message":"Welcome to the Brain AI Backend API",
        "status": "running",
    }