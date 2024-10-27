
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
    """

    id: int
    task_id: int
    timestamp: datetime
    field_changed: str
    old_value: str
    new_value: str
