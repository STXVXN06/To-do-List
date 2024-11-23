"""
Module defining authentication routes.

Includes endpoints for user registration and login,
providing JWT tokens for authentication.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from models.user import UserRead, UserCreate
from services.auth_service import AuthService
from services.user_service import UserService
from utils.dependencies import OAuth2PasswordRequestFormEmail

router = APIRouter(
    tags=["Authentication"],
)


class Token(BaseModel):
    """
    Token response model for authentication.

    Attributes:
    -----------
    access_token : str
        The JWT access token.
    token_type : str
        The type of the token (usually "bearer").
    """

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

    @field_validator("email")
    @classmethod
    def email_format(self, value):
        """
        Validates the format of an email address.
        This method ensures that the email address contains only valid characters
        (alphanumeric, '@', '.', and '_') and that the domain part (the part after
        the last '.') has at least two characters.
        Args:
            value (str): The email address to validate.
        Returns:
            str: The validated email address.
        Raises:
            ValueError: If the email contains invalid characters or if the domain
                        part has fewer than two characters.
        """
        valid_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._"
        )
        if not all(char in valid_chars for char in value):
            raise ValueError("Email contains invalid characters")

        # Validate the domain (part after the last '.')
        domain_part = value.split(".")[-1]
        if len(domain_part) < 2:
            raise ValueError(
                "Email domain must have at least two characters after the last dot"
            )

        return value

    @field_validator("password", "role_id", pre=True, always=True)
    @classmethod
    def non_empty_fields(self, v):
        """
        Validates that the given field is not empty.
        Args:
            cls: The class that this method is a part of.
            v: The value to be validated.
        Returns:
            The value if it is not empty.
        Raises:
            ValueError: If the value is None or an empty string.
        """
        if v is None or v == "":
            raise ValueError("This field cannot be empty")
        return v


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
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
    existing_user = UserService.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = AuthService.get_password_hash(user.password)
    try:
        new_user = UserService.create_user(
            email=user.email, password=hashed_password, role_id=user.role_id
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
    return {"access_token": access_token, "token_type": "bearer"}
