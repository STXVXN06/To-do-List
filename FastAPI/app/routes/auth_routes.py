"""
Module defining authentication routes.

Includes endpoints for user registration and login,
providing JWT tokens for authentication.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
<<<<<<< HEAD
from pydantic import validator, BaseModel, EmailStr
=======
from pydantic import BaseModel, EmailStr
>>>>>>> 995301a9ad8cd20d1078bf6be8d0d793bc5747b7
from models.user import UserRead, UserCreate
from services.auth_service import AuthService
from services.user_service import UserService
from utils.dependencies import OAuth2PasswordRequestFormEmail
<<<<<<< HEAD

=======
>>>>>>> 995301a9ad8cd20d1078bf6be8d0d793bc5747b7

router = APIRouter(
    tags=["Authentication"],
)

class Token(BaseModel):
<<<<<<< HEAD
    status : str
    status_code: int
=======
    """
    Token response model for authentication.

    Attributes:
    -----------
    access_token : str
        The JWT access token.
    token_type : str
        The type of the token (usually "bearer").
    """
>>>>>>> 995301a9ad8cd20d1078bf6be8d0d793bc5747b7
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    """
    Token data model to store user email information from the JWT token.

    Attributes:
    -----------
    email : Optional[EmailStr]
        The email of the user extracted from the token (if available).
    """
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
<<<<<<< HEAD
def register(user: UserCreateEnhanced):
=======
def register(user: UserCreate):
    """
    Registers a new user and returns user data.

    Parameters:
    -----------
    user : UserCreate
        The user registration data including email, password, and role.

    Returns:
    --------
    UserRead
        The registered user's data.
    """
>>>>>>> 995301a9ad8cd20d1078bf6be8d0d793bc5747b7
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
    """
    Authenticates a user and returns an access token.

    Parameters:
    -----------
    form_data : OAuth2PasswordRequestFormEmail
        The login credentials (email and password).

    Returns:
    --------
    Token
        The generated JWT token.
    """
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
<<<<<<< HEAD
    return {
        "status": "success",
        "status_code": status.HTTP_200_OK,
        "access_token": access_token,
        "token_type": "Bearer"
    }
=======
    return {"access_token": access_token, "token_type": "bearer"}
>>>>>>> 995301a9ad8cd20d1078bf6be8d0d793bc5747b7
