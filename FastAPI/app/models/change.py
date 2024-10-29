"""
Model for logging changes to tasks.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Change(BaseModel):
    """
    Represents a record of a change made to a task.

    Attributes:
        id (int): Unique identifier of the change.
        task_id (int): ID of the task associated with the change.
        timestamp (datetime): Date and time when the change was made.
        field_changed (str): Field that was changed.
        old_value (Optional[str]): Previous value of the field.
        new_value (Optional[str]): New value of the field.
    """
    id: int
    task_id: int
    timestamp: datetime
    field_changed: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None

    class Config: # pylint: disable=too-few-public-methods
        """
        Model Config
        """
        orm_mode = True
