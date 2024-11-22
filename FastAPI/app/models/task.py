# pylint: disable=import-error, no-member,too-few-public-methods
"""
This module defines the Task class, which represents a task model for handling 
task-related data within an application.

The Task class includes attributes such as title, description, creation date, 
expiration date, and flags for tracking the status and importance of the task.

It is based on the Pydantic `BaseModel` to ensure data validation and type checking.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from .change import Change


class Task(BaseModel):
    """
    Represents a task with relevant details.

    Attributes:
    -----------
    id : int
        Unique identifier for the task.
    title : str
        Title of the task.
    description : str
        Detailed description of the task.
    date_of_creation : date
        The date when the task was created.
    expiration_date : date
        The deadline or expiration date for the task.
    status_id : int
        The status identifier, representing the current state
        of the task (e.g., completed, pending).
    user_id : int
        The identifier of the user associated with the task.
    is_favorite : bool
        Flag indicating whether the task is marked as a favorite.
    """

    id: int
    title: str
    description: str
    date_of_creation: date
    expiration_date: date
    status_id: int
    user_id: int
    is_favorite: bool
    changes: Optional[List[Change]] = None

    class Config:
        """
        Configuration class for the Task model.
        Attributes:
            from_attributes (bool): Indicates whether to use attributes from the ORM model.
        """
        from_attributes = True  # Cambia 'orm_mode' a 'from_attributes' para Pydantic v2

class TaskCreate(BaseModel):
    """
    TaskCreate is a Pydantic model for creating a new task.
    Attributes:
        title (str): The title of the task.
        description (Optional[str]): An optional description of the task.
        expiration_date (Optional[date]): An optional expiration date for the task.
        status_id (int): The ID representing the status of the task.
    """

    title: str
    description: Optional[str] = None
    expiration_date: Optional[date] = None
    status_id: int
class TaskUpdate(BaseModel):
    """
    This is so that the task can be updated.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    expiration_date: Optional[date] = None
    status_id: Optional[int] = None
    is_favorite: Optional[bool] = None
