import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")
MODEL_NAME = os.getenv("OLLAMA_MODEL")

if not OLLAMA_HOST:
    raise ValueError("OLLAMA_HOST is not configured")

if not MODEL_NAME:
    raise ValueError("OLLAMA_MODEL is not configured")

client = Client(host=OLLAMA_HOST)


def generate_response(messages: list[dict]) -> str:
    response = client.chat(
        model=MODEL_NAME,
        messages=messages
    )

    return response["message"]["content"]