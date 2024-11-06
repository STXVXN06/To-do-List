"""
Security dependencies for authentication and authorization handling.
Includes functions to obtain the current user and verify roles.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.user import UserRead
from services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserRead:
    """Retrieves the current user from the JWT token."""
    user = AuthService.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_active_user(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    """Verifies that the user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_admin(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    """Verifies if the user is an administrator."""
    if current_user.role.name != "Administrator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Administrator access required"
        )
    return current_user