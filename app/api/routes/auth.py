

from app.core.security import create_access_token
from app.core.security import verify_password
from app.db import database
from app.core.security import hash_password
from app.models.user import User
from app.db.database import get_db
from sqlalchemy.ext.asyncio import session
from app.schemas.auth import RegisterRequest, LoginRequest
from fastapi import APIRouter, Depends, HTTPException

router=APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    request: RegisterRequest,
    db: session= Depends(get_db)
    ):

    existing_user= (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
   
    password_hash= hash_password(request.password)

    user=User(
        name= request.name,
        email= request.email,
        password_hash= password_hash
    )
        

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token= create_access_token(user.user_id)

    return {
        "success":True,
        "message": "Registration successful",
        "user": {
            "user_id":user.user_id,
            "name": user.name,
            "email": user.email,
            "access_token": access_token,
            "token_type": "bearer",
        }
    }

@router.post("/login")
def login(
    request: LoginRequest,
    db: session=Depends(get_db)
):

    retreive_data_from_DB= db.query(User).filter(User.email == request.email).first()

    if not retreive_data_from_DB:
        raise HTTPException(
            status_code=400,
            detail="Email not found"
        )
    
    valid_password= verify_password(request.password, retreive_data_from_DB.password_hash)
    
    if not valid_password:
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )
    access_token= create_access_token(retreive_data_from_DB.user_id)

    return{
        "success":True,
        "message": "Login successful",
        "user": {
            "user_id": retreive_data_from_DB.user_id,
            "name": retreive_data_from_DB.name,
            "email": retreive_data_from_DB.email,
            "access_token": access_token,
            "token_type": "bearer",
        }
    }