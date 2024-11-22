"""
Module defining authentication routes.

Includes endpoints for user registration and login,
providing JWT tokens for authentication.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import validator, BaseModel, EmailStr
from models.user import UserRead, UserCreate
from services.auth_service import AuthService
from services.user_service import UserService
from utils.dependencies import OAuth2PasswordRequestFormEmail


router = APIRouter(
    tags=["Authentication"],
)

class Token(BaseModel):
    status : str
    status_code: int
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class UserCreateEnhanced(UserCreate):
    """
    Extended UserCreate model to add additional validations:
    - Restrict email format to avoid special characters.
    - Ensure non-empty fields.
    """

    @validator("email")
    def email_format(cls, value):
        # Permitir solo caracteres alfanuméricos, @, ., y _
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._")
        if not all(char in valid_chars for char in value):
            raise ValueError("Email contains invalid characters")

        # Validar el dominio (parte después de la última '.')
        domain_part = value.split('.')[-1]
        if len(domain_part) < 2:
            raise ValueError("Email domain must have at least two characters after the last dot")

        return value

    @validator("password", "role_id", pre=True, always=True)
    def non_empty_fields(cls, v):  # Método de clase, usa 'cls' en vez de 'self'
        if v is None or v == "":
            raise ValueError("This field cannot be empty")
        return v
    

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user: UserCreateEnhanced):
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
    return {
        "status": "success",
        "status_code": status.HTTP_200_OK,
        "access_token": access_token,
        "token_type": "Bearer"
    }
