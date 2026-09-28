

from app.schemas.auth import RegisterRequest
from app.schemas.auth import LoginRequest
from fastapi import APIRouter

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(request: RegisterRequest):

    