"""
This module defines the Role class, which represents a role model used to manage 
different roles or permissions within an application.

The Role class includes attributes such as the role's unique identifier and name.

It is built using Pydantic's `BaseModel` to ensure data validation and type checking.
"""

from pydantic import BaseModel


class Role(BaseModel):
    """
    Represents a role with relevant details.

    Attributes:
    -----------
    id : int
        Unique identifier for the role.
    name : str
        The name of the role (e.g., 'admin', 'user', 'moderator'),
        representing the permissions associated with it.
    """

    id: int
    name: str
