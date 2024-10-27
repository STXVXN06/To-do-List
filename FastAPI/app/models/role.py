"""
role.py
"""
from typing import Optional  # Standard library import
from pydantic import BaseModel  # Third-party import

class RoleBase(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Base class for representing a role.
    """

    name: str


class RoleCreate(RoleBase):  # pylint: disable=too-few-public-methods
    """
    Class for creating a new role.
    """


class RoleUpdate(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Class for updating an existing role.
    """

    name: Optional[str] = None


class RoleRead(RoleBase):  # pylint: disable=too-few-public-methods
    """
    Class for representing a role read from the database.
    """

    id: int

    class Config:  # pylint: disable=too-few-public-methods
        """
        Pydantic configuration settings.
        """

        orm_mode = True
