from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.service import AuthService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)
