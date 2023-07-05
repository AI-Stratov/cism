from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from src.models import User
from src.auth.schemas import UserRegisterRequest, UserLoginRequest
from logger_config import logger


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, request: UserRegisterRequest):
        if len(request.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

        user = self.db.query(User).filter(User.username == request.username).first()
        if user:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = bcrypt.hash(request.password)
        new_user = User(username=request.username, password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        logger.info(f"User {new_user.username} registered successfully")

        return new_user

    def login_user(self, request: UserLoginRequest):
        user = self.db.query(User).filter(User.username == request.username).first()
        if not user or not bcrypt.verify(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        self.logger.info(f"User {user.username} logged in successfully")
        return user

    def get_users(self) -> List[User]:
        users = self.db.query(User).all()
        logger.info("List of users requested")
        return users
