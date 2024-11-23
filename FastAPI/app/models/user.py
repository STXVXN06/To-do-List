# pylint: disable=import-error, no-member, too-few-public-methods
"""
This module defines the User-related models for managing user data in the system.

Includes models for reading, creating, and updating user information, including
their email, role, and active status.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr
from .role import Role

class UserRead(BaseModel):
    """
    Represents a user with the details required for reading user data.

    Attributes:
    -----------
    id : int
        Unique identifier for the user.
    email : EmailStr
        The email address of the user.
    role_id : int
        The ID of the role assigned to the user.
    is_active : bool
        Indicates whether the user account is active.
    role : Role
        The role of the user, represented by a Role object.
    """
    id: int
    email: EmailStr
    role_id: int
    is_active: bool
    role: Role

    class Config:
        """
        Configuration class for the user model.
        Attributes:
            from_attributes (bool): Indicates whether the
            configuration should be derived from attributes.
        """

        from_attributes = True

class UserCreate(BaseModel):
    """
    Represents the data required to create a new user.

    Attributes:
    -----------
    email : EmailStr
        The email address of the user.
    password : str
        The password of the user (stored as plaintext, hashed before saving).
    role_id : int
        The ID of the role assigned to the user.
    """
    email: EmailStr
    password: str  # Password in plain text; hashed before storing
    role_id: int

class UserUpdate(BaseModel):
    """
    Represents the data required to update an existing user.

    Attributes:
    -----------
    email : Optional[EmailStr]
        The new email address of the user (optional).
    password : Optional[str]
        The new password for the user (optional).
    role_id : Optional[int]
        The new role ID assigned to the user (optional).
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
