"""
This module defines the Status class, which represents a status model for managing 
different statuses that can be assigned to tasks or other entities within an application.

The Status class includes attributes such as the unique identifier and the name of the status.

It is built using Pydantic's `BaseModel` to ensure data validation and type checking.
"""

from pydantic import BaseModel


class Status(BaseModel):
    """
    Represents a status with relevant details.

    Attributes:
    -----------
    id : int
        Unique identifier for the status.
    name : str
        The name of the status (e.g., 'pending', 'completed', 'in progress'),
        describing the current state of an entity.
    """

    id: int
    name: str
