"""
Module defining authentication routes.

Includes endpoints for user registration and login,
providing JWT tokens for authentication.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Form
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from models.user import UserRead, UserCreate
from services.auth_service import AuthService
from services.user_service import UserService
from utils.dependencies import OAuth2PasswordRequestFormEmail 


router = APIRouter(
    tags=["Authentication"],
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
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
def login(form_data: OAuth2PasswordRequestFormEmail = Depends()):
    # Autenticación usando el email
    user = AuthService.authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AuthService.create_access_token(
        data={"sub": user.email}  # Guarda el email en el token
    )
    return {"access_token": access_token, "token_type": "bearer"}