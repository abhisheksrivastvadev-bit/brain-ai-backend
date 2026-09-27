from typing import Optional
from pydantic import BaseModel

class charRequest(BaseModel):
    session_id: str
    message:str
    system_prompt: Optional[str] = None
    
class chatResponse(BaseModel):
    message:str