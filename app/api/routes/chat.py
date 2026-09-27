from app.services.memory import saveConversationHistory
from app.services.memory import getConversationHistory
from fastapi import APIRouter
from app.schemas.chat import charRequest, chatResponse
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

router=APIRouter(prefix="/api/chat" ,tags=["chat"])

load_dotenv()

hf_token=os.getenv("Hugging_Face_Api_Key")
client=InferenceClient(api_key= hf_token)

@router.post("/", response_model= chatResponse)
def chat(request:charRequest):
    try:

        conversation=getConversationHistory(request.session_id)

        saveConversationHistory(
            request.session_id,
            "user",
            request.message
        )

        harcoded_system_prompt="""
                You are Brain AI, a friendly and helpful AI assistant.

                Always respond in a polite, friendly, and conversational tone.
                Never sound annoyed, angry, sarcastic, or dismissive.

                If the user asks something that was already discussed,
                answer it naturally using the conversation context.

                Do not tell the user that they have already asked something
                unless it is genuinely useful to mention it.
            """

        system_prompt= {
            "role": "system",
            "content": request.system_prompt if request.system_prompt else harcoded_system_prompt    
        }

        messages= conversation + [
                {
                    "role":"user",
                    "content":request.message
                },
                system_prompt
        ]

        response=client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct", 
            messages=messages
        )

        # response=client.chat.completions.create(
        #     model="meta-llama/Llama-3.1-8B-Instruct", 
        #     messages=[ conversation+
        #         {
        #             "role":"user",
        #             "content":request.message
        #         }
        #     ]
        # )

        api_response=response.choices[0].message.content

        saveConversationHistory(
            request.session_id,
            "assistant",
            api_response
        )

        return{
            "message":api_response
        }
    except Exception as e:
        return {
            "message":f"error in api call {e}"
        }