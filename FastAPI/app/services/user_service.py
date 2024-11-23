# Pylint: disable=import-error, no-member
"""
Service layer for User operations.

This module contains the business logic for managing users.
It interacts with the `UserModel` and uses the `User` model from Pydantic for data validation.
"""

import re
from typing import Optional, List

from fastapi import HTTPException
from peewee import DoesNotExist  # <-- Fixed the issue here

from config.database import UserModel, RoleModel
from models.role import Role
from models.user import UserRead

class UserService:
    """Service layer for User operations."""    
    @staticmethod
    def email_format(email: str) -> str:
        """Valida que el formato del correo sea correcto."""
        valid_chars = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
        if not valid_chars.match(email):
            raise ValueError("Email format is invalid")
        return email

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
            raise HTTPException(status_code=404,
                                detail=f"Status:{404},Role with id {role_id} not found") from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

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

        # Initial validation to avoid empty values
        if email == "" or (email is not None and not email.strip()):
            raise ValueError("Email cannot be empty")
        if password == "" or (password is not None and not password.strip()):
            raise ValueError("Password cannot be empty")
        if role_id in {"", 0}:
            raise ValueError("Role ID cannot be empty or zero")

        try:
            # Retrieve the existing user
            user_instance = UserModel.get_by_id(user_id)

            # Validate and update email if provided
            if email:
                # Validate the email format
                email = UserService.email_format(email)

                # Check if the email already exists for another user
                existing_user = UserModel.select().where(
                    (UserModel.email == email)&
                    (UserModel.id != user_id)
                ).first()
                if existing_user:
                    raise ValueError("Email already registered")
                # Assign the email to the user if it is valid
                user_instance.email = email

            # Validate and update the password if provided
            if password:
                user_instance.password = password  # Already hashed

            # Validate and update the role if provided
            if role_id:
                try:
                    role_instance = RoleModel.get_by_id(role_id)
                    user_instance.role = role_instance
                except DoesNotExist as exc:
                    raise ValueError(f"Role with id {role_id} not found") from exc

            # Save changes only if all validations passed successfully
            user_instance.save()

            # Prepare data for Pydantic
            user_data = user_instance.__data__.copy()
            user_data['role_id'] = user_instance.role.id
            user_data['role'] = user_instance.role

        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail=f"Status:{404}, User not found") from exc
        except Exception as exc:
            raise ValueError(str(exc)) from exc

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
