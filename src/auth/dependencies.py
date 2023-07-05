from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError, decode
from sqlalchemy.orm import Session

from src.auth.service import AuthService
from src.config import settings
from src.database import get_db
from src.models import User


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """
    Get the authentication service.

    - **db**: Database session dependency.
    """
    return AuthService(db)


def create_token(username: str) -> str:
    """
    Create an authentication token for the provided username.

    - **username**: Username for which the token is created.
    """
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE),
    }
    token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM,
    )
    return token


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> Optional[User]:
    """
    Get the current authenticated user.

    - **credentials**: HTTP authorization credentials
    containing the authentication token.
    """
    try:
        token = credentials.credentials
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM],
        )
        username = payload.get("username")
        if username:
            user = User()
            user.username = username
            return user
    except InvalidTokenError:
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication token",
    )
