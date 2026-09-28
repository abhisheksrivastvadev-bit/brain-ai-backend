
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from pwdlib import PasswordHash
import os
import jwt

load_dotenv()

password_hash= PasswordHash.recommended()

JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password,hashed_password)
    
def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return token