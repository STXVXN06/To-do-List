"""
This module defines Pydantic and ORM models for managing task statuses within the application.
These models validate and serialize task status data, providing interfaces for database
interactions and data validation in API operations.

Imports:
    - External:
        - peewee.Model: Base model class for ORM support.
        - peewee.CharField, AutoField, Check, SQL: Field and constraint definitions.
        - pydantic.BaseModel: Base class for Pydantic models.
        - pydantic.field_validator: Decorator for field validation in Pydantic models.
    - Internal:
        - TaskStatusEnum (from enums): Enum defining valid task statuses.
        - database: Database connection instance.
        - Optional (typing): Type hint for optional fields.

Classes:
    StatusModel (Model):
        ORM model for the 'status' table, defining attributes for each status and ensuring 
        each status name is unique and conforms to TaskStatusEnum values.

    StatusCreate (BaseModel):
        Pydantic model for creating a new status. Ensures the `name` field is a valid 
        TaskStatusEnum value.

    StatusUpdate (BaseModel):
        Pydantic model for updating an existing status. Validates the optional `name` field 
        if provided.

    StatusRead (BaseModel):
        Pydantic model for reading status data, including the status `id` and `name`, and 
        enables ORM mode for seamless data conversion.
"""

from typing import Optional
from pydantic import BaseModel, field_validator
from peewee import CharField, AutoField, Check, SQL
from app.config.database import database  # pylint: disable=import-error
from app.models.enums import TaskStatusEnum  # pylint: disable=import-error

# pylint: disable=too-few-public-methods
class StatusModel(BaseModel):
    """
    Model representing the 'status' table, with predefined task status values.
    """

    id = AutoField(primary_key=True)
    name = CharField(
        null=False,
        unique=True,
        constraints=[
            Check(SQL(f'"name" IN {tuple(status.value for status in TaskStatusEnum)}'))
        ],
    )

    class Meta:
        # pylint: disable=too-few-public-methods
        """Metadata for table name and database connection."""

        table_name = "status"
        database = database
        doc = "Table defining the different statuses for tasks."


# pylint: disable=too-few-public-methods
class StatusCreate(BaseModel):
    """
    Pydantic model for creating a new status record.
    """

    name: TaskStatusEnum

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, v):
        """Ensures that the 'name' field is not empty."""
        if not v:
            raise ValueError("The status name cannot be empty.")
        return v


# pylint: disable=too-few-public-methods
class StatusUpdate(BaseModel):
    """
    Pydantic model for updating an existing status record.
    """

    name: Optional[TaskStatusEnum] = None

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, v):
        """Validates that the 'name' field is not empty if provided."""
        if v is not None and not v:
            raise ValueError("The status name cannot be empty.")
        return v


# pylint: disable=too-few-public-methods
class StatusRead(BaseModel):
    """
    Pydantic model for reading status data.
    """

    id: int
    name: TaskStatusEnum

    class Config:
        """Enables ORM mode for automatic data conversion from ORM models."""

        orm_mode = True
