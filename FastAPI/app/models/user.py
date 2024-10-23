"""
This module defines the User class, which represents a user model for managing 
user-related data and authentication within an application.

The User class includes attributes for user credentials, an associated role 
(which is a reference to the Role model), and other relevant user information.

It is built using Pydantic's `BaseModel` to enable data validation and type checking.
"""

from pydantic import BaseModel
from .role import Role  # pylint: disable=relative-beyond-top-level


class User(BaseModel):
    """
    Represents a user with their credentials and associated role.

    Attributes:
    -----------
    id : int
        Unique identifier for the user.
    email : str
        The user's email address, used as their login.
    password : str
        The user's hashed password for authentication.
    role_id : int
        Identifier for the role associated with the user.
    role : Role
        The role object, representing the user's permissions and access levels.
    """

    id: int
    email: str
    password: str
    role_id: int
    role: Role
