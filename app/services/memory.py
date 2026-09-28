## Short-term memory (RAM-based)
## In production we will use Redis or database for storing conversation history

conversations = {}

def getConversationHistory(session_id: str):
    if session_id not in conversations:
        conversations[session_id] = []
    return conversations[session_id]

def saveConversationHistory(session_id: str, role: str, content: str, image_url: str = None):
    if session_id not in conversations:
        conversations[session_id] = []
    
    item = {
        "role": role,
        "content": content
    }
    if image_url:
        item["image_url"] = image_url

    conversations[session_id].append(item)
    print("saveConversationHistory:", f"[{role}] {content[:40]}... (image: {bool(image_url)})")
