"""
This module defines the Pydantic models for managing tasks in the application.
The models are used to validate and serialize data related to tasks.
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, constr, field_validator

class TaskBase(BaseModel):
    """
    Base model for common task fields.
    """
    id: int
    title: str
    description: str
    date_of_creation: date
    expiration_date: date

class TaskCreate(BaseModel):
    """
    Model to create a new task.
    """

    title: constr(min_length=1, max_length=255)  # type: ignore
    description: str
    expiration_date: date
    status_id: int
    user_id: Optional[int] = None
    is_favorite: Optional[bool] = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """
        Validates that the task title is not empty.
        """
        if not v.strip():
            raise ValueError("The task title cannot be empty.")
        return v


class TaskUpdate(BaseModel):
    """
    Model to update an existing task.
    """

    title: Optional[constr(min_length=1, max_length=255)] = None  # type: ignore
    description: Optional[str] = None
    expiration_date: Optional[date] = None
    status_id: Optional[int] = None
    user_id: Optional[int] = None
    is_favorite: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        """
        Validates that the new task title is not empty, if provided.

        Args:
            v (Optional[str]): The new task title.

        Returns:
            Optional[str]: The new task title if valid.

        Raises:
            ValueError: If the title is empty or contains only spaces.
        """
        if v is not None and not v.strip():
            raise ValueError("The task title cannot be empty.")
        return v


# pylint: disable=too-few-public-methods
class TaskRead(BaseModel):
    """
    Model to read task information.
    """

    id: int
    title: str
    description: str
    date_of_creation: date
    expiration_date: date
    status_name: str
    user_id: int
    is_favorite: bool

    class Config:
        """
        Model configuration to enable ORM compatibility.
        """

        orm_mode = True
