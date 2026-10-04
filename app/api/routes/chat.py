from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.db.database import get_db
import io
import base64
import re
import os
from typing import Tuple
from fastapi import APIRouter, Depends
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from app.services.memory import saveConversationHistory, getConversationHistory, getAllConversationHistory
from app.schemas.chat import charRequest, chatResponse
from langsmith import traceable


router = APIRouter(prefix="/api/chat", tags=["chat"])

load_dotenv()

hf_token = os.getenv("Hugging_Face_Api_Key")
client = InferenceClient(api_key=hf_token)

MODEL = "meta-llama/Llama-3.1-8B-Instruct"


def detect_image_request(message: str) -> Tuple[bool, str]:
    """
    Detects if the user query is asking to generate/draw/create an image.
    Returns (is_image_request, clean_image_prompt).
    """
    lower = message.lower().strip()
    image_words = ['image', 'picture', 'photo', 'drawing', 'illustration', 'sketch', 'painting', 'wallpaper', 'portrait']
    action_words = ['generate', 'create', 'draw', 'make', 'paint', 'produce', 'render', 'show me', 'give me']

    has_action = any(a in lower for a in action_words)
    has_image = any(i in lower for i in image_words)
    starts_draw = lower.startswith('draw ') or lower.startswith('paint ') or lower.startswith('/imagine ') or lower.startswith('generate image') or lower.startswith('create image')

    if not ((has_action and has_image) or starts_draw):
        return False, message

    # Clean the prompt to isolate the subject for the image model
    cleaned = re.sub(
        r'^(?:please\s+)?(?:can you\s+)?(?:generate|create|make|draw|paint|show me|produce|render)\s+(?:an?\s+)?(?:image|picture|photo|illustration|drawing|sketch|painting)?(?:\s+of)?(?:\s*:)?\s*',
        '',
        message,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(r'\s+image$', '', cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip(' :,-')
    return True, cleaned or message

def generate_image_flux(prompt: str) -> str:
    """
    Generates an image with FLUX.1-schnell and returns a base64 data URI string.
    """
    img = client.text_to_image(prompt, model="black-forest-labs/FLUX.1-schnell")
    img.thumbnail((768, 768))
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_str}"


@traceable(name="LLM Conversation")
def ask_llm(messages: list):

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content

@router.post("/", response_model=chatResponse)
def chat(
    request: charRequest,
    db: Session= Depends(get_db)
    ):

    try:
        conversation = getConversationHistory(db, request.user_id, request.session_id)

        saveConversationHistory(
            db,
            request.user_id,
            request.session_id,
            "user",
            request.message
        )

        # 1. Check if user is requesting image generation
        is_image_req, img_prompt = detect_image_request(request.message)
        if is_image_req:
            try:
                print(f"[chat] Generating image with FLUX for prompt: '{img_prompt}'")
                image_data_url = generate_image_flux(img_prompt)
                response_text = f"Here is the generated image for: **{img_prompt}**\n\n![{img_prompt}]({image_data_url})"
                
                saveConversationHistory(
                    db,
                    request.user_id,
                    request.session_id,
                    "assistant",
                    response_text,
                    image_url=image_data_url
                )

                return {
                    "message": response_text,
                    "image_url": image_data_url
                }
            except Exception as img_err:
                print(f"[chat] Image generation failed, falling back to LLM text: {img_err}")
                # Fall through to standard LLM chat completion below

        # 2. Standard LLM Chat Completion
        harcoded_system_prompt = """
                You are Brain AI, a friendly and helpful AI assistant.

                Always respond in a polite, friendly, and conversational tone.
                Never sound annoyed, angry, sarcastic, or dismissive.

                If the user asks something that was already discussed,
                answer it naturally using the conversation context.

                Do not tell the user that they have already asked something
                unless it is genuinely useful to mention it.
            """

        system_prompt = {
            "role": "system",
            "content": request.system_prompt if request.system_prompt else harcoded_system_prompt
        }

        # Filter out massive data URLs from messages payload sent to Llama context to prevent token overflows
        clean_history = []
        for msg in conversation:
            c = msg.get("content", "")
            # Truncate any long base64 embedded in history
            c_clean = re.sub(r'data:image\/[a-zA-Z0-9.+_-]+;base64,[a-zA-Z0-9+/=]+', '[AI Generated Image]', c)
            clean_history.append({
                "role": msg.get("role", "user"),
                "content": c_clean
            })

        messages = clean_history + [
            {
                "role": "user",
                "content": request.message
            },
            system_prompt
        ]

        response = ask_llm(messages)

        # response = client.chat.completions.create(
        #     model=MODEL,
        #     messages=messages
        # )

        # api_response = response.choices[0].message.content
        print("api_response",response)

        saveConversationHistory(
            db,
            request.user_id,
            request.session_id,
            "assistant",
            response
        )

        return {
            "message": response
        }
    except Exception as e:
        print(f"[chat] Error: {e}")
        return {
            "message": f"error in api call {e}"
        }

@router.get("/history")
def getChatHistory(
    user_id: str,
    db: Session= Depends(get_db)
    ):
    try:
        conversation = getAllConversationHistory(db, user_id)
        print(conversation)
        return {
            "success": True,
            "message": "conversation history",
            "data": {
                "conversation": conversation
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"error in api call {e}",
            "data": {
                "conversation": []
            }
        }

@router.get("/history/{session_id}")
def getConversationMessages(
    session_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    try:

        messages = getConversationHistory(
            db,
            user_id,
            session_id
        )

        return {
            "success": True,
            "message": "conversation messages",
            "data": {
                "messages": messages
            }
        }

    except Exception as e:

        return {
            "success": False,
            "message": f"error in api call {e}",
            "data": {
                "messages": []
            }
        }