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
from config.database import UserModel
# Configurar passlib context para password hashing

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Authentication Service."""

    @staticmethod
    def verify_password(plain_password: str, password: str) -> bool:
        """Verifica si la contraseña en texto plano coincide con la contraseña hasheada."""
        return pwd_context.verify(plain_password, password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hashea una contraseña en texto plano antes de almacenarla."""
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[UserModel]:
        """
        Autentica a un usuario utilizando su email y contraseña.
        """
        user = UserService.get_user_by_email_login(email)
        if not user or not AuthService.verify_password(password, user.password):  # Usa `user.password`
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
    def get_current_user(token: str) -> Optional[UserRead]:
        """
        Decodes the JWT token and retrieves the user based on the email.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Decodifica el token JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # Busca el usuario en la base de datos usando el email
        user = UserService.get_user_by_email(email)
        if user is None:
            raise credentials_exception
        return user