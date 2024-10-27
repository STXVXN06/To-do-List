"""
Imports:
    Enum (from enum): Base class for creating enumerated constants in Python.

Classes:
    TaskStatusEnum (str, Enum): Enumeration representing the possible statuses of a task.

Enumerations:
    TO_DO (str): Indicates that the task is yet to be started.
    IN_PROGRESS (str): Indicates that the task is currently in progress.
    COMPLETED (str): Indicates that the task has been completed.
"""
from app.models.enums import Enum # pylint: disable=import-error

class TaskStatusEnum(str, Enum):
    """
    Enumeration for task statuses in a task management system.
    """

    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
