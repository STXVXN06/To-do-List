"""
Authentication service for handling password hashing, JWT creation, and user authentication.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from config.database import UserModel
from models.user import UserRead
from services.user_service import UserService

# Config passlib context para password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Service class for handling authentication operations."""

    @staticmethod
    def verify_password(plain_password: str, password: str) -> bool:
        """Verify if the plaintext password matches the hashed password."""
        return pwd_context.verify(plain_password, password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hashea a password in plain text before storing it."""
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[UserModel]:
        """
        Authenticate a user using their email and password.
        """
        user = UserService.get_user_by_email_login(email)
        if not user or not AuthService.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow()+(expires_delta if expires_delta else
                                      timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user(token: str) -> Optional[UserRead]:
        """
        Decode a JWT token and retrieve the user based on the email in the token payload.

        Args:
            token (str): The JWT token to decode.

        Returns:
            Optional[UserRead]: The user object if authentication is successful.

        Raises:
            HTTPException: If token validation fails.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Decode the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError as exc:
            raise credentials_exception from exc

        # Searches for the user in the database using the email address
        user = UserService.get_user_by_email(email)
        if user is None:
            raise credentials_exception
        return user
