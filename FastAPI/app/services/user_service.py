# Pylint: disable=import-error, no-member
"""
Service layer for User operations.

This module contains the business logic for managing users.
It interacts with the `UserModel` and uses the `User` model from Pydantic for data validation.
"""

from typing import Optional, List
from peewee import DoesNotExist  # <-- Fixed the issue here
from config.database import UserModel, RoleModel
from models.user import UserRead
from models.role import Role

class UserService:
    """Service layer for User operations."""

    @staticmethod
    def create_user(email: str, password: str, role_id: int) -> UserRead:
        """
        Create a new user.
        """
        try:
            role_instance = RoleModel.get_by_id(role_id)
            user_instance = UserModel.create(email=email, password=password, role=role_instance)
            # Prepare data for Pydantic
            user_data = user_instance.__data__.copy()
            user_data['role_id'] = role_instance.id  # Add role_id explicitly
            # Serialize the 'role' field correctly
            role_data = {
                "id": role_instance.id,
                "name": role_instance.name
            }
            user_data['role'] = Role.model_validate(role_data)  # Using the Pydantic Role model
            return UserRead.model_validate(user_data)
        except DoesNotExist as exc:
            raise ValueError(f"Role with id {role_id} not found") from exc

    @staticmethod
    def get_user_by_email_login(email: str) -> Optional[UserModel]:
        """
        Retrieve the complete user from the database by email.
        """
        try:
            return UserModel.get(UserModel.email == email)
        except DoesNotExist:  # <-- Fixed the issue here
            return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserRead]:
        """
        Obtain a user by email.
        """
        try:
            user_instance = UserModel.get(UserModel.email == email)
            user_data = user_instance.__data__.copy()
            user_data['role_id'] = user_instance.role.id  # Add role_id explicitly
            #  Serialize the 'role' field correctly
            role_instance = user_instance.role
            role_data = {
                "id": role_instance.id,
                "name": role_instance.name
            }
            user_data['role'] = Role.model_validate(role_data)  # Using the Pydantic Role model
            return UserRead.model_validate(user_data)
        except DoesNotExist:
            return None

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[UserRead]:
        """
        Obtain a user by ID.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)
            user_data = user_instance.__data__.copy()
            user_data['role_id'] = user_instance.role.id  # Add role_id explicitly
            # Serialize the 'role' field correctly
            role_instance = user_instance.role
            role_data = {
                "id": role_instance.id,
                "name": role_instance.name
            }
            user_data['role'] = Role.model_validate(role_data)  #  Using the Pydantic Role model
            return UserRead.model_validate(user_data)
        except DoesNotExist:
            return None
    @staticmethod
    def update_user_status(user_id: int, is_active: bool) -> bool:
        """
        Updates the active status of a user.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)
            user_instance.is_active = is_active
            user_instance.save()
            return True
        except DoesNotExist:
            return False
    @staticmethod
    def update_user(
        user_id: int,
        email: Optional[str] = None,
        password: Optional[str] = None,
        role_id: Optional[int] = None,
    ) -> Optional[UserRead]:
        """
        Update an existing user by its ID.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)

            if email:
                user_instance.email = email
            if password:
                user_instance.password = password
            if role_id:
                try:
                    role_instance = RoleModel.get_by_id(role_id)
                    user_instance.role = role_instance
                except DoesNotExist as exc:
                    raise ValueError(f"Role with id {role_id} not found") from exc

            user_instance.save()

            # Prepare data for Pydantic
            user_data = user_instance.__data__.copy()
            user_data['role_id'] = user_instance.role.id
            user_data['role'] = user_instance.role

            return UserRead.model_validate(user_data)
        except DoesNotExist:
            return None

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        Delete a user by ID.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)
            user_instance.delete_instance()
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def list_all_users() -> List[UserRead]:
        """
        Get a list of all users.
        """
        users = UserModel.select().where(UserModel.role == 2)
        return users
