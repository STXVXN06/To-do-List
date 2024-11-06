"""
Authentication Service for handling password hashing and JWT.

Includes functions for verifying passwords, hashing passwords,
authenticating users, and creating access tokens.
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from services.user_service import UserService
from models.user import UserRead  # Asegúrate de importar UserRead correctamente

# Configurar passlib context para password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Authentication Service."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si la contraseña plana coincide con la contraseña hasheada.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hashea una contraseña plana.
        """
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[UserRead]:
        """
        Autentica a un usuario.
        """
        user = UserService.get_user_by_email(email)
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Crea un token de acceso JWT.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user(token: str) -> UserRead:
        """
        Recupera el usuario actual desde el token JWT.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError as ve:
            raise credentials_exception from ve
        user = UserService.get_user_by_email(email)
        if user is None:
            raise credentials_exception
        return user