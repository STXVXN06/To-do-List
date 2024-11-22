"""
Authentication Service for handling password hashing and JWT.

Includes functions for verifying passwords, hashing passwords,
authenticating users, and creating access tokens.
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt  # Importación de terceros antes de la aplicación
from passlib.context import CryptContext  # Importación de terceros antes de la aplicación

from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from config.database import UserModel  # Agrupando importaciones de config
from services.user_service import UserService
from models.user import UserRead  # Orden de importación corregido

# Configurar el contexto de Passlib para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Service class for handling authentication operations."""

    @staticmethod
    def verify_password(plain_password: str, password: str) -> bool:
        """
        Verify if a plain password matches the hashed password.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return pwd_context.verify(plain_password, password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hashes a plain password for storage.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[UserModel]:
        """
        Authenticate a user by email and password.

        Args:
            email (str): User's email address.
            password (str): User's plain password.

        Returns:
            Optional[UserModel]: The authenticated user object if credentials are correct, None otherwise.
        """
        user = UserService.get_user_by_email_login(email)
        if not user or not AuthService.verify_password(password, user.password):  # Usa `user.password`
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.

        Args:
            data (dict): The data to include in the token payload.
            expires_delta (Optional[timedelta]): The expiration time for the token.

        Returns:
            str: The encoded JWT token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
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
            raise credentials_exception from exc  # Re-raising with context for pylint compliance

        # Retrieve the user from the database using the email
        user = UserService.get_user_by_email(email)
        if user is None:
            raise credentials_exception
        return user
