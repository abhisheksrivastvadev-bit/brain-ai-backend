
from app.services.memory import getConversationHistory
from fastapi import APIRouter

router= APIRouter(prefix="/api/history" ,tags=["history"])

@router.get("/")
def getChatHistory(session_id:str):

    try:

        conversation= getConversationHistory(session_id)
        # print(conversation)

        return{
            "success": True,
            "message": "conversation history",
            "data":{
                "conversation": conversation
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"error in api call {e}",
            "data":{
                "conversation": []
            }
        }
    