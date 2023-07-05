from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import (create_token, get_auth_service,
                                   get_current_user)
from src.auth.schemas import (UserLoginRequest, UserLoginResponse,
                              UserRegisterRequest, UserRegisterResponse,
                              UserResponse)
from src.auth.service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    tags=["Authentication"],
    summary="Register a new user",
    description="Register a new user with the provided credentials.",
)
def register_user(
    request: UserRegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    Register a new user.

    - **request**: User registration request containing
    the username and password.
    """
    user = service.register_user(request)
    register_response = UserRegisterResponse(
        username=user.username,
        message=f"User {user.username} registered successfully",
    )
    return register_response


@router.post(
    "/login",
    response_model=UserLoginResponse,
    tags=["Authentication"],
    summary="User login",
    description=(
        "Authenticate the user with the provided credentials and generate a"
        " login token."
    ),
)
def login_user(
    request: UserLoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    User login.

    - **request**: User login request containing the username and password.
    """
    user = service.login_user(request)
    token = create_token(user.username)
    login_response = UserLoginResponse(
        message=f"User {user.username} logged in successfully", token=token,
    )
    return login_response


@router.get(
    "/users",
    response_model=List[UserResponse],
    tags=["Authentication"],
    summary="Get all users",
    description="Get the list of all registered users.",
)
def get_users(
    service: AuthService = Depends(get_auth_service),
    is_authenticated: bool = Depends(get_current_user),
):
    """
    Get all users.

    - **service**: Authentication service dependency.
    - **is_authenticated**: Indicates if the user is authenticated.
    """
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    users = service.get_users()
    user_responses = [
        UserResponse(id=user.id, username=user.username) for user in users
    ]
    return user_responses
