
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class RegisterResponse(BaseModel):
    message: str
    user: dict