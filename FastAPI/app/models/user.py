"""
    Represents a user with its credentials and associated role.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr
from .role import Role

class User(BaseModel):
    """
    Represents a user with their credentials and associated role.
    """
    id: int
    email: EmailStr
    role_id: int
    is_active: bool
    role: Role

    class Config: # pylint: disable=too-few-public-methods
        """
        Model config.
        """
        orm_mode = True

class UserCreate(BaseModel):
    """
    Model for creating a new user.
    """
    email: EmailStr
    password: str # Plaintext; hash before storing.
    role_id: int

class UserUpdate(BaseModel):
    """
    Model for updating an existing user.
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
