from typing import List

from fastapi import APIRouter, Depends
from src.auth.schemas import UserRegisterRequest, UserLoginRequest, UserResponse
from src.auth.service import AuthService
from src.auth.dependencies import get_auth_service

router = APIRouter()


@router.post("/register")
def register_user(request: UserRegisterRequest, service: AuthService = Depends(get_auth_service)):
    user = service.register_user(request)
    return {"message": f"User {user.username} registered successfully"}


@router.post("/login")
def login_user(request: UserLoginRequest, service: AuthService = Depends(get_auth_service)):
    user = service.login_user(request)
    return {"message": f"User {user.username} logged in successfully"}


@router.get("/users", response_model=List[UserResponse])
def get_users(service: AuthService = Depends(get_auth_service)):
    users = service.get_users()
    user_responses = [UserResponse(id=user.id, username=user.username) for user in users]
    return user_responses

