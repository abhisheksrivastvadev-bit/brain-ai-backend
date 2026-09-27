
## This is for shprt-term memory, in this case conversation is storing into the RAM, if uvicorn server restart or crash then memory will disappear, LLM no longer remember the previous conversation.

## In production we will use Redis or database for storing the conversation history

conversations = {}

def getConversationHistory(session_id: str):

    if session_id not in conversations:
        conversations[session_id]= []

    return conversations[session_id]

def saveConversationHistory(session_id: str,role: str, content: str):

    if session_id not in conversations:
        conversations[session_id]= []
    
    conversations[session_id].append({
        "role": role,
        "content": content
    })

    print("saveConversationHistory",conversations)