"""
This module defines the Task class, which represents a task model for handling 
task-related data within an application.

The Task class includes attributes such as title, description, creation date, 
expiration date, and flags for tracking the status and importance of the task.

It is based on the Pydantic `BaseModel` to ensure data validation and type checking.
"""

from datetime import date
from pydantic import BaseModel


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
