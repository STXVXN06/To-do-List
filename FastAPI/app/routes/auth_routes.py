"""
Module defining authentication routes.

Includes endpoints for user registration and login,
providing JWT tokens for authentication.
"""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from models.user import User, UserCreate
from services.auth_service import AuthService
from services.user_service import UserService
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    tags=["Authentication"],
)


class Token(BaseModel):
    """
    Response model for JWT tokens.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model for the data contained in the JWT token.
    """
    email: Optional[EmailStr] = None


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    """
    Endpoint for registering a new user.

    Args:
        user (UserCreate): User data to be registered.

    Returns:
        User: Registered user.

    Raises:
        HTTPException: If the email is already in use or there is an error during creation.
    """
    existing_user = UserService.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = AuthService.get_password_hash(user.password)
    try:
        new_user = UserService.create_user(
            email=user.email,
            password=hashed_password,
            role_id=user.role_id
        )
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.post("/login", response_model=Token)
def login(user: UserCreate):
    """
    Endpoint to authenticate a user and provide a JWT token.

    Args:
        user (UserCreate): User credentials.

    Returns:
        Token: JWT token for authentication.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    user_auth = AuthService.authenticate_user(user.email, user.password)
    if not user_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user_auth.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
