"""
This module defines the User Pydantic models for data validation and serialization.
"""

from typing import Optional  # Standard library import
from pydantic import BaseModel, EmailStr  # Third-party import
from .role import RoleRead  # pylint: disable=E0402


class UserCreate(BaseModel):
    """
    Model for creating a new user.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
        role_id (int): The ID of the role assigned to the user.
    """

    email: EmailStr
    password: str
    role_id: int


class UserUpdate(BaseModel):
    """
    Model for updating an existing user.

    Attributes:
        email (Optional[EmailStr]): The new email address.
        password (Optional[str]): The new password.
        role_id (Optional[int]): The new role ID.
    """

    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None


class UserRead(BaseModel):  # pylint: disable=R0903
    """
    Model for reading user information.

    Attributes:
        id (int): The unique identifier of the user.
        email (EmailStr): The user's email address.
        role (RoleRead): The role assigned to the user.
    """

    id: int
    email: EmailStr
    role: RoleRead

    class Config:  # pylint: disable=too-few-public-methods
        """
        class Config
        """

        orm_mode = True
