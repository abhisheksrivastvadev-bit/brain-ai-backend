from typing import Optional
from pydantic import BaseModel

class chatRequest(BaseModel):
    session_id: str
    message: str
    system_prompt: Optional[str] = None

class chatResponse(BaseModel):
    message: str
    image_url: Optional[str] = None
