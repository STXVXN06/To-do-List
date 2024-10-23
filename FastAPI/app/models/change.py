"""
This module defines the Change class, which represents a model for tracking changes 
made to tasks or other entities within an application.

The Change class captures details about what field was changed, the old value, 
the new value, and when the change occurred.

It is built using Pydantic's `BaseModel` to ensure data validation and type checking.
"""

from datetime import datetime
from pydantic import BaseModel


class Change(BaseModel):
    """
    Represents a record of a change made to a task.

    Attributes:
    -----------
    id : int
        Unique identifier for the change record.
    task_id : int
        Identifier of the task associated with this change.
    timestamp : datetime
        The date and time when the change was made.
    field_changed : str
        The name of the field that was changed (e.g., 'status', 'description').
    old_value : str
        The previous value of the field before the change.
    new_value : str
        The new value of the field after the change.
    """

    id: int
    task_id: int
    timestamp: datetime
    field_changed: str
    old_value: str
    new_value: str
