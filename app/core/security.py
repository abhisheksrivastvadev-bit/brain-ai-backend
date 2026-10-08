
from fastapi import Depends, HTTPException
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from pwdlib import PasswordHash
import os
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


load_dotenv()

security = HTTPBearer(auto_error=False)

password_hash= PasswordHash.recommended()

JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password,hashed_password)

def create_access_token(user_id: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token
    
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security)
):
    # Guest user
    if credentials is None:
        return None

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        return payload.get("sub")

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security)
# ):
#     token = credentials.credentials

#     try:
#         payload = jwt.decode(
#             token,
#             JWT_SECRET_KEY,
#             algorithms=[JWT_ALGORITHM]
#         )

#         user_id = payload.get("sub")

#         if not user_id:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Invalid token"
#             )

#         return user_id

#     except jwt.ExpiredSignatureError:
#         raise HTTPException(
#             status_code=401,
#             detail="Token expired"
#         )

#     except jwt.InvalidTokenError:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid token"
#         )